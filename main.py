import asyncio
import logging

from aiogram import Bot,Dispatcher
from config import conf
from hendlers import ad_r, pe_r

async def main():

    bot = Bot(conf.tg_conf.bot_token)
    dp = Dispatcher()

    dp.workflow_data.update({"bot":bot})

    #регистрация роутеров
    dp.include_router(pe_r)
    dp.include_router(ad_r)

    await bot.delete_webhook(drop_pending_updates=True) #пропуск апдейтов
    await dp.start_polling(bot) #старт бота

asyncio.run(main())