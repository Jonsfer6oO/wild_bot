from aiogram.types import Message
from utils import check_people

from config import conf

def walid_people(message:Message):
    return message.from_user.id in check_people()
