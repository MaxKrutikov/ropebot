import logging

from aiogram import Router
from aiogram.types import (Message,
                           ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           )
from aiogram.filters import CommandStart, StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext
from ropebot.FSM.fsm import AdminFSM

from ropebot.lexicon.lexicon import admin_lexicon
from ropebot.handlers.admin_handlers.admin_callback import router
from ropebot.database.database import get_data
from ropebot.keyboards.keyboards import keyboard_with_set_and_get, keyboard_with_help, keyboard_with_groups
from ropebot.filters.filters import IsAdmin
from ropebot.keyboards.keyboards import keyboard_with_station

logger = logging.getLogger(__name__)


admin_router = Router()
admin_router.message.filter(IsAdmin())
admin_router.include_router(router)

@admin_router.message(CommandStart(), ~StateFilter(AdminFSM.admin, AdminFSM.in_set))
async def not_authorized_start(message: Message, state: FSMContext):

    await message.answer(
        text=admin_lexicon['not_authorized_start'],
        reply_markup=keyboard_with_station()
    )
@admin_router.message(CommandStart(), StateFilter(AdminFSM.admin))
async def authorized_start(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/help')]], resize_keyboard=True, one_time_keyboard=True)

    await message.answer(
        text=admin_lexicon['authorized_start'],
        reply_markup=keyboard
    )

@admin_router.message(Command(commands=['start', 'get', 'set', 'help']), StateFilter(AdminFSM.in_set))
async def in_set_start(message: Message):
    await message.answer(
        text=admin_lexicon["/start_or_help_in_set"],
    )

@admin_router.message(Command(commands='get'), StateFilter(AdminFSM.admin))
async def get_a_data(message: Message):
    data = get_data()


    text = ''
    for info in data:
        text += f'{"@" + info[0]} - {info[1]} - {[info[2], admin_lexicon["null"]][info[2] == 0]}\n'

    await message.answer(
        text=[text, admin_lexicon['no_text']][not text],
        reply_markup=keyboard_with_set_and_get()
    )

@admin_router.message(Command(commands=['get', 'set', 'help']), ~StateFilter(AdminFSM.admin, AdminFSM.in_set))
async def not_authorized_get_and_set(message: Message):
    await message.reply(
        text=admin_lexicon['not_authorized_get_and_set']
    )

@admin_router.message(Command(commands='set'), StateFilter(AdminFSM.admin))
async def set_station(message: Message, state: FSMContext):
    await message.answer(
        text=admin_lexicon['choice'],
        reply_markup=keyboard_with_groups()
    )

    await state.set_state(AdminFSM.in_set)
@admin_router.message(Command(commands='help'), StateFilter(AdminFSM.admin))
async def set_staton(message: Message):

    await message.answer(
        text=admin_lexicon['help'],
        reply_markup=keyboard_with_set_and_get()
    )


#Обработчики ниже являются вспомогательными и не должны быть в проде
@admin_router.message(lambda x: x.text == 'Не зарегистрирован')
async def set_me_not_authorized(message: Message, state: FSMContext):
    await message.answer(
        text='Вернул назад на незарегистрированого'
    )
    await state.clear()

@admin_router.message(~StateFilter(AdminFSM.in_set, AdminFSM.admin))
async def send_echo(message: Message):
    await message.answer(
        text=admin_lexicon['not_authorized_echo'],
    )


@admin_router.message(StateFilter(AdminFSM.in_set))
async def send_echo(message: Message):
    await message.answer(
        text=admin_lexicon['/start_or_help_in_set'],
    )

@admin_router.message(StateFilter(AdminFSM.admin))
async def send_echo(message: Message):
    await message.answer(
        text=admin_lexicon['echo'],
        reply_markup=keyboard_with_help()
    )

