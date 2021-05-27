import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers import *
import settings

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

commands = {'start': 'Start using this bot',
            'country': 'Please, write a country name',
            'help': 'Useful information about this bot'}

COUNTRY = 0


def main():
    mybot = Updater(settings.API_KEY)

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

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(country_name)
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
