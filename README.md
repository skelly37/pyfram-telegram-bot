# pyfram-telegram-bot
Open-source backend for [WolframAlpha](https://wolframalpha.com) Telegram bot

## Current status:
*in an early stage of development*

### What will be here?
Code of a simple bot that can make using WolframAlpha easier. Either by inline mode, or by starting a conversation with it, it will:
- Provide short anwser (default option)
- Provide simple anwser as a .png file (fallback if no short anwser is available or if specified)

### Already done:
- [x] Python interface for WolframAlpha API

### TODO:
- [x] Write or find a webhook to work with Telegram Bot API 
  - solved with [telebot](https://github.com/eternnoir/pyTelegramBotAPI)
- [x] Put WolframAlpha interface into the webhook
- [ ] Introduce type-checker for is_image in WolframBot.query_wolfram()
- [x] Implement server side whitelist (of users allowed to use the bot)
- [ ] Deploy the code onto a server
- [ ] Write fancy `setup.py` and documentation
- [ ] Make final test of everything

## Why won't we develop a public bot?
Wolfram API for a non-personal use is quite expensive and we cannot afford being *Santa Claus*. That's why we provide only the code and left the `appID` empty. Feel free to set up such a bot for personal use with your own API key or to gain funds for a fully public one. 

## Contribution
Feel free to create issues, to make PRs, every kind of help is welcome here

## License
The code is and will be distributed under the permissive [MIT License](https://github.com/skelly37/pyfram-telegram-bot/blob/main/LICENSE)
