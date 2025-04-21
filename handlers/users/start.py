from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from data.config import ADMINS
import sqlite3


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        db.add_user(user_id==user_id, name=name)
        count = db.count_users()[0]

        welcome_text = f"Xush kelibsiz, {name}!\n"
        welcome_text += "🤖 Bu bot sizga ob-havo ma'lumotlarini taqdim etadi.\n\n"
        welcome_text += "🌆 Shahringiz nomini kiriting:"

        await message.answer(welcome_text)
        users = db.select_all_users()
        print("Current users in database:", users)

        # Adminlarga xabar
        admin_msg = f"{name} (ID: {user_id}) bazaga qo'shildi.\n"
        admin_msg += f"Bazada {count} ta foydalanuvchi bor."

        await bot.send_message(chat_id=ADMINS[0], text=admin_msg)

    except sqlite3.IntegrityError:
        welcome_text = "🤖 Bu bot sizga ob-havo ma'lumotlarini taqdim etadi.\n\n"
        welcome_text += "🌆 Shahringiz nomini kiriting:"
        # Foydalanuvchi oldin qo‘shilgan
        await message.answer(f"Xush kelibsiz, {name}!\n💾Siz bazaga allaqachon qo'shilgansiz. \n\n{welcome_text}")
        await bot.send_message(chat_id=ADMINS[0], text=f"{name} (ID: {user_id}) bazada mavjud.")

    except Exception as err:
        # Boshqa xatoliklarni ushlab log qilish
        await message.answer("Kechirasiz, tizimda nosozlik yuz berdi.")
        await bot.send_message(chat_id=ADMINS[0], text=f"❌ Xatolik: {err}")

