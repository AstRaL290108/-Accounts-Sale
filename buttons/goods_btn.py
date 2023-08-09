from aiogram import types

preview_btn = types.InlineKeyboardMarkup()
i1 = types.InlineKeyboardButton(text = "Подтвердить", callback_data = "confirm")
i2 = types.InlineKeyboardButton(text = "Отменить", callback_data = "disconfirm")
preview_btn.add(i1)
preview_btn.add(i2)

cansel_btn = types.InlineKeyboardMarkup()
i = types.InlineKeyboardButton(text = "❌Отменить", callback_data = "cansel")
cansel_btn.add(i)