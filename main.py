import asyncio
import logging

import psycopg_pool
from aiogram import Bot, Dispatcher

from core.middlewares.db_middleware import DbSession
from core.settings import settings


# Для psycopg.pool, чтобы не было ошибок
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def start_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bots.admin_id, text='Started')

async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bots.admin_id, text='Stopped')

psycopg_pool
async def create_pool(user, password, database, host):
    return psycopg_pool.AsyncConnectionPool(f"host={host} port=5432 dbname={database} user={user} password={password} connect_timeout=10")

async def run_bot():
    logging.basicConfig(
        level=logging.INFO
    )
    bot = Bot(settings.bots.bot_token, parse_mode= "HTML")
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    pooling = await create_pool(settings.db.user, settings.db.host, settings.db.password, settings.db.db)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

    # Middleware
    dp.message.middleware(DbSession(pooling))


if __name__ == '__main__':
    try:
        asyncio.run(run_bot())
    except(KeyboardInterrupt, SystemExit):
        print('Error')