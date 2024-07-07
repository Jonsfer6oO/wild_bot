from aiogram.types import Message
from utils import check_people

from config import conf
from utils import list_str_people

def walid_people(message:Message):
    return message.from_user.id in check_people() and list_str_people(message.from_user.id)[3] == 1
