from aiogram import types
from loader import dp

from aiogram import types
from .api import obhavo

@dp.message_handler(content_types='text')
async def first_handler(message:types.Message):
    shahar = message.text
    data = obhavo(shahar)
    if data=='Error':
        await message.answer("Malumot topilmadi!")
    else:
        await message.answer(data)
