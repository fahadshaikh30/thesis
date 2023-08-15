import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

import seaborn as sns
import matplotlib.pyplot as plt

def ols_regression():
    df_final = pd.read_parquet(r"C:\Users\fashaikh\Desktop\Thesis_main\final_v2.parquet")

    grouped = df_final.groupby('category').mean()

    df_demo = pd.read_csv(r"C:\Users\fashaikh\Desktop\Thesis_main\thesis\acp_data\cleaned_demo.csv")

    demo_columns = df_demo.columns

    grouped = grouped.merge(df_demo, 'inner', right_on= 'Community', left_on='category')

    y = grouped['Normalized_sentiment_score']

    for cols in demo_columns[1:]:
        x = grouped[cols]
        x = sm.add_constant(x)

        results = sm.OLS(y, x).fit()
        save_text(results, cols)

def save_text(results, cols):

    file_name = rf"C:\Users\fashaikh\Desktop\Thesis_main\thesis\statistical_modeling\results\{cols}.txt"
    with open(file_name, 'w') as fh:
        fh.write(results.summary().as_text())

ols_regression()