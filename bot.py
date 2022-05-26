from loader import bot, db
from data import constants
from handlers import dp
from event_loop_tasks import check_tests
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
        db.close_session()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Bot stopped!')
