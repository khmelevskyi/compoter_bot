from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, LabeledPrice
from os import getcwd
from variables import *
from text import text


def prod_choice_handler(update, context):
    print(update.callback_query.data)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    try:
        for mssg in context.chat_data['photo_to_edit']:
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=mssg.message_id)  
    except:
        pass
    # lang = language(update)
    if update.callback_query.data =='lemonade':
        context.chat_data['active'] = 'lemonade'
    elif update.callback_query.data =='kompot':
        context.chat_data['active'] = 'kompot'
    else:
        context.chat_data['active'] = 'lemonade'
        return main_menu_handler(update, context)
    
    order_item = context.chat_data['active']
    inline_one_two_buttons = [InlineKeyboardButton('1', callback_data='1'), InlineKeyboardButton('2', callback_data='2')]
    inline_three_four_buttons = [InlineKeyboardButton('3', callback_data='3'), InlineKeyboardButton('4', callback_data='4')]
    inline_five_ten_buttons = [InlineKeyboardButton('5', callback_data='5'), InlineKeyboardButton('10', callback_data='10')]
    markup = InlineKeyboardMarkup([inline_one_two_buttons, inline_three_four_buttons, inline_five_ten_buttons], resize_keyboard=True, one_time_keyboard=True)
    context.chat_data['amount_msg_to_del'] = context.bot.send_message(chat_id=update.effective_chat.id, text=str('Отлично!\nВыберите количество или напишите вручную: '), reply_markup=markup).message_id
    return AMOUNT_HANDLER
    


def main_menu_handler(update, context):
    # print(update.callback_query.data)
    # print(update.message_id)
    print(update.effective_chat)

    filename = getcwd() + '/src/img/lemonade.png'
    filename2 = getcwd() + '/src/img/kompot.png'
    with open(filename, 'rb') as file:
        with open(filename2, 'rb') as file2:
            limonad_photo = InputMediaPhoto(media=file)
            compot_photo = InputMediaPhoto(media=file2)
            photos_to_delete = context.bot.send_media_group(update.effective_chat.id, media=[limonad_photo, compot_photo])
        # photo_to_edit = context.bot.send_photo(chat_id=update.effective_chat.id, photo=file).message_id

    inline_limonad_button = [InlineKeyboardButton('Лимонад', callback_data='lemonade')]
    inline_compot_buttons = [InlineKeyboardButton('Компот', callback_data='kompot')]
    markup = InlineKeyboardMarkup([inline_limonad_button, inline_compot_buttons], resize_keyboard=True, one_time_keyboard=True)
    try:
        update.message.reply_text(text=text['items_descr'], reply_markup=markup)
    except AttributeError:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text['items_descr'], reply_markup=markup)
    
    context.chat_data['active'] = ''
    context.chat_data['photo_to_edit'] = photos_to_delete
    return PROD_CHOICE_HANDLER


def unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Unknown command')
    filename = getcwd() + '/src/img/photo.png'
    #picture = PhotoSize(getcwd() + '/src/Logic/', 'photo.png', width=120, height=50)
    with open(filename, 'rb') as file:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=file, caption='Press this button and choose the option')