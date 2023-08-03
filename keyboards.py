from typing import Any
from aiogram.types import KeyboardButton, InlineKeyboardButton


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


class ApproveOrNotKeyboard:
    kb = [
        [InlineKeyboardButton(text="✅", callback_data="Approved")],
        [InlineKeyboardButton(text="❌", callback_data="Unapproved")]
    ]


class MenuKeyboard:
    kb = [[KeyboardButton(text="Menu")]]
