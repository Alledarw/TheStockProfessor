# Import the 'requests' library for making HTTP requests
import requests
import time


# Function to fetch insider trading data from an API
def getInsiderTradingData(api_key):
    # Define the API endpoint URL with the provided API key
    endpoint = f"https://financialmodelingprep.com/api/v4/insider-trading?symbol=&page=0&apikey={api_key}"

    # Make an HTTP GET request to the API endpoint
    response = requests.get(endpoint)

    # Pause for 1 second before processing the response
    time.sleep(1)

    # Parse the response JSON data into a Python dictionary
    insider_trading_data = response.json()

    # Return the insider trading data as a dictionary
    return insider_trading_data


# Function to filter insider trades data by specific company tickers
# Maybe this one isnt even needed
def filterInsiderTradesByCompany(trading_data, companies):
    # Create a list of insider trades where the 'symbol' matches one of the specified 'companies'
    filtered_trades = [trade for trade in trading_data if trade['symbol'] in companies]

    # Return the filtered insider trades as a list
    return filtered_trades


# Function to compare two trades and check if they have the same values
def trades_are_equal(trade1, trade2):
    return (
            trade1['symbol'] == trade2['symbol'] and
            trade1['price'] == trade2['price'] and
            trade1['reportingName'] == trade2['reportingName'] and
            trade1['typeOfOwner'] == trade2['typeOfOwner'] and
            trade1['securitiesTransacted'] == trade2['securitiesTransacted'] and
            trade1['filingDate'] == trade2['filingDate'] and
            trade1['acquistionOrDisposition'] == trade2['acquistionOrDisposition']
    )


# Function to generate SMS messages based on insider trading data
def generateInsideTradeSMS(trading_data):
    # Initialize an empty list to store SMS messages
    messages = []

    # Iterate through each insider trade in the provided data
    for trade in trading_data:
        # Extract relevant information from the trade
        ticker = trade['symbol']
        price = trade['price']
        name = trade['reportingName']
        typeOfOwner = trade['typeOfOwner']
        amountOfStocks = trade['securitiesTransacted']
        time = trade['filingDate']
        accordepp = trade['acquistionOrDisposition']

        # Create a formatted message with trade details
        message = '\u26A0\ufe0f <b>INSIDE TRADE</b> \u26A0\ufe0f'
        message += "\n\n" + ticker + " -  $" + str(price)
        message += "\n<b>Stocks transferred:</b> " + "<b>" + str(amountOfStocks) + "</b>"

        # Tell us if the ammount on stocks transferred were aqquired or dispotisioned
        message += "\n<b>Acquistion or disposition: </b>" + f"<b>{accordepp}</b>"

        # Add a line of dashes for separation
        message += "\n" + "-" * 33  # 33 dashes for separation

        message += "\n\nName: " + name
        message += "\nType of owner: " + typeOfOwner
        message += "\n\nFiling date: " + time

        # Define a GIF URL for the message
        gif_url = 'https://media.giphy.com/media/AgHBbekqDik0g/giphy.gif'

        # Append the formatted message and GIF URL as a tuple to the 'messages' list
        messages.append((message, gif_url))

    # Return the list of generated SMS messages
    # Note: You can uncomment the line below if you want to limit the messages to the 30 newest trades
    # latest_30_trades = messages[:30]
    return messages
