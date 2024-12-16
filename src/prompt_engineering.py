import os
import glob
import pickle

import pandas as pd
from tqdm import tqdm
from openai import AzureOpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.utils.helpers import *
from src.constants import *

if __name__ == "__main__":
    movies_df = pd.read_csv(DATA_FOLDER_PREPROCESSED + "merged_movies.csv")

    print(movies_df.shape)

    endpoint = os.environ.get("OAI_ENDPOINT")
    key = os.environ.get("OAI_KEY")

    # import keyring

    # endpoint = keyring.get_password("AzureOpenAI", "endpoint4omini")
    # key = keyring.get_password("AzureOpenAI", "key4omini")

    # print(endpoint)
    # print(key)

    model_name = "gpt-4o-mini"

    client = AzureOpenAI(
        azure_endpoint=endpoint, api_version="2024-08-01-preview", api_key=key
    )

    with open("src/utils/prompt.txt", "r") as f:
        prompt = f.read()

    def process_row(row, index):
        query = create_query_movie(
            prompt, row["title"], str(row["release_date"]), row["plot_summary"]
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": query},
            ],
        )
        output = str(response.choices[0].message.content)
        # Write output to a file
        with open(
            f"{PROMPT_ENGINEERING}output_{index}.txt", "w", encoding="utf-8"
        ) as f:
            f.write(output)
        return output

    responses = []
    with ThreadPoolExecutor(max_workers=12) as executor:
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

    output_files = sorted(
        glob.glob(PROMPT_ENGINEERING + "output_*.txt"),
        key=lambda x: int(x.split("_")[1].split(".txt")[0]),
    )

    output_4o = []

    # read all the output files
    for file in output_files:
        with open(file, "r") as f:
            output_4o.append(f.read())

    pickle.dump(output_4o, open(DATA_FOLDER_PREPROCESSED + "output4o.pkl", "wb"))
