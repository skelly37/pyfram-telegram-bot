"""
You can use it basically anywhere, this script does not use webhook,
thus it requires no domain. Feel free to run it on, e.g., your own PC
"""


import telebot
from os import system
from api_calls import WolframBot

if __name__ == "__main__":
    TOKEN = open("./bot_token.txt").readline().strip()
    WHITELIST = [x.strip() for x in open("./whitelist.txt").readlines()]
    API_KEYS = [x.strip() for x in open("./api_key.txt").readlines()]
    wolfram = WolframBot(API_KEYS)

bot = telebot.TeleBot(TOKEN, parse_mode="MARKDOWN")

#message is telebot.types.Message' type

def is_authorized(message) -> bool:
    return message.from_user.username in WHITELIST

@bot.message_handler(commands=["start", "help"])
def welcome_and_help(message) -> None:
    if is_authorized(message):
        bot.reply_to(message, "Welcome to WolframAlpha bot. Only text input is supported.\nDefault option is to send short message if possible.\nUse /i or /image to force image output\nUser /s or steps to get step-by-step solution.")
    else:
        bot.reply_to(message, "Sorry but you're not authorized to use this bot :)")


def send_prompt_message(message, is_step_by_step=False):
    data = None
    if is_step_by_step:
        data = bot.reply_to(message, "I'm processing your request...\nPlease be patient...")
    else:
        data = bot.reply_to(message, "I'm processing your request...")
    return dict(message_id = data.message_id, chat_id = data.chat.id)

def get_wolfram_response(message, is_image=False):
    prompt = send_prompt_message(message)

    text = message.text.replace("/image ", "").replace("/i ", "").strip()
    search = wolfram.query_wolfram(text, is_image)

    bot.delete_message(prompt["chat_id"], prompt["message_id"])
    return search

def get_wolfram_steps(message):
    prompt = send_prompt_message(message, True)

    text = message.text.replace("/steps ", "").replace("/s ", "").strip()
    search = wolfram.get_step_by_step(text)

    bot.delete_message(prompt["chat_id"], prompt["message_id"])
    return search


def send_image_result(message, search_result):
    search_result = search_result.replace("Query result saved in: ", "")
    bot.send_document(message.chat.id, open(search_result, "rb"), reply_to_message_id=message.id)
    system("rm {}".format('"./' + search_result + '"'))

    
@bot.message_handler(commands=["i", "image"])
def send_image(message) -> None:
    if is_authorized(message):
        search_result = get_wolfram_response(message, True)
        if search_result != "Error processing your request.":
            send_image_result(message, search_result)
        else:
            bot.reply_to(message, search_result)
    else:
        bot.reply_to(message, "Sorry but you're not authorized to use this bot :)")

@bot.message_handler(commands=["s", "steps"])
def send_steps(message) -> None:
    if is_authorized(message):
        search_result = get_wolfram_steps(message)
        if search_result != "Error processing your request." and search_result != "No step by step solution available.":
            send_image_result(message, search_result)
        else:
            bot.reply_to(message, search_result)
    else:
        bot.reply_to(message, "Sorry but you're not authorized to use this bot :)")

@bot.message_handler(func=lambda message: True)
def handle_query(message) -> None:
    if is_authorized(message):
        search_result = get_wolfram_response(message)

        if not search_result.startswith("Query result saved in:"):
            bot.reply_to(message, search_result)
        else:
            send_image_result(message, search_result)
    else:
        bot.reply_to(message, "Sorry but you're not authorized to use this bot :)")


if __name__ == "__main__":
    bot.infinity_polling(interval=0, timeout=25)
