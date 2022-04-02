"""
Главный модуль бота @CurrencyRatesXchange_bot

Здесь расположены работы с Telegram, функции-обработчики сообщений бота
"""

import telebot

import config
from extensions import Convertor
from extensions import APIException
from extensions import CURRENCIES


def main():
    bot.polling()


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = f"Здравствуйте, {message.from_user.first_name}\n\n" \
          f"Здесь Вы можете узнать цену на некоторые валюты, отправив " \
          f"сообщение с текстом:\n\n" \
          f"<имя валюты, цену которой хотите узнать> <имя валюты, в " \
          f"которой хотите узнать цену первой валюты> <количество первой " \
          f"валюты>.\n\nНапример, сообщение \"доллар рубль 100\" выведет" \
          f" цифру, которая показывает за сколько рублей можно купить 100 " \
          f"долларов по текущему курсу.\n\n" \
          f"Чтобы посмотреть список доступных валют введите команду /values"

    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['values'])
def send_values(message):
    msg = "Вам доступны следующие валюты:\n"
    for v in CURRENCIES.keys():
        msg += '- ' + v + '\n'

    bot.send_message(message.chat.id, msg)


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
        bot.reply_to(message, "Неправильная строка. Слишком много параметров")
        return
    if len(msg) < 3:
        bot.reply_to(message, "Неправильная строка. Слишком мало параметров")
        return

    try:
        # Сейчас msg содержит ровно 3 элемента. Передаем их все
        bot.reply_to(message, Convertor.get_price(*msg))
    except APIException as e:
        bot.reply_to(message, e)


if __name__ == "__main__":
    main()
