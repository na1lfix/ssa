import telebot
import requests
import os
from telebot import types

bot = telebot.TeleBot('7720459539:AAGkmjU3qJI4W9N2kbTYePLgkoy0DDQ1ctU')  # Замените на свой токен
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    search_button = types.KeyboardButton('Искать Игру')
    markup.add(search_button)
    bot.send_message(message.chat.id, "Привет! Нажмите 'Искать Игру', чтобы начать.", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Искать Игру':
            bot.send_message(message.chat.id, 'Введите название игры:')
        else:
            searchQuery = message.text.lower()  # Приводим поисковый запрос к нижнему регистру
            url = f"http://127.0.0.1:5000/search?query={searchQuery}"


            try:
                response = requests.get(url)
                response.raise_for_status()

                files = response.json().get('files', [])
                if not files:
                    bot.send_message(message.chat.id, 'Я ничего не нашел по вашему запросу.')
                else:
                    for file_path in files:
                        if os.path.exists(file_path):
                            with open(file_path, 'rb') as file_to_send:
                                bot.send_document(message.chat.id, file_to_send)
                        else:
                            bot.send_message(message.chat.id, f"Файл не найден: {file_path}")

            except requests.exceptions.RequestException as e:
                bot.send_message(message.chat.id, f"Произошла ошибка при выполнении запроса: {e}")
            except ValueError:
                bot.send_message(message.chat.id, "Ошибка декодирования ответа сервера.")


bot.polling(none_stop=True)
