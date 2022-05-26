from data import constants as const
import keyboards as keyboards_markup
from loader import dp


async def time_out_of_bounds(message, state):
    # if time input is integer but less than update period
    text = f'Chosen period is not updated. Please, input the integer in range _[{const.SLEEP_TIME}; 20000]_'

    await message.answer(
        text=text,
        reply_markup=keyboards_markup.out_test_managing,
        parse_mode='Markdown'
    )
    dp.current_state(user=message.from_user.id)
    await state.reset_state()
