from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from messages import *
from buttons import *

from bin.state import *
from bot import *


async def Start(msg: types.Message, state: FSMContext):
	chat_id = msg.chat.id
	user = db.select({'type': 'one', 'table': 'users', 'user_id': chat_id})

	await bot.send_sticker(chat_id, main_msg.hello_sticker)
	if user is None:
		if len(msg.text.split(" ")) != 1:
			r = msg.text.split(" ")
			friend_id = int(r[1])

			friend = db.select({'type': 'one', 'table': 'users', 'user_id': friend_id})
			db.update({'table': 'users', 'colamns': {'referals': friend['referals'] + 1}, 'where': {'user_id': friend_id}})

		else:
			friend_id = 0

		db.insert_into({
			'table': 'users', 
			'user_id': chat_id,
			'username': str(msg.chat.username),
			'full_name': str(msg.chat.full_name),
			'favorites': '',
			'money': 0,
			'max_input': 0,
			'max_output': 0,
			'trades': 0,
			'friend_id': friend_id,
			'referals': 0
		})

		await bot.send_message(chat_id, main_msg.hello_new_msg, reply_markup = main_btn.main_menu)

	else:
		await bot.send_message(chat_id, main_msg.hello_old_msg, reply_markup = main_btn.main_menu)



def registration_handlers(dp: Dispatcher):
	dp.register_message_handler(Start, commands = ["start"], state = None)