from config import *
import telebot
from json_funcs import *
from telebot import types

bot = telebot.TeleBot(API)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_data = get_json_data(USER_DATA_PATH)
    user_data[user_id] = {'genre': '', 'character': '',
                          'location': '', 'msg': '',
                          'reply': {
                              'function_back': '',
                              'function_next': ''
                              }
                          }
    bot.send_message(user_id, 'start')
    save_json_data(user_data, USER_DATA_PATH)

@bot.message_handler(commands=['begin'])
def pick_genre(message):
    user_id = message.chat.id
    genres = get_json_data(GENRE_PATH)
    user_data = get_json_data(USER_DATA_PATH)
    msg = user_data[str(user_id)]['msg']
    text = 'Выберите жанр'
    markup = types.InlineKeyboardMarkup()
    for genre in genres:
        markup.add(
            types.InlineKeyboardButton(genre, callback_data=str(genre))
        )
    if not msg:
        msg = bot.send_message(user_id, text=text, reply_markup=markup)
        user_data[str(user_id)]['msg'] = msg.id
        user_data[str(user_id)]['reply']['function_back'] = "pick_genre"
        user_data[str(user_id)]['reply']['function_next'] = "pick_character"
    else:
        bot.edit_message_text(message_id=msg, chat_id=user_id,
                              reply_markup=markup, text=text)
    save_json_data(user_data, USER_DATA_PATH)

def pick_character(user_id):
    characters = get_json_data(CHARACTERS_PATH)
    user_data = get_json_data(USER_DATA_PATH)
    msg = user_data[str(user_id)]['msg']
    markup = types.InlineKeyboardMarkup()
    for character in characters:
        markup.add(
            types.InlineKeyboardButton(character, callback_data=str(character))
        )
    user_data[str(user_id)]['reply']['function_back'] = "pick_character"
    user_data[str(user_id)]['reply']['function_next'] = "pick_location"
    bot.edit_message_text(message_id=msg, chat_id=user_id,
                          reply_markup=markup, text='Выберите персонажа')
    save_json_data(user_data, USER_DATA_PATH)

def pick_location(user_id):
    locations = get_json_data(LOCATION_PATH)
    user_data = get_json_data(USER_DATA_PATH)
    msg = user_data[str(user_id)]['msg']
    markup = types.InlineKeyboardMarkup()
    for location in locations:
        markup.add(
            types.InlineKeyboardButton(location, callback_data=str(location))
        )
    user_data[str(user_id)]['reply']['function_back'] = "pick_location"
    user_data[str(user_id)]['reply']['function_next'] = ""
    bot.edit_message_text(message_id=msg, chat_id=user_id,
                          reply_markup=markup, text='Выберите локацию')
    save_json_data(user_data, USER_DATA_PATH)






@bot.callback_query_handler(func = lambda call: True)
def call_back(call):
    user_id = call.message.chat.id
    user_data = get_json_data(USER_DATA_PATH)
    msg = user_data[str(user_id)]['msg']
    genres = get_json_data(GENRE_PATH)
    characters = get_json_data(CHARACTERS_PATH)
    locations = get_json_data(LOCATION_PATH)
    if call.data in genres:
        genre = call.data
        user_data[str(user_id)]['genre'] = str(genre)
        bot.edit_message_text(message_id=msg, chat_id=user_id,
                              reply_markup=MARKUP_CALLBACK, text=f'{genre}\n'
                                                                 f'{genres[genre]}')
        save_json_data(user_data, USER_DATA_PATH)
    elif call.data in characters:
        character = call.data
        user_data[str(user_id)]['character'] = character
        bot.edit_message_text(message_id=msg, chat_id=user_id,
                              reply_markup=MARKUP_CALLBACK, text=f'{character}\n'
                                                                 f'{characters[character]}')
        save_json_data(user_data, USER_DATA_PATH)
    elif call.data in locations:
        location = call.data
        user_data[str(user_id)]['location'] = location
        bot.edit_message_text(message_id=msg, chat_id=user_id,
                              reply_markup=MARKUP_CALLBACK, text=f'{location}\n'
                                                                 f'{locations[location]}')
        save_json_data(user_data, USER_DATA_PATH)

    elif call.data == 'назад':
        function = user_data[str(user_id)]['reply']['function_back']
        eval(f'{function}({user_id})')
    elif call.data == 'выбрать':
        function = user_data[str(user_id)]['reply']['function_next']
        eval(f'{function}({user_id})')

if __name__ == '__main__':
    bot.polling()