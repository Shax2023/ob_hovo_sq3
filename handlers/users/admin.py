import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd


# Foydalanuvchilar ro'yxatini olish va yuborish
@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    if not users:
        await message.answer("Bazada foydalanuvchilar yo'q.")
        return

    # Pandas bilan to'g'ri chiqarish
    data = {
        "Telegram ID": [user[0] for user in users],
        "Name": [user[1] for user in users]
    }

    df = pd.DataFrame(data)

    # DataFrameni bo'lib yuborish
    for x in range(0, len(df), 50):
        chunk = df.iloc[x:x + 50]
        await bot.send_message(message.chat.id, chunk.to_string(index=False))



# Barcha foydalanuvchilarga reklama yuborish
@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()
    
    # Har bir foydalanuvchiga reklama yuborish
    for user in users:
        try:
            user_id = user[0]
            await bot.send_message(user_id, "@ib0dullayev kanaliga obuna bo'ling!")
            await asyncio.sleep(0.05)  # Biror foydalanuvchiga yuborishdan oldin kichik kutish
        except Exception as error:
            print(f"Error sending message to {user_id}: {error}")


# Baza tozalash
@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def clean_db(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")


