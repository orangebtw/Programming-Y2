import requests

def fetch_currencies():
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    if response.status_code != 200:
        raise Exception("Ошибка выполнения запроса к API")
    try:
        data = response.json()
    except ValueError:
        raise Exception("Ошибка выполнения запроса к API")

    valutes = data['Valute']
    result: list[dict] = []

    for v in valutes:
        result.append(valutes[v])

    return result
