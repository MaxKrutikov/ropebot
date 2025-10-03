from aiogram.types import (
ReplyKeyboardMarkup,
KeyboardButton,
InlineKeyboardButton,
InlineKeyboardMarkup
)

from ropebot.lexicon.lexicon import stations, groups

def keyboard_with_set_and_get():
    buttons = [KeyboardButton(text=text) for text in ['/set', '/get']]
    keyboard = ReplyKeyboardMarkup(keyboard=[[buttons[0]], [buttons[1]]], resize_keyboard=True, one_time_keyboard=True)

    return keyboard

def keyboard_with_help():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/help')]], one_time_keyboard=True, resize_keyboard=True)


def keyboard_with_station():
    button = [InlineKeyboardButton(text=name, callback_data=callback) for name, callback in stations.items()]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[button])

    return keyboard

def keyboard_with_groups():
    group_button = [InlineKeyboardButton(text=number, callback_data=group) for number, group in groups.items() if group != 'no_group']
    no_group_button = [InlineKeyboardButton(text='Нет группы', callback_data='no_group')]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[group_button, no_group_button])

    return keyboard