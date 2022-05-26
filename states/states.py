from aiogram.dispatcher.filters.state import State, StatesGroup

# create states for saving user answer


# state for saving path info
class PytestPath(StatesGroup):
    pytest_path = State()


# state for saving notifications period info
class Period(StatesGroup):
    period = State()
