from aiogram import Router, F
from aiogram.types import Message
from time import sleep

from filter import Walid_admin, walid_quer
from config import conf
from lexicon import text



#инициализация роутера
ad_r = Router()

ad_r.message.filter(Walid_admin(conf))



#вход в панель администратора
@ad_r.message(F.text.lower() == 'admin')
async def walid_adm(message:Message):
    await message.answer(text = text['ADMIN_REG'])

#перессылка опроса
@ad_r.message(walid_quer)
async def return_poll(message:Message, bot):

    if message.poll:
        await bot.send_message(chat_id=conf.tg_conf.chat_id,
                               text=text["NEW_POLL"])
        mess = await bot.send_poll(
                            chat_id=conf.tg_conf.chat_id,
                            question=message.poll.question,
                            options=[i.text for i in message.poll.options],
                            is_anonymous=False
        )

        sleep(600)
        await bot.send_message(chat_id=conf.tg_conf.chat_id,
                               text=text["TEN_MIN"])
        sleep(600)
        await bot.send_message(chat_id=conf.tg_conf.chat_id,
                               text=text["TWEN_MIN"])
        sleep(600)
        await bot.send_message(chat_id=conf.tg_conf.chat_id,
                               text=text["EXIT_POLL"])


        await bot.stop_poll(chat_id=conf.tg_conf.chat_id,
                              message_id=mess.message_id)



#неизвестные команды
@ad_r.message()
async def not_walid(message:Message):
    await message.answer(text=text['NOT_WALID'])
