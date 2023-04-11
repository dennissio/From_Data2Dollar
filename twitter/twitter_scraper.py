import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime

queries = [
    "#amsterdam",
    "#kingsday",
    "#amsterdam #kingsday"
]

since_date = '2023-03-29'
until_date = '2023-04-16'
output_file = 'tweets.csv'

def scrape_tweets(queries, since_date, until_date, output_file):
    tweets_data = []

    for query in queries:
        full_query = f'{query} since:{since_date} until:{until_date}'
        for tweet in sntwitter.TwitterSearchScraper(full_query).get_items():
            cleaned_content = tweet.rawContent.replace('\n', ' ')
            tweets_data.append([tweet.date, tweet.id, cleaned_content, tweet.user.username, tweet.retweetCount, tweet.likeCount, tweet.replyCount])

    tweets_df = pd.DataFrame(tweets_data, columns=['date', 'tweet_id', 'content', 'username', 'retweets', 'likes', 'replies'])
    tweets_df.to_csv(output_file, index=False)

if __name__ == '__main__':
    scrape_tweets(queries, since_date, until_date, output_file)