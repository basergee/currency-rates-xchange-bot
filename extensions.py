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
        # Для удобства пользователя делаем наименования валют не зависящими от
        # регистра букв
        base = base.lower()
        quote = quote.lower()

        if base not in currencies or quote not in currencies:
            raise APIException("Нет такой валюты")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Введите количество валюты")

        if amount <= 0:
            raise APIException("Введите положительное число")

        # Документация на API: https://exchangerate.host/#/#docs
        # API позволяет сразу получить интересующую нас сумму
        payload = {'from': currencies.get(base), 'to': currencies.get(quote),
                   'amount': amount}
        api_url = f'https://api.exchangerate.host/convert'

        try:
            response = requests.get(api_url, params=payload)
            # Проверим статус запроса, чтобы выявить ошибки, такие как '404'
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise APIException("Ошибка! Ответ сервера: " + e.response.reason)
        except requests.exceptions.ConnectionError:
            raise APIException("Ошибка соединения с сервером!")
        except requests.RequestException as e:
            raise APIException(e)
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


# Проверим работу функции отдельно от остальной программы
if __name__ == "__main__":
    tests = [
        ("долларЫ", "рубль", 100),
        ("доллар", "рублИ", 100),
        ("доллар", "рубль", -1),
        ("доллар", "рубль", 0),
        ("доллар", "рубль", 100),
        ("Доллар", "руБль", 100),
    ]

    for t in tests:
        try:
            print(Convertor.get_price(*t))
        except APIException as e:
            print(e)
