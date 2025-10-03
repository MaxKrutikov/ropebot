from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from ropebot.filters.filters import IsGodCallback, IdExamination
from ropebot.FSM.fsm import GodFSM
from ropebot.lexicon.lexicon import god_lexicon, stations, groups
from ropebot.keyboards.keyboards import keyboard_with_station, keyboard_with_groups
from ropebot.database.database import set_data

router = Router()
router.callback_query.filter(IsGodCallback())

#регистрация username в бд, надо продумать, проверка айдишников хлипкая по идее
@router.callback_query(StateFilter(GodFSM.in_set), IdExamination())
async def set_a_username(callback: CallbackQuery, state: FSMContext, admin_dict: dict):


    data: dict = await state.get_data()
    for key in admin_dict.keys():
        if int(callback.data) == admin_dict[key]:
            data['second_list'].append(key)
    await state.set_data(data=data)

    button = [[b] for b in [InlineKeyboardButton(text=name, callback_data=callback) for name, callback in stations.items()]]
    button.append([InlineKeyboardButton(text='Выйти', callback_data='exit')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)

    try:
        await callback.message.edit_text(text=god_lexicon['set_station'])
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except:
        await callback.answer(
            text=god_lexicon['no_success'],
        )

#регистрация станции в бд
@router.callback_query(StateFilter(GodFSM.in_set), lambda x: x.data in stations.values())
async def set_a_station(callback: CallbackQuery, state: FSMContext):
    for key in stations.keys():
        if callback.data == stations[key]:
            station = key

    data: dict = await state.get_data()
    data['second_list'].append(station)

    await state.set_data(data=data)

    group_button = [[button] for button in [InlineKeyboardButton(text=number, callback_data=group) for number, group in groups.items() if group != 'no_group']]
    no_group_button = [InlineKeyboardButton(text='Нет группы', callback_data='no_group')]
    group_button.append(no_group_button)
    group_button.append([InlineKeyboardButton(text='Выйти', callback_data='exit')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=group_button)
    try:
        await callback.message.edit_text(text=god_lexicon['set_a_group'])
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except:
        await callback.answer(
            text=god_lexicon['no_success'],
        )

@router.callback_query(StateFilter(GodFSM.in_set), lambda x: x.data in groups.values())
async def set_a_group(callback: CallbackQuery, state: FSMContext):
    for key in groups.keys():
        if callback.data == groups[key]:
            group = key

    data: dict = await state.get_data()
    try:
        data['second_list'].append(int(group))
    except ValueError:
        data['second_list'].append(0)

    admin_name, station, ff_group = data['second_list']
    set_data(admin_name, station, ff_group)

    await callback.message.edit_text(text=god_lexicon['success_of_set'])
    try:
        await callback.message.edit_reply_markup()
    except:
        pass

    await state.set_state(GodFSM.god)

@router.callback_query(lambda x: x.data == 'exit')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GodFSM.god)

    await callback.message.edit_text(text=god_lexicon['cancel'])
    try:
        await callback.message.edit_reply_markup()
    except:
        pass

    await state.set_state(GodFSM.god)