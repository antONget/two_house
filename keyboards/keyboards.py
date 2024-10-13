from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder
#from database.table import async_session, Stations, Doctors
import logging

# Кнопки главной клавиатуры
def kb_hause() -> ReplyKeyboardMarkup:
    logging.info(f'def kb_hause() -> ReplyKeyboardMarkup:')
    button_1 = KeyboardButton(text='дом 1')
    button_2 = KeyboardButton(text='дом 2')

    keybord = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2], ], resize_keyboard=True
    )
    return keybord

def kb_yes_no() -> ReplyKeyboardMarkup:
    logging.info(f'def kb_yes_no() -> ReplyKeyboardMarkup:')
    button_1 = KeyboardButton(text='Да')
    button_2 = KeyboardButton(text='Нет')

    keybord = ReplyKeyboardMarkup(
        keyboard=[[button_1, button_2], ], resize_keyboard=True
    )
    return keybord

def kb_doorway() -> ReplyKeyboardMarkup:
    logging.info(f'def kb_yes_no() -> ReplyKeyboardMarkup:')
    button_1 = KeyboardButton(text='1 подъезд')
    button_2 = KeyboardButton(text='2 подъезд')
    button_3 = KeyboardButton(text='3 подъезд')
    button_4 = KeyboardButton(text='4 подъезд')

    keybord = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2],  [button_3],  [button_4], ], resize_keyboard=True
    )
    return keybord

def kb_stage() -> ReplyKeyboardMarkup:
    logging.info(f'def kb_stage() -> ReplyKeyboardMarkup:')
    button_1 = KeyboardButton(text='1 этаж')
    button_2 = KeyboardButton(text='2 этаж')
    button_3 = KeyboardButton(text='3 этаж')
    button_4 = KeyboardButton(text='4 этаж')
    button_5 = KeyboardButton(text='5 этаж')
    button_6 = KeyboardButton(text='6 этаж')
    button_7 = KeyboardButton(text='7 этаж')
    button_8 = KeyboardButton(text='8 этаж')

    keybord = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2],  [button_3],  [button_4], [button_5], [button_6],  [button_7],  [button_8], ], resize_keyboard=True
    )
    return keybord


def kb_no_send() -> ReplyKeyboardMarkup:
    logging.info(f'def kb_no_send() -> ReplyKeyboardMarkup:')
    button_1 = KeyboardButton(text='Нет')
    button_2 = KeyboardButton(text='Отправить')

    keybord = ReplyKeyboardMarkup(
        keyboard=[[button_1, button_2], ], resize_keyboard=True
    )
    return keybord

def kb_aristarch() -> ReplyKeyboardMarkup:
    logging.info(f'def kb_aristarch() -> ReplyKeyboardMarkup:')
    button_1 = KeyboardButton(text='Мой профиль')
    button_2 = KeyboardButton(text='Справочник')
    button_3 = KeyboardButton(text='Новости')
    button_4 = KeyboardButton(text='Поиск')

    keybord = ReplyKeyboardMarkup(
        keyboard=[[button_1, button_2],  [button_3, button_4], ], resize_keyboard=True, is_persistent=True
    )
    return keybord

def kb_inline_set_my_profile() -> InlineKeyboardMarkup:
    logging.info(f'def kb_inline_set_my_profile() -> InlineKeyboardMarkup:')
    button_phone = InlineKeyboardButton(
        text= 'Телефон',
        callback_data='set_phone'
    )
    button_auto1 = InlineKeyboardButton(
        text= 'Авто 1',
        callback_data='set_auto1'
    )
    button_auto2 = InlineKeyboardButton(
        text= 'Авто 2',
        callback_data='set_auto2'
    )
    button_fullname = InlineKeyboardButton(
        text= 'Фамилия Имя Отчество',
        callback_data='set_fullname'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_phone], [button_auto1, button_auto2], [button_fullname]]
    )
    return keyboard

def kb_phone() -> ReplyKeyboardMarkup:
    logging.info(f'def kb_phone() -> ReplyKeyboardMarkup:')
    button_1 = KeyboardButton(text='Поделиться', request_contact=True)
    keybord = ReplyKeyboardMarkup(
        keyboard=[[button_1] ], resize_keyboard=True
    )
    return keybord

def kb_inline_yes_no(line_name: str) -> InlineKeyboardMarkup:
    logging.info(f'def kb_inline_yes_no() -> InlineKeyboardMarkup:')
    button_yes = InlineKeyboardButton(
        text= 'Да',
        callback_data=f"yes_{line_name}"
    )
    button_no = InlineKeyboardButton(
        text= 'Нет',
        callback_data=f"no_{line_name}"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_yes, button_no]]
    )
    return keyboard


def kb_inline_search() -> InlineKeyboardMarkup:
    logging.info(f'def kb_inline_search() -> InlineKeyboardMarkup:')
    button_flat = InlineKeyboardButton(
        text= '№ квартиры',
        callback_data=f"search_flat"
    )
    button_auto = InlineKeyboardButton(
        text= '№ авто',
        callback_data=f"search_auto"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_flat, button_auto]]
    )
    return keyboard
