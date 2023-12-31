import logging
from config import bot, channel_id
import os
from aiogram import types


async def is_it_image(filename: str) -> bool:
    return (
        "jpg" in filename.lower() or
        "png" in filename.lower() or
        "jpeg" in filename.lower()
    )


async def choose_image(directory_path: str):
    imgs = []
    logging.info("in choose_image")
    for _, _, files in os.walk(directory_path):
        for filename in files:
            if await is_it_image(filename):
                imgs.append(directory_path + '/' + filename)
    return imgs


async def post_photo(photo_path: str):
    photo = types.FSInputFile(photo_path)
    await bot.send_photo(channel_id, photo, disable_notification=True)
    await bot.send_document(channel_id, photo, disable_notification=True)
