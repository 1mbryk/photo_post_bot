from aiogram import F, Router
import asyncio
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from states import *
import additional_func as ad_f
from config import *
import logging
from aiogram import types
from keyboards import *
from aiogram.types import (Message,
                           ReplyKeyboardMarkup,
                           InlineKeyboardMarkup,
                           )
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
        await msg.answer("You\'re haven\'t right!")
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


@router.message(Text("Post with preview"))
async def turn_on_preview_mode(msg: Message, state: FSMContext):
    logging.info("in turn_on_preview_mode")
    await state.set_state(BotStates.preview_mode)
    logging.info(f"current state: {await state.get_state()}")
    await msg.answer(text="Do you want to use default directory?",
                     reply_markup=ReplyKeyboardMarkup(keyboard=YesNoKeyboard.kb, resize_keyboard=True, one_time_keyboard=True))


@router.message((BotStates.all_mode or BotStates.preview_mode) and Text("Yes"))
async def post_with_default_dir(msg: Message, state: FSMContext):
    await msg.answer(text="Done!", reply_markup=ReplyKeyboardMarkup(keyboard=MenuKeyboard.kb, resize_keyboard=True, one_time_keyboard=True))
    logging.info("in post_with_default_dir")
    logging.info(f"current state {await state.get_state()}")
    if await state.get_state() == BotStates.all_mode:
        await post_all(state)
    elif await state.get_state() == BotStates.preview_mode:
        pass
        await post_preview(state, msg.chat.id)


async def post_all(state: FSMContext, directory_path: str = None):
    logging.info("In Post All")
    logging.info(f"current state: {await state.get_state()}")
    # await msg.answer("Input Directory")
    if directory_path == None:
        directory_path = default_directory

    imgs = await ad_f.choose_image(directory_path)
    imgs.sort()
    for img in imgs:
        img_path = str(img)
        logging.info(img_path)
        await ad_f.post_photo(img_path)
        await asyncio.sleep(3)
        if await state.get_state() == BotStates.cancel:
            break

    await state.clear()


async def post_preview(state: FSMContext, chat_id: int, directory_path: str = None):
    logging.info(" In post_preview")
    logging.info(f" current state: {await state.get_state()}")
    logging.info(f" user_id: {chat_id}")

    if directory_path == None:
        directory_path = default_directory

    imgs = await ad_f.choose_image(directory_path)
    imgs.sort()
    for img in imgs:
        img_path = str(img)
        logging.info(img_path)
        photo = types.FSInputFile(img_path)
        await bot.send_photo(chat_id, photo, caption=img_path, reply_markup=InlineKeyboardMarkup(
            inline_keyboard=ApproveOrNotKeyboard.kb))

        if await state.get_state() == BotStates.cancel:
            break
    await state.clear()


@router.callback_query()
async def callback_query_handler(cb_query: types.CallbackQuery):
    msg_id = cb_query.inline_message_id
    cb_data = cb_query.data
    img_path = cb_query.message.caption
    logging.info(img_path)

    logging.info(cb_data)
    if (cb_data == "Approved"):
        await cb_query.message.edit_caption(
            inline_message_id=msg_id, caption="✅ Approved", reply_markup=None)
        await ad_f.post_photo(img_path)
    else:
        await cb_query.message.edit_caption(
            inline_message_id=msg_id, caption="❌ Unapproved", reply_markup=None)


@router.message(Command("cancel"))
async def canceling(msg: Message, state: FSMContext):
    logging.info(f"current state: {await state.get_state()}")
    await state.set_state(BotStates.cancel)
    await start_handler(msg)
