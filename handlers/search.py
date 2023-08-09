from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from messages import search_msg
from buttons import search_btn

from bin.state import *
from bot import *


async def start_search(msg: types.Message, state: FSMContext):
	chat_id = msg.chat.id

	await bot.send_message(chat_id, search_msg.start_search, reply_markup = search_btn.cansel)
	await Search.on_search.set()


async def main_search(msg: types.Message, state: FSMContext):
	chat_id = msg.chat.id
	text = msg.text.lower()

	text = text.replace(",", "").replace("/", "").replace(".", "").replace(":", "").replace(";", "").replace("!", "").replace("'", "").replace('"', "")
	key_words = text.split(" ")
	exit = []
	asd = 0

	all_announcements = db.select({'type': 'all', 'table': 'goods'})
	#По названию
	for i in all_announcements:
		title = i['title'].lower()
		title = title.replace(",", "").replace("/", "").replace(".", "").replace(":", "").replace(";", "").replace("!", "").replace("'", "").replace('"', "")
		title = title.split(" ")
		asd = 1

		if len(title) >= len(key_words):
			for item in title:
				if asd == 1:
					for e in key_words:
						if item == e:
							exit.append(i)
							asd = 0


		if len(title) < len(key_words):
			for item in key_words:
				if asd == 1:
					for e in title:
						if item == e:
							exit.append(i)
							asd = 0

	#По описанию
	# for i in all_announcements:
	# 	title = i['description'].lower()
	# 	title = title.replace(",", "").replace("/", "").replace(".", "").replace(":", "").replace(";", "").replace("!", "").replace("'", "").replace('"', "")
	# 	title = title.split(" ")
	# 	asd = 1

	# 	if len(title) >= len(key_words):
	# 		for item in title:
	# 			if asd == 1:
	# 				for e in key_words:
	# 					if item == e:
	# 						exit.append(i)
	# 						asd = 0


	# 	if len(title) < len(key_words):
	# 		for item in key_words:
	# 			if asd == 1:
	# 				for e in title:
	# 					if item == e:
	# 						exit.append(i)
	# 						asd = 0



	if str(exit) == "[]":
		await bot.send_message(chat_id, search_msg.nothing)
		await state.finish()

	else:
		keyboard = types.InlineKeyboardMarkup()
		for item in exit:
			keyboard.add(types.InlineKeyboardButton(text = f"{item['title']} ➖ {item['price']}руб.", callback_data = f"view-{item['id']}"))

		await bot.send_message(chat_id, search_msg.exit.format(request = text), reply_markup = keyboard)
		await state.finish()


def registration_handlers(dp: Dispatcher):
	dp.register_message_handler(start_search, text = "🔎Поиск", state = None)
	dp.register_message_handler(main_search, content_types = ["text"], state = Search.on_search)