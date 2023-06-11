import tweetnlp
import pandas as pd
from tqdm import tqdm
from pathlib import Path

path = r'C:\Users\fashaikh\Desktop\Thesis main\partitioned_data\LDSEnclaves.parquet'
model = tweetnlp.load_model('sentiment')

def get_sentiment(path):
    df = pd.read_parquet(path)

    text = list(df['cleanedContent'])

    res = []

    for i in tqdm(text):
        sentiment_result = model.sentiment(i, return_probability=True)
        res.append(sentiment_result)
    
    data = pd.json_normalize(res)

    df = pd.concat(objs=[df, data], axis=1)

    filename = Path(path).stem + f"_sentiment"

    output_path = fr'C:\Users\fashaikh\Desktop\Thesis main\thesis\tweet_sentiment\{filename}.parquet'

    df.to_parquet(output_path)


get_sentiment(path)