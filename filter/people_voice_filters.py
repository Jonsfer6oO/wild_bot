from aiogram.types import Message
from utils import check_people_voice

from config import conf
from utils import list_str_people

def walid_people_voice(message:Message):
    return message.from_user.id in check_people_voice() and list_str_people(message.from_user.id)[4] == 1
