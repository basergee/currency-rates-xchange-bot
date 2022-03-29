"""
Здесь расположены классы работы с API сервера, классы исключений и т.п.
"""

import requests
import json


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        api_request = f'https://api.exchangerate.host/convert?from={base}&to={quote}'
        response = requests.get(api_request)

        # Можно вызвать response.json(), но в задании указано, что надо
        # использовать библиотеку JSON, поэтому делаем так
        data = json.loads(response.text)
        return amount * data['info']['rate']


# Проверим работу функции отдельно от остальной программы
if __name__ == "__main__":
    print(Convertor.get_price("USD", "RUB", 45))
