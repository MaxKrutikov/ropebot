from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, StateFilter

from ropebot.lexicon.lexicon import player_lexicon
from ropebot.FSM.fsm import PlayerFSM
from ropebot.filters.filters import IsPlayer
player_router = Router()
player_router.message.filter(IsPlayer())

#
@player_router.message(CommandStart(), ~StateFilter(PlayerFSM.in_station, PlayerFSM.with_task, PlayerFSM.player))
async def send_me_default_start(message: Message, state: FSMContext):
    await message.answer(
        text=player_lexicon['default_start']
    )
    await state.set_state(PlayerFSM.player)
    await state.update_data(answer=False)

@player_router.message(CommandStart(), StateFilter(PlayerFSM.in_station, PlayerFSM.with_task, PlayerFSM.player))
async def send_me_not_default_start(message: Message):
    await message.answer(
        text=player_lexicon['not_default_start']
    )
#
#
@player_router.message(Command(commands='help'), ~StateFilter(PlayerFSM.in_station, PlayerFSM.with_task, PlayerFSM.player))
async def send_me_default_help(message: Message):
    await message.answer(
        text=player_lexicon['default_help']
    )

@player_router.message(Command(commands='help'), StateFilter(PlayerFSM.player) )
async def send_me_player_help(message: Message):
    buttons = [[KeyboardButton(text='/give_a_task')], [KeyboardButton(text='give_the_key')]]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, one_time_keyboard=True, resize_keyboard=True)

    await message.answer(
        text=player_lexicon['player_help'],
        reply_markup=keyboard
    )

@player_router.message(Command(commands='help'), StateFilter(PlayerFSM.in_station, PlayerFSM.with_task))
async def send_me_help_in_another_states(message: Message):
    await message.answer(
        text=player_lexicon['get_no_help']
    )
#
#
@player_router.message(Command(commands='give_a_task'), StateFilter(PlayerFSM.player))
async def give_a_task(message: Message):


#Вспомогательная функция
@player_router.message(lambda x: x.text == 'Не зарегистрирован')
async def set_default_state(message: Message, state: FSMContext):
    await message.answer(
        text='Все четко, теперь ты не зарегистрирован'
    )
    await state.clear()