from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
import os

from messages import goods_msg, main_msg
from buttons import goods_btn

from bin.state import *
from bot import *


# Начинаем обзор и запрашиваем название
async def start_add(call: types.CallbackQuery, state: FSMContext):
	chat_id = call.message.chat.id

	await AddNewGoods.get_title.set()
	await bot.send_message(chat_id, goods_msg.start_add_msg, parse_mode = pm, reply_markup = goods_btn.cansel_btn)


# Получаем название и запрашиваем описание
async def get_data_send_description(msg: types.Message, state: FSMContext):
	chat_id = msg.chat.id

	await state.set_data({'title': msg.text})

	await AddNewGoods.get_description.set()
	await bot.send_message(chat_id, goods_msg.get_description, parse_mode = pm, reply_markup = goods_btn.cansel_btn)	


# Получаем описание и запрашиваем цену
async def get_description_send_price(msg: types.Message, state: FSMContext):
	chat_id = msg.chat.id

	await state.update_data({'description': msg.text})

	await AddNewGoods.get_price.set()
	await bot.send_message(chat_id, goods_msg.get_price, parse_mode = pm, reply_markup = goods_btn.cansel_btn)


# Получаем цену и запрашиваем превью
async def get_price_send_preview(msg: types.Message, state: FSMContext):
	chat_id = msg.chat.id

	try:
		await state.update_data({'price': int(msg.text)})

		await AddNewGoods.get_image.set()
		await bot.send_message(chat_id, goods_msg.get_image, parse_mode = pm, reply_markup = goods_btn.cansel_btn)

	except ValueError:
		await bot.send_message(chat_id, goods_msg.fail_price, parse_mode = pm, reply_markup = goods_btn.cansel_btn)


# Получаем превью
async def get_preview(msg: types.Message, state: FSMContext):
	chat_id = msg.chat.id
	data = await state.get_data()

	await state.update_data({'image': msg.document.file_name})

	await msg.document.download(f"./bin/image/{msg.document.file_name}")

	preview = f"""<b>{data['title']}</b>

<u>Описание:</u> {data['description']} 

<u>{data['price']}</u>
	"""
	await AddNewGoods.confirm.set()

	await bot.send_message(chat_id, goods_msg.goods_preview, parse_mode = pm, reply_markup = goods_btn.preview_btn)

	file = open(f"bin/image/{msg.document.file_name}", "rb")
	await bot.send_photo(chat_id, file, caption = preview, parse_mode = pm)
	file.close()
	

# Подтверждение
async def confirm(call: types.CallbackQuery, state: FSMContext):
	chat_id = call.message.chat.id
	data = await state.get_data()

	db.insert_into({
		'table': 'goods', 
		'user_id': chat_id,
		'image': data['image'],
		'title': data['title'],
		'description': data['description'],
		'price': data['price']
	})

	await state.finish()
	await bot.send_message(chat_id, goods_msg.confirm_msg, parse_mode = pm)


# Неподтверждение
async def disconfirm(call: types.CallbackQuery, state: FSMContext):
	chat_id = call.message.chat.id
	data = await state.get_data()

	await state.finish()
	await bot.send_message(chat_id, goods_msg.disconfirm_msg, parse_mode = pm)



# Мои товары
async def my_goods(msg: types.Message):
	chat_id = msg.chat.id
	my_goods = db.select({'table': 'goods', 'type': 'many', 'user_id': chat_id})

	if my_goods is None:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text = f"➕Добавить объявление", callback_data = "start_add_goods"))
		await bot.send_message(chat_id, main_msg.nothing, reply_markup = keyboard)
	else:
		keyboard = types.InlineKeyboardMarkup()
		for item in my_goods:
			keyboard.add(types.InlineKeyboardButton(text = f"{item['title']} ➖ {item['price']}руб.", callback_data = f"view-{item['id']}"))

		keyboard.add(types.InlineKeyboardButton(text = "🆑Удалить все объявление", callback_data = "clear_my_goods"))	
		keyboard.add(types.InlineKeyboardButton(text = f"➕Добавить объявление", callback_data = "start_add_goods"))
		await bot.send_message(chat_id, goods_msg.favorite_goods, reply_markup = keyboard)


# Удалить все объявления
async def clear_my_goods(call: types.CallbackQuery):
	chat_id = call.message.chat.id
	my_goods = db.select({'table': 'goods', 'type': 'many', 'user_id': chat_id})
	for i in my_goods:
		os.remove(f"./bin/image/{i['image']}")

	db.delete({'table': 'goods', 'user_id': chat_id})

	await bot.send_message(chat_id, goods_msg.clear_my_goods)


def registration_handlers(dp: Dispatcher):
	dp.register_message_handler(get_data_send_description, content_types = ["text"], state = AddNewGoods.get_title)
	dp.register_message_handler(get_description_send_price, content_types = ["text"], state = AddNewGoods.get_description)
	dp.register_message_handler(get_price_send_preview, content_types = ["text"], state = AddNewGoods.get_price)

	dp.register_message_handler(get_preview, content_types = ["document", "photo"], state = AddNewGoods.get_image)

	dp.register_callback_query_handler(clear_my_goods, lambda c: c.data == "clear_my_goods", state = None)
	dp.register_callback_query_handler(start_add, lambda c: c.data == "start_add_goods", state = None)
	dp.register_message_handler(my_goods, text = "🔮Мои объявления", state = None)

	dp.register_callback_query_handler(confirm, lambda c: c.data == "confirm", state = AddNewGoods.confirm)
	dp.register_callback_query_handler(disconfirm, lambda c: c.data == "disconfirm", state = AddNewGoods.confirm)