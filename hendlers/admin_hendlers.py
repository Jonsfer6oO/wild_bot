from aiogram import Router, F
from aiogram.types import Message
from time import sleep
from aiogram.types.poll_answer import PollAnswer
from aiogram.filters import Command
from aiogram.enums import ParseMode


from filter import Walid_admin, walid_quer, walid_percent, walid_time_poll, walid_price,walid_add_admin, walid_del_admin, service_on, service_off
from utils import sql_admin, list_str_sql, update_data, del_admin_sql, list_admin_sql, update_status
from utils import sql_status, upgrate_poll, list_str_poll
from config import conf
from lexicon import text
import datetime
import asyncio

#подключение к базе данных и создание курсора

#инициализация роутера
ad_r = Router()

ad_r.message.filter(Walid_admin)

list_poll = [] # список ответивших в голосовании
time_p = 30 # время на голосование

status_admin = 0 # статус дминской панели
percent = 20 # процент от стоимости на оплату голосований
numder_poll = 0 # номер опроса
price = 500 # цена на подписку
status_servis = True # статус сервиса



#вход в панель администратора
@ad_r.message(F.text.lower() == 'admin')
async def walid_adm(message:Message):
    status_admin = list_str_sql(message.from_user.id)[-1]

    if int(status_admin) == 0:
        await message.answer(text = text['ADMIN_REG'])
        update_data(message.from_user.id, status_admin=1)
    else:
        await message.answer(text=text["YOU_ADMIN"])

@ad_r.message(Command(commands="help"))
async def help_func(message:Message):
    status_admin = list_str_sql(message.from_user.id)[-1]
    if int(status_admin) == 1:
        await message.answer(text=text['HELP'].format(list_str_sql(conf.tg_conf.admin_id)[1]), parse_mode=ParseMode.HTML)
    else:
        await message.answer(text=text['NO_ADMIN_HELP'])

#перессылка опроса
@ad_r.message(walid_quer)
async def return_poll(message:Message, bot):

    global list_poll # status_admin, numder_poll, time_p

    print(message.model_dump_json(indent=4))

    status_poll = list_str_poll()[1]
    status_admin = list_str_sql(message.from_user.id)[-1]
    poll_id_base = list_str_poll()[0]

    if message.poll and int(status_admin) == 1 and status_poll == 0:

        # внесение данные опроса в базу данных
        sql_status(poll_id=poll_id_base+1, poll_status=1,  customer="@" + str(message.chat.username), id_customer=message.chat.id)

        # Информирование об отправке опроса
        await message.reply(text=text["SEND_POLL"].format(list_str_sql(message.from_user.id)[-2]))

        # поступление нового опроса
        await bot.send_message(chat_id=conf.tg_conf.chat_id,
                               text=text["NEW_POLL"].format(list_str_poll()[0]))

        # создание опроса
        mess = await bot.send_poll(
                            chat_id=conf.tg_conf.chat_id,
                            question=message.poll.question,
                            options=[i.text for i in message.poll.options],
                            is_anonymous=False
        )


        t = int(list_str_sql(message.from_user.id)[-2])
        while t != 0:
            if t > 10:
                mess_1 = await bot.send_message(chat_id=conf.tg_conf.chat_id,
                                                text=text["TIME_MIN"].format(t))
                await asyncio.sleep(600)
                await bot.delete_message(chat_id=conf.tg_conf.chat_id,
                                        message_id=mess_1.message_id)
                t -= 10
            else:
                mess_1 = await bot.send_message(chat_id=conf.tg_conf.chat_id,
                                                text=text["TIME_MIN"].format(t))
                await asyncio.sleep(t*60)
                await bot.delete_message(chat_id=conf.tg_conf.chat_id,
                                        message_id=mess_1.message_id)
                t = 0

        # остановка опроса
        await bot.stop_poll(chat_id=conf.tg_conf.chat_id,
                              message_id=mess.message_id)

        # смена статуса опроса в базе
        upgrate_poll(poll_id_base+1, 0)


        await bot.send_message(chat_id=conf.tg_conf.chat_id,
                               text=text["EXIT_POLL"])

        await asyncio.sleep(3)
        # проверка на участие людей в опросе
        if list_poll:

            # отправка сообщения с пользователями
            list_user_str = ' '.join(list_poll)
            await bot.send_message(chat_id=conf.tg_conf.chat_id,
                                text=text["ANSWER_POLL"].format(list_user_str))

            # отправка опроса
            await bot.forward_message(chat_id = list_str_sql(message.from_user.id)[0],
                                      message_id = mess.message_id,
                                      from_chat_id = mess.chat.id)

            # статистика
            await message.answer(text=text['STATE_ADMIN'].format("@" + str(message.chat.username),
                                                        "#" + f"{list_str_poll()[0]}" + "X",
                                                        str(list_str_sql(message.from_user.id)[3]) + "%",
                                                        len(list_poll),
                                                        list_str_sql(message.from_user.id)[2]//len(list_poll),
                                                        list_str_sql(message.from_user.id)[2],
                                                        datetime.datetime.now(),
                                                        list_str_sql(conf.tg_conf.admin_id)[1]))


        else:
            # опрос не состоялся
            await bot.send_message(chat_id=conf.tg_conf.chat_id,
                                text=text["NO_POLL"])

            await message.answer(text=text["NO_POLL"])


        list_poll = []

    elif message.poll and int(status_admin) == 1 and status_poll == 1:
        await message.answer(text=text['NOT_POLL_STOP'])


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

    status_admin = int(list_str_sql(message.from_user.id)[-1])
    per = int(message.text.split()[1])

    if status_admin == 1:

        if per <= 40:
            update_data(message.from_user.id, percent=per)
            await message.answer(text = text["NEW_PERCENT"].format(per))
        else:
            await message.answer(text=text["ERR_PERCENT"])

    else:
        await message.answer(text=text['NOT_WALID'])

