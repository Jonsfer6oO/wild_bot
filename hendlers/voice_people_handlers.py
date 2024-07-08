from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from config import conf
from utils import  list_str_people_voice, update_in_voice, update_money_voice
from filter import walid_people_voice
from lexicon import text

vs_r = Router(walid_people_voice)

# команда старт
@vs_r.message(Command(commands='start'))
async def voise_start(message:Message):
    await message.answer(text=text["VOICE_START"].format(conf.tg_conf.admin_id))

# выплата зарплаты
@vs_r.message(Command(commands='salary'))
async def salary_voice(message:Message):
    await message.answer(text=text["SALARY_VOICE"])

# проверка баланса
@vs_r.message(Command(commands='balance'))
async def balance_voice(message:Message):
    await message.answer(text=text["BALANCE_VOICE"].format(list_str_people_voice(message.from_user.id)[2]))

# выход из панели голосующего
@vs_r.message(Command(commands="exit"))
async def exit_voice(message:Message):
    update_in_voice(message.from_user.id, 0)
    await message.answer(text=text['EXIT_VOICE'])

# неизвестные команды
@vs_r.message()
async def not_msg(message:Message):
    await message.answer(text=text['NOT_WALID'])