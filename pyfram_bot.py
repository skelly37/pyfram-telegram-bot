"""
You can use it basically anywhere, this script does not use webhook,
thus it requires no domain. Feel free to run it on, e.g., your own PC
"""


import telebot  # type: ignore
from os import system
from api_calls import WolframBot
from typing import List, Dict

if __name__ == "__main__":
    TOKEN: str = open("./bot_token.txt").readline().strip()
    WHITELIST: List[str] = [x.strip() for x in open("./whitelist.txt").readlines()]
    API_KEYS: List[str] = [x.strip() for x in open("./api_key.txt").readlines()]
    wolfram: WolframBot = WolframBot(API_KEYS)

# noinspection PyUnboundLocalVariable
bot: telebot.TeleBot = telebot.TeleBot(TOKEN, parse_mode="MARKDOWN")

NOT_AUTHORIZED_MSG: str = "Sorry but you're not authorized to use this bot :)"
WELCOME_MSG: str = """Welcome to WolframAlpha bot. Only text input is supported.
Default option is to send short message if possible.
Use /i or /image to force image output
Use /s or /steps to get step-by-step solution."""
PROMPT_MSG: str = "I'm processing your request..."

#message is telebot.types.Message' type

def is_authorized(message: telebot.types.Message) -> bool:
    return message.from_user.username in WHITELIST

@bot.message_handler(commands=["start", "help"])
def welcome_and_help(message: telebot.types.Message) -> None:
    if is_authorized(message):
        bot.reply_to(message, WELCOME_MSG)
    else:
        bot.reply_to(message, NOT_AUTHORIZED_MSG)


def send_prompt_message(message: telebot.types.Message, is_step_by_step: bool = False) -> Dict[str, str]:
    data = None
    if is_step_by_step:
        data = bot.reply_to(message, PROMPT_MSG + "\nPlease be patient...")
    else:
        data = bot.reply_to(message, PROMPT_MSG)
    # noinspection PyTypeChecker
    return dict(message_id = data.message_id, chat_id = data.chat.id)

def delete_prompt_message(prompt: Dict[str, str]) -> None:
    # noinspection PyTypeChecker  
    bot.delete_message(prompt["chat_id"], prompt["message_id"])

def remove_commands_from_message(message_text: str) -> str:
    return message_text.replace("/image ", "").replace("/steps", "").replace("/i ", "").replace("/s ", "").strip()


def get_wolfram_response(message: telebot.types.Message, is_image: bool = False) -> str:
    prompt: Dict[str, str] = send_prompt_message(message)

    text: str = remove_commands_from_message(message.text)
    search: str = wolfram.query_wolfram(text, is_image)

    delete_prompt_message(prompt)
    return search

def get_wolfram_steps(message: telebot.types.Message) -> str:
    prompt: Dict[str, str] = send_prompt_message(message, True)

    text: str = remove_commands_from_message(message.text)
    search: str = wolfram.get_step_by_step(text)

    delete_prompt_message(prompt)
    return search


def send_image_result(message: telebot.types.Message, search_result: str) -> None:
    search_result = search_result.replace(WolframBot.RESULT_SAVED_MSG, "")
    bot.send_document(message.chat.id, open(search_result, "rb"), reply_to_message_id=message.id)
    system("rm {}".format('"./' + search_result + '"'))


@bot.message_handler(commands=["i", "image"])
def send_image(message: telebot.types.Message) -> None:
    if is_authorized(message):
        search_result: str = get_wolfram_response(message, True)
        if search_result != WolframBot.ERROR_MSG:
            send_image_result(message, search_result)
        else:
            bot.reply_to(message, search_result)
    else:
        bot.reply_to(message, NOT_AUTHORIZED_MSG)

@bot.message_handler(commands=["s", "steps"])
def send_steps(message: telebot.types.Message) -> None:
    if is_authorized(message):
        search_result: str = get_wolfram_steps(message)
        if search_result != WolframBot.ERROR_MSG and search_result != WolframBot.NO_STEPS_MSG:
            send_image_result(message, search_result)
        else:
            bot.reply_to(message, search_result)
    else:
        bot.reply_to(message, NOT_AUTHORIZED_MSG)

@bot.message_handler(func=lambda message: True)
def handle_query(message: telebot.types.Message) -> None:
    if is_authorized(message):
        search_result: str = get_wolfram_response(message)

        if not search_result.startswith(WolframBot.RESULT_SAVED_MSG):
            bot.reply_to(message, search_result)
        else:
            send_image_result(message, search_result)
    else:
        bot.reply_to(message, NOT_AUTHORIZED_MSG)

@bot.inline_handler(lambda message: len(message.query) > 0)
def handle_inline_query(inline_query: telebot.types.InlineQuery) -> None:
    if inline_query.from_user.username in WHITELIST:
        q: str = inline_query.query
        res: str = wolfram.query_wolfram(query=q, is_image=False, inline_mode=True)
        if res != WolframBot.NO_SHORT_MSG:
            r = telebot.types.InlineQueryResultArticle("1", q, telebot.types.InputTextMessageContent(res))
        else:
            r = telebot.types.InlineQueryResultArticle("1", res, telebot.types.InputTextMessageContent(res))

        # noinspection PyTypeChecker
        bot.answer_inline_query(inline_query.id, [r])
    else:
        r = telebot.types.InlineQueryResultArticle("1", NOT_AUTHORIZED_MSG, telebot.types.InputTextMessageContent(NOT_AUTHORIZED_MSG))
        # noinspection PyTypeChecker
        bot.answer_inline_query(inline_query.id, [r])

if __name__ == "__main__":
    bot.infinity_polling(interval=0, timeout=25)
