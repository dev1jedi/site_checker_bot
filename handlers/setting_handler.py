from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from markups.admin_markup import return_menu
import json

class State_c(StatesGroup):
    time = State()


async def time_set(call: types.CallbackQuery):
    await State_c.time.set()
    await call.message.answer("Интервал между проверками сайтов(в минутах): ")


async def time_add(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            if int(message.text) > 0:
                f = open("data_files/settings.json")
                time = json.load(f)

                time["time"] = int(message.text)

                f = open("data_files/settings.json", "w")
                f.write(json.dumps(time, indent=4))

                await message.answer("Готово!", reply_markup=return_menu)
                await state.finish()
            else:
                await message.answer("Время введено неправильно! Попробуйте еще раз!")
        else:
            await message.answer("Введите число!")
    except:
        await message.answer("Неправильный формат!")



def register_handlers_setting(dp : Dispatcher):
    dp.register_callback_query_handler(time_set, text="bot_settings", state=None)
    dp.register_message_handler(time_add, content_types=["text"], state=State_c.time)
