import asyncio
from twikit import Client

async def scrape_tweets(username, count=30):
    client = Client(language='en-US')
    client.load_cookies("cookies.json")  # ✅ Don't await this

    query = f'(from:{username}) lang:en since:2022-01-01 until:2025-01-01'
    tweets = None
    tweet_texts = []

    while len(tweet_texts) < count:
        if tweets is None:
            tweets = await client.search_tweet(query, product='Top')  # ✅ Await this
        else:
            tweets = await tweets.next()  # ✅ Await this

        if not tweets:
            break

        for tweet in tweets:
            tweet_texts.append(tweet.text)
            if len(tweet_texts) >= count:
                break

    return tweet_texts

# Run the async function
if __name__ == "__main__":
    tweets = asyncio.run(scrape_tweets("RakJhun"))
    for i, tweet in enumerate(tweets, 1):
        print(f"{i}. {tweet}")
