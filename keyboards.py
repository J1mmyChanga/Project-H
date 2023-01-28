from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(row_width=2) \
    .add(InlineKeyboardButton("🏪 Продукты")) \
    .add(InlineKeyboardButton("🧈 Рецепт"))


