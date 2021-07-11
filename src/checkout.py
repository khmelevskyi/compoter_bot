from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, LabeledPrice, ShippingOption

from main_menu import main_menu_handler
from variables import *
from text import text


def forward_to_admin_handler(update, context):
    context.bot.forward_message(chat_id=476800499, from_chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    context.bot.send_message(chat_id=476800499, text=f"User data: {update.effective_chat}, \nOrder info: {context.user_data}")
    context.chat_data['active'] = ''
    context.user_data.clear()

def successful_payment_callback(update, context):
    """Confirms the successful payment."""
    # do something after successfully receiving payment?
    update.message.reply_text("Спасибо за покупку!")
    context.bot.send_message(chat_id=476800499, text=f"User data: {update.effective_chat}, \nOrder info: {context.user_data}")
    context.chat_data['active'] = ''
    context.user_data.clear()

def precheckout_callback(update, context):
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Compoter-Bot':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Что-то пошло не так...")
    else:
        query.answer(ok=True)


def shipping_callback(update, context):
    """Answers the ShippingQuery with ShippingOptions"""
    query = update.shipping_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Compoter-Bot':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Что-то пошло не так...")
        return

    # First option has a single LabeledPrice
    options = [ShippingOption('1', 'Доставка по Одессе', [LabeledPrice('Доставка', 0)])]
    # second option has an array of LabeledPrice objects
    # price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
    # options.append(ShippingOption('2', 'Shipping Option B', price_list))
    query.answer(ok=True, shipping_options=options)


def checkout_handler(update, context):
    # print(context.user_data[context.chat_data['active']])
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    try:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.chat_data['photo_to_edit'])
    except:
        pass

    # if update.callback_query.data == 'online' or update.callback_query.data == 'cash':
    #     context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your order was accepted \n You ordered:\n{context.user_data}')\
    price = 45
    
    if update.callback_query.data == 'online':
        chat_id = update.effective_chat.id
        title = "Оплата"
        description = f"Оплата за {int(context.user_data[context.chat_data['active']])} {text['checkout_items'][context.chat_data['active']]}"
        # select a payload just for you to recognize its the donation from your bot
        payload = "Compoter-Bot"
        # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
        provider_token = "632593626:TEST:sandbox_i5742576186"
        currency = "UAH"
        # price in dollars
        price_online = price * int(context.user_data[context.chat_data['active']])
        # price * 100 so as to include 2 decimal points
        # check https://core.telegram.org/bots/payments#supported-currencies for more details
        prices = [LabeledPrice("Лимонад/Компот", price_online * 100)]

        # optionally pass need_name=True, need_phone_number=True,
        # need_email=True, need_shipping_address=True, is_flexible=True
        context.bot.send_invoice(
            chat_id,
            title,
            description,
            payload,
            provider_token,
            currency,
            prices,
            timeout=30,
            need_name=True,
            need_phone_number=True,
            need_email=False,
            need_shipping_address=True,
            is_flexible=True,
        )

    elif update.callback_query.data == 'cash':
        context.bot.send_message(chat_id=update.effective_chat.id, text=
        f'Ваш заказ: {int(context.user_data[context.chat_data["active"]])} {text["checkout_items"][context.chat_data["active"]]}\nСтоимость заказа:{price*int(context.user_data[context.chat_data["active"]])}\nУкажите куда привезти!')

        return FORWARD_TO_ADMIN
    
    elif update.callback_query.data == 'cancel':
        context.user_data.clear()
        context.chat_data['active'] = ''
        return main_menu_handler(update, context)



def amount_handler(update, context):
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    try:
        amount = update.message.text
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.chat_data['amount_msg_to_del'])
    except AttributeError:
        amount = update.callback_query.data

    order_item = context.chat_data['active']
    order = dict()
    order[order_item] = amount
    context.user_data[order_item] = amount

    print(context.user_data)
    inline_online_button = [InlineKeyboardButton('Картой', callback_data='online')]
    inline_cash_button = [InlineKeyboardButton('Наличными', callback_data='cash')]
    inline_cancel_button = [InlineKeyboardButton('Отмена / Очистить корзину', callback_data='cancel')]
    markup = InlineKeyboardMarkup([inline_online_button, inline_cash_button, inline_cancel_button], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=str('Каким способом хотите оплатить?'), reply_markup=markup)
    return CHECKOUT