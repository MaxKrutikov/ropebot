from aiogram.fsm.state import State, StatesGroup

class AdminFSM(StatesGroup):
    admin = State()
    in_set = State()


#еще в разработке
class PlayerFSM(StatesGroup):
    player = State()
    with_task = State()
    in_station = State()
    # waiting_answer = State()

class GodFSM(StatesGroup):
    god = State()
    in_set = State()

