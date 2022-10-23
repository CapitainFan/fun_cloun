import random

from requests import ConnectionError, get
from telebot import TeleBot, types
from bs4 import BeautifulSoup


API_KEY = '5683812978:AAFPMVCHxY0ZZCnsObZ8h7FtA3cm-OhUhBw'
HOLIDAYS_URL = 'https://prazdnikisegodnya.ru'
USUAL_JOKES_URL = 'https://www.anekdot.ru/last/good/'

bot = TeleBot(API_KEY)


def holidays_parser(url):
    try:
        response = get(url)
    except ConnectionError:
        return 'Сетевая ошибка'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        holidays = soup.find_all('span')
        response = [c.text for c in holidays]
        return [response[i] for i in range(0, len(response))
                if response[i][0] == 'Д']

    return 'Ошибка на сервере'


def jokes_parser(url):
    try:
        response = get(url)
    except ConnectionError:
        return 'Сетевая ошибка'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        result = soup.find_all('div', class_='text')
        return [response.text for response in result]

    return 'Ошибка на сервере'


holidays = holidays_parser(HOLIDAYS_URL)
jokes = jokes_parser(USUAL_JOKES_URL)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('/holidays')
    item2 = types.KeyboardButton('/jokes')
    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     'This bot can perform some of Yarik\'s functions',
                     reply_markup=markup)


@bot.message_handler(commands=['holidays'])
def get_holidays(message):
    for i in range(0, 5):
        bot.send_message(message.chat.id, holidays[i])

    random.shuffle(holidays)


@bot.message_handler(commands=['jokes'])
def get_jokes(message):
    for i in range(0, 5):
        bot.send_message(message.chat.id, jokes[i])

    random.shuffle(jokes)


bot.polling()
