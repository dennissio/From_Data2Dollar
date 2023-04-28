import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime

# Liste der Hashtags für die jeweiligen Events, die gescrapet wurden
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

# Start- und Enddatum für den Suchzeitraum festlegen sowie Name der Output-Datei
since_date = '2023-03-29'
until_date = '2023-04-16'
output_file = 'all_tweets.csv'

# Funktion zum Scrapen von Tweets defineren
def scrape_tweets(queries, since_date, until_date, output_file):
    # Leere Liste erstellen, um die gesammelten Daten zu speichern
    all_tweets_data = []

    # For-Schleife zum Durchlaufen der Hashtag-Liste
    for query in queries:
        # Erstellen einer leeren Liste für jeden Hashtag, um dessen gesammelte Daten darin zu speichern
        tweets_data = []
        # Abfrage mit Hashtag und Datum
        full_query = f'{query} since:{since_date} until:{until_date}'
        # Gesammelten Tweets für die Abfrage durchlaufen
        for tweet in sntwitter.TwitterSearchScraper(full_query).get_items():
            # Zeilenumbrüchen entfernen 
            cleaned_content = tweet.rawContent.replace('\n', ' ')
            # Twitter-Daten zur Liste tweets_data hinzufügen
            tweets_data.append([query, tweet.date, tweet.id, cleaned_content, tweet.user.username, tweet.retweetCount, tweet.likeCount, tweet.replyCount])

        # Daten für jeden Hashtag in der Gesamtliste zusammenführen
        all_tweets_data.extend(tweets_data)

    # DF für alle gesammelten Daten erstellen und in CSV-Datei speichern
    all_tweets_df = pd.DataFrame(all_tweets_data, columns=['hashtag', 'date', 'tweet_id', 'content', 'username', 'retweets', 'likes', 'replies'])
    all_tweets_df.to_csv(output_file, index=False)

# Aufruf der Funktion scrape_tweets beim Ausführen des Skripts 
if __name__ == '__main__':
    scrape_tweets(queries, since_date, until_date, output_file)
