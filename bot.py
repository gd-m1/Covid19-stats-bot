import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from handlers import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

commands = {'start': 'Start using this bot',
            'country': 'Please, write a country name',
            'statistics': 'Query statistics',
            'help': 'Useful information about this bot'}

COUNTRY = 0


def main():
    PORT = int(os.environ.get('PORT', '8443'))
    mybot = Updater(os.getenv('API_KEY'))

    logging.info('Bot is starting')

    country_name = ConversationHandler(
        entry_points=[CommandHandler('country', country_start)],
        states={
            COUNTRY: [CommandHandler('cancel', cancel),
                      MessageHandler(Filters.text, get_country)],
        },
        fallbacks=[MessageHandler(
            Filters.video | Filters.photo | Filters.document,
            help)]
    )
    # Add handlers
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(country_name)
    dp.add_handler(CommandHandler('statistics', get_query_stats))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    # Set up a webhook
    # For long polling connection read README file
    mybot.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=os.getenv('API_KEY'),
                        webhook_url=os.getenv('HEROKU_URL') + os.getenv('API_KEY'))
    mybot.idle()


if __name__ == '__main__':
    main()
