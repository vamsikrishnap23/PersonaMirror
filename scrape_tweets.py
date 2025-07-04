import asyncio
from twikit import Client

async def scrape_tweets(username, count=30):
    client = Client(language='en-US')
    client.load_cookies("cookies.json")  

    query = f'(from:{username}) lang:en since:2022-01-01 until:2025-01-01'
    tweets = None
    tweet_texts = []

    while len(tweet_texts) < count:
        if tweets is None:
            tweets = await client.search_tweet(query, product='Top')  
        else:
            tweets = await tweets.next()  

        if not tweets:
            break

        for tweet in tweets:
            tweet_texts.append(tweet.text)
            if len(tweet_texts) >= count:
                break

    return tweet_texts

