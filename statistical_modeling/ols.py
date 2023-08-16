import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from itertools import combinations

import seaborn as sns
import matplotlib.pyplot as plt

def ols_regression():
    df_final = pd.read_parquet(r"C:\Users\fashaikh\Desktop\Thesis_main\final_v2.parquet")

    grouped = df_final.groupby('category').mean()

    df_demo = pd.read_csv(r"C:\Users\fashaikh\Desktop\Thesis_main\thesis\acp_data\semi_cleaned_demo.csv")

    demo_columns = df_demo.columns

    grouped = grouped.merge(df_demo, 'inner', right_on= 'Community', left_on='category')

    y = grouped['Normalized_sentiment_score']

    for cols in demo_columns[1:]:
        x = grouped[cols]
        x = sm.add_constant(x)

        results = sm.OLS(y, x).fit()
        save_text(results, cols)

def save_text(results, cols):

    file_name = rf"C:\Users\fashaikh\Desktop\Thesis_main\thesis\statistical_modeling\five_variables\{cols}.txt"
    with open(file_name, 'w') as fh:
        fh.write(results.summary().as_text())

def ols_v2():
    df_final = pd.read_parquet(r"C:\Users\fashaikh\Desktop\Thesis_main\final_v2.parquet")

    grouped = df_final.groupby('category').mean()

    df_demo = pd.read_csv(r"C:\Users\fashaikh\Desktop\Thesis_main\thesis\acp_data\semi_cleaned_demo.csv")

    grouped = grouped.merge(df_demo, 'inner', right_on= 'Community', left_on='category')

    y = grouped['Normalized_sentiment_score']

    df_demo.drop(columns='Community', inplace=True)

    # Generate all combinations of 2 columns
    column_combinations = combinations(df_demo.columns, 5)

    # Loop through each combination and run OLS regression
    for cols in column_combinations:
        x = grouped[list(cols)]
        x = sm.add_constant(x)  # Add a constant term for the intercept

        results = sm.OLS(y, x).fit()
        first = 1 - results.pvalues[1]
        second = 1 - results.pvalues[2]
        third = 1 - results.pvalues[3]
        fourth = 1 - results.pvalues[4]
        fifth = 1 - results.pvalues[5]
        test = first * second * third * fourth * fifth

        if test > 0.99:
            save_text(results, cols)

#ols_regression()
ols_v2()