import requests


def checkStockGrade(tickers, key):
    base_url = f"https://financialmodelingprep.com/api/v3/grade/{tickers}?limit=500&apikey={key}"

    response = requests.get(base_url)
    stock_grade_data = response.json()

    return stock_grade_data
