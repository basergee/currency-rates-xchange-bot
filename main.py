"""
Главный модуль бота @CurrencyRatesXchange_bot

Здесь расположены работы с Telegram, функции-обработчики сообщений бота
"""

import telebot

import config
from extensions import Convertor
from extensions import APIException


def main():
    bot.polling()


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет")


# Функция реагирует на обычные сообщения. Предполагается, что каждое сообщение
# боту -- это запрос на преобразование валюты. Такой запрос состоит из трех
# частей:
#
# <имя валюты, цену которой требуется узнать>
# <имя валюты, в которой надо узнать цену первой валюты>
# <количество первой валюты>.
#
# Части разделяет один или несколько пробелов.
# Например: сообщение "доллар рубль 100" должна вывести цифру, которая
# показывает за сколько рублей можно купить 100 долларов по текущему курсу.
@bot.message_handler(content_types=['text'])
def make_conversion(message):
    # проверить, что сообщение соответствует критерию: два слова и одно число
    msg = message.text.split()
    if len(msg) > 3:
        bot.reply_to(message, "Неправильная строка. Слишком много слов")
        return
    if len(msg) < 3:
        bot.reply_to(message, "Неправильная строка. Слишком мало слов")
        return

    try:
        # Сейчас msg содержит ровно 3 элемента. Передаем их все
        bot.reply_to(message, Convertor.get_price(*msg))
    except APIException as e:
        bot.reply_to(message, e)


if __name__ == "__main__":
    main()
