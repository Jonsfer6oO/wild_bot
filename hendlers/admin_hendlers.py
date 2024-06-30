from aiogram import Router, F
from aiogram.types import Message
from time import sleep
from aiogram.types.poll_answer import PollAnswer
from aiogram.filters import Command
from aiogram.enums import ParseMode


from filter import Walid_admin, walid_quer, walid_percent, walid_time_poll
from config import conf
from lexicon import text
import datetime


#инициализация роутера
ad_r = Router()

ad_r.message.filter(Walid_admin(conf))

list_poll = [] # список ответивших в голосовании
status_admin = False # статус дминской панели
percent = 20 # процент от стоимости на оплату голосований
numder_poll = 0 # номер опроса
price = 500 # цена на подписку
status_servis = True # статус сервиса
time_p = 30 # время на голосование

#вход в панель администратора
@ad_r.message(F.text.lower() == 'admin')
async def walid_adm(message:Message):
    global status_admin
    if status_admin == False:
        await message.answer(text = text['ADMIN_REG'])
        status_admin = True
    else:
        await message.answer(text=text["YOU_ADMIN"])

@ad_r.message(Command(commands="help"))
async def help_func(message:Message):
    if status_admin:
        await message.answer(text=text['HELP'], parse_mode=ParseMode.HTML)
    else:
        await message.answer(text=text['NO_ADMIN_HELP'])

#перессылка опроса
@ad_r.message(walid_quer)
async def return_poll(message:Message, bot):
    global list_poll, status_admin, numder_poll, time_p
    print(message.model_dump_json(indent=4))

    if message.poll and status_admin:

        # Информирование об отправке опроса
        await message.reply(text=text["SEND_POLL"].format(time_p))

        numder_poll += 1
        # поступление нового опроса
        await bot.send_message(chat_id=conf.tg_conf.chat_id,
                               text=text["NEW_POLL"].format(numder_poll, time_p))

        # создание опроса
        mess = await bot.send_poll(
                            chat_id=conf.tg_conf.chat_id,
                            question=message.poll.question,
                            options=[i.text for i in message.poll.options],
                            is_anonymous=False
        )

        t = time_p
        while t != 0:
            if t >= 10:
                t -= 10
                sleep(600)
                mess_1 = await bot.send_message(chat_id=conf.tg_conf.chat_id,
                                                text=text["TIME_MIN"].format(t))
                await bot.delete_message(chat_id=conf.tg_conf.chat_id,
                                        message_id=mess_1.message_id)
            else:
                sleep(t*60)
                mess_1 = await bot.send_message(chat_id=conf.tg_conf.chat_id,
                                                 text=text["TIME_MIN"].format(t))
                await bot.delete_message(chat_id=conf.tg_conf.chat_id,
                                        message_id=mess_1.message_id)
                t = 0
        # sleep(30)
        # mess_1 = await bot.send_message(chat_id=conf.tg_conf.chat_id,
        #                        text=text["TEN_MIN"])
        # sleep(30)
        # await bot.delete_message(chat_id=conf.tg_conf.chat_id,
        #               message_id=mess_1.message_id)
        # mess_2 = await bot.send_message(chat_id=conf.tg_conf.chat_id,
        #                        text=text["TWEN_MIN"])
        # sleep(30)
        # await bot.delete_message(chat_id=conf.tg_conf.chat_id,
        #               message_id=mess_2.message_id)
        # await bot.send_message(chat_id=conf.tg_conf.chat_id,
        #                        text=text["EXIT_POLL"])

        # остановка опроса
        await bot.stop_poll(chat_id=conf.tg_conf.chat_id,
                              message_id=mess.message_id)

        sleep(3)
        # проверка на участие людей в опросе
        if list_poll:

            # отправка сообщения с пользователями
            list_user_str = ' '.join(list_poll)
            await bot.send_message(chat_id=conf.tg_conf.chat_id,
                                text=text["ANSWER_POLL"].format(list_user_str))

            # отправка опроса
            await bot.forward_message(chat_id = conf.tg_conf.chat_id,
                                      message_id = mess.message_id)

            # статистика
            await message.answer(text=text['STATE_ADMIN'].format("@" + str(message.chat.username),
                                                        "#" + f"{numder_poll}" + "X",
                                                        str(percent) + "%",
                                                        len(list_poll),
                                                        300//len(list_poll),
                                                        300,
                                                        datetime.datetime.now()))
        else:
            # опрос не состоялся
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

# изменение процента
@ad_r.message(walid_percent)
async def upd_percent(message:Message):
    global percent
    per = int(message.text.split()[1])
    if per <= 40:
        percent = per
        await message.answer(text = text["NEW_PERCENT"].format(percent))
    else:
        await message.answer(text=text["ERR_PERCENT"])

# выход из панели админестратора
@ad_r.message(F.text.lower() == "exit")
async def exit_admin(message:Message):
    global status_admin

    await message.answer(text=text['ADMIN_EXIT'])
    status_admin = False

# конфигурационные данные
@ad_r.message(F.text.lower() == "configuration")
async def con(message:Message):
    await message.answer(text=text['CONFIG'].format(price,
                                                    percent,
                                                    status_servis,
                                                    numder_poll))
# смена времени на голосование
@ad_r.message(walid_time_poll)
async def time_poll(message:Message):
    global time_p
    time_p = int(message.text.split()[1])
    await message.answer(text=text["TIME_POLL"].format(time_p))

#неизвестные команды
@ad_r.message()
async def not_walid(message:Message):
    await message.answer(text=text['NOT_WALID'])
