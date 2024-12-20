import pandas as pd
from src.utils.constants import *
from src.utils.helpers import *


def get_plot_summary(tconst, imdb_instance):
    try:
        movie = imdb_instance.get_movie(int(str(tconst)[2:]))
        # Retrieve the plot, if available, or return None
        plot = movie.get("plot")
        if plot:
            return plot[0]  # return the first plot summary
        else:
            return None
    except Exception as e:
        return None


def combine_columns(df, name_1, name_2):
    df[name_1] = df.apply(
        lambda row: list(
            set(
                (row[name_1] if isinstance(row[name_1], list) else [])
                + (row[name_2] if isinstance(row[name_2], list) else [])
            )
        ),
        axis=1,
    )

    # Replace empty lists by NaN
    df[name_1] = df[name_1].apply(lambda x: np.nan if len(x) == 0 else x)

    return df


def clean_languages(row):
    if isinstance(row["languages"], list):
        languages = set(
            [string.replace(" Language", "") for string in row["languages"]]
        )
    else:
        languages = (
            set([row["original_language"]])
            if isinstance(row["original_language"], str)
            else np.nan
        )

    return languages


def clean_countries(row):
    if isinstance(row["countries"], list):
        countries = set(row["countries"])
    else:
        countries = set([row["region"]]) if isinstance(row["region"], str) else np.nan

    return countries


def get_soviet_movies():
    title_akas = pd.read_csv(IMDB_AKA, sep="\t", usecols=["titleId", "title", "region"])
    title_basics = pd.read_csv(
        IMDB_BASIC,
        sep="\t",
        usecols=["tconst", "primaryTitle", "titleType", "startYear", "genres"],
    )

    # Merge the DataFrames on the common column tconst
    imdb_movies = pd.merge(
        title_akas, title_basics, left_on="titleId", right_on="tconst"
    )

    # Select only the columns we need and rename `titleId` to `tconst` for consistency
    imdb_movies = imdb_movies[
        [
            "tconst",
            "title",
            "primaryTitle",
            "region",
            "titleType",
            "startYear",
            "genres",
        ]
    ]

    # select region that are related to the Soviet Union
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

    # Filter the movies that are related to the Soviet Union
    soviet_movies = imdb_movies[
        imdb_movies["region"].fillna("").str.contains("|".join(regions), case=False)
    ]

    # Drop the columns that are not needed
    soviet_movies = (
        soviet_movies[soviet_movies["titleType"] == "movie"]
        .drop_duplicates(subset="primaryTitle", keep="first")
        .drop(columns=["title", "titleType"])
    )

    return soviet_movies


def create_dataset_api():
    from concurrent.futures import ThreadPoolExecutor
    from tqdm import tqdm
    import time
    from imdb import IMDb
    from functools import partial

    time.sleep(1)

    imdb_instance = IMDb()

    soviet_movies = get_soviet_movies()

    # Use partial to pass the IMDb instance to the function
    get_plot_with_imdb = partial(get_plot_summary, imdb_instance=imdb_instance)

    with ThreadPoolExecutor(max_workers=4) as executor:

        soviet_movies["plot"] = list(
            tqdm(
                executor.map(get_plot_with_imdb, soviet_movies["tconst"]),
                total=len(soviet_movies),
            )
        )

    # save the dataframe to soviet_movies.tsv
    soviet_movies.to_csv(DATA_FOLDER_PREPROCESSED + "soviet_movies.tsv", sep="\t")


