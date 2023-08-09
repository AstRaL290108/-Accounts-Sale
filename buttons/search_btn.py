from aiogram import types

cansel = types.InlineKeyboardMarkup()
i = types.InlineKeyboardButton(text = "❌Отменить поиск", callback_data = "cansel")
cansel.add(i)