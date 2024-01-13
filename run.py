import time
import telebot
from timeloop import Timeloop
from datetime import timedelta, datetime
import datetime
from insidetradingalert import getInsiderTradingData, generateInsideTradeSMS, filterInsiderTradesByCompany, \
    trades_are_equal
from stockalert import getStockData, generatePriceChangeSMS
from dailystocktips import getDailyTip
import csv

# API_KEY from  financialmodelingprep.com
API_KEY = 'API_KEY'

# Your Telegram Bot Token and Channel ID
TOKEN = "API_KEY"
CHANNEL_ID = -0000000
# If you're sending bulk notifications to multiple users, the API will not allow more than 30
# messages per second or so. Consider spreading out notifications over large intervals of 8—12 hours for best results.

# Company stock ticker(s) you want to monitor
all_company_tickers = []

# tickers.csv contains the biggest 100 stock companies in the world
# use row[2] to get the tickers from the csv file. (It contains more than just the tickers
with open('tickers.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        all_company_tickers.append(row[2])

# Optionally, close the file
file.close()

# First value is the title name (Symbol)
biggest_company_tickers = all_company_tickers[1:501]
print(biggest_company_tickers)
print(len(biggest_company_tickers))

# Initialize the Telegram Bot
bot = telebot.TeleBot(TOKEN, parse_mode=None)


# Function to send messages via Telegram
def sendMessage(messages):
    # If you remove the if statement without any replacement logic, the sendMessage function will still be called
    # with an empty list, but it won't send any messages to Telegram because there are no messages in the list. In
    # other words, the function will be executed, but it won't result in any messages being sent. Adding the if
    # statement is a way to prevent the function from sending messages if there are none to send, which can be
    # helpful to avoid unnecessary API calls and improve code efficiency.
    if messages:  # Check if the messages list is not empty
        for message, gif_url in messages:
            bot.send_animation(chat_id=CHANNEL_ID, animation=gif_url, caption=message, parse_mode='HTML')

            # Prevent to many requests to telegram API
            time.sleep(5)
    else:
        print('No messages to send')  # Print a message if there are no messages to send


# Check stock price every 60 seconds
tl = Timeloop()

# Save all trades here
processed_trades = []


# Define a scheduled job to run every 3 min using Timeloop
@tl.job(interval=timedelta(seconds=180))
def run_stock_alert_tasks():
    # Check if it's a weekend (Saturday or Sunday)
    current_day = datetime.datetime.now().weekday()
    if current_day in [5, 6]:  # 5 is Saturday, 6 is Sunday
        print('Weekend pause, skipping stock alert task')
        return  # Skip the task on weekends

    print('running task 1')
    real_time_data = getStockData(','.join(biggest_company_tickers))
    textMessages = generatePriceChangeSMS(real_time_data)
    sendMessage(textMessages)

    # Add this to not over-work the CPU. Let the program rest
    # https://raspberrypi.stackexchange.com/questions/8077/how-can-i-lower-the-usage-of-cpu-for-this-python-program
    time.sleep(5)


# Define a scheduled job to run every 5 min using Timeloop
@tl.job(interval=timedelta(seconds=300))
def run_inside_trade_alert_tasks():
    # Check if it's a weekend (Saturday or Sunday)
    current_day = datetime.datetime.now().weekday()
    if current_day in [5, 6]:  # 5 is Saturday, 6 is Sunday
        print('Weekend pause, skipping inside trade alert task')
        return  # Skip the task on weekends

    print('running task 2')

    # Filter the insider trades data to include only specific company tickers
    insiderTradingData = getInsiderTradingData(API_KEY)

    # Filter the insider trades data to include only specific company tickers
    filteredTrades = filterInsiderTradesByCompany(insiderTradingData, biggest_company_tickers)

    # Initialize an empty list to store new trades
    new_trades = []

    # Iterate through each trade in the filtered insider trades data
    for trade in filteredTrades:
        # Check if there is a trade in processed_trades that is equal to the current trade (from filtered trades)
        if not any(trades_are_equal(trade, processed_trade) for processed_trade in processed_trades):
            # If it's a new trade, add it to the new_trades list
            new_trades.append(trade)

            # THIS CODE IS THE SAME AS ABOVE BUT MORE CLEAR
            # # Initialize a flag to check if the current trade is already processed
            # trade_is_new = True
            #
            # # Iterate through each trade in processed_trades to check for equality
            # for processed_trade in processed_trades:
            #     # Check if the current trade is equal to the processed trade
            #     if trades_are_equal(trade, processed_trade):
            #         # If a match is found, set the flag to False, indicating it's not a new trade
            #         trade_is_new = False
            #         break  # Exit the loop since we found a match
            #
            # # Check if the trade is new (not found in processed_trades)
            # if trade_is_new:
            #     If it's a new trade, add it to the new_trades list
            #     new_trades.append(trade)

    if new_trades:
        # Generate SMS messages for the new insider trades
        latestTrades = generateInsideTradeSMS(new_trades)

        # Send the generated SMS messages for the new trades
        sendMessage(latestTrades)

        # Add the new trades to the processed_trades list
        processed_trades.extend(new_trades)

    else:
        # If there are no new trades, print a message
        print('No new trades')

    # Testing purposes
    # print(processed_trades)

    # Add this to not over-work the CPU. Let the program rest
    # https://raspberrypi.stackexchange.com/questions/8077/how-can-i-lower-the-usage-of-cpu-for-this-python-program
    time.sleep(5)


# Define a scheduled job to run couple of times a day using Timeloop
@tl.job(interval=timedelta(seconds=31500))
def run_stock_tips_tasks():
    sendMessage(getDailyTip())


# Start the Timeloop
tl.start(block=True)

