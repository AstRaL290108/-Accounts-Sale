from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from messages import *
from buttons import goods_btn

from bin.state import *
from bot import *


async def new_goods(msg: types.Message):
	chat_id = msg.chat.id
	goods = db.select({'table': 'goods', 'type': 'all'})[0:11]
	
	keyboard = types.InlineKeyboardMarkup()
	for item in goods:
		keyboard.add(types.InlineKeyboardButton(text = f"{item['title']} ➖ {item['price']}руб.", callback_data = f"view-{item['id']}"))

	await bot.send_message(chat_id, goods_msg.new_goods_msg, reply_markup = keyboard)


async def Favorites(msg: types.Message):
	chat_id = msg.chat.id

	user = db.select({'type': 'one', 'table': 'users', 'user_id': chat_id})
	if user['favorites'] == "":
		await bot.send_message(chat_id, main_msg.nothing)
	else:
		favorites = user['favorites'].split("&")
		keyboard = types.InlineKeyboardMarkup()
		for i in favorites:
			item = db.select({'table': 'goods', 'type': 'one', 'id': i})
			keyboard.add(types.InlineKeyboardButton(text = f"{item['title']} ➖ {item['price']}руб.", callback_data = f"view-{item['id']}"))

		keyboard.add(types.InlineKeyboardButton(text = "🆑Очистить корзину", callback_data = "clear_favorites"))
		await bot.send_message(chat_id, goods_msg.favorite_goods, reply_markup = keyboard)



async def view_good_path(call: types.CallbackQuery):
	chat_id = call.message.chat.id
	move = call.data.split("-")

	#Удалить одно объявление
	if move[0] == "delete":
		db.delete({'table': 'goods', 'id': move[1]})

		await bot.send_message(chat_id, goods_msg.was_delete_msg)


	# Просмотр одного товара
	if move[0] == "view":
		goods = db.select({'type': 'one', 'table': 'goods', 'id': move[1]})
		resp = f"""<b>{goods['title']}</b>
<u>Описание</u>: <i>{goods['description']}</i>

<u>Цена: {goods['price']}руб.</u>

""" 

		user = db.select({'type': 'one', 'table': 'users', 'user_id': chat_id})
		favorites = user['favorites'].split("&")

		keyboard = types.InlineKeyboardMarkup()
		i1 = types.InlineKeyboardButton(text = "💰Купить", callback_data = f"buy-{goods['id']}")
		i2 = types.InlineKeyboardButton(text = "🗑Добавить в корзину", callback_data = f"fav-{goods['id']}")
		i3 = types.InlineKeyboardButton(text = "❌Убрать из корзины", callback_data = f"del-{goods['id']}")

		i5 = types.InlineKeyboardButton(text = "❌Удалить объявление", callback_data = f"delete-{goods['id']}")

		if goods['user_id'] != chat_id:
			keyboard.add(i1)
			for i in favorites:
				if i == str(goods['id']):
					keyboard.add(i3)
					break
			else:
				keyboard.add(i2)
		else:
			keyboard.add(i5)


		file = open(f"bin/image/{goods['image']}", "rb")
		await bot.send_photo(chat_id, file, caption = resp, parse_mode = pm, reply_markup = keyboard)
		file.close()

	# Добавить товар в корзину
	if move[0] == "fav":
		user = db.select({'type': 'one', 'table': 'users', 'user_id': chat_id})
		if user['favorites'] == "":
			db.update({
				'table': 'users', 
				'colamns': {
					'favorites': move[1]
				},
				'where': {
					'user_id': chat_id
				}
			})
			await bot.send_message(chat_id, goods_add)
		else:
			good = True
			for i in user['favorites'].split("&"):
				if i == move[1]:
					good = False

			if good:
				db.update({
					'table': 'users', 
					'colamns': {
						'favorites': f"{user['favorites']}&{move[1]}"
					},
					'where': {
						'user_id': chat_id
					}
				})

				await bot.send_message(chat_id, goods_add)
			else:
				await bot.send_message(chat_id, goods_add_last)


	# Удалить один товар из корзины
	if move[0] == "del":
		goods_id = move[1]

		user = db.select({'type': 'one', 'table': 'users', 'user_id': chat_id})
		favorites = user['favorites'].split("&")

		for i in favorites:
			if i == goods_id:
				favorites.remove(i)

		new = ""
		for i in favorites:
			if new == "":
				new += i
			else:
				new += f"&{i}"

		db.update({'table':'users','colamns':{'favorites':new},'where':{'user_id':chat_id}})

		await bot.send_message(chat_id, goods_del)


def registration_handlers(dp: Dispatcher):
	dp.register_message_handler(Favorites, text = "🗑Корзина", state = None)
	dp.register_message_handler(new_goods, text = "🆕Новые объявления", state = None)

	dp.register_callback_query_handler(view_good_path, lambda c: c.data, state = None)