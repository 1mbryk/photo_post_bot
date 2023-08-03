from aiogram import F, Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from states import *
from additional_func import *
from config import *
import logging
from aiogram.types import FSInputFile
from keyboards import *
from aiogram.types import (Message,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
router = Router()


@router.message(Command("start"))
@router.message(Command("menu"))
@router.message(Text("Menu"))
async def start_handler(msg: Message):  # start menu
    logging.info(msg.from_user.id)
    await msg.answer(text="What do you want to do?", reply_markup=ReplyKeyboardMarkup(keyboard=StartKeyboard.kb, resize_keyboard=True, one_time_keyboard=True))


@router.message(Command("post_photo"))
@router.message(Text("Post Photos"))
async def message_handler(msg: Message):
    if msg.from_user.id not in admin_id:
        await msg.answer("You haven\'t right!")
        return
    await msg.answer(text="Do you want to post all photos from directory or preview each of them before post?",
                     reply_markup=ReplyKeyboardMarkup(keyboard=PostKeyboard.kb, resize_keyboard=True, one_time_keyboard=True))


@router.message(Text("Post All"))
async def turn_on_all_mode(msg: Message, state: FSMContext):
    logging.info("in turn_on_all_mode")
    await state.set_state(BotStates.all_mode)
    logging.info(f"current state: {await state.get_state()}")
    await msg.answer(text="Do you want to use default directory?",
                     reply_markup=ReplyKeyboardMarkup(keyboard=YesNoKeyboard.kb, resize_keyboard=True, one_time_keyboard=True))


@router.message((BotStates.all_mode or BotStates.preview_mode) and Text("Yes"))
async def post_with_default_dir(msg: Message, state: FSMContext):
    logging.info("in post_photo")
    logging.info(f"current state {await state.get_state()}")
    if await state.get_state() == BotStates.all_mode:
        await post_all(state)
    elif await state.get_state() == BotStates.preview_mode:
        pass
        # await post_preview()

# @router.message(BotStates.all_mode)


async def post_all(state: FSMContext, directory_path: str = None):
    logging.info("In Post All")
    logging.info(f"current state: {await state.get_state()}")
    # await msg.answer("Input Directory")
    if directory_path == None:
        directory_path = default_directory

    imgs = await choose_image(directory_path)
    imgs.sort()
    for img in imgs:
        img_path = str(img)
        logging.info(img_path)
        photo = FSInputFile(img_path, chunk_size=3000000)
        await bot.send_photo(channel_id, photo, disable_notification=True)
        await bot.send_document(channel_id, photo, disable_notification=True)
        await asyncio.sleep(3)
        if await state.get_state() == BotStates.cancel:
            await state.clear()
            break

    await state.clear()


# @router.message(Text("Post with preview"))
# @router.message(BotStates.preview_mode)
# async def post_preview(msg: Message, state: FSMContext):


@router.message(Command("cancel"))
async def canceling(msg: Message, state: FSMContext):
    logging.info(f"current state: {await state.get_state()}")
    if await state.get_state() == BotStates.cancel:
        state.clear()
    else:
        await state.set_state(BotStates.cancel)
    await start_handler(msg)
