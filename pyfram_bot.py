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

NOT_AUTHORIZED_MSG = "Sorry but you're not authorized to use this bot :)"
WELCOME_MSG = """Welcome to WolframAlpha bot. Only text input is supported.
Default option is to send short message if possible.
Use /i or /image to force image output
Use /s or /steps to get step-by-step solution."""
PROMPT_MSG = "I'm processing your request..."

#message is telebot.types.Message' type

def is_authorized(message) -> bool:
    return message.from_user.username in WHITELIST

@bot.message_handler(commands=["start", "help"])
def welcome_and_help(message) -> None:
    if is_authorized(message):
        bot.reply_to(message, WELCOME_MSG)
    else:
        bot.reply_to(message, NOT_AUTHORIZED_MSG)


def send_prompt_message(message, is_step_by_step=False):
    data = None
    if is_step_by_step:
        data = bot.reply_to(message, PROMPT_MSG + "\nPlease be patient...")
    else:
        data = bot.reply_to(message, PROMPT_MSG)
    return dict(message_id = data.message_id, chat_id = data.chat.id)

def delete_prompt_message(prompt):
    bot.delete_message(prompt["chat_id"], prompt["message_id"])

def remove_commands_from_message(message_text):
    return message_text.replace("/image ", "").replace("/steps", "").replace("/i ", "").replace("/s ", "").strip()


def get_wolfram_response(message, is_image=False):
    prompt = send_prompt_message(message)

    text = remove_commands_from_message(message.text)
    search = wolfram.query_wolfram(text, is_image)

    delete_prompt_message(prompt)
    return search

def get_wolfram_steps(message):
    prompt = send_prompt_message(message, True)

    text = remove_commands_from_message(message.text)
    search = wolfram.get_step_by_step(text)

    delete_prompt_message(prompt)
    return search


def send_image_result(message, search_result):
    search_result = search_result.replace(WolframBot.RESULT_SAVED_MSG, "")
    bot.send_document(message.chat.id, open(search_result, "rb"), reply_to_message_id=message.id)
    system("rm {}".format('"./' + search_result + '"'))

    
@bot.message_handler(commands=["i", "image"])
def send_image(message) -> None:
    if is_authorized(message):
        search_result = get_wolfram_response(message, True)
        if search_result != WolframBot.ERROR_MSG:
            send_image_result(message, search_result)
        else:
            bot.reply_to(message, search_result)
    else:
        bot.reply_to(message, NOT_AUTHORIZED_MSG)

@bot.message_handler(commands=["s", "steps"])
def send_steps(message) -> None:
    if is_authorized(message):
        search_result = get_wolfram_steps(message)
        if search_result != WolframBot.ERROR_MSG and search_result != WolframBot.NO_STEPS_MSG:
            send_image_result(message, search_result)
        else:
            bot.reply_to(message, search_result)
    else:
        bot.reply_to(message, NOT_AUTHORIZED_MSG)

@bot.message_handler(func=lambda message: True)
def handle_query(message) -> None:
    if is_authorized(message):
        search_result = get_wolfram_response(message)

        if not search_result.startswith(WolframBot.RESULT_SAVED_MSG):
            bot.reply_to(message, search_result)
        else:
            send_image_result(message, search_result)
    else:
        bot.reply_to(message, NOT_AUTHORIZED_MSG)


if __name__ == "__main__":
    bot.infinity_polling(interval=0, timeout=25)
