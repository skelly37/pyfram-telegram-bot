# pyfram-telegram-bot
Open-source backend for [WolframAlpha](https://wolframalpha.com) Telegram bot

## Current status:
*almost finished*

### What will be here?
Code of a simple bot that can make using WolframAlpha easier. By starting a conversation with it, it will:
- Provide short anwser (default option)
- Provide simple anwser as a .png file (fallback if no short anwser is available or if specified)

### Already done:
- [x] Python interface for WolframAlpha API
- [x] Write or find a webhook to work with Telegram Bot API 
  - solved with [telebot](https://github.com/eternnoir/pyTelegramBotAPI)
- [x] Implement server side whitelist (of users allowed to use the bot)
- [x] Deploy the code onto a server 
  - Solved with Heroku: remember to run `heroku ps:scale worker=1` after starting the enviroment (or add it into Procfile)
- [x] Add `./` in file paths
- [x] Add some prompt like `I'm processing your request...`

### TODO:
- [ ] Make good use of `typing` and enforce strict type checking in all functions.
- [ ] Test fastapi or replace infinite pooling with webhook any possible way
- [ ] Make it async (?)
- [ ] Handle Step-by-Step anwsers somehow (i.e. put these small pictures together into one and send it)
- [ ] Write decent documentation


## Why won't we develop a public bot?
Wolfram API for a non-personal use is quite expensive and we cannot afford being *Santa Claus*. That's why we provide only the code and left the `appID` empty. Feel free to set up such a bot for personal use with your own API key or to gain funds for a fully public one.

But if you want to see the bot in action: @wolaph_bot

## Contribution
Feel free to create issues, to make PRs, every kind of help is welcome here

You can reach me and talk about this project on:
- Telegram (preferred): @skelly37
- Discord: skelly#3578

## License
The code is and will be distributed under the permissive [MIT License](https://github.com/skelly37/pyfram-telegram-bot/blob/main/LICENSE)
