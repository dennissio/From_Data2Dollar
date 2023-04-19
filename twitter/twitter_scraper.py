import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime

queries = [
    "#MLF23",
    "#BBF23",
    "#NS20ans",
    "#lbjw23",
    "#Frühlingsfest",
    "#kingsday",
    "#FeriadeAbril",
    "#apriljazz",
    "#FoodiesFestival",
    "#hafengeburtstag",
    "#Karnevalderkulturen",
    "#MonacoGP",
    "#bloemencorso",
    "#ImolaGP",
    "#HändelFestival"
]

since_date = '2023-03-29'
until_date = '2023-04-16'
output_file = 'all_tweets.csv'

def scrape_tweets(queries, since_date, until_date, output_file):
    all_tweets_data = []

    for query in queries:
        tweets_data = []
        full_query = f'{query} since:{since_date} until:{until_date}'
        for tweet in sntwitter.TwitterSearchScraper(full_query).get_items():
            cleaned_content = tweet.rawContent.replace('\n', ' ')
            tweets_data.append([query, tweet.date, tweet.id, cleaned_content, tweet.user.username, tweet.retweetCount, tweet.likeCount, tweet.replyCount])

        all_tweets_data.extend(tweets_data)

    # Erstellt den DataFrame für alle gesammelten Daten
    all_tweets_df = pd.DataFrame(all_tweets_data, columns=['hashtag', 'date', 'tweet_id', 'content', 'username', 'retweets', 'likes', 'replies'])
    all_tweets_df.to_csv(output_file, index=False)

if __name__ == '__main__':
    scrape_tweets(queries, since_date, until_date, output_file)
