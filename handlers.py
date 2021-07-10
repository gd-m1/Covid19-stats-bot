import logging

from jinja2 import Template
from telegram import ParseMode
from telegram.ext.conversationhandler import ConversationHandler

from bot import commands, COUNTRY
from db import db, save_user_query, get_users_queries
from utils import get_country_statistics


# Start command handler
def greet_user(update, _):
    text = f"Hello {update.message.chat.first_name}! Please choose commands from the menu.\n"
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(text)
    help(update, _)


# Reply if user message is not handled by other handlers
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


# Get statistics and render it as html
def get_country(update, _):
    country = update.message.text
    save_user_query(db, country, update.effective_user)
    country_stats = get_country_statistics(country.strip().lower())
    if country_stats['Country_text'] == 'World':
        update.message.reply_text("The name is incorrect. Sending World statistics...")
    with open('templates/country_stats.html', 'r', encoding='UTF-8') as html:
        template = Template(html.read())
    result = template.render(date=country_stats['Last Update'],
                             country=country_stats['Country_text'].upper(),
                             new_cases=country_stats['New Cases_text'],
                             active_cases=country_stats['Active Cases_text'],
                             recovered=country_stats['Total Recovered_text'],
                             total_cases=country_stats['Total Cases_text'],
                             new_deaths=country_stats['New Deaths_text'],
                             total_deaths=country_stats['Total Deaths_text'])
    update.message.reply_text(result, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


# Statistics handler
def get_query_stats(update, _):
    query_stats = get_users_queries(db)
    with open('templates/query_stats.html', 'r', encoding='UTF-8') as html:
        template = Template(html.read())
    result = template.render(queries=query_stats['queries'], users=query_stats['users'])
    update.message.reply_text(result, parse_mode=ParseMode.HTML)


# Cancel command handler
def cancel(update, _):
    update.message.reply_text("Bye! See you again soon.")

    return ConversationHandler.END


# Help command handler
def help(update, _):
    help_text = "The following commands are available:\n\n"
    for key in commands:
        help_text += '/' + key + ': '
        help_text += commands[key] + '\n'
    help_text += 'Be careful, @covid19_stats21_bot speaks English.'
    update.message.reply_text(help_text)
