import asyncio
import logging
from loader import bot, db
from functional import pytest_results_parser


async def check_tests(period):
    while True:

        # wait T seconds till next failure check happens (among all users)
        await asyncio.sleep(period)

        # get list of active watchers
        users = db.get_users()

        for user in users:

            ok_status, comments = pytest_results_parser.pytest_results(user.user_path)

            # Scheduled notifications
            if user.checks_since_last * period >= user.notifications_period:

                logging.info(msg=f'User {user.user_id}, comments: \n {comments} \n\n')
                await bot.send_message(chat_id=user.user_id, text=comments, parse_mode='Markdown')

                # if message is sent, then we start counting number of checks again
                db.update_user(user_id=user.user_id, checks_since_last=1)
            else:
                # if time has not passed, then we increase number of checks
                db.update_user(user_id=user.user_id, checks_since_last=user.checks_since_last + 1)

            if user.detect_failures:

                # Failure notifications
                if user.failures_since_last * period >= user.failures_period and ok_status == 0:
                    await bot.send_message(chat_id=user.user_id, text=comments, parse_mode='Markdown')
                    # if message is sent, then we start counting failures again
                    db.update_user(user_id=user.user_id, failures_since_last=1)

                elif ok_status == 0:
                    # if current check is with failures, then we increase its quantity
                    db.update_user(user_id=user.user_id, failures_since_last=user.failures_since_last + 1)
                else:
                    # if current is without failures, then we start counting them again
                    db.update_user(user_id=user.user_id, failures_since_last=1)
