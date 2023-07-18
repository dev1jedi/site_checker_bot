from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from markups.admin_markup import return_menu, otmena, main
import os
import json
import validators


class State_c(StatesGroup):
    add_domain = State()
    add_domains = State()
    del_domain = State()
    del_domains = State()

async def add_domain(call: types.CallbackQuery):
    await State_c.add_domain.set()
    await call.message.answer("Пришлите домен и я добавлю его в общий список: ", reply_markup=otmena)

async def add_dmn(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена действия":
        await state.finish()
        await message.answer("Главное меню", reply_markup=main)
    else:

        if validators.domain(message.text):

            dom = message.text.split("\n")[0]

            with open("data_files/domains.json", "r") as f:
                domains = json.load(f)

            flag = True
            for i in domains["domains"]:
                if i['domain'] == dom:
                    flag = False

            if flag:
                domains["domains"].append({"domain": dom})

                f = open("data_files/domains.json", "w")
                f.write(json.dumps(domains, indent=4))

                await message.answer("Домен записан!", reply_markup=return_menu)
                await state.finish()
            else:
                await message.answer("Такой домен уже записан!", reply_markup=return_menu)
                await state.finish()

        else:
            await message.answer("Неверный домен!")
            await state.finish()
            await message.answer("Пришлите домен и я добавлю его в общий список: ", reply_markup=otmena)
            await State_c.add_domain.set()


async def add_domains(call: types.CallbackQuery):
    await State_c.add_domains.set()
    await call.message.answer("Пришлите список доменов, которые хотите добавить(в формате .txt): ", reply_markup=otmena)

async def add_dmns(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена действия":
        await state.finish()
        await message.answer("Главное меню", reply_markup=main)
    else:
        await message.document.download("data_files/temp_domains.txt")
        with open("data_files/temp_domains.txt", "r") as f:
            with open("data_files/domains.json", "r") as g:
                domain = json.load(g)
                for line in f:
                    if validators.domain(line):

                        dom = line.split("\n")[0]
                        flag = True
                        for i in domain["domains"]:
                            if i['domain'] == dom:
                                flag = False

                        if flag:
                            domain["domains"].append({"domain": dom})

                            f = open("data_files/domains.json", "w")
                            f.write(json.dumps(domain, indent=4))


        os.remove("data_files/temp_domains.txt")

        await message.answer("Список добавлен!", reply_markup=return_menu)
        await state.finish()



async def del_domain(call: types.CallbackQuery):
    await State_c.del_domain.set()
    await call.message.answer("Пришлите домен и я удалю его из общего списка: ", reply_markup=otmena)

async def del_dmn(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена действия":
        await state.finish()
        await message.answer("Главное меню", reply_markup=main)
    else:
        with open("data_files/domains.json", "r") as f:
            domains = json.load(f)

        index = 0
        for domain in domains["domains"]:
          if domain["domain"] == message.text:
            domains["domains"].pop(index)
          index += 1

        f = open("data_files/domains.json", "w")
        f.write(json.dumps(domains, indent=4))

        await message.answer("Домен удален!", reply_markup=return_menu)
        await state.finish()


async def del_domains(call: types.CallbackQuery):
    await State_c.del_domains.set()
    await call.message.answer("Пришлите список доменов, которые хотите удалить(в формате .txt): ", reply_markup=otmena)

async def del_dmns(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена действия":
        await state.finish()
        await message.answer("Главное меню", reply_markup=main)
    else:
        await message.document.download("data_files/temp_domains_del.txt")

        with open('data_files/temp_domains_del.txt', "r") as f:

            with open("data_files/domains.json", "r") as g:
                domains = json.load(g)

                for line in f:
                    index = 0
                    if validators.domain(line):
                        for domain in domains["domains"]:
                            if domain["domain"] == line.split("\n")[0]:
                                domains["domains"].pop(index)
                            index += 1

        f = open("data_files/domains.json", "w")
        f.write(json.dumps(domains, indent=4))

        os.remove("data_files/temp_domains_del.txt")


        await message.answer("Домены удалены!", reply_markup=return_menu)
        await state.finish()


#types.ContentType.DOCUMENT

def register_handlers_domains(dp : Dispatcher):
    dp.register_callback_query_handler(add_domain, text="add_domain", state=None)
    dp.register_message_handler(add_dmn, content_types=["text"], state=State_c.add_domain)

    dp.register_callback_query_handler(del_domain, text="del_domain", state=None)
    dp.register_message_handler(del_dmn, content_types=["text"], state=State_c.del_domain)

    dp.register_callback_query_handler(add_domains, text="add_domains", state=None)
    dp.register_message_handler(add_dmns, content_types=["document", "text"], state=State_c.add_domains)

    dp.register_callback_query_handler(del_domains, text="del_domains", state=None)
    dp.register_message_handler(del_dmns, content_types=["document", "text"], state=State_c.del_domains)