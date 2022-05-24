from loader import bot
from data import constants
from database_config import init_database
import logging
import asyncio


async def main():
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(check_tests(constants.SLEEP_TIME))
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    from handlers import dp, check_tests
    init_database.create_database(constants.PATH_TO_DATABASE)

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Bot stopped!')
