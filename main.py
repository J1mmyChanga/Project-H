import asyncio
from lib import Lib
from keyboards import main_keyboard
from aiogram import Bot, Dispatcher, types

bot = Bot(token="5984577215:AAHqvZm2mjKfjRHjV0lAUU4PqdunHPSfYkU")
dp = Dispatcher(bot)

share_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
share_button = types.KeyboardButton(text="📞 Предоставить телефон", request_contact=True)
share_keyboard.add(share_button)

from_action = {}


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет, что ты хочешь сделать?", reply_markup=main_keyboard)


@dp.message_handler(lambda message: message.text == "🏪 Продукты")
async def products(message: types.Message):
    user_id = message.from_user.id
    from_action[user_id] = 2

    await message.answer("☎️Пожалуйста, поделитесь своим телефоном", reply_markup=share_keyboard)


@dp.message_handler(lambda message: message.text == "🧈 Рецепт")
async def recipe(message: types.Message):
    user_id = message.from_user.id
    from_action[user_id] = 1

    await message.answer("☎️Пожалуйста, поделитесь своим телефоном", reply_markup=share_keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def phone(message: types.Message):
    number = "+" + message.contact.phone_number

    user_id = Lib.get_user_by_phone(number)

    get = Lib.get_last_recipe_request(int(user_id))

    if from_action[message.from_user.id] == 1:
        await message.answer(get["cooking"], reply_markup=main_keyboard)
    else:
        await message.answer(get["products"], reply_markup=main_keyboard)


async def main():
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
