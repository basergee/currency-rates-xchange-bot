"""
Здесь расположены классы работы с API сервера, классы исключений и т.п.
"""

import requests


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        api_request = f'https://api.exchangerate.host/convert?from={base}&to={quote}'
        response = requests.get(api_request)

        data = response.json()
        return amount * data['info']['rate']


# Проверим работу функции отдельно от остальной программы
if __name__ == "__main__":
    print(Convertor.get_price("USD", "RUB", 45))
