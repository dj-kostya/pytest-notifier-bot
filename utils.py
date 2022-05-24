from data import constants as const
from keyboards import keyboards as keyboards_markup
from loader import dp, db


# if user not in db, then add
def register_user(user_id):
    if not db.user_exists(user_id):
        db.add_user(user_id=user_id, status=False)


async def time_out_of_bounds(message, state):
    # if time input is integer but less than update period
    text = f'Chosen period is not updated. Please, input the integer in range _[{const.SLEEP_TIME}; 20000]_'

    await message.answer(
        text=text,
        reply_markup=keyboards_markup.path_periods_testing_help,
        parse_mode='Markdown'
    )
    dp.current_state(user=message.from_user.id)
    await state.reset_state()
