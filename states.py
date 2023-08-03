from aiogram.fsm.state import State, StatesGroup

# cancel = State()


class BotStates(StatesGroup):
    cancel = State(state="cancel")
    # all mode - post all photo from directory
    all_mode = State(state="all_mode")
    # preview mode - preview each photo before post
    preview_mode = State(state="preview_mode")
    change_chanel = State(state="change_channel")
    custom_dir = State(state="custom_dir")
