"""
Здесь расположены классы работы с API сервера, классы исключений и т.п.
"""

import requests
import json


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        # Документация на API: https://exchangerate.host/#/#docs
        # API позволяет сразу получить интересующую нас сумму
        payload = {'from': base, 'to': quote, 'amount': amount}
        api_url = f'https://api.exchangerate.host/convert'
        response = requests.get(api_url, params=payload)

        # Можно вызвать response.json(), но в задании указано, что надо
        # использовать библиотеку JSON, поэтому делаем так
        data = json.loads(response.text)

        # API не выдает ошибку, но в случае неудачной конверсии, результат
        # будет None
        result = data['result']
        if result is None:
            raise APIException("Неправильная валюта")
        return result


# Проверим работу функции отдельно от остальной программы
if __name__ == "__main__":
    print(Convertor.get_price("USD", "RUB", 45))
