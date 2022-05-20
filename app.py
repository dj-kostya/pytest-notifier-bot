# Imports
import tempfile
from os import path
from pytest_handling import tests_passed, parse_results
from json_parser import parse

from config import TOKEN

from keyboards import set_up_path, testing_managing, rewritePath_editPeriods_testing_help
from states import PytestPath, Notification, Failure

import logging
import asyncio

from create_db import create_database
from sqlite import SQLiteDatabase

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Command, Text


T = 5  # Bot sleep time
database_name = "test.db"
# Bot setting
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# Database create and connect
create_database(database_name)
db = SQLiteDatabase(database_name)


# ================ Handlers =======================
# Start command handler
@dp.message_handler(Command("start"))
async def show_menu(message: types.Message):
    text = """
Hi!

Once you start testing I will update you when you want ⏱
When a failure occurs I will notify you immediately 🖨️

The steps to *start* bot: 🏁
--------------------------------------------------------
• ***Set up path*** - gives bot your path to pytest folder 🌐

• ***Edit notifications period*** - every _<input>_ seconds get response _(600 by default)_ ♾️

• ***Edit fails period*** - every _<input>_ seconds get messages if tests failed _(30 by default)_ 🔁

• ***Start testing*** - start checking tests & getting updates 📺
"""

    await message.answer(text, parse_mode='Markdown')
    await message.answer("To set up the path click the button below🔽", reply_markup=set_up_path)


# Help command handler
@dp.message_handler(Text(equals=["Help", "/help"]))
async def process_start_command(message: types.Message):
    text = """
The steps to start bot: 🏁
--------------------------------------------------------
• ***Set up path*** - gives bot your path to pytest folder 🌐

• ***Edit notifications period*** - every _<input>_ seconds get response _(600 by default)_ ♾️

• ***Edit fails period*** - every _<input>_ seconds get messages if tests failed _(30 by default)_ 🔁

• ***Start testing*** - start checking tests & getting updates 📺
--------------------------------------------------------


Commands inside ***Start testing***:
--------------------------------------------------------
• ***Unmute failures notifications*** - unmutes failures detection if muted _(unmuted by default)_ 🔊

• ***Mute failures notifications*** - mutes failures detection if not muted 🔇

• ***Get only scheduled notifications*** - turn off alert failures updates 📅

• ***Get all notifications*** - get all updates _(all by default)_ 🔔

• ***Stop testing*** - stop getting updates 🎬
--------------------------------------------------------

Enjoy 🍿
    """

    await message.reply(text, parse_mode="Markdown")
    await message.answer("To set the path click one of the buttons below🔽", reply_markup=rewritePath_editPeriods_testing_help)




# Set up path command & user registration in db
@dp.message_handler(Text(equals=["Set up path", "Reset path"]))
async def cmd_dialog_stream(message: types.Message):
    await PytestPath.pytest_path.set()  # states start working
    await message.reply("Input the path to your pytest folder: ", reply=False)


