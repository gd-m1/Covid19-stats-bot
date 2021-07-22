# Covid19 Stats Bot
A Telegram bot that grabs live Coronavirus statistics from [API](https://rapidapi.com/slotixsro-slotixsro-default/api/covid-19-tracking/).  
Check the bot here [@covid19_stats21_bot](https://t.me/covid19_stats21_bot).

## Requirements:
* Python 3.8+
* MongoDB 4.4+

## Installation
* Setup a virtual environment and install the project requirements:
```
pip install -r requirements.txt
```
* Install [MongoDB](https://www.mongodb.com/try/download/community)
* Set environment variables
* Go to [RAPIDAPI](https://rapidapi.com/slotixsro-slotixsro-default/api/covid-19-tracking/) and get a free API key. You can obtain it from the user dashboard after registration.
* Change Telegram API connection from webhook to long polling:
```python
# Long polling
mybot.start_polling()
mybot.idle()


if __name__ == '__main__':
    main()
```  
```python
# Webhook
PORT = int(os.environ.get('PORT', '8443'))
mybot.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=os.getenv('API_KEY'),
                        webhook_url=os.getenv('HEROKU_URL') + os.getenv('API_KEY'))
    mybot.idle()


if __name__ == '__main__':
    main()
```

## Available commands:
* /start - start a conversation with the bot
* /country - get covid-19 cases by country
* /statistics - usage of the bot
* /help - useful information
