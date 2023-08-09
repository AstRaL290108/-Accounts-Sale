from aiogram import types
from aiogram.utils import executor
from bot import *

from handlers import *


commands.registration_handlers(dp)
other.registration_handlers(dp)
add_new_goods.registration_handlers(dp)
search.registration_handlers(dp)
view_goods.registration_handlers(dp)


if __name__ == "__main__":
	try:
		print("Бот запущен")
		executor.start_polling(dp)

	except Exception as e:
		print('Ошибка:\n\n', traceback.format_exc())