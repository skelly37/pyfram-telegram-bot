# pyfram-telegram-bot
Open-source backend for [WolframAlpha](https://wolframalpha.com) Telegram bot

- Telegram API wrapper: [telebot](https://github.com/eternnoir/pyTelegramBotAPI)
- Deployed on: [Heroku](https://heorku.com)

## Current status:
The bot works pretty fine for the end-user, all the functionality I wanted to introduce is already there. Only the code [needs some polishing](#todo)

## What can the end-user achieve with bot? How to use it?
- `/s` or `/steps` command before actual query — get step-by-step solution (if possible).
  - **NOTE** This may take quite a long time but it's not a problem with my code, it's WolframAlpha API issue. 
- `/i` or `/image` command before actual query — force get result as an image.
- `/start` or `/help` commands — provide basic help.
- If no commands are provided, the bot has these defaults:
  - Try getting and sending short text anwser
  - If the short anwser is not available, return image (as in `/image`)

## How the code works?
Well, it's no dark magic. I simply query WolframAlpha API and send text anwser or image:
  - get user input via telebot
  - `requests.get()`
  - then send the result via telebot

The short import lists are also self-explanatory. As you can see in [TODO](#todo), in free time I'll also introduce type checking. Bot is ready to go to Heroku, code is clear and understandable (at least I hope so).

## Why won't we develop a public bot?
Wolfram API for a non-personal use is quite expensive and we cannot afford being *Santa Claus*. That's why we provide only the code and left the `appID` empty. Feel free to set up such a bot for personal use with your own API key or to gain funds for a fully public one.

But if you want to see the bot in action: @wolaph_bot

## [api_calls.py](https://github.com/skelly37/pyfram-telegram-bot/blob/main/api_calls.py) simple documentation
The whole API wrapper is developed in `WolframBot` class. 

- Attributes:
  - `__app_ids` (list) — list of app_ids to use with the `WolframBot`  
  - `__num_of_appids` (int) — how many app IDs are provided?

- Methods:
  - `__init__`
    - Arguments:
      - `app_ids` (list) — list of app_ids to use with the `WolframBot`
    - Returns:
      - None    
  - `__get_random_id`
    - Arguments:
      - None
    - Returns:
      - Randomly chosen app ID from `self.__app_ids` (str)
  - `__short_anwser`
    - Arguments:
      - `query` (str) — question to ask WolframAlpha
    - Returns:
      - Result of querying WolframAlpha. May return "No short answer available" (str)
  - `__get_image`
    - Arguments:
      - `query` (str) — question to ask WolframAlpha
    - Returns:
      - Name of the file where result is stored. May return "Error processing your request." (str)
  - `__get_url_of_steps_image`
    - Arguments:
      - `img_xml` (str) — raw query result.
    - Returns:
      - Desired url from XML. May return "No step by step solution available." (str)
  - `get_step_by_step`
    - Arguments:
      - `query` (str) — question to ask WolframAlpha
    - Returns:
      - Name of the file where result is stored. May return "Error processing your request." or "No step by step solution available." (str)
  - `query_wolfram`
    - Arguments:
      - `query` (str) — question to ask WolframAlpha
      - `is_image` (bool, optional) — if True, the method will skip trying to get short anwser and proceed to fetching image in the first place
    - Returns:
      - Short anwser, filename, may also return "Error processing your request." or "No step by step solution available." (str)



## TODO:
- [ ] Make good use of `typing` and enforce strict type checking in all functions.
- [ ] Insert here a short video showing the bot in action.
- [ ] Test fastapi or replace infinite pooling with webhook any possible way (?)
- [ ] Make it async (?)

## Contribution
Feel free to create issues, to make PRs, every kind of help is welcome here

You can reach me and talk about this project on:
- Telegram (preferred): @skelly37
- Discord: skelly#3578

## License
The code is and will be distributed under the permissive [MIT License](https://github.com/skelly37/pyfram-telegram-bot/blob/main/LICENSE)
