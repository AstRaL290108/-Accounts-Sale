import configparser
setting = configparser.ConfigParser()
setting.read('config.ini')

#Параметры бота
token = setting["BOT_SETTING"]["token"]
admin_id = setting["BOT_SETTING"]["admin_id"]

#Параметры бaзы данных
password = setting["DATABASE_SETTING"]["password"]
user = setting["DATABASE_SETTING"]["user"]
host = setting["DATABASE_SETTING"]["host"]
database = setting["DATABASE_SETTING"]["database"]