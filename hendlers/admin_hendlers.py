from aiogram import Router, F
from aiogram.types import Message
from time import sleep
from  aiogram.types.poll_answer import PollAnswer

from filter import Walid_admin, walid_quer
from config import conf
from lexicon import text




#инициализация роутера
ad_r = Router()

ad_r.message.filter(Walid_admin(conf), )

list_poll = []
status_admin = False

#вход в панель администратора
@ad_r.message(F.text.lower() == 'admin')
async def walid_adm(message:Message):
    global status_admin
    await message.answer(text = text['ADMIN_REG'])
    status_admin = True

#перессылка опроса
@ad_r.message(walid_quer)
async def return_poll(message:Message, bot):
    global list_poll, status_admin
    print(message.model_dump_json(indent=4))

    if message.poll and status_admin:

        # Информирование об отправке опроса
        await message.reply(text=text["SEND_POLL"])

        # поступление нового опроса
        await bot.send_message(chat_id=conf.tg_conf.chat_id,
                               text=text["NEW_POLL"])

        # создание опроса
        mess = await bot.send_poll(
                            chat_id=conf.tg_conf.chat_id,
                            question=message.poll.question,
                            options=[i.text for i in message.poll.options],
                            is_anonymous=False
        )

        sleep(5)
        await bot.send_message(chat_id=conf.tg_conf.chat_id,
                               text=text["TEN_MIN"])
        sleep(5)
        await bot.send_message(chat_id=conf.tg_conf.chat_id,
                               text=text["TWEN_MIN"])
        sleep(5)
        await bot.send_message(chat_id=conf.tg_conf.chat_id,
                               text=text["EXIT_POLL"])

        # остановка опроса
        await bot.stop_poll(chat_id=conf.tg_conf.chat_id,
                              message_id=mess.message_id)

        # проверка на участие людей в опросе
        if list_poll:

            # отправка сообщения с пользователями
            list_user_str = ' '.join(list_poll)
            await bot.send_message(chat_id=conf.tg_conf.chat_id,
                                text=text["ANSWER_POLL"].format(list_user_str))

            # статистика
            await message.answer(text=text['STATE'].format("@" + str(message.chat.username),
                                                        len(list_poll),
                                                        300//len(list_poll),
                                                        300))
        else:
            # опроса не состоялся
            await bot.send_message(chat_id=conf.tg_conf.chat_id,
                                text=text["NO_POLL"])

            await message.answer(text=text["NO_POLL"])

        list_poll = []

    else:
        # отправка без админки
        await message.answer(text=text['NOT_WALID'])

# Составления списка пользователей участвоваших в опросе
@ad_r.poll_answer()
async def func(poll:PollAnswer):
    print(poll)
    if poll.user.username not in list_poll:
        list_poll.append("@" + str(poll.user.username))


#неизвестные команды
@ad_r.message()
async def not_walid(message:Message):
    await message.answer(text=text['NOT_WALID'])