def create_merged_dataset():
    # Load the preprocessed data

    df_movies = pd.read_csv(DATA_FOLDER_PREPROCESSED + "movie_summaries.csv")

    # TMDb
    df_tmdb_movies = pd.read_csv(
        TMDB_MOVIE,
        usecols=[
            "id",
            "title",
            "release_date",
            "revenue",
            "runtime",
            "genres",
            "production_countries",
            "original_language",
            "spoken_languages",
            "overview",
        ],
    )

    df_tmdb_keywords = pd.read_csv(TMDB_KEYWORDS)

    # Use the helper function to preprocess the data before the merging
    df_tmdb_movies = preprocess_movie_data(df_tmdb_movies)

    # Merge the TMDb movies with TMDb keywords based on id
    df_tmdb_movies["id"] = df_tmdb_movies["id"].astype(int)
    df_tmdb_movies = pd.merge(df_tmdb_movies, df_tmdb_keywords, on="id", how="left")

    for column_name in [
        "genres",
        "production_countries",
        "spoken_languages",
        "keywords",
    ]:
        df_tmdb_movies[column_name] = df_tmdb_movies[column_name].apply(
            lambda row: (
                [item["name"] for item in ast.literal_eval(row)]
                if pd.notnull(row) and ast.literal_eval(row)
                else np.nan
            )
        )

    # Merge with MoviesSummaries based on the title
    df_merged_movies = pd.merge(
        df_movies,
        df_tmdb_movies,
        on="title",
        how="outer",
        suffixes=("_original", "_additional"),
    )

    for _, column_name in enumerate(df_merged_movies.columns):

        if column_name in [
            "release_date_original",
            "revenue_original",
            "runtime_original",
        ]:
            # craft the additional column name
            new_column_name = column_name[: -len("_original")]
            column_name_additional = new_column_name + "_additional"
            # fill the missing values
            df_merged_movies[new_column_name] = df_merged_movies[
                column_name
            ].combine_first(df_merged_movies[column_name_additional])
            # drop the original and additional column
            df_merged_movies = df_merged_movies.drop(
                columns=[column_name, column_name_additional]
            )

    df_merged_movies["release_date"] = pd.to_datetime(
        df_merged_movies["release_date"], errors="coerce"
    )

    df_merged_movies = combine_columns(
        df_merged_movies, "genres_original", "genres_additional"
    )
    df_merged_movies = df_merged_movies.rename(columns={"genres_original": "genres"})

    df_merged_movies = combine_columns(
        df_merged_movies, "languages", "spoken_languages"
    )

    df_merged_movies = combine_columns(
        df_merged_movies, "countries", "production_countries"
    )

    df_merged_movies = df_merged_movies.drop(
        columns=["spoken_languages", "production_countries", "id", "genres_additional"]
    )

    # IMDb

    soviet_movies = pd.read_csv(
        DATA_FOLDER_PREPROCESSED + "soviet_movies.tsv",
        sep="\t",
        usecols=[
            "tconst",
            "title",
            "primaryTitle",
            "region",
            "titleType",
            "startYear",
            "genres",
            "plot",
        ],
    )

    # Drop the columns that are not needed and rename the columns to match our column names
    soviet_movies = soviet_movies.drop(columns=["title", "titleType"]).rename(
        columns={
            "primaryTitle": "title",
            "startYear": "release_date",
            "plot": "plot_summary",
        }
    )

    soviet_movies["release_date"] = pd.to_datetime(
        soviet_movies["release_date"], format="%Y", errors="coerce"
    )

    soviet_movies["genres"] = soviet_movies["genres"].apply(
        lambda genres: genres.split(",")
    )

    # Merge the ´soviet_movies´ dataframe with the ´df_merged_movies´
    df_merged_movies = pd.merge(
        df_merged_movies,
        soviet_movies,
        on="title",
        how="outer",
        suffixes=("_original", "_additional"),
    )

    df_merged_movies["release_date_original"] = df_merged_movies[
        "release_date_original"
    ].combine_first(df_merged_movies["release_date_additional"])

    df_merged_movies = combine_columns(
        df_merged_movies, "genres_original", "genres_additional"
    )

    df_merged_movies = df_merged_movies.rename(
        columns={"release_date_original": "release_date", "genres_original": "genres"}
    )
    df_merged_movies = df_merged_movies.drop(
        columns=["release_date_additional", "genres_additional"]
    )

    df_merged_movies["languages"] = df_merged_movies.apply(clean_languages, axis=1)

    # Map ISO language codes to their usual names
    mapping = {
        "en": "English",
        "de": "German",
        "it": "Italian",
        "hi": "Hindi",
        "zh": "Chinese",
        "fr": "French",
        "ko": "Korean",
        "ja": "Japanese",
        "nl": "Dutch",
        "te": "Telugu",
        "sv": "Swedish",
        "bs": "Bosnian",
        "es": "Spanish",
        "cn": "Chinese",
        "no": "Norwegian",
        "is": "Icelandic",
        "pl": "Polish",
        "ru": "Russian",
        "ro": "Romanian",
        "th": "Thai",
        "ab": "Abkhazian",
        "et": "Estonian",
        "fi": "Finnish",
        "el": "Greek",
        "ta": "Tamil",
        "pt": "Portuguese",
        "ur": "Urdu",
        "fa": "Persian",
        "da": "Danish",
        "tr": "Turkish",
        "nb": "Norwegian Bokmål",
        "xx": "Unknown",
        "sl": "Slovenian",
        "pa": "Punjabi",
        "sr": "Serbian",
        "sh": "Serbo-Croatian",
        "hu": "Hungarian",
        "lv": "Latvian",
        "cs": "Czech",
        "bn": "Bengali",
        "uk": "Ukrainian",
        "sq": "Albanian",
        "he": "Hebrew",
        "ml": "Malayalam",
        "vi": "Vietnamese",
        "mr": "Marathi",
        "ar": "Arabic",
        "ay": "Aymara",
        "ms": "Malay",
        "ka": "Georgian",
        "id": "Indonesian",
        "hr": "Croatian",
        "bg": "Bulgarian",
        "mk": "Macedonian",
        "bm": "Bambara",
        "tl": "Tagalog",
        "ku": "Kurdish",
        "ca": "Catalan",
        "sk": "Slovak",
        "uz": "Uzbek",
        "wo": "Wolof",
        "lo": "Lao",
        "gl": "Galician",
        "fy": "Frisian",
        "lt": "Lithuanian",
        "eu": "Basque",
        "am": "Amharic",
        "cy": "Welsh",
        "eo": "Esperanto",
        "kk": "Kazakh",
        "qu": "Quechua",
        "kn": "Kannada",
        "ne": "Nepali",
        "iu": "Inuktitut",
        "bo": "Tibetan",
        "rw": "Kinyarwanda",
        "jv": "Javanese",
        "ps": "Pashto",
        "ky": "Kyrgyz",
        "af": "Afrikaans",
        "la": "Latin",
        "mt": "Maltese",
        "hy": "Armenian",
        "mn": "Mongolian",
        "si": "Sinhalese",
        "sm": "Samoan",
        "lb": "Luxembourgish",
        "tg": "Tajik",
        "zu": "Zulu",
    }

    df_merged_movies["languages"] = df_merged_movies["languages"].apply(
        lambda bag: (
            [mapping.get(string, string) for string in bag]
            if isinstance(bag, set)
            else bag
        )
    )

    df_merged_movies = df_merged_movies.drop("original_language", axis=1)

    df_merged_movies["countries"] = df_merged_movies.apply(clean_countries, axis=1)

    region_to_country = {
        "SU": "Soviet Union",
        "SUHH": "Soviet Union",
        "RU": "Russia",
        "UA": "Ukraine",
        "BY": "Belarus",
        "KZ": "Kazakhstan",
        "UZ": "Uzbekistan",
        "GE": "Georgia",
        "AM": "Armenia",
        "AZ": "Azerbaijan",
        "LT": "Lithuania",
        "LV": "Latvia",
        "EE": "Estonia",
        "TM": "Turkmenistan",
        "KG": "Kyrgyzstan",
        "TJ": "Tajikistan",
        "MD": "Moldova",
    }

    df_merged_movies["countries"] = df_merged_movies["countries"].apply(
        lambda bag: (
            [region_to_country.get(string, string) for string in bag]
            if isinstance(bag, set)
            else bag
        )
    )

    df_merged_movies = df_merged_movies.drop("region", axis=1)

    df_merged_movies["plot_summary"] = (
        df_merged_movies["plot_summary_original"]
        .combine_first(df_merged_movies["overview"])
        .combine_first(df_merged_movies["plot_summary_additional"])
    )

    # Dropping the used columns
    df_merged_movies.drop(
        columns=[
            "plot_summary_original",
            "overview",
            "plot_summary_additional",
            "tconst",
            "revenue",
        ],
        inplace=True,
    )

    # drop nan values
    df_merged_movies = df_merged_movies.dropna(
        subset=["plot_summary", "title", "release_date", "countries"]
    )

    df_merged_movies = df_merged_movies[
        df_merged_movies["release_date"] <= pd.to_datetime("1995")
    ]
    df_merged_movies = df_merged_movies[
        df_merged_movies["release_date"] >= pd.to_datetime("1945")
    ]

    df_merged_movies["release_date"] = df_merged_movies["release_date"].dt.year

    df_merged_movies.drop_duplicates(subset=["title", "release_date"], inplace=True)

    # save the dataframe to merged_movies.csv
    df_merged_movies.to_csv(DATA_FOLDER_PREPROCESSED + "merged_movies.csv", index=False)

    return df_merged_movies


if __name__ == "__main__":
    create_merged_dataset()
