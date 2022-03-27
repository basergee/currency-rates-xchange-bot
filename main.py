"""
Главный модуль бота @CurrencyRatesXchange_bot

Здесь расположены работы с Telegram, функции-обработчики сообщений бота
"""

import telebot

import config


def main():
    bot.polling()


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет")


if __name__ == "__main__":
    main()
