import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(__file__)
os.chdir(script_dir)

# Load each TSV file into a DataFrame
title_akas = pd.read_csv(
    "data/title.akas.tsv", sep="\t", usecols=["titleId", "title", "region"]
)
title_basics = pd.read_csv(
    "data/title.basics.tsv",
    sep="\t",
    usecols=["tconst", "primaryTitle", "titleType", "startYear", "genres"],
)

# Merge the DataFrames on the common column (`tconst` in title.basics and `titleId` in title.akas)
merged_df = pd.merge(title_akas, title_basics, left_on="titleId", right_on="tconst")

# Select only the columns you need and rename `titleId` to `tconst` if you want consistency
imdb_movies = merged_df[
    ["tconst", "title", "primaryTitle", "region", "titleType", "startYear", "genres"]
]

regions = [
    "SU",
    "RU",
    "UA",
    "BY",
    "KZ",
    "UZ",
    "GE",
    "AM",
    "AZ",
    "LT",
    "LV",
    "EE",
    "TM",
    "KG",
    "TJ",
    "MD",
]

soviet_movies = imdb_movies[
    imdb_movies["region"].fillna("").str.contains("|".join(regions), case=False)
]

soviet_movies = soviet_movies[soviet_movies["titleType"] == "movie"]
soviet_movies = soviet_movies[
    (soviet_movies["startYear"] > "1945") & (soviet_movies["startYear"] < "1991")
].drop_duplicates(subset="primaryTitle", keep="first")


def get_plot_summary(tconst):
    try:
        movie = ia.get_movie(int(str(tconst)[2:]))
        # Retrieve the plot, if available, or return None
        plot = movie.get("plot")
        if plot:
            return plot[0]  # return the first plot summary
        else:
            return None
    except Exception as e:
        return None


from imdb import IMDb
import time
from tqdm import tqdm

ia = IMDb()

tqdm.pandas()

soviet_movies = soviet_movies.sample(20)

soviet_movies["plot"] = soviet_movies["tconst"].progress_apply(get_plot_summary)
time.sleep(0.1)

soviet_movies.to_csv("data/soviet_movies.tsv", sep="\t")
