from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram import F, Router

from config import conf
from lexicon import text
from utils import new_people, check_people, list_str_sql, update_exit, update_in_voice, new_people_voice, check_people_voice

st_r = Router()

# команда старт
@st_r.message(Command(commands="start"))
async def start_men(message:Message):
    await message.answer(text=text["START_PANEL"].format(list_str_sql(conf.tg_conf.admin_id)[1]),
                         parse_mode=ParseMode.HTML)

# регистрация заказчика
@st_r.message(Command(commands='poll'))
async def register_people(message:Message):

    if message.from_user.username == "none":
        await message.answer(text=text['NOT_USERNAME'].format(list_str_sql(conf.tg_conf.admin_id)[1]))
    else:
        if int(message.from_user.id) in check_people():
            await message.answer(text=text["IN_BASE"])
        else:
            new_people(message.from_user.id, "@" + str(message.from_user.username),0,1,0)
            await message.answer(text=text['POLL_PANEL'])

#регистрация голосующих
@st_r.message(Command(commands='voting'))
async def voting_people(message:Message):

    if message.from_user.username == "none":
        await message.answer(text=text['NOT_USERNAME'].format(list_str_sql(conf.tg_conf.admin_id)[1]))
    else:
        if int(message.from_user.id) in check_people_voice():
            await message.answer(text=text["IN_BASE_VOTING"])
        else:
            new_people_voice(message.from_user.id, "@" + str(message.from_user.username),0,1,0)
            await message.answer(text=text['POLL_PANEL_VOTING'])

#вход в панель заказчика
@st_r.message(Command(commands='main'))
async def main_people(message:Message):
    update_exit(message.from_user.id,
                1)
    await message.answer(text=text["MAIN_ON"])

#вход в панель голосующего
@st_r.message(Command(commands='voice'))
async def voice_people(message:Message):
    update_in_voice(message.from_user.id, 1)
    await message.answer(text=text['VOICE_ON'])

# неизвестные команды
@st_r.message()
async def not_msg(message:Message):
    await message.answer(text=text["NOT_WALID"])
