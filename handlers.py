import logging

from emoji import emojize
from telegram import ParseMode
from telegram.ext.conversationhandler import ConversationHandler
from bot import commands, COUNTRY
from utils import get_country_statistics


# Start command handler
def greet_user(update, _):
    text = "Hello! Please choose commands from the menu.\n"
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(text)
    help(update, _)


# Replies if user message is not handled by other handlers
def talk_to_me(update, _):
    user_text = update.message.text
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(f"Hello {update.message.chat.first_name}! You texted: {user_text}")
    help(update, _)


# Country command handler
def country_start(update, _):
    text = "Write name of the country or press /cancel"
    update.message.reply_text(text)
    
    return COUNTRY


# Gets statistics and renders it as html
def get_country(update, _):
    country = update.message.text
    country_statistics = get_country_statistics(country.strip().lower())
    if country_statistics['Country_text'] == 'World':
        update.message.reply_text("The name is incorrect. Sending World statistics...")
    
    message = emojize(
        f"<b>:watch: Last Update: {country_statistics['Last Update']}</b>\n\n"
        f"<b>:earth_americas: {country_statistics['Country_text'].upper()}</b>\n\n"
        "<b>:mask: CASES</b>\n\n"
        f"<b>New Cases: {country_statistics['New Cases_text']}</b>\n"
        f"<b>Active: {country_statistics['Active Cases_text']}</b>\n"
        f"<b>Recovered: {country_statistics['Total Recovered_text']}</b>\n"
        f"<b>Total Cases: {country_statistics['Total Cases_text']}</b>\n"
        f"<b>New Deaths: {country_statistics['New Deaths_text']}</b>\n"
        f"<b>Total Deaths: {country_statistics['Total Deaths_text']}</b>",
        use_aliases=True
    )
    update.message.reply_text(message, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


# Cancel command handler
def cancel(update, _):
    update.message.reply_text("Bye! I hope to see you again soon.")
    
    return ConversationHandler.END


# Help command handler
def help(update, _):
    help_text = "The following commands are available:\n"
    for key in commands:
        help_text += '/' + key + ': '
        help_text += commands[key] + '\n'
    update.message.reply_text(help_text)
