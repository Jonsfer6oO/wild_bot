from aiogram.filters import BaseFilter
from aiogram.types import Message



# валидация админа
class Walid_admin(BaseFilter):

    def __init__(self, conf):
        self.id_adm = conf.tg_conf.admin_id
        self.id_chat = conf.tg_conf.chat_id

    async def __call__ (self, message:Message):
        return message.from_user.id == int(self.id_adm) and message.chat.id != int(self.id_chat)


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

# проверка что в опросе участвовали
class Walid_press_poll(BaseFilter):
    def __init__(self,list_poll):
        self.list_poll = list_poll

    async def __call__(self, message:Message):
        return len(self.list_poll) > 0

class Walid_press_poll_not(BaseFilter):
    def __init__(self,list_poll):
        self.list_poll = list_poll

    async def __call__(self, message:Message):
        return len(self.list_poll) == 0