@dp.message_handler(state=PytestPath.pytest_path)
async def testing(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        pytest_path = data['text']
        print(pytest_path)  # as log

        if not path.exists(pytest_path):
            await message.answer(
                "Path is invalid...", disable_notification=False,
                reply_markup=rewritePath_editPeriods_testing_help)
            dp.current_state(user=message.from_user.id)
            await state.reset_state()

        else:
            # Check if path valid, if not - reset path or test previous successfully set path
            if not db.user_exists(message.from_user.id):
                # if user not in db then add it
                db.add_user(user_id=message.from_user.id, status=False, my_path=pytest_path)
            else:
                # if user already in db then update it
                db.update_path(user_id=message.from_user.id, status=False, my_path=pytest_path)

            # Path successfully set
            await message.answer(
                "Path successfully set...", reply_markup=rewritePath_editPeriods_testing_help)

            # Close state
            dp.current_state(user=message.from_user.id)
            await state.reset_state()



# Start testing command
@dp.message_handler(Text(equals=["Start testing"]))
async def start_testing(message: types.Message):
    if not path.exists(db.get_user_path(message.from_user.id)):
        await message.answer(
            "Path is invalid...", disable_notification=False,
            reply_markup=rewritePath_editPeriods_testing_help)

    if not db.user_exists(message.from_user.id):
        # if user not in db then add it
        db.add_user(user_id=message.from_user.id, status=True)

    else:
        # if user already in db then update it
        db.update_status(user_id=message.from_user.id, status=True)

    await message.answer(
        "Checking tests starting...")
    await message.answer("Now you will get periodical notifications and messages about tests failure if it occurs!")
    await message.answer("To modify the process click one of the buttons below🔽",
                         reply_markup=testing_managing)


# Stop testing command
@dp.message_handler(Text(equals=["End testing"]))
async def stop_testing(message: types.Message):
    if not db.user_exists(message.from_user.id):
        # if user not in db then just write it to db with non-active status
        db.add_user(user_id=message.from_user.id, status=False)
        await message.answer("The tests are not checking yet!", disable_notification=False)

    else:
        # if user in db then update his status to non-active
        db.update_status(user_id=message.from_user.id, status=False)
        await message.answer("Testing is being stopped...", reply_markup=rewritePath_editPeriods_testing_help)


# Set notification period & user registration in db
@dp.message_handler(Text(equals=["Edit notifications period"]))
async def cmd_dialog_notifications(message: types.Message):
    await Notification.notifications_period.set()
    await message.reply("Every N seconds you will get the notification independently on tests result\nInput N: ", reply=False)


@dp.message_handler(state=Notification.notifications_period)
async def notification_period(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        time = data['text']
        try:
            time = int(time)
            if time < T or time > 20000:

                # if time input is integer but less than update period
                text = f'Failure period is not updated. Please, input the integer in range _[{T}; 20000]_'

                await message.answer(
                    text=text,
                    reply_markup=rewritePath_editPeriods_testing_help,
                    parse_mode="Markdown")
                dp.current_state(user=message.from_user.id)
                await state.reset_state()

            else:

                # if time input is correct
                if not db.user_exists(message.from_user.id):
                    # if user not in db then add it
                    db.add_user(user_id=message.from_user.id, status=False)
                    db.update_notifications_period(user_id=message.from_user.id, status=False,
                                                   notifications_period=time)
                else:
                    # if user already in db then update it
                    db.update_notifications_period(user_id=message.from_user.id, status=False, notifications_period=time)

                await message.answer(
                    "Notification period is updated...", reply_markup=rewritePath_editPeriods_testing_help)

                dp.current_state(user=message.from_user.id)
                await state.reset_state()

        except:

            # if time input cannot be converted to integer
            await message.answer(
                "Notification period is not updated. Please, input the integer...", reply_markup=rewritePath_editPeriods_testing_help)
            dp.current_state(user=message.from_user.id)
            await state.reset_state()


# Set failure period & user registration in db
@dp.message_handler(Text(equals=["Edit failure period"]))
async def cmd_dialog_defects(message: types.Message):
    await Failure.failure_period.set()
    await message.reply("Once you get failure notification, you will get it every K seconds\nInput K: ", reply=False)


@dp.message_handler(state=Failure.failure_period)
async def failure_period(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        time = data['text']

        try:
            time = int(time)

            if time < T or time > 20000:

                # if time input is integer but less than update period
                text = f'Failure period is not updated. Please, input the integer in range _[{T}; 20000]_'

                await message.answer(
                    text=text,
                    reply_markup=rewritePath_editPeriods_testing_help, parse_mode="Markdown")
                dp.current_state(user=message.from_user.id)
                await state.reset_state()

            else:

                # if time input is correct
                if not db.user_exists(message.from_user.id):
                    # if user not in db then add it
                    db.add_user(user_id=message.from_user.id, status=False)
                    db.update_failures_period(user_id=message.from_user.id, status=False,
                                              failures_period=time)
                else:
                    # if user already in db then update it
                    db.update_failures_period(user_id=message.from_user.id, status=False,
                                              failures_period=time)

                await message.answer(
                    "Failure period is updated...", reply_markup=rewritePath_editPeriods_testing_help)

                dp.current_state(user=message.from_user.id)
                await state.reset_state()

        except:

            # if time input cannot be converted to integer
            await message.answer(
                "Failure period is not updated. Please, input the integer...",
                reply_markup=rewritePath_editPeriods_testing_help)
            dp.current_state(user=message.from_user.id)
            await state.reset_state()


# Mute failure notifications command
@dp.message_handler(Text(equals=["Mute failure notifications"]))
async def mute(message: types.Message):

    db.update_mute(user_id=message.from_user.id, failure_mute=True)
    await message.answer(
        "Now failure notifications are muted...", reply_markup=testing_managing)


# Unmute alert notifications command
@dp.message_handler(Text(equals=["Unmute failure notifications"]))
async def unmute(message: types.Message):

    db.update_mute(user_id=message.from_user.id, failure_mute=False)
    await message.answer(
        "Now failure notifications are loud...", reply_markup=testing_managing)


# Not to detect failures command (only scheduled notifications)
@dp.message_handler(Text(equals=["Get only scheduled notifications"]))
async def stop_failure(message: types.Message):

    db.update_defects_detect(user_id=message.from_user.id, detect_failures=False)
    await message.answer(
        "Now you will only receive scheduled notifications...", reply_markup=testing_managing)


# Detect failures command (all notifications)
@dp.message_handler(Text(equals=["Get all notifications", "/get_all"]))
async def start_failures(message: types.Message):

    db.update_defects_detect(user_id=message.from_user.id, detect_failures=True)
    await message.answer(
        "Now you will also receive notifications about failures...", reply_markup=testing_managing)


async def check_tests(T):
    while True:

        # wait T seconds till next defects check happens (among all users)
        await asyncio.sleep(T)

        # get list of active watchers
        users = db.get_users()

        for user in users:
            """
            Column structure by index:
            0 - id
            1 - user_id (chat_id)
            2 - status (testing or not)
            3 - my_path (path to pytest folder)
            4 - notifications_period (in what time next notification appears independently on result)
            5 - checks_since_last (number of checks made since last check)
            6 - failures_period (in what time next notification about failure appears if last one was about failure as well)
            7 - failures_since_last (number of failures occured since last failure)
            8 - detect_failures (True if you want to get notifications when failures occur)
            9 - failure_mute (Mutes failures notifications)
            """


            # if failure detection needed
            if user[8]:

                '''if we want to get all notifications, 
                then we need check tests state every T seconds'''
                is_ok, str_results = parse(user[3])
                print(is_ok, str_results)
                print(is_ok)
                print(user[5], user[4])
                print(user[7], user[6])

                # Scheduled notifications
                if user[5] * T >= user[4]:

                    # await bot.send_message(
                    #     user[1],
                    #     f'Sheduled response:',
                    #     disable_notification=True
                    # )
                    print(str_results)
                    await bot.send_message(user[1], str_results, parse_mode="Markdown")


                    # if message is sent, then we start counting number of checks again
                    db.update_checks_since_last(user_id=user[1], checks_since_last=1)
                else:
                    # if time has not passed, then we increase number of checks
                    db.update_checks_since_last(user_id=user[1], checks_since_last=user[5] + 1)

                # Failure notifications
                if user[7] * T >= user[6] and is_ok == 0:
                    print(f"Failure detected! {user[1]}"
                          f"Message: {str_results}, {is_ok}")

                    # await bot.send_message(
                    #     user[1],
                    #     f'Failure detected:',
                    #     disable_notification=user[9]
                    # )
                    print(str_results)
                    await bot.send_message(user[1], str_results, parse_mode="Markdown")
                    # if message is sent, then we start counting failures again
                    db.update_failures_since_last(user_id=user[1], failures_since_last=1)

                elif is_ok == 0:
                    # if current check is with failures, then we increase its quantity
                    db.update_failures_since_last(user_id=user[1], failures_since_last=user[7] + 1)
                else:
                    # if current is without failures, then we start counting them again
                    db.update_failures_since_last(user_id=user[1], failures_since_last=1)

            else:

                '''if only scheduled notifications needed, 
                then check tests only when needed time is gone'''
                if user[5] * T >= user[4]:

                    is_ok, str_results = parse(user[3])
                    # await bot.send_message(
                    #     user[1],
                    #     f'Sheduled response',
                    #     disable_notification=True
                    # )
                    await bot.send_message(user[1], str_results, parse_mode="Markdown")

                    db.update_checks_since_last(user_id=user[1], checks_since_last=1)
                else:
                    db.update_checks_since_last(user_id=user[1], checks_since_last=user[5] + 1)




async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(check_tests(T))
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")