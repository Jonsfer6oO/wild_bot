from aiogram.filters import BaseFilter
from aiogram.types import Message

from utils import list_admin_sql, list_str_sql
from config import conf


# валидация админа
def Walid_admin(message:Message):

    id_adm = conf.tg_conf.admin_id
    id_chat = conf.tg_conf.chat_id
    list_adm = list_admin_sql()
    status_service = list_str_sql(conf.tg_conf.admin_id)[4]
    if message.photo:
        return False
    else:
        return (int(message.from_user.id) in list_adm and message.chat.id != int(id_chat) and status_service.lower() == "работает") or (int(message.from_user.id) == int(id_adm) and message.chat.id != int(id_chat))


# проверка на то что пришел опрос
def walid_quer(message:Message):
    return message.poll

# валидация сообщения со сменой процентов
def walid_percent(message:Message):
    msg = message.text.lower().split()
    return len(msg) == 2 and msg[0].isalpha() and msg[1].isdigit() and msg[0] == "percent"

# валидация смены времени на опрос
def walid_time_poll(message:Message):
    msg = message.text.lower().split()
    return len(msg) == 2 and msg[0].isalpha() and msg[1].isdigit() and msg[0] == "time"

# валидация на изменение цены
def walid_price(message:Message):
    msg = message.text.lower().split()
    return len(msg) == 2 and msg[0].isalpha() and msg[1].isdigit() and msg[0] == "price"

# валидация сообщения для добавления админа
def walid_add_admin(message:Message):
    msg = message.text.lower().split()
    return len(msg) == 3 and msg[0].isalpha() and msg[1].isdigit() and msg[0] == "admin" and msg[2][0] == "@"

# удаление админов
def walid_del_admin(message:Message):
    msg = message.text.lower().split()
    return len(msg) == 2 and msg[0].isalpha() and msg[1].isdigit() and msg[0] == "del"

# отключение сервиса
def service_off(message:Message):
    msg = message.text.lower().split()
    return len(msg) == 2 and msg[0].isalpha() and msg[1].isalpha() and msg[0] == "service" and msg[1] == "off"

# включение сервиса
def service_on(message:Message):
    msg = message.text.lower().split()
    return len(msg) == 2 and msg[0].isalpha() and msg[1].isalpha() and msg[0] == "service" and msg[1] == 'on'