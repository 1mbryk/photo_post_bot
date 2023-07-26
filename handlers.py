from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import *
from adsitional_func import *
from config import bot, CHANNEL_ID
import logging
from aiogram.types import FSInputFile
from PIL import Image

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")


@router.message(Command("post_to_channel"))
async def message_handler(msg: Message, state: FSMContext):
    await state.set_state(States.waiting_path)
    await msg.answer("Input Directory")


@router.message(States.waiting_path)
async def confirm_post(msg: Message, state: FSMContext):
    logging.info("In confirm_post")
    imgs = await choose_image(msg.text)
    imgs.sort()
    for img in imgs:
        img_path = str(img)
        logging.info(img_path)
        photo = FSInputFile(img_path, chunk_size=3000000)
        await bot.send_photo(CHANNEL_ID, photo, disable_notification=True)
        await bot.send_document(CHANNEL_ID, photo, disable_notification=True)
        await asyncio.sleep(3)

    await msg.answer("Confirmed")

    await state.clear()
