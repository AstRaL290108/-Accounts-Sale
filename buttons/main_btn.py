from aiogram import types

main_menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
i1 = types.KeyboardButton("🗑Корзина")
i2 = types.KeyboardButton("🔎Поиск")
i3 = types.KeyboardButton("🔮Мои объявления")
main_menu.add(i1, i2, i3)

i4 = types.KeyboardButton("🆕Новые объявления")
i5 = types.KeyboardButton("👤Профиль")
main_menu.add(i4, i5)

profile = types.InlineKeyboardMarkup()
i1 = types.InlineKeyboardButton(text = "📬Реферальный кабинет", callback_data = "referal")
i2 = types.InlineKeyboardButton(text = "⬇️Пополнить баланс", callback_data = "add_money")
i3 = types.InlineKeyboardButton(text = "⬆️Вывести деньги", callback_data = "del_money")
profile.add(i1)
profile.add(i2)
profile.add(i3)