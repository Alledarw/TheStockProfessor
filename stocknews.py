import requests
import datetime

# Replace 'API_KEY' with your actual API key obtained from newsapi.org
API_KEY = ' API_KEY'


# Function to retrieve news data for specific tickers
def getNewsData(ticker):
    # Get the current date in string format
    current_date = str(datetime.date.today())

    url = ('https://financialmodelingprep.com/api/v3/stock_news?'
           f'tickers={ticker}'  # Join tickers into a comma-separated string
           f'&limit=50'
           f'&apikey={API_KEY}')

    # Send an HTTP GET request to the News 
    r = requests.get(url)

    # Parse the JSON response into a Python dictionary
    news_data = r.json()

    # Return the news data as a Python dictionary
    return news_data


# Function to extract the titles and URLs of the three latest articles
def threeLatestArticles(data):
    latest_articles = []

    # Loop to retrieve information for the first 3 articles
    for i in range(3):
        article_title = data['articles'][i]['title']
        article_url = data['articles'][i]['url']

        # Append the article title and URL as a list to the latest_articles list
        latest_articles.append([article_title, article_url])

    # Return the list of the three latest articles, where each article is represented as a list
    return latest_articles
