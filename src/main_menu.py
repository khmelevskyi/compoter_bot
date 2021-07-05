from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from os import getcwd
from variables import *


def another_prod_handler(update, context):
    print(update.callback_query.data)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    try:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.chat_data['photo_to_edit'])
    except:
        pass
    # lang = language(update)
    if update.callback_query.data =='next' or update.callback_query.data =='prev':
        update.callback_query.data = 'next_prev_plug'
        
        return main_menu_handler(update, context)
    elif update.callback_query.data =='buy':
        order_item = context.chat_data['active']
        inline_one_two_buttons = [InlineKeyboardButton('1', callback_data='1'), InlineKeyboardButton('2', callback_data='2')]
        inline_three_four_buttons = [InlineKeyboardButton('3', callback_data='3'), InlineKeyboardButton('4', callback_data='4')]
        inline_five_ten_buttons = [InlineKeyboardButton('5', callback_data='5'), InlineKeyboardButton('10', callback_data='10')]
        markup = InlineKeyboardMarkup([inline_one_two_buttons, inline_three_four_buttons, inline_five_ten_buttons], resize_keyboard=True, one_time_keyboard=True)
        context.chat_data['amount_msg_to_del'] = context.bot.send_message(chat_id=update.effective_chat.id, text=str('Выберите количество или напишите вручную: '), reply_markup=markup).message_id
        return AMOUNT_HANDLER
    else:
        return unknown_command(update, context)


def main_menu_handler(update, context):
    print(update.callback_query.data)
    # print(update.message_id)
    try:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    except:
        pass
    try:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.chat_data['photo_to_edit'])
    except:
        pass
    # lang = language(update)
    if update.callback_query.data =='next' or update.callback_query.data =='prev':
        filename = getcwd() + '/src/compot.png'
        with open(filename, 'rb') as file:
            photo_to_edit = context.bot.send_photo(chat_id=update.effective_chat.id, photo=file).message_id

        inline_next_prev_buttons = [InlineKeyboardButton('назад', callback_data='prev'), InlineKeyboardButton('вперед', callback_data='next')]
        inline_buy_buttons = [InlineKeyboardButton('купить', callback_data='buy')]
        inline_info_buttons = [InlineKeyboardButton('инфо', callback_data='info')]
        markup = InlineKeyboardMarkup([inline_next_prev_buttons, inline_buy_buttons, inline_info_buttons], resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=str('compot'), reply_markup=markup)
        context.chat_data['active'] = 'compot'
        context.chat_data['active_photo'] = '/src/compot.png'
        context.chat_data['photo_to_edit'] = photo_to_edit
        return ANOTHER_PROD_HANDLER
    elif update.callback_query.data =='buy':
        order_item = context.chat_data['active']
        inline_one_two_buttons = [InlineKeyboardButton('1', callback_data='1'), InlineKeyboardButton('2', callback_data='2')]
        inline_three_four_buttons = [InlineKeyboardButton('3', callback_data='3'), InlineKeyboardButton('4', callback_data='4')]
        inline_five_ten_buttons = [InlineKeyboardButton('5', callback_data='5'), InlineKeyboardButton('10', callback_data='10')]
        markup = InlineKeyboardMarkup([inline_one_two_buttons, inline_three_four_buttons, inline_five_ten_buttons], resize_keyboard=True, one_time_keyboard=True)
        context.chat_data['amount_msg_to_del'] = context.bot.send_message(chat_id=update.effective_chat.id, text=str('Выберите количество или напишите вручную: '), reply_markup=markup).message_id
        return AMOUNT_HANDLER
    else:
        filename = getcwd() + '/src/limonad.png'
        with open(filename, 'rb') as file:
            photo_to_edit = context.bot.send_photo(chat_id=update.effective_chat.id, photo=file).message_id

        inline_next_prev_buttons = [InlineKeyboardButton('назад', callback_data='prev'), InlineKeyboardButton('вперед', callback_data='next')]
        inline_buy_buttons = [InlineKeyboardButton('купить', callback_data='buy')]
        inline_info_buttons = [InlineKeyboardButton('инфо', callback_data='info')]
        markup = InlineKeyboardMarkup([inline_next_prev_buttons, inline_buy_buttons, inline_info_buttons], resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=str('Лимонад'), reply_markup=markup)
        
        context.chat_data['active'] = 'limonad'
        context.chat_data['active_photo'] = '/src/limonad.png'
        context.chat_data['photo_to_edit'] = photo_to_edit
        return MAIN_MENU_HANDLER


def unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Unknown command')
    filename = getcwd() + '/src/photo.png'
    #picture = PhotoSize(getcwd() + '/src/Logic/', 'photo.png', width=120, height=50)
    with open(filename, 'rb') as file:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=file, caption='Press this button and choose the option')