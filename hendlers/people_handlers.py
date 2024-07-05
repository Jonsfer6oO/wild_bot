from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from config import conf
from filter import walid_people, walid_time_poll
from lexicon import text
from utils import check_people, list_str_sql, list_str_people, update_time

# инициализация роутера
pe_r = Router()

# подключение фильтров
pe_r.message.filter(walid_people)


# старт
@pe_r.message(Command(commands="start"))
async def start_from_people(message:Message):
    await message.answer(text=text["START"].format(list_str_sql(conf.tg_conf.admin_id)[1]),
                         parse_mode=ParseMode.HTML)

# help
@pe_r.message(Command(commands="help"))
async def help_from_people(message:Message):
    await message.answer(text=text["HELP"].format(list_str_sql(conf.tg_conf.admin_id)[1]),
                         parse_mode=ParseMode.HTML)

# правила создания опроса
@pe_r.message(Command(commands="manual"))
async def manual_people(message:Message):
    await message.answer(text=text["MANUAL"])

# цена за подписку
@pe_r.message(Command(commands='price'))
async def price_people(message:Message):
    await message.answer(text=text["PRICE"].format(list_str_sql(conf.tg_conf.admin_id)[2]),
                         parse_mode=ParseMode.HTML)

# баланс пользователя
@pe_r.message(Command(commands="balance"))
async def balance_people(message:Message):
    await message.answer(text=text["BALANCE_PEOPLE"].format(list_str_people(message.from_user.id)[2]))

# конфигурации опроса
@pe_r.message(Command(commands='configuration'))
async def configuration_people(message:Message):
    data = list_str_sql(message.from_user.id)
    await message.answer(text=text["CONFIGURATION"].format(list_str_people(message.from_user.id)[2], data[5],data[2]),
                         parse_mode=ParseMode.HTML)

# изменение времени на голосование
@pe_r.message(walid_time_poll)
async def time_people(message:Message):
    time = int(message.text[1])
    await message.answer(tetx=text["TIME_PEOPLE"].format((message.from_user.id, time)))

# неизвестные команды
@pe_r.message()
async def no_command(message:Message):
    await message.answer(text=text["NOT_WALID"])
