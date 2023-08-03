from typing import Any
from aiogram.types import KeyboardButton


class StartKeyboard():
    kb = [
        [KeyboardButton(text="Post Photos")],
        [KeyboardButton(text="Change Default Directory")]
    ]


class PostKeyboard():
    kb = [
        [KeyboardButton(text="Post All")],
        [KeyboardButton(text="Post with preview")],
        [KeyboardButton(text="Menu")]
    ]


class YesNoKeyboard():
    kb = [
        [KeyboardButton(text="Yes")],
        [KeyboardButton(text="No")]
    ]
