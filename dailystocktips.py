import random

stock_tips = [
    "Stay patient and avoid impulsive trading decisions.",
    "Consider investing in index funds or ETFs for diversification.",
    "Set clear investment goals and a well-defined strategy.",
    "Avoid trying to predict short-term market movements.",
    "Invest in what you understand; don't follow investment trends blindly.",
    "Keep an emergency fund separate from your investment capital.",
    "Consider the tax implications of your investment decisions.",
    "Don't invest money you can't afford to lose.",
    "Learn from successful investors and their strategies.",
    "Avoid overtrading; high transaction volume can erode profits.",
    "Understand the impact of inflation on your investments.",
    "Consider a mix of growth and value stocks in your portfolio.",
    "Pay attention to company earnings reports and financial statements.",
    "Use stop-loss orders to limit potential losses in volatile markets.",
    "Regularly rebalance your portfolio to maintain your desired asset allocation.",
    "Stay informed about changes in market regulations and policies.",
    "Avoid chasing hot stocks or market fads.",
    "Keep emotions in check; fear and greed can lead to poor decisions.",
    "Consider the competitive landscape when evaluating a company.",
    "Diversify not only across stocks but also across asset classes.",
    "Understand the importance of compounding for long-term growth.",
    "Investigate a company's debt levels and financial stability.",
    "Have a clear exit strategy and know when to sell a stock.",
    "Avoid making investment decisions based solely on tips or rumors.",
    "Consider the impact of currency exchange rates on international investments.",
    "Stay patient during market downturns; they are part of the investing cycle.",
    "Monitor and adjust your portfolio as your financial situation changes.",
    "Consider the impact of fees and expenses on your investment returns.",
    "Learn from your investment mistakes and adapt your strategy.",
    "Regularly assess your risk tolerance and adjust your portfolio accordingly.",
    "Be cautious of the 'herd mentality' in the stock market; what's popular may not be the best choice for you.",
    "Keep a long-term perspective and focus on the fundamentals of the companies you invest in.",
    "Consider dollar-cost averaging, which involves investing a fixed amount at regular intervals to reduce market timing risk.",
    "Stay diversified within asset classes; for example, if you invest in stocks, consider diversifying across different sectors.",
    "Be aware of market cycles and historical patterns, but don't rely solely on past performance to predict the future.",
    "Invest in companies with strong management teams and a history of prudent decision-making.",
    "Have a clear understanding of the fees and expenses associated with any investment product or fund.",
    "Stay patient and avoid making impulsive decisions during periods of market volatility.",
    "Consider setting up automatic contributions to your investment accounts to ensure consistent saving and investing.",
    "Avoid investing based solely on political or economic predictions; the market is influenced by many factors.",
    "Stay cautious of 'pump and dump' schemes and unsolicited investment advice.",
    "Periodically review and update your investment plan to ensure it aligns with your changing financial goals.",
    "Understand the concept of 'buy and hold' investing for long-term wealth accumulation.",
    "Stay aware of changes in interest rates and how they can impact your investment portfolio.",
    "Avoid excessive trading, as it can lead to higher transaction costs and lower returns.",
    "Consider the impact of dividend yield and dividend growth when evaluating dividend-paying stocks.",
    "Be aware of the potential risks associated with trading options and derivatives.",
    "Avoid borrowing to invest (margin trading) unless you fully understand the risks involved.",
    "Stay cautious of penny stocks, which can be highly speculative and risky investments.",
    "Keep an eye on economic indicators and their potential impact on your investments.",
    "Don't let recent market performance overly influence your investment decisions; stay focused on your long-term goals.",
    "Consider the impact of environmental, social, and governance (ESG) factors on your investment choices.",
    "Avoid market timing; consistently investing over time tends to yield better results than trying to time the market.",
    "Stay aware of the impact of technological advancements and disruptions on the industries you invest in.",
    "Consider the potential impact of geopolitical events on your investments.",
    "Diversify your investments geographically to reduce country-specific risk.",
    "Evaluate the liquidity of the assets you invest in; some investments may be harder to sell quickly.",
    "Maintain a well-organized record of your investments, including purchase prices and dates.",
    "Consider the impact of interest rate changes on bond investments; bond prices tend to move inversely to interest rates.",
]


def getDailyTip():
    messages = []
    daily_tip_number = random.randint(0, 58)
    daily_tip = stock_tips[daily_tip_number]

    message = "ℹ️ <b>DAILY ADVICE</b> ℹ️"
    message += "\n\n"
    message += "<i>" + daily_tip + "</i>"
    gif_url = 'https://media.giphy.com/media/aqK2XQPuTtLYQ/giphy.gif'

    messages.append((message, gif_url))

    return messages
