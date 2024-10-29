"""Modify this code and make improvements. Good luck!"""

# publication data in json format
# each entry is a publication in JOSS
# we convert the json data into a pandas dataframe

from glob import glob
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd


def clean(json_path):
    # read the json data as text
    with open(json_path, "r") as z:
        x = json.load(z)

    # convert json text into df
    a = pd.json_normalize(x)

    # variables to keep
    b = [
        "publisher",
        "DOI",
        "type",
        "author",
        "is-referenced-by-count",
        "title",
        "published.date-parts",
    ]
    # subset variables
    df = a.filter(items=b)

    # fmt:off
    for i,r in df.iterrows(): # for each row of data
        l = r["published.date-parts"][0] # extract list of date values
        df.at[i, 'title'] = df.at[i, 'title'][0] # extract list of title values
        s = f"{l[0]}-{l[1]:02d}-{l[2]:02d}" # convert to YYYY-MM-DD format
        d = pd.to_datetime(s, format='%Y-%m-%d') # turn into date time format
        df.at[i, 'published_date'] = d # set publish date variable

    df.drop("published.date-parts", axis=1, inplace=True) # drop original publish column
    # fmt: on

    return df


path = "data/part-1-data.json"

df = clean(path)
print(df.shape)

path = "data/part-1-datab.json"

df2 = clean(path)
print(df2.shape)

df_combined = pd.concat([df, df2], axis=0)
df_combined.shape
