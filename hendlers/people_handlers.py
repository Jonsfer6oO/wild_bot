from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from config import conf
from filter import walid_people, walid_time_poll, walid_quer
from lexicon import text
from utils import check_people, list_str_sql, list_str_people, update_time, update_money, update_attems, list_str_poll, update_exit

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
    await message.answer(text=text["CONFIGURATION"].format(list_str_people(message.from_user.id)[2],
                                                            list_str_people(message.from_user.id)[5],
                                                            data[2]),
                         parse_mode=ParseMode.HTML)

#выход из панели заказчика
@pe_r.message(Command(commands="exit"))
async def exit_people_panel(message:Message):
    update_exit(message.from_user.id, 0)
    await message.answer(text=text["EXIT_PEOPLE"])


# отправка опроса админу
@pe_r.message(walid_quer)
async def poll_people(message:Message, bot):

    # данные пользователя
    price_poll = list_str_sql(conf.tg_conf.admin_id)[2]
    time_people_poll = list_str_people(message.from_user.id)[5]
    money = list_str_people(message.from_user.id)[2]

    if time_people_poll - 30 == 0:
        # если не было увелечения по времени
        price_send = price_poll
        if money - price_send >= 0:

            update_money(message.from_user.id, money-price_send) # изменение количества денег
            update_attems(message.from_user.id, list_str_people(message.from_user.id)[4]+1) # изменение количства опросов
            mess = await message.answer(text=text['PRICE_PEOPLE_POLL'].format(list_str_people(message.from_user.id)[1],
                                                                     price_send,
                                                                     list_str_people(message.from_user.id)[5]
                                                                     ))

            # отправка параметров опросу админу
            await bot.forward_message(chat_id = conf.tg_conf.admin_id,
                                message_id = message.message_id,
                                from_chat_id = message.from_user.id)

            # отправка параметров опроса админу
            await bot.forward_message(chat_id = conf.tg_conf.admin_id,
                                message_id = mess.message_id,
                                from_chat_id = message.from_user.id)



        else:
            # недосточно денег
            await message.answer(text=text["NO_MONEY"])

    else:
        # если было увелечения по времени
        price_send = price_poll+((time_people_poll-30)//10)*50
        if money - price_send >= 0:
            update_money(message.from_user.id, money-price_send)
            await message.answer(text=text["PRICE_PEOPLE_POLL"].format(list_str_people(message.from_user.id)[1],
                                                                     price_send,
                                                                     list_str_people(message.from_user.id)[5]
                                                                     ))

            # отправка параметров опросу админу
            await bot.forward_message(chat_id = int(conf.tg_conf.admin_id),
                                message_id = message.message_id,
                                from_chat_id = message.from_user.id)

            # отправка параметров опросу админу
            await bot.forward_message(chat_id = conf.tg_conf.admin_id,
                                message_id = mess.message_id,
                                from_chat_id = message.from_user.id)

        else:
            # недосточно денег
            await message.answer(text=text["NO_MONEY"])

# пополнение баланса
@pe_r.message(Command(commands='replenish'))
async def replenish_people(message:Message):
    await message.answer(text=text['REPLENISH'].format(list_str_sql(conf.tg_conf.admin_id)[1]))

# изменение времени на голосование
@pe_r.message(walid_time_poll)
async def time_people(message:Message):
    time = int(message.text.lower().split()[1])
    if time > 30 and time <= 60 and time%10 == 0:
        update_time(message.from_user.id, time)
        await message.answer(text=text["TIME_PEOPLE"].format(time))
    else:
        await message.answer(text=text["ERR_TIME_PEOPLE"])

# неизвестные команды
@pe_r.message()
async def no_command(message:Message):
    await message.answer(text=text["NOT_WALID"])
