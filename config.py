from telebot import types

API = '6984372204:AAGtZfw8O1MYbyt-bE-Yh2InS2CUKU2ni-I'

USER_DATA_PATH = 'json/users_data.json'
GENRE_PATH = 'json/genres.json'
CHARACTERS_PATH = 'json/characters.json'
LOCATION_PATH = 'json/locations.json'

MARKUP_CALLBACK = types.InlineKeyboardMarkup()
MARKUP_CALLBACK.add(
    types.InlineKeyboardButton('⬅️Назад', callback_data='назад'),
    types.InlineKeyboardButton('✅Выбрать', callback_data='выбрать')
)

FOLDER_ID = ''