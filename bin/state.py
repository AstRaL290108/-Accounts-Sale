from aiogram.dispatcher.filters.state import StatesGroup, State

class AddNewGoods(StatesGroup):
	get_title = State()
	get_description = State()
	get_price = State()
	get_image = State()
	confirm = State()


class Search(StatesGroup):
	on_search = State()