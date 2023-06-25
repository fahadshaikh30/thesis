import tweetnlp
import pandas as pd
from tqdm import tqdm
from pathlib import Path

path = r'C:\Users\fashaikh\Desktop\Thesis main\partitioned_data\UrbanSuburbs.parquet'
model = tweetnlp.load_model('emotion')

def get_emotion(path):
    df = pd.read_parquet(path)

    text = list(df['cleanedContent'])

    res = []

    for i in tqdm(text):
        emotion_result = model.emotion(i, return_probability=True)
        res.append(emotion_result)
    
    data = pd.json_normalize(res)

    df = pd.concat(objs=[df, data], axis=1)

    filename = Path(path).stem + f"_emotion"

    output_path = fr'C:\Users\fashaikh\Desktop\Thesis main\emotion_results\{filename}.parquet'

    df.to_parquet(output_path)


get_emotion(path)