from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

main = InlineKeyboardMarkup(row_width=1)
domain_choice = InlineKeyboardButton(text="💾 Добавить/удалить домены", callback_data="domain_choice")
settings = InlineKeyboardButton(text="⌚ Настроить интервал проверки", callback_data="bot_settings")
start = InlineKeyboardButton(text="✅ Запустить чекер", callback_data="start_check")

main.add(domain_choice, settings, start)

dmn_choice = InlineKeyboardMarkup(row_width=1)
add_domain = InlineKeyboardButton(text="➕ Добавить домен", callback_data="add_domain")
add_domains = InlineKeyboardButton(text="➕➕ Добавить домены(список)", callback_data="add_domains")
del_domain = InlineKeyboardButton(text="➖ Удалить домен", callback_data="del_domain")
del_domains = InlineKeyboardButton(text="➖➖ Удалить домены(список)", callback_data="del_domains")
my_domains = InlineKeyboardButton(text="❗ Мои текущие домены", callback_data="my_domains")

dmn_choice.add(add_domain, add_domains, del_domain, del_domains, my_domains)

return_menu = InlineKeyboardMarkup(row_width=1)
rtrn = InlineKeyboardButton(text="♻ Вернуться в главное меню", callback_data="menu")
return_menu.add(rtrn)

otmena = ReplyKeyboardMarkup(row_width=2)
otm = KeyboardButton(text="❌ Отмена действия", callback_data="menu")
otmena.add(otm)




menu_btn = ReplyKeyboardMarkup(row_width=2)
stop = KeyboardButton(text="Остановить чекер")
start = KeyboardButton(text="✅ Запустить чекер")
menu_btn.add(start, stop)
