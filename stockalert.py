import requests
import datetime, time
from stocknews import getNewsData
from stockgradealert import checkStockGrade

# API KEY for financemodelingrep
API_KEY = 'API_KEY'

# Dictionary to store the last alert timestamps for each stock
last_alert_timestamps = {}

# Cooldown time in seconds (e.g., 1 hour = 3600 seconds)
cooldown_time = 21200  # 6h


# Function to get stock data from the API
def getStockData(tickers):
    base_url = "https://financialmodelingprep.com/api/v3/quote/"
    key = API_KEY

    stock_data = []
    tickers_list = tickers.split(",")  # Split tickers into a list

    for ticker in tickers_list:
        full_url = base_url + ticker + "?apikey=" + key
        r = requests.get(full_url)
        stock_data.extend(r.json())  # Extend the list with data for each ticker

        # Add a 1-second delay between requests
        time.sleep(1)

    return stock_data


# Function to generate SMS based on stock data for multiple companies
def generatePriceChangeSMS(data):
    messages = []

    for stock in data:
        symbol = stock['symbol']
        price = stock['price']
        changesPercentage = stock['changesPercentage']

        current_date = datetime.date.today()
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime('%H:%M')
        formatted_date = current_date.strftime('%m-%d')

        last_alert_timestamp = last_alert_timestamps.get(symbol, None)
        if (
                last_alert_timestamp is None
                or (datetime.datetime.now() - last_alert_timestamp).total_seconds() >= cooldown_time
        ):

            # Check if changesPercentage is not None and if it's less than -5
            if changesPercentage is not None and changesPercentage < -5:
                message = '\U0001F911 <b>PRICE DROP</b> \U0001F911'
                message += "\n\n" + symbol
                message += " - $" + str(price)
                message += "<b>\nPrice drop more than 5%! \u2193</b>"

                stock_grades = checkStockGrade(symbol, API_KEY)
                if stock_grades and len(stock_grades) > 0:
                    latest_stock_grade = stock_grades[0]
                    message += "\n" + "Latest rating: " + "<b>" + latest_stock_grade['newGrade'] + "</b>"
                    # message += "\n" + latest_stock_grade['symbol'] CHECK IF ITS THE GRADE FOR THE ACTUALL STOCK

                # Add a line of dashes for separation
                message += "\n" + "-" * 33  # 33 dashes for separation

                # Retrieve the latest news article for the stock
                stock_news = getNewsData(symbol)
                if stock_news and len(stock_news) > 0:
                    latest_article = stock_news[0]

                    # Include the link in the news header instead of printing the full link
                    message += f'\n\n<b><a href="{latest_article["url"]}">Latest News Article:</a></b>'
                    message += "\n" + "<i>" + latest_article['title'] + "</>"  # NEWS TITLE

                message += "\n\nTime stamp: " + str(formatted_date) + " " + str(formatted_time) + " UTC"

                gif_url = 'https://media.giphy.com/media/SWVF41fAxIrwIyUr8b/giphy.gif'
                messages.append((message, gif_url))

                # Update the last alert timestamp for this stock
                last_alert_timestamps[symbol] = datetime.datetime.now()

            elif changesPercentage is not None and changesPercentage > 5:
                message = '📈 <b>PRICE INCREASE</b> 📈'
                message += "\n\n" + symbol
                message += " - $" + str(price)
                message += "<b>\nPrice increase more than 5%! \u2191</b>"

                # Get latest stock rating for the specific stock
                stock_grades = checkStockGrade(symbol, API_KEY)
                if stock_grades and len(stock_grades) > 0:
                    latest_stock_grade = stock_grades[0]
                    message += "\n" + "Latest rating: " + "<b>" + latest_stock_grade['newGrade'] + "</b>"
                    # message += "\n" + latest_stock_grade['symbol'] CHECK IF ITS THE GRADE FOR THE ACTUALL STOCK

                # Add a line of dashes for separation
                message += "\n" + "-" * 33  # 33 dashes for separation

                # Retrieve the latest news article for the stock
                stock_news = getNewsData(symbol)
                if stock_news and len(stock_news) > 0:
                    latest_article = stock_news[0]

                    # Include the link in the news header instead of printing the full link
                    message += f'\n\n<b><a href="{latest_article["url"]}">Latest News Article:</a></b>'
                    message += "\n" + "<i>" + latest_article['title'] + "</>"  # NEWS TITLE

                # Add UTC because thats the time zone where the server is located
                message += "\n\nTime stamp: " + str(formatted_date) + " " + str(formatted_time) + " UTC"

                gif_url = 'https://media.giphy.com/media/bMycGOQLESDCEnLNUz/giphy.gif'
                messages.append((message, gif_url))

                # Update the last alert timestamp for this stock
                last_alert_timestamps[symbol] = datetime.datetime.now()

            else:
                print('No price change registered')

    return messages
