"""
You can use it basically anywhere, this script does not use webhook,
thus it requires no domain. Feel free to run it on, e.g., your own PC
"""


import telebot
from os import system
from api_calls import WolframBot

if __name__ == "__main__":
    TOKEN = open("bot_token.txt").readline().strip()
    WHITELIST = [x.strip() for x in open("whitelist.txt").readlines()]
    API_KEYS = [x.strip() for x in open("api_key.txt").readlines()]
    wolfram = WolframBot(API_KEYS)

bot = telebot.TeleBot(TOKEN, parse_mode="MARKDOWN")

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
        system("rm {}".format('"' + search + '"'))
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
            system("rm {}".format('"' + search + '"'))
    else:
        bot.reply_to(message, "Sorry but you're not authorized to use this bot :)")


if __name__ == "__main__":
    bot.infinity_polling(interval=0, timeout=25)
