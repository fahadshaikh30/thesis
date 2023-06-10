import pandas as pd
import os
import snscrape.modules.twitter as twitter
import dataclasses

start_date = "2020-01-01"
end_date = "2022-12-31"


def download_tweets(start_date, end_date):
    df_county = pd.read_csv(
        "/Users/fahad/Desktop/Thesis/twitter-data/County-Type-Share.csv"
    )
    path = "/Users/fahad/development/thesis/"
    df_county = df_county[
        df_county["category"] == "Big Cities"
    ]  # Rural Middle America, College Towns, LDS Enclaves, Aging Farmlands, Big Cities, Middle Suburbs

    for county, category in zip(df_county["County"], df_county["category"]):
        in_memory = []
        n_tweets = 50000

        save_path = os.path.join(
            path,
            f"{category}",
            f"BLM_{county}_{start_date}_{end_date}.parquet",
        )

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        df = pd.DataFrame()

        scraper = twitter.TwitterSearchScraper(
            f"(BlackLivesMatter OR BLM) lang:en near:United States since:{start_date} until:{end_date}",
        )

        for i, tweet in enumerate(scraper.get_items()):
            print(i, tweet.url, county)
            di = dataclasses.asdict(tweet)
            # use pandas.concat to append the new tweet to the dataframe

            in_memory.append(di)

            # persist the dataframe every 1000 tweets
            if i % n_tweets == 0 and i > 0:
                df = pd.concat([df, pd.DataFrame(in_memory)], ignore_index=True)
                df.to_parquet(save_path)
                in_memory = []

            if i > n_tweets:
                break

        # persist the dataframe at the end
        if df.size > 0 or len(in_memory) > 0:
            if len(in_memory) > 0:
                df = pd.concat([df, pd.DataFrame(in_memory)], ignore_index=True)
            df.to_parquet(save_path)


download_tweets(start_date, end_date)
