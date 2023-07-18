from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_menu_btn = ReplyKeyboardMarkup(row_width=2)
stop = KeyboardButton(text="❌ Остановить чeкeр")
start = KeyboardButton(text="✅ Запустить чeкeр")
user_menu_btn.add(start, stop)