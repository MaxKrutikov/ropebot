from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from ropebot.lexicon.lexicon import god_lexicon
from ropebot.handlers.god_handlers.god_callback import router
from ropebot.keyboards.keyboards import keyboard_with_set_and_get
from ropebot.filters.filters import IsGod
from ropebot.FSM.fsm import GodFSM
from ropebot.database.database import get_data

god_router = Router()
god_router.include_router(router)
god_router.message.filter(IsGod())

@god_router.message(Command(commands=['start']), ~StateFilter(GodFSM.in_set, GodFSM.god))
async def send_me_start_or_help(message: Message, state : FSMContext):
    await message.answer(
        text=god_lexicon[message.text],
        reply_markup=keyboard_with_set_and_get() if message.text == '/help' else None
    )
    await state.set_state(GodFSM.god)

@god_router.message(Command(commands='start'), StateFilter(GodFSM.god))
async def send_me_godstart(message: Message):
    await message.answer(
        text=god_lexicon['god_start']
    )


#тут не god_dict, а admin_dict
@god_router.message(Command(commands='set'), StateFilter(GodFSM.god))
async def set_all(message: Message, state: FSMContext, admin_dict: dict):
    buttons = [[button] for button in [InlineKeyboardButton(text=username, callback_data=str(id)) for username, id in admin_dict.items()]]
    buttons.append([InlineKeyboardButton(text='Выйти', callback_data='exit')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await state.update_data(second_list=[])
    await message.answer(
        text=god_lexicon[message.text],
        reply_markup=keyboard
    )
    await state.set_state(GodFSM.in_set)

@god_router.message(Command(commands=['start', 'help', 'set', 'get']), StateFilter(GodFSM.in_set))
async def send_me_start_or_help(message: Message):
    await message.reply(
        text=god_lexicon['/start_or_help_in_set']
    )


@god_router.message(Command(commands=['help', 'set', 'get']), ~StateFilter(GodFSM.god, GodFSM.in_set))
async def send_me_start_or_help(message: Message):
    await message.reply(
        text=god_lexicon['command_without_start']
    )

@god_router.message(Command(commands='help'), StateFilter(GodFSM.god))
async def send_me_god_helo(message: Message):
    await message.answer(
        text=god_lexicon[message.text],
        reply_markup=keyboard_with_set_and_get()
    )

@god_router.message(Command(commands='get'), StateFilter(GodFSM.god))
async def get_a_data(message: Message):
    data = get_data()


    text = ''
    for info in data:
        text += f'{info[0]} - {info[1]} - {[info[2], god_lexicon["null"]][info[2] == 0]}\n'

    await message.answer(
        text=[text, god_lexicon['no_text']][not text],
        reply_markup=keyboard_with_set_and_get()
    )

@god_router.message(lambda x: x.text == 'Не зарегистрирован')
async def set_me_not_authorized(message: Message, state: FSMContext):
    await message.answer(
        text='Вернул назад на незарегистрированого'
    )
    await state.clear()

@god_router.message(~StateFilter(GodFSM.god, GodFSM.in_set))
async def send_me_echo_without_start(message: Message):
    await message.reply(
        text=god_lexicon['command_without_start']
    )

@god_router.message(StateFilter(GodFSM.god))
async def send_me_echo(message: Message):
    await message.reply(
        text=god_lexicon['echo']
    )

@god_router.message(StateFilter(GodFSM.in_set))
async def send_me_start_or_help(message: Message):
    await message.reply(
        text=god_lexicon['echo_in_set']
    )

