import asyncio
from os import path
from aiogram import types

from loader import bot, dp, db
from states import states
import keyboards.keyboards as keyboards_markup
from data import constants, bot_text
from functional import pytest_results_parser
from utils import register_user, time_out_of_bounds

from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command('start'))
async def show_menu(message: types.Message):

    await message.answer(bot_text.start_text, parse_mode='Markdown')
    await message.answer('To set up the path click the button below🔽', reply_markup=keyboards_markup.set_up_path)


# Help command handler
@dp.message_handler(Text(equals=['Help', '/help']))
async def process_start_command(message: types.Message):

    await message.reply(bot_text.help_text, parse_mode='Markdown')
    await message.answer('To set the path click one of the buttons below🔽',
                         reply_markup=keyboards_markup.path_periods_testing_help
                         )


# Set up path command & user registration in db
@dp.message_handler(Text(equals=['Set up path', 'Reset path']))
async def cmd_dialog_stream(message: types.Message):
    await states.PytestPath.pytest_path.set()  # states start working
    await message.reply('Input the path to your pytest folder: ', reply=False)


@dp.message_handler(state=states.PytestPath.pytest_path)
async def testing(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_path = data['text']

        if not path.exists(user_path):
            await message.answer(
                'Path is invalid...', disable_notification=False,
                reply_markup=keyboards_markup.path_periods_testing_help)
            dp.current_state(user=message.from_user.id)
            await state.reset_state()

        else:
            register_user(message.from_user.id)
            # updating path
            db.update_path(user_id=message.from_user.id, status=False, my_path=user_path)

            # Path successfully set
            await message.answer(
                'Path successfully set...', reply_markup=keyboards_markup.path_periods_testing_help
            )
            dp.current_state(user=message.from_user.id)  # Close state
            await state.reset_state()


# Start testing command
@dp.message_handler(Text(equals=['Start testing']))
async def start_testing(message: types.Message):

    register_user(message.from_user.id)
    if not path.exists(db.get_user_path(message.from_user.id)):
        await message.answer(
            'Path is invalid...', disable_notification=False,
            reply_markup=keyboards_markup.path_periods_testing_help)
    else:
        db.update_status(user_id=message.from_user.id, status=True)

        await message.answer('Checking tests starting...')
        await message.answer('Now you will get periodical notifications and messages about tests failure if it occurs!')
        await message.answer('To modify the process click one of the buttons below🔽',
                             reply_markup=keyboards_markup.testing_managing)


# Stop testing command
@dp.message_handler(Text(equals=['End testing']))
async def stop_testing(message: types.Message):
    register_user(message.from_user.id)
    # update status to non-active
    db.update_status(user_id=message.from_user.id, status=False)
    await message.answer('Testing is being stopped...', reply_markup=keyboards_markup.path_periods_testing_help)


# Set notification period & user registration in db
@dp.message_handler(Text(equals=['Edit notifications period']))
async def cmd_dialog_notifications(message: types.Message):
    await states.Notification.notifications_period.set()
    await message.reply(
        'Every N seconds you will get the notification independently on tests result\nInput N: ', reply=False
    )


@dp.message_handler(state=states.Notification.notifications_period)
async def notification_period(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        time = data['text']
        try:
            time = int(time)
            if time < constants.SLEEP_TIME or time > constants.TIME_LIMIT:
                await time_out_of_bounds(message, state)

            else:
                register_user(message.from_user.id)
                db.update_notifications_period(user_id=message.from_user.id, status=False,
                                               notifications_period=time
                                               )
                await message.answer(
                    'Notification period is updated...', reply_markup=keyboards_markup.path_periods_testing_help
                )
                dp.current_state(user=message.from_user.id)
                await state.reset_state()

        except ValueError:

            # if time input cannot be converted to integer
            await message.answer(
                'Notification period is not updated. Please, input the integer...',
                reply_markup=keyboards_markup.path_periods_testing_help)
            dp.current_state(user=message.from_user.id)
            await state.reset_state()


# Set failure period & user registration in db
@dp.message_handler(Text(equals=['Edit failure period']))
async def cmd_dialog_defects(message: types.Message):
    await states.Failure.failure_period.set()
    await message.reply('Once you get failure notification, you will get it every K seconds\nInput K: ',
                        reply=False)


@dp.message_handler(state=states.Failure.failure_period)
async def failure_period(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        time = data['text']

        try:
            time = int(time)

            if time < constants.SLEEP_TIME or time > constants.TIME_LIMIT:
                await time_out_of_bounds(message, state)

            else:
                register_user(message.from_user.id)
                db.update_failures_period(user_id=message.from_user.id, status=False,
                                          failures_period=time)
                await message.answer(
                    'Failure period is updated...', reply_markup=keyboards_markup.path_periods_testing_help
                )
                dp.current_state(user=message.from_user.id)
                await state.reset_state()

        except ValueError:

            # if time input cannot be converted to integer
            await message.answer(
                'Failure period is not updated. Please, input the integer...',
                reply_markup=keyboards_markup.path_periods_testing_help)
            dp.current_state(user=message.from_user.id)
            await state.reset_state()


# Mute failure notifications command
@dp.message_handler(Text(equals=['Mute failure notifications']))
async def mute(message: types.Message):

    db.update_mute(user_id=message.from_user.id, failure_mute=True)
    await message.answer(
        'Now failure notifications are muted...', reply_markup=keyboards_markup.testing_managing
    )


# Unmute alert notifications command
@dp.message_handler(Text(equals=['Unmute failure notifications']))
async def unmute(message: types.Message):

    db.update_mute(user_id=message.from_user.id, failure_mute=False)
    await message.answer(
        'Now failure notifications are loud...', reply_markup=keyboards_markup.testing_managing
    )


# Not to detect failures command (only scheduled notifications)
@dp.message_handler(Text(equals=['Get only scheduled notifications']))
async def stop_failure(message: types.Message):

    db.update_defects_detect(user_id=message.from_user.id, detect_failures=False)
    await message.answer(
        'Now you will only receive scheduled notifications...', reply_markup=keyboards_markup.testing_managing)


# Detect failures command (all notifications)
@dp.message_handler(Text(equals=['Get all notifications', '/get_all']))
async def start_failures(message: types.Message):

    db.update_defects_detect(user_id=message.from_user.id, detect_failures=True)
    await message.answer(
        'Now you will also receive notifications about failures...', reply_markup=keyboards_markup.testing_managing)


async def check_tests(period):
    while True:

        # wait T seconds till next failure check happens (among all users)
        await asyncio.sleep(period)

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
            6 - failures_period (in what time next notification about failure appears
                    if last one was about failure as well)
            7 - failures_since_last (number of failures occured since last failure)
            8 - detect_failures (True if you want to get notifications when failures occur)
            9 - failure_mute (Mutes failures notifications)
            """

            is_ok, str_results = pytest_results_parser.pytest_results(user[3])

            # Scheduled notifications
            if user[5] * period >= user[4]:

                print(str_results)
                await bot.send_message(user[1], str_results, parse_mode='Markdown')

                # if message is sent, then we start counting number of checks again
                db.update_checks_since_last(user_id=user[1], checks_since_last=1)
            else:
                # if time has not passed, then we increase number of checks
                db.update_checks_since_last(user_id=user[1], checks_since_last=user[5] + 1)

            if user[8]:

                # Failure notifications
                if user[7] * period >= user[6] and is_ok == 0:
                    await bot.send_message(user[1], str_results, parse_mode='Markdown')
                    # if message is sent, then we start counting failures again
                    db.update_failures_since_last(user_id=user[1], failures_since_last=1)

                elif is_ok == 0:
                    # if current check is with failures, then we increase its quantity
                    db.update_failures_since_last(user_id=user[1], failures_since_last=user[7] + 1)
                else:
                    # if current is without failures, then we start counting them again
                    db.update_failures_since_last(user_id=user[1], failures_since_last=1)
