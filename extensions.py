"""
Здесь расположены классы работы с API сервера, классы исключений и т.п.
"""

import requests
import json


currencies = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        if base not in currencies or quote not in currencies:
            raise APIException("Нет такой валюты")
        if amount <= 0:
            raise APIException("Введите положительное число")

        # Документация на API: https://exchangerate.host/#/#docs
        # API позволяет сразу получить интересующую нас сумму
        payload = {'from': currencies.get(base), 'to': currencies.get(quote),
                   'amount': amount}
        api_url = f'https://api.exchangerate.host/convert'

        # response = None
        try:
            response = requests.get(api_url, params=payload)
        except requests.exceptions.ConnectionError as e:
            print("Connection error! ", e)
        except requests.RequestException as e:
            print("Some error! ", e)
        else:
            # Можно вызвать response.json(), но в задании указано, что надо
            # использовать библиотеку JSON, поэтому делаем так
            data = json.loads(response.text)

            # API не выдает ошибку, но в случае неудачной конверсии, результат
            # будет None
            print(data)
            result = data['result']
            if result is None:
                raise APIException("Сервер не смог выполнить преобразование")
            return result

        return -1


# Проверим работу функции отдельно от остальной программы
if __name__ == "__main__":
    tests = [
        ("долларЫ", "рубль", 100),
        ("доллар", "рублИ", 100),
        ("доллар", "рубль", -1),
        ("доллар", "рубль", 0),
        ("доллар", "рубль", 100),
    ]

    for t in tests:
        try:
            print(Convertor.get_price(*t))
        except APIException as e:
            print(e)
