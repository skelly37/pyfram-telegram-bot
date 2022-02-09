"""
This is a more advanced and clean implementation of the bot.
Pretty decent webhook ready to be deployed.

NOT TESTED YET!!
"""

import fastapi
import uvicorn

import telebot
from os import system
from api_calls import WolframBot

if __name__ == "__main__":
    WEBHOOK_HOST = "" #DOMAIN
    WEBHOOK_PORT = 8443 #or 443, 80, 88 but it needs to be open
    WEBHOOK_LISTEN = "0.0.0.0" #or VPS IP adress
    WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key
    WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)


    TOKEN = open("./bot_token.txt").readline().strip()
    WHITELIST = [x.strip() for x in open("./whitelist.txt").readlines()]
    API_KEYS = [x.strip() for x in open("./api_key.txt").readlines()]
    wolfram = WolframBot(API_KEYS)


    WEBHOOK_URL = "{}/{}/".format(WEBHOOK_URL_BASE, TOKEN)


webhook = fastapi.FastAPI()
bot = telebot.TeleBot(TOKEN, parse_mode="MARKDOWN")

@webhook.post(f"/{TOKEN}/")
def webhook_updater(update: dict) -> None:
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return



#message is telebot.types.Message' type

def is_authorized(message) -> bool:
    return message.from_user.username in WHITELIST

@bot.message_handler(commands=["start", "help"])
def welcome_and_help(message) -> None:
    if is_authorized(message):
        bot.reply_to(message, "Welcome to WolframAlpha bot. Only text input is supported.\nDefault option is to send short message if possible.\nUse /i or /image to force image output")
    else:
        bot.reply_to(message, "Sorry but you're not authorized to use this bot :)")

@bot.message_handler(commands=["i", "image"])
def send_image(message) -> None:
    if is_authorized(message):
        text = message.text.replace("/i ", "").replace("/image ", "")
        search = wolfram.query_wolfram(text, is_image=True)
        search = search.replace("Query result saved in: ", "")
        bot.send_document(message.chat.id, open(search, "rb"), reply_to_message_id=message.id)
        system("rm {}".format('"./' + search + '"'))
    else:
        bot.reply_to(message, "Sorry but you're not authorized to use this bot :)")


@bot.message_handler(func=lambda message: True)
def handle_query(message) -> None:
    if is_authorized(message):
        text = message.text
        search = wolfram.query_wolfram(text)
        if not search.startswith("Query result saved in:"):
            bot.reply_to(message, search)
        else:
            search = search.replace("Query result saved in: ", "")
            bot.send_document(message.chat.id, open(search, "rb"), reply_to_message_id=message.id)
            system("rm {}".format('"./' + search + '"'))
    else:
        bot.reply_to(message, "Sorry but you're not authorized to use this bot :)")


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL,
                    certificate=open(WEBHOOK_SSL_CERT, "r"))

    uvicorn.run(
        webhook,
        host = WEBHOOK_LISTEN,
        port = WEBHOOK_PORT,
        ssl_certfile=WEBHOOK_SSL_CERT,
        ssl_keyfile=WEBHOOK_SSL_PRIV
    )
