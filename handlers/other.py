from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from messages import *
from buttons import *

from bin.state import *
from bot import *


async def referal (call: types.CallbackQuery):
	chat_id = call.message.chat.id
	link = f"https://t.me/accounts_sale_bot?start={chat_id}"

	await bot.send_message(chat_id, main_msg.referal.format(link = link), parse_mode = pm)

async def clear_favorites(call: types.CallbackQuery):
	chat_id = call.message.chat.id
	db.update({
		'table': 'users', 
		'colamns': {
			'favorites': ''
		},
		'where': {
			'user_id': chat_id
		}
	})

	await bot.send_message(chat_id, main_msg.favorite_was_clear)


async def Profile(msg: types.Message):
	chat_id = msg.chat.id
	user = db.select({'type': 'one', 'table': 'users', 'user_id': chat_id})

	favorites = len(user['favorites'].split(" "))
	if user['favorites'] == "":
		favorites = 0

	resp = f"""
<b>#️⃣Ваш Telegram ID - {user['user_id']}</b>

🗑Товаров в корзине: {favorites}
💵Денег на счету: {user['money']}
📝Человек приглашено: {user['referals']}

⬇️Всего положено денег: {user['max_input']}
⬆️Всего выведено денег: {user['max_output']}
🤝Сделок совершено: {user['trades']}
""" 

	await bot.send_message(chat_id, resp, parse_mode = pm, reply_markup = main_btn.profile)
	

async def cansel_add(call: types.CallbackQuery, state: FSMContext):
	chat_id = call.message.chat.id
	await state.finish()

	await bot.send_message(chat_id, goods_msg.cansel_msg, parse_mode = pm)

async def cansel_search(call: types.CallbackQuery, state: FSMContext):
	chat_id = call.message.chat.id
	await state.finish()

	await bot.send_message(chat_id, search_msg.cansel_msg, parse_mode = pm)


def registration_handlers(dp: Dispatcher):
	dp.register_message_handler(Profile, text = "👤Профиль", state = None)
	dp.register_callback_query_handler(cansel_add, lambda c: c.data == "cansel", state = AddNewGoods)
	dp.register_callback_query_handler(cansel_search, lambda c: c.data == "cansel", state = Search)

	dp.register_callback_query_handler(clear_favorites, lambda c: c.data == "clear_favorites", state = None)
	dp.register_callback_query_handler(referal, lambda c: c.data == "referal", state = None)