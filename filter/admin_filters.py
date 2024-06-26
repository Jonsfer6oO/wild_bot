from aiogram.filters import BaseFilter
from aiogram.types import Message




class Walid_admin(BaseFilter):

    def __init__(self, conf):
        self.id_adm = conf.tg_conf.admin_id
        self.id_chat = conf.tg_conf.chat_id

    async def __call__ (self, message:Message):
        return message.from_user.id == int(self.id_adm) and message.chat.id != int(self.id_chat)


def walid_quer(message:Message):
    return message.poll
