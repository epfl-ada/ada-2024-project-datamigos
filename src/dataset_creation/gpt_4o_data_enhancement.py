import pandas as pd
from src.utils.helpers import *
from src.utils.constants import *
import pickle
import re


def parse_gpt_answer(answer):

    def split(line):
        line = re.sub(r"^[^:]*:", "", line)
        line = line.replace(", ", ",")
        # remove lasst character if " "
        if line[-1] == " ":
            line = line[:-1]
        return re.split(r",|\n", line)

    parsed_answer = {}

    answer = answer.replace(" \n", "\n")
    answer = answer.replace("\n\n", "\n")

    # Split the answer
    answer = answer.split("\n")

    try:
        # Parse the Cold War side
        parsed_answer["cold_war_side"] = answer[0]
        # Parse the Western bloc representation
        parsed_answer["character_western_bloc_representation"] = split(answer[1])
        # Parse the Eastern bloc representation
        parsed_answer["character_eastern_bloc_representation"] = split(answer[2])
        # Parse the Western bloc values;
        parsed_answer["western_bloc_values"] = split(answer[3])
        # Parse the Eastern bloc values
        parsed_answer["eastern_bloc_values"] = split(answer[4])
        # Parse the theme of the movie
        parsed_answer["theme"] = split(answer[5])
    except:
        parsed_answer = {
            "cold_war_side": "None",
            "character_western_bloc_representation": "None",
            "character_eastern_bloc_representation": "None",
            "western_bloc_values": "None",
            "eastern_bloc_values": "None",
            "theme": "None",
        }

    return parsed_answer


def preprocess_side(row):
    # remove all non alphanumeric characters
    try:
        row["cold_war_side"] = re.sub(r"\W+", "", row["cold_war_side"])
    except:
        row["cold_war_side"] = "None"

    if row["character_western_bloc_representation"] is np.nan:
        row["character_western_bloc_representation"] = ["None"]
    if row["character_eastern_bloc_representation"] is np.nan:
        row["character_eastern_bloc_representation"] = ["None"]
    if row["western_bloc_values"] is np.nan:
        row["western_bloc_values"] = ["None"]
    if row["eastern_bloc_values"] is np.nan:
        row["eastern_bloc_values"] = ["None"]
    if row["theme"] is np.nan:
        row["theme"] = ["None"]

    if (
        row["character_western_bloc_representation"][0] == "None"
        and row["character_eastern_bloc_representation"][0] == "None"
    ) and row["cold_war_side"] != "None":
        row["cold_war_side"] = "None"

    return row


def create_enhanced_dataset():
    output_4o = pickle.load(open(DATA_FOLDER_PREPROCESSED + "output4o.pkl", "rb"))
    parsed_4o = []

    for answer in output_4o:
        parsed_4o.append(parse_gpt_answer(answer))

    movies_df = pd.read_csv(DATA_FOLDER_PREPROCESSED + "merged_movies.csv")
    movies_df = movies_df.assign(
        **{key: [d[key] for d in parsed_4o] for key in parsed_4o[0].keys()}
    )
    movies_df = movies_df.apply(preprocess_side, axis=1)

    movies_df["cold_war_side"] = movies_df["cold_war_side"].apply(lambda x: f'"{x}"')

    movies_df.to_csv(DATA_FOLDER_PREPROCESSED + "v2_movies_cleaned.csv", index=False)

    return movies_df
