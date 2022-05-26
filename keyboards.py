from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

set_up_path = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Set up path'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

in_test_managing = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Unmute failure notifications'),
            KeyboardButton(text='Mute failure notifications')
        ],
        [
            KeyboardButton(text='Get only scheduled notifications'),
            KeyboardButton(text='Get all notifications')
        ],
        [
            KeyboardButton(text='End testing')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

out_test_managing = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Reset path'),
            KeyboardButton(text='Edit notifications period'),
            KeyboardButton(text='Edit failure period')
        ],
        [
            KeyboardButton(text='Help'),
            KeyboardButton(text='Start testing')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
