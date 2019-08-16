import pandas as pd


def export(df, name):
    df.to_csv(name, index=False)
