from environs import Env
from dataclasses import dataclass

#данные бота
@dataclass
class TgBot:
    bot_token:str
    admin_id:int
    chat_id:int
    chat_main_id:int

#конфигурационные данные
@dataclass
class Config:
    tg_conf:TgBot


# добавление данных в окружение
env = Env()
env.read_env()

#обхект с конфигурационными данными
conf = Config(
    tg_conf=TgBot(
        env("BOT_TOKEN"),
        env("ADMIN_ID"),
        env("CHAT_ID"),
        env("CHAT_MAIN_ID")
        )
)
