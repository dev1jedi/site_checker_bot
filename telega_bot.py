from aiogram import types, Dispatcher
from markups.admin_markup import main, dmn_choice, return_menu, menu_btn
from markups.user_markup import user_menu_btn
from handlers import setting_handler, domain_handler
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
import json
import asyncio
from instrument.checker import check_d
from config import glav_users


stop_flags = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    stop_flags[message.from_user.id] = False

    if message.from_user.id in glav_users:
        await bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}. Перейдем к настройке бота: ", reply_markup=main)
    else:
        await bot.send_message(message.from_user.id,f"Привет, {message.from_user.first_name}. Бот готов к работе! ", reply_markup=user_menu_btn)



@dp.callback_query_handler(text="menu")
async def menu(message: types.Message):
    await bot.send_message(message.from_user.id, "Главное меню", reply_markup=main)

@dp.callback_query_handler(text="domain_choice")
async def domain_choice(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите действие: ", reply_markup=dmn_choice)

@dp.callback_query_handler(text="my_domains")
async def my_domains(message: types.Message):
    with open("data_files/domains.json", "r") as f:
        domains = json.load(f)

    list_of_domains = ""

    for domain in domains["domains"]:
        list_of_domains = list_of_domains + domain["domain"] + "\n"

    await bot.send_message(message.from_user.id, f"Список доменов: \n\n{list_of_domains}", reply_markup=return_menu)


@dp.callback_query_handler(text="start_check")
async def check(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите действие", reply_markup=menu_btn)


@dp.message_handler()
async def start_check(message: types.Message, state: FSMContext):
    global sostoyanie

    f = open("data_files/settings.json")
    time = json.load(f)["time"]

    #ДЛЯ АДМИНА
    if message.text == "✅ Запустить чекер":

        stop_flags[message.from_user.id] = False
        await message.answer("Чекер запущен!", reply_markup=menu_btn)

        while True:

            if stop_flags.get(message.from_user.id):
                break

            check_result = check_d.request_check()
            await message.answer(check_result)
            await asyncio.sleep(60 * int(time))


    if message.text == "Остановить чекер":
        stop_flags[message.from_user.id] = True
        await message.answer("Чекер остановлен!", reply_markup=main)

    #ДЛЯ ЮЗЕРОВ
    if message.text == "✅ Запустить чeкeр":
        sostoyanie = True
        await message.answer("Чекер запущен!")

        while sostoyanie:
            check_result = check_d.request_check()
            await message.answer(check_result)
            await asyncio.sleep(60 * int(time))

    if message.text == "❌ Остановить чeкeр":
        sostoyanie = False
        await message.answer("Чекер остановлен!")


setting_handler.register_handlers_setting(dp)
domain_handler.register_handlers_domains(dp)

def main_register(dp : Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
