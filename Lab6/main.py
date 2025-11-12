import requests
import logging

type Result = dict[str, float]

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def log_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
    return wrapper

@log_errors
def get_currencies(currency_codes: list[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Result:
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Ошибка выполнения запроса к API")

    try:
        data = response.json()
    except ValueError:
        raise Exception("Ошибка выполнения запроса к API")

    if 'Valute' not in data:
        raise Exception("В ответе не содержатся курсы валют")
    
    valutes = data['Valute']

    result: Result = {}
    
    for code in currency_codes:
        if code not in valutes:
            raise Exception("В словаре не существует валюты '{}'".format(code))

        result[code] = valutes[code]['Value']
    return result

if __name__ == '__main__':
    print(get_currencies(['USD', 'EUR', 'GBP']))