# изменение цены
@ad_r.message(walid_price)
async def format_price(message:Message):

    status_admin = int(list_str_sql(message.from_user.id)[-1])

    if status_admin:

        pr = int(message.text.split()[1])
        update_data(message.from_user.id,price=pr)
        await message.answer(text=text["PRICE_FORMAT"].format(pr))

    else:
        await message.answer(text=text['NOT_WALID'])

# выход из панели администратора
@ad_r.message(F.text.lower() == "exit")
async def exit_admin(message:Message):

    status_adm = int(list_str_sql(message.from_user.id)[-1])

    if status_adm == 1:
        await message.answer(text=text['ADMIN_EXIT'])
        update_data(message.from_user.id, status_admin=0)
    else:
        await message.answer(text=text['NOT_WALID'])

# конфигурационные данные
@ad_r.message(F.text.lower() == "configuration")
async def con(message:Message):

    status_admin = int(list_str_sql(message.from_user.id)[-1])
    configur = list_str_sql(message.from_user.id)

    if status_admin:
        await message.answer(text=text['CONFIG'].format(configur[2],
                                                        configur[3],
                                                        configur[4],
                                                        list_str_poll()[0],
                                                        configur[5]))
    else:
        await message.answer(text=text['NOT_WALID'])

# добавление админов
@ad_r.message(walid_add_admin)
async def add_admin(message:Message):

    status_admin = int(list_str_sql(message.from_user.id)[-1])
    new_admin = message.text.split()

    if status_admin and int(message.from_user.id) == int(conf.tg_conf.admin_id) and int(new_admin[1]) not in list_admin_sql():

        sql_admin(int(new_admin[1]), new_admin[2], price, percent, "работает", time_p, 0)
        await message.answer(text=text["NEW_ADMIN"].format(new_admin[2]))

    elif status_admin == 1 and int(message.from_user.id) == int(conf.tg_conf.admin_id) and int(new_admin[1]) in list_admin_sql():
        await message.answer(text=text["YES_ADMIN_IN_LIST"])

    else:
        await message.answer(text=text['NOT_WALID'])

# удаление админов
@ad_r.message(walid_del_admin)
async def del_admin(message:Message):

    mes = message.text.split()
    status_admin = list_str_sql(message.from_user.id)[-1]

    if status_admin == 1 and int(message.from_user.id) == int(conf.tg_conf.admin_id) and int(mes[1]) in list_admin_sql():

        us = list_str_sql(int(mes[1]))
        await message.answer(text=text["DEL_ADMIN"].format(us[1]))
        del_admin_sql(int(mes[1]))

    elif status_admin == 1 and int(message.from_user.id) == int(conf.tg_conf.admin_id) and int(mes[1]) not in list_admin_sql():
        await message.answer(text=text["NO_ADMIN_IN_LIST"])
    else:

        await message.answer(text=text['NOT_WALID'])


# смена времени на голосование
@ad_r.message(walid_time_poll)
async def time_poll(message:Message):

    status_admin = int(list_str_sql(message.from_user.id)[-1])

    if status_admin:

        time_p = int(message.text.split()[1])
        update_data(message.from_user.id, time = time_p)
        await message.answer(text=text["TIME_POLL"].format(time_p))

    else:

        await message.answer(text=text['NOT_WALID'])

#отключение сервиса
@ad_r.message(service_off)
async def off(message:Message):
    status_admin = list_str_sql(conf.tg_conf.admin_id)[-1]
    status_service = list_str_sql(conf.tg_conf.admin_id)[4]
    if status_admin == 1 and int(message.from_user.id) == int(conf.tg_conf.admin_id) and status_service.lower() == "работает":
        await message.answer(text=text["SERVICE_OFF"])
        update_status(message.from_user.id, work_service='не работает')
    elif status_service == "не работает" and status_admin == 1 and int(message.from_user.id )== int(conf.tg_conf.admin_id):
        await message.answer(text=text['NOT_ON'])
    else:
        await message.answer(text=text['NOT_WALID'])


#включение сервиса
@ad_r.message(service_on)
async def off(message:Message):

    status_admin = list_str_sql(conf.tg_conf.admin_id)[-1]
    status_service = list_str_sql(conf.tg_conf.admin_id)[4]

    if status_admin == 1 and int(message.from_user.id) == int(conf.tg_conf.admin_id) and status_service.lower() == "не работает":
        await message.answer(text=text["SERVICE_ON"])
        update_status(message.from_user.id, work_service='работает')
    elif status_service == "работает" and status_admin == 1 and int(message.from_user.id )== int(conf.tg_conf.admin_id):
        await message.answer(text=text['NOT_OFF'])
    else:
        await message.answer(text=text['NOT_WALID'])

#неизвестные команды
@ad_r.message()
async def not_walid(message:Message):
    await message.answer(text=text['NOT_WALID'])
