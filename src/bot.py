from telegram.callbackquery import CallbackQuery
from telegram.ext import Updater, Filters, ConversationHandler, MessageHandler, CommandHandler, ChosenInlineResultHandler, InlineQueryHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ as env, getcwd, path
import logging # used for error detection
from dotenv import load_dotenv
from telegram.files.inputmedia import InputMedia, InputMediaPhoto

from main_menu import another_prod_handler, main_menu_handler
from variables import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def enviroment_files():
    def check_file(filename):
        print()
        create_path = path.abspath(getcwd())
        create_path = path.join(create_path, filename)
        if not path.exists(create_path):
            print(f"{filename} not found")
            print(f"create_path: {create_path}")
            if filename == ".env":
                with open(create_path, "w") as env:
                    env.write("API_KEY=''\n\n")

                    env.write("host=''\n")
                    env.write("port=''\n\n")

                    env.write("user_email=''\n")
                    env.write("password_email=''\n\n")

                    env.write("from=''\n")
                    env.write("to=''\n\n")
            else:
                f = open(create_path, "x")
                f.close()
            print(f"{filename} need to be completed")
        else:
            print(f"{filename} exist")
        print()
    check_file(".env")
    # check_file("Vargan-API.json")


enviroment_files()
load_dotenv()
print("Modules import succesfull")


def checkout_handler(update, context):
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    try:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.chat_data['photo_to_edit'])
    except:
        pass

    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your order was accepted \n You ordered:\n{context.user_data}')
    context.chat_data['active'] = ''
    context.user_data.clear()
    return main_menu_handler(update, context)


def checkout_or_continue_handler(update, context):
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    try:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.chat_data['photo_to_edit'])
    except:
        pass

    answer = update.callback_query.data
    if answer == 'checkout':
        print(context.user_data)
        inline_online_button = [InlineKeyboardButton('Картой', callback_data='online')]
        inline_cash_button = [InlineKeyboardButton('Наличными', callback_data='cash')]
        inline_cancel_button = [InlineKeyboardButton('Отмена / Очистить корзину', callback_data='cancel')]
        markup = InlineKeyboardMarkup([inline_online_button, inline_cash_button, inline_cancel_button], resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=str('Каким способом хотите оплатить?'), reply_markup=markup)
        return CHECKOUT
    elif answer == 'continue':
        filename = getcwd() + '/src/limonad.png'
        with open(filename, 'rb') as file:
            photo_to_edit = context.bot.send_photo(chat_id=update.effective_chat.id, photo=file).message_id

        inline_next_prev_buttons = [InlineKeyboardButton('назад', callback_data='prev'), InlineKeyboardButton('вперед', callback_data='next')]
        inline_buy_buttons = [InlineKeyboardButton('купить', callback_data='buy')]
        inline_info_buttons = [InlineKeyboardButton('инфо', callback_data='info')]
        markup = InlineKeyboardMarkup([inline_next_prev_buttons, inline_buy_buttons, inline_info_buttons], resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=str('limonad'), reply_markup=markup)

        context.chat_data['active'] = 'limonad'
        context.chat_data['active_photo'] = '/src/limonad.png'
        context.chat_data['photo_to_edit'] = photo_to_edit
        return MAIN_MENU_HANDLER
    elif answer == 'cancel':
        context.user_data.clear()
        return main_menu_handler(update, context)


def amount_handler(update, context):
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    try:
        amount = update.message.text
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.chat_data['amount_msg_to_del'])
    except AttributeError:
        amount = update.callback_query.data

    order_item = context.chat_data['active']
    order_list = []
    order = dict()
    order[order_item] = amount
    context.user_data[order_item] = amount

    inline_checkout_button = [InlineKeyboardButton('Оформляем заказ', callback_data='checkout')]
    inline_continue_button = [InlineKeyboardButton('Прододжить покупки', callback_data='continue')]
    inline_cancel_button = [InlineKeyboardButton('Отмена / Очистить корзину', callback_data='cancel')]
    markup = InlineKeyboardMarkup([inline_checkout_button, inline_continue_button, inline_cancel_button], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=str('Оформляем заказ или продолжаем покупки?'), reply_markup=markup)
    return CHECKOUT_OR_CONTINUE
    


def start(update, context):
    """Welcome greating and proposing to choose the language"""
    # lang = language(update)
    # DB.add_user(update.effective_chat.id)
    
    # if update.effective_chat.id in UM.currentUsers:
    #     del UM.currentUsers[update.effective_chat.id]

    context.bot.send_message(chat_id=update.effective_chat.id, text='What do you want bitch\n')
    print(update.effective_chat)

    filename = getcwd() + '/src/limonad.png'
    with open(filename, 'rb') as file:
        photo_to_edit = context.bot.send_photo(chat_id=update.effective_chat.id, photo=file).message_id

    inline_next_prev_buttons = [InlineKeyboardButton('назад', callback_data='prev'), InlineKeyboardButton('вперед', callback_data='next')]
    inline_buy_buttons = [InlineKeyboardButton('купить', callback_data='buy')]
    inline_info_buttons = [InlineKeyboardButton('инфо', callback_data='info')]
    markup = InlineKeyboardMarkup([inline_next_prev_buttons, inline_buy_buttons, inline_info_buttons], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text=str('limonad'), reply_markup=markup)
    
    context.chat_data['active'] = 'limonad'
    context.chat_data['active_photo'] = '/src/limonad.png'
    context.chat_data['photo_to_edit'] = photo_to_edit
    return MAIN_MENU_HANDLER


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
            MAIN_MENU_HANDLER:            [*necessary_handlers, CallbackQueryHandler(main_menu_handler, pass_chat_data=True, pass_user_data=True, pass_update_queue=True)],
            AMOUNT_HANDLER:            [*necessary_handlers, CallbackQueryHandler(amount_handler, pass_chat_data=True, pass_user_data=True, pass_update_queue=True), MessageHandler(Filters.text, amount_handler)],
            ANOTHER_PROD_HANDLER:      [*necessary_handlers, CallbackQueryHandler(another_prod_handler, pass_chat_data=True, pass_user_data=True, pass_update_queue=True)],
            CHECKOUT_OR_CONTINUE:      [*necessary_handlers, CallbackQueryHandler(checkout_or_continue_handler, pass_chat_data=True, pass_user_data=True, pass_update_queue=True)],
            CHECKOUT:                  [*necessary_handlers, CallbackQueryHandler(checkout_handler, pass_chat_data=True, pass_user_data=True, pass_update_queue=True)],

        },

        fallbacks=[CommandHandler('stop', done)], allow_reentry=True
    )
    dispatcher.add_handler(conv_handler)
    # dispatcher.add_error_handler(error)

    updater.start_polling()
    print("Started succesfully")
    updater.idle()


if __name__ == '__main__':
    main()