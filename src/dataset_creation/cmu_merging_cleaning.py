import pandas as pd
from src.utils.constants import *
from src.utils.helpers import *


def create_plot_summary_dataset():

    # Load CMU character data
    df_characters = pd.read_table(
        CMU_CHARACTER,
        names=[
            "wikipedia_id",
            "freebase_id",
            "release_date",
            "character_name",
            "actor_dob",
            "actor_gender",
            "actor_height",
            "actor_ethnicity",
            "actor_name",
            "actor_age_at_movie_release",
            "freebase_actor_map_id",
            "freebase_character_id",
            "freebase_actor_id",
        ],
    )

    df_characters["release_date"] = df_characters["release_date"].apply(
        convert_to_datetime
    )
    df_characters["release_date"] = pd.to_datetime(
        df_characters["release_date"], errors="coerce"
    )

    df_characters["actor_dob"] = df_characters["actor_dob"].apply(convert_to_datetime)
    df_characters["actor_dob"] = pd.to_datetime(
        df_characters["actor_dob"], errors="coerce"
    )
    df_characters.loc[df_characters["actor_height"] == 510, "actor_height"] = 1.78
    df_characters.drop(
        df_characters[df_characters["actor_height"] > 2.5].index, inplace=True
    )
    df_characters = df_characters[df_characters["actor_age_at_movie_release"] > 0]
    df_characters.drop_duplicates(
        subset=["freebase_id", "freebase_actor_id", "freebase_character_id"],
        inplace=True,
    )

    # Load CMU movie data
    df_movies = pd.read_table(
        CMU_MOVIE,
        names=[
            "wikipedia_id",
            "freebase_id",
            "title",
            "release_date",
            "revenue",
            "runtime",
            "languages",
            "countries",
            "genres",
        ],
        header=None,
    )

    df_movies["release_date"] = df_movies["release_date"].apply(convert_to_datetime)
    df_movies["release_date"] = pd.to_datetime(
        df_movies["release_date"], errors="coerce"
    )

    df_movies.drop(df_movies[df_movies["runtime"] > 500].index, inplace=True)
    df_movies.drop(df_movies[df_movies["runtime"] <= 0].index, inplace=True)

    df_movies["genres"] = df_movies.apply(
        lambda row: extract_list(row, "genres"), axis=1
    )
    df_movies["genres"] = df_movies["genres"].apply(
        lambda x: np.nan if len(x) == 0 else x
    )

    df_movies["countries"] = df_movies.apply(
        lambda row: extract_list(row, "countries"), axis=1
    )

    # Replace empty lists by NaN
    df_movies["countries"] = df_movies["countries"].apply(
        lambda x: np.nan if len(x) == 0 else x
    )

    df_movies["languages"] = df_movies.apply(
        lambda row: extract_list(row, "languages"), axis=1
    )

    # Replace empty lists by NaN
    df_movies["languages"] = df_movies["languages"].apply(
        lambda x: np.nan if len(x) == 0 else x
    )

    # Load CMU plot summaries

    df_plots = pd.read_table(
        PLOT_SUMMARIES, names=["wikipedia_id", "plot_summary"], header=None
    )

    df_temp = pd.DataFrame(df_plots[df_plots.duplicated(subset=["plot_summary"])])

    # Merge the dataframes
    df_movies[df_movies["wikipedia_id"].isin(df_temp["wikipedia_id"])].sort_values(
        by=["wikipedia_id"]
    )

    df_movies = preprocess_movie_data(df_movies)

    df_movies = df_movies.join(df_plots.set_index("wikipedia_id"), on="wikipedia_id")

    df_movies.to_csv(DATA_FOLDER_PREPROCESSED + "movie_summaries.csv", index=False)

    return df_movies


if __name__ == "__main__":
    create_plot_summary_dataset()
