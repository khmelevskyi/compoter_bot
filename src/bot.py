from telegram.ext import Updater, Filters, ConversationHandler, MessageHandler, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler, ShippingQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, LabeledPrice, ShippingOption
from os import environ as env
import logging # used for error detection
from dotenv import load_dotenv

from helpers import enviroment_files
from main_menu import prod_choice_handler, main_menu_handler
from variables import *
from text import text
from checkout import amount_handler, checkout_handler, shipping_callback, precheckout_callback, successful_payment_callback, forward_to_admin_handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


enviroment_files()
load_dotenv()
print("Modules import succesfull")


def start(update, context):
    """Welcome greating and proposing to choose the language"""
    # lang = language(update)
    # DB.add_user(update.effective_chat.id)
    
    # if update.effective_chat.id in UM.currentUsers:
    #     del UM.currentUsers[update.effective_chat.id]
    context.bot.send_message(chat_id=update.effective_chat.id, text='What do you want bitch\n')

    
    return main_menu_handler(update, context)


def done(update, context):
    # context.bot.send_message('Your message was not recognized')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    print("Starting")
    api_key = env.get('API_KEY')

    updater = Updater(token=api_key, use_context=True)
    updater.start_polling()
    dispatcher = updater.dispatcher

    necessary_handlers = [CommandHandler('start', start),
                          CommandHandler('stop', done),]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            # LANG:                 [*necessary_handlers, MessageHandler(Filters.text, setting_lang)],
            MAIN_MENU_HANDLER:         [*necessary_handlers, CallbackQueryHandler(main_menu_handler, pass_chat_data=True, pass_user_data=True, pass_update_queue=True)],
            AMOUNT_HANDLER:            [*necessary_handlers, CallbackQueryHandler(amount_handler, pass_chat_data=True, pass_user_data=True, pass_update_queue=True), MessageHandler(Filters.text, amount_handler)],
            PROD_CHOICE_HANDLER:       [*necessary_handlers, CallbackQueryHandler(prod_choice_handler, pass_chat_data=True, pass_user_data=True, pass_update_queue=True)],
            CHECKOUT:                  [*necessary_handlers, CallbackQueryHandler(checkout_handler, pass_chat_data=True, pass_user_data=True, pass_update_queue=True)],
            FORWARD_TO_ADMIN:          [*necessary_handlers, MessageHandler(Filters.all, forward_to_admin_handler, pass_chat_data=True, pass_user_data=True, pass_update_queue=True)],

        },

        fallbacks=[CommandHandler('stop', done)], allow_reentry=True
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(ShippingQueryHandler(shipping_callback)) # for checkout, doesn't work with conversation handler
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))
    # dispatcher.add_error_handler(error)

    updater.start_polling()
    print("Started succesfully")
    updater.idle()


if __name__ == '__main__':
    main()