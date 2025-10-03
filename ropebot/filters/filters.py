from aiogram.filters import BaseFilter
from aiogram.types import Message, TelegramObject, CallbackQuery


class IsGod(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message, god_dict: dict):
        print(f'Проверка {IsGod.__name__} - {message.from_user.id in god_dict.values()}')
        return message.from_user.id in god_dict.values()


class IsGodCallback(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery, god_dict: dict):
        print(f'Проверка {IsGodCallback.__name__} - {callback.from_user.id in god_dict.values()}')
        return callback.from_user.id in god_dict.values()


class IsAdmin(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message, admin_dict: dict):
        print(f'Проверка {IsAdmin.__name__} - {message.from_user.id in admin_dict.values()}')

        return False


class IsAdminCallback(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery, admin_dict: dict):
        print(f'Проверка {IsAdminCallback.__name__} - {callback.from_user.id in admin_dict.values()}')

        return callback.from_user.id in admin_dict.values()


class IsPlayer(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message, players_dict: dict):
        print(f'Проверка {IsPlayer.__name__} - {str(message.from_user.id) in players_dict.keys()}')
        return str(message.from_user.id) in players_dict.keys()





class IdExamination(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery ,admin_dict):
        try:
            return int(callback.data) in admin_dict.values()
        except:
            return False