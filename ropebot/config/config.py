import os
import json
from environs import Env
from dataclasses import dataclass



@dataclass
class LogSettings:
    log_level: int
    log_format: str

@dataclass
class TelegramBot:
    bot_token: str
    players_dict: dict
    admin_dict: dict
    god_dict: dict

@dataclass
class Config:
    log_settings: LogSettings
    telegrambot: TelegramBot

def load_config():
    env = Env()
    env.read_env()

    players_dict = json.loads(os.getenv('players_dict'))
    admin_dict = json.loads(os.getenv('admin_dict'))
    god_dict = json.loads(os.getenv('god_dict'))

    return Config(
        log_settings=LogSettings(
            log_level=os.getenv('log_level'),
            log_format=os.getenv('log_format')
        ),
        telegrambot=TelegramBot(
            bot_token=os.getenv('bot_token'),
            players_dict=players_dict,
            admin_dict=admin_dict,
            god_dict=god_dict
        )
    )



