import openai
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from openai import AzureOpenAI
# import keyring
import pandas as pd
from src.utils.helpers import *
import dotenv
import os
from src.utils.helpers import *

# endpoint = keyring.get_password("AzureOpenAI", "endpoint4omini")
# endpoint = keyring.get_password("AzureOpenAI", "endpoint4o")
endpoint = os.environ.get("OAI_ENDPOINT")

# key = keyring.get_password("AzureOpenAI", "key4omini")
# key = keyring.get_password("AzureOpenAI", "key4o")
key = os.environ.get("OAI_KEY")


model_name = "gpt-4o-mini"
# model_name = "gpt-4o"

df = pd.read_csv("data/preprocessed/cleaned_merged_movies.csv")

movies_df = df

client = AzureOpenAI(
    azure_endpoint=endpoint, api_version="2024-08-01-preview", api_key=key
)

prompt = "\
You are an expert in movie history and Cold War. You will be given the name of the film, the year and the plot of the movie. You first need to analyse if the movie can be identified to the Eastern or Western bloc during the Cold War. If yes come up with the character or group of character impersonating the Western and Eastern bloc and their values as well as their main archetye.\n\
Your output needs to be parsable comma separated without context (the output needs to start directly), use only keyword and very important use new line character after each of the following:\n\
- Cold War side belonging either Easter, Western or None.\n\
- The character or group of character representing Western bloc with their values and archetype comma separated or None.\n\
- The character or group of character representing Eastern bloc with their values and archetype comma separated or None.\n\
- The Western bloc representation main values and characteristics comma separated or None.\n\
- The Eatern bloc representation main values and characteristics comma separated or None.\n\
- The theme of the movies and keywords.\n\
If and only if the movie does not belong to any of the blocs, put `None` in the respective fields.\n\
"


def process_row(row, index):
    query = create_query_movie(
        prompt, row["title"], str(row["year_release_date"]), row["plot_summary"]
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": query},
        ],
    )
    output = response.choices[0].message.content
    # Write output to a file
    with open(
        f"data/prompt_engineering/output_{index}.txt", "w", encoding="utf-8"
    ) as f:
        f.write(output)
    return output


responses = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {
        executor.submit(process_row, row, index): index
        for index, row in movies_df.iterrows()
    }

    # Use tqdm to track progress
    for future in tqdm(
        as_completed(futures), total=len(futures), desc="Processing rows"
    ):
        try:
            data = future.result()
            responses.append(data)
        except Exception as exc:
            print(f"Generated an exception: {exc}")

exit()
