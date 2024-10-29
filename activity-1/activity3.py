"""
Process JOSS data.
The publication data comes in as a JSON file where
each entry is a publication in JOSS.

This script converts the json data into a pandas dataframe
"""

from glob import glob
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd


def clean_date(date_col):
    publication_date = date_col[0]  # the date looks like [[2024-10-29]]
    publication_date_formatted = f"{int(publication_date[0])}-{int(publication_date[1]):02d}-{int(publication_date[2]):02d}"
    publication_date_dt = pd.to_datetime(
        publication_date_formatted, format="%Y-%m-%d"
    )
    return publication_date_dt


def clean_title(title_col):
    return title_col[0]  # the title looks like [["my paper title"]]


def clean(json_path):
    """Process json file into a pandas dataframe

    Parameters
    ----------

    json_path : path to a json file

    Returns
    -------
    A pandas dataframe object


    Examples
    --------
    clean("path_to_file.json")
    """
    # read the json data
    with open(json_path, "r") as file:
        json_data = json.load(file)

    # convert json into df
    df_json = pd.json_normalize(json_data)

    # variables to keep
    to_keep = [
        "publisher",
        "DOI",
        "type",
        "author",
        "is-referenced-by-count",
        "title",
        "published.date-parts",
    ]
    # subset variables
    df_filtered = df_json.filter(items=to_keep)

    df_filtered["title"] = df_filtered["title"].apply(clean_title)

    df_filtered["published_date"] = df_filtered["published.date-parts"].apply(
        clean_date
    )

    # drop original publish column
    df = df_filtered.drop("published.date-parts", axis=1)

    return df


data_path = Path("data")
data_files = ["part-1-data.json", "part-1-datab.json"]
to_combine = [clean(data_path / file) for file in data_files]
df_combined = pd.concat(to_combine, axis=0)

print(df_combined.shape)
