import tweetnlp
import pandas as pd
from tqdm import tqdm
from pathlib import Path

path = r'C:\Users\fashaikh\Desktop\Thesis main\partitioned_data\GrayingAmerica.parquet'
smodel = tweetnlp.load_model('sentiment')
emodel = tweetnlp.load_model('emotion')

def get_sentiment_emotion(path):
    df = pd.read_parquet(path)

    text = list(df['cleanedContent'])

    sen = []
    em = []

    for i in tqdm(text):
        sentiment_result = smodel.sentiment(i, return_probability=True)
        emotion_result = emodel.emotion(i, return_probability=True)
        sen.append(sentiment_result)
        em.append(emotion_result)
    
    sdata = pd.json_normalize(sen)

    sdf = pd.concat(objs=[df, sdata], axis=1)

    edata = pd.json_normalize(em)

    edf = pd.concat(objs=[df, edata], axis=1)

    sfilename = Path(path).stem + f"_sentiment"

    efilename = Path(path).stem + f"_emotion"

    soutput_path = fr'C:\Users\fashaikh\Desktop\Thesis main\sentiment_results\{sfilename}.parquet'
    
    eoutput_path = fr'C:\Users\fashaikh\Desktop\Thesis main\emotion_results\{efilename}.parquet'

    sdf.to_parquet(soutput_path)

    edf.to_parquet(eoutput_path)

get_sentiment_emotion(path)