import asyncio
import logging
from os import path
from aiogram import types
from loader import bot, dp, db
from states import states
import keyboards as keyboards_markup
from data import constants, bot_text
from functional import pytest_results_parser
from utils import time_out_of_bounds
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command(bot_text.COMMAND_START))
async def show_menu(message: types.Message):

    await message.answer(bot_text.START_TEXT, parse_mode='Markdown')
    await message.answer(text=bot_text.SET_UP_PATH, reply_markup=keyboards_markup.set_up_path)


# Help command handler
@dp.message_handler(Text(equals=[bot_text.BUTTON_HELP]))
async def process_start_command(message: types.Message):

    await message.reply(text=bot_text.HELP_TEXT, parse_mode='Markdown')
    await message.answer(text=bot_text.SET_UP_PATH, reply_markup=keyboards_markup.out_test_managing)


# Set up path command & user registration in db
@dp.message_handler(Text(equals=[bot_text.BUTTON_SET_PATH, bot_text.BUTTON_RESET_PATH]))
async def cmd_dialog_stream(message: types.Message):
    await states.PytestPath.pytest_path.set()  # states start working
    await message.reply(text=bot_text.SETTING_PATH_INSTRUCTION, reply=False)


@dp.message_handler(state=states.PytestPath.pytest_path)
async def testing(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_path = data['text']

        if not path.exists(user_path):
            await message.answer(text=bot_text.INVALID_PATH, reply_markup=keyboards_markup.out_test_managing)
            dp.current_state(user=message.from_user.id)
            await state.reset_state()

        else:

            # updating path
            db.add_user(message.from_user.id)
            db.update_user(message.from_user.id, user_path=user_path)

            # Path successfully set
            await message.answer(text=bot_text.SETTING_PATH_SUCCESS, reply_markup=keyboards_markup.out_test_managing)
            dp.current_state(user=message.from_user.id)  # Close state
            await state.reset_state()


# Start testing command
@dp.message_handler(Text(equals=[bot_text.BUTTON_START_TESTING]))
async def start_testing(message: types.Message):

    db.add_user(message.from_user.id)
    user_path = db.get_user_path(message.from_user.id)
    if user_path is None:
        await message.answer(text=bot_text.INVALID_PATH, reply_markup=keyboards_markup.out_test_managing)

    else:

        db.update_user(user_id=message.from_user.id, status=True)

        await message.answer(text=bot_text.START_TESTING_INSTRUCTION_1)
        await message.answer(text=bot_text.START_TESTING_INSTRUCTION_2)
        await message.answer(text=bot_text.START_TESTING_INSTRUCTION_3, reply_markup=keyboards_markup.in_test_managing)


# Stop testing command
@dp.message_handler(Text(equals=[bot_text.BUTTON_END_TESTING]))
async def stop_testing(message: types.Message):
    db.add_user(message.from_user.id)
    db.update_user(user_id=message.from_user.id, status=False)
    await message.answer(text=bot_text.STOP_TESTING, reply_markup=keyboards_markup.out_test_managing)


# Set notification period & user registration in db
@dp.message_handler(Text(equals=[bot_text.BUTTON_EDIT_FAILURE_PERIOD, bot_text.BUTTON_EDIT_NOTIFICATIONS_PERIOD]))
async def cmd_dialog_notifications(message: types.Message):
    await states.Period.period.set()

    if message.text == bot_text.BUTTON_EDIT_FAILURE_PERIOD:
        await message.reply(text=bot_text.FAILURE_PERIOD_INSTRUCTION_1)
        await message.reply(text=bot_text.FAILURE_PERIOD_INSTRUCTION_2)

    else:
        await message.reply(text=bot_text.NOTIFICATION_PERIOD_INSTRUCTION_1)
        await message.reply(text=bot_text.NOTIFICATION_PERIOD_INSTRUCTION_2)


@dp.message_handler(state=states.Period.period)
async def update_period(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['text'] = message.text
        try:
            period_method, time = data['text'].split()
            if period_method not in [bot_text.CHANGE_NOTIFICATION_PERIOD, bot_text.CHANGE_FAILURE_PERIOD]:
                raise ValueError

            time = int(time)
            if time < constants.SLEEP_TIME or time > constants.TIME_LIMIT:
                await time_out_of_bounds(message, state)

            else:
                db.add_user(message.from_user.id)

                if period_method == bot_text.CHANGE_NOTIFICATION_PERIOD:
                    db.update_user(user_id=message.from_user.id, notifications_period=time)
                else:
                    db.update_user(user_id=message.from_user.id, failures_period=time)

                await message.answer(text=bot_text.UPDATE_PERIOD_SUCCESS,
                                     reply_markup=keyboards_markup.out_test_managing)
                dp.current_state(user=message.from_user.id)
                await state.reset_state()

        except ValueError:

            # if time input cannot be converted to integer
            await message.answer(text=bot_text.UPDATE_PERIOD_FAILURE, reply_markup=keyboards_markup.out_test_managing)
            dp.current_state(user=message.from_user.id)
            await state.reset_state()


# Mute failure notifications command
@dp.message_handler(Text(equals=[bot_text.BUTTON_MUTE_FAILURE_NOTIFICATIONS]))
async def mute(message: types.Message):

    db.update_user(user_id=message.from_user.id, failure_mute=False)
    await message.answer(text=bot_text.MUTED_FAILURE_NOTIFICATIONS, reply_markup=keyboards_markup.in_test_managing)


# Unmute alert notifications command
@dp.message_handler(Text(equals=[bot_text.BUTTON_UNMUTE_FAILURE_NOTIFICATIONS]))
async def unmute(message: types.Message):

    db.update_user(user_id=message.from_user.id, failure_mute=False)
    await message.answer(text=bot_text.LOUD_FAILURE_NOTIFICATIONS, reply_markup=keyboards_markup.in_test_managing)


# Not to detect failures command (only scheduled notifications)
@dp.message_handler(Text(equals=[bot_text.BUTTON_GET_ONLY_SCHEDULED_NOTIFICATIONS]))
async def stop_failure(message: types.Message):

    db.update_user(user_id=message.from_user.id, detect_failures=False)
    await message.answer(text=bot_text.GET_SCHEDULED_NOTIFICATIONS_ANSWER,
                         reply_markup=keyboards_markup.in_test_managing)


# Detect failures command (all notifications)
@dp.message_handler(Text(equals=[bot_text.BUTTON_GET_ALL_NOTIFICATIONS]))
async def start_failures(message: types.Message):

    db.update_user(user_id=message.from_user.id, detect_failures=True)
    await message.answer(text=bot_text.GET_ALL_NOTIFICATIONS_ANSWER, reply_markup=keyboards_markup.in_test_managing)


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
