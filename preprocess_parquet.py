import pandas as pd

source = "/Users/fahad/Desktop/processed_data/combined_data6.parquet"
dest = "/Users/fahad/Desktop/preprocessed_data/processed_data11.parquet"


def main(source, dest):
    print(f"Reading from {source} to {dest}")
    df = pd.read_parquet(source)

    dropped_cols = [
        "id",
        "conversationId",
        "source",
        "sourceUrl",
        "sourceLabel",
        "cashtags",
        "vibe",
        "inReplyToTweetId",
        "viewCount",
        "retweetedTweet",
        "links",
        "lang",
        "media",
        "quotedTweet",
        "inReplyToUser",
        "mentionedUsers",
        "card",
    ]

    df.drop(columns=dropped_cols, inplace=True)

    user = list(df["user"])

    user_df = pd.json_normalize(user)

    user_df_dropped_cols = [
        "descriptionLinks",
        "displayname",
        "favouritesCount",
        "id",
        "label",
        "listedCount",
        "profileBannerUrl",
        "profileImageUrl",
        "protected",
        "username",
        "statusesCount",
        "link.indices",
        "link.tcourl",
        "link.text",
        "link.url",
        "link",
        "label.badgeUrl",
        "label.description",
        "label.longDescription",
        "label.url",
    ]
    user_df.drop(user_df_dropped_cols, inplace=True, axis=1)

    df = pd.concat([df, user_df], axis=1)

    df.drop("user", inplace=True, axis=1)

    coordinates = list(df["coordinates"])

    coordinates_df = pd.json_normalize(coordinates)

    df = pd.concat([df, coordinates_df], axis=1)

    df.drop("coordinates", inplace=True, axis=1)

    place = list(df["place"])

    place_df = pd.json_normalize(place)

    place_df.drop("id", inplace=True, axis=1)

    df = pd.concat([df, place_df], axis=1)

    df.drop("place", inplace=True, axis=1)

    df.to_parquet(dest)


if __name__ == "__main__":
    main(source, dest)
