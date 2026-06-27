from engine.newsroom import generate_daily_news

news = generate_daily_news()

print(news["stories"][0]["headline"])