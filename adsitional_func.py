from PIL import Image
import asyncio
import logging
import os
from aiogram.types import FSInputFile


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
