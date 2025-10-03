import logging

from aiogram import Router
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest

from ropebot.database.database import set_data, get_data, set_group
from ropebot.lexicon.lexicon import stations
from ropebot.lexicon.lexicon import admin_lexicon, groups
from ropebot.FSM.fsm import AdminFSM
from ropebot.filters.filters import IsAdminCallback

logger = logging.getLogger(__name__)
router = Router()
router.callback_query.filter(IsAdminCallback())

#регистрация в бд инструктора по username, станции
@router.callback_query(lambda x: x.data in stations.values())
async def set_a_station(callback: CallbackQuery, state: FSMContext):
    for key in stations:
        if callback.data == stations[key]:
            text = key
    del stations[key]

    set_data(callback.from_user.username, text, 0)

    await callback.answer(
        text=admin_lexicon['set_a_station']
    )
    await state.set_state(AdminFSM.admin)


    try:
        await callback.message.edit_reply_markup()
        await callback.message.edit_text(text=admin_lexicon['edit_text'])
    except:
        pass

#установка группы на станцию инструктора
@router.callback_query(lambda x: x.data in groups.values(), StateFilter(AdminFSM.in_set))
async def set_a_group(callback: CallbackQuery, state: FSMContext):
    for key in groups.keys():
        if groups[key] == callback.data:
            try:
                group = int(key)
            except:
                group = 0



    await callback.answer()

    await state.set_state(AdminFSM.admin)
    try:
        set_group(group, callback.from_user.username)
    except:
        #logger.warning(...)
        pass

    try:
        await callback.message.edit_text(text=admin_lexicon['success'])
    except:
        #logger.warning(...)
        await callback.message.edit_text(text=admin_lexicon['no_success'])

    try:
        await callback.message.edit_reply_markup()
    except TelegramBadRequest:
        pass

