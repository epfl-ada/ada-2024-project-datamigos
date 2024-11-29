from openai import AzureOpenAI
import keyring
import pandas as pd
from src.utils.helpers import *

endpoint = keyring.get_password("AzureOpenAI", "endpoint4omini")
# endpoint = keyring.get_password("AzureOpenAI", "endpoint4o")
key = keyring.get_password("AzureOpenAI", "key4omini")
# key = keyring.get_password("AzureOpenAI", "key4o")

model_name = "gpt-4o"

client = AzureOpenAI(
    azure_endpoint=endpoint, api_version="2024-08-01-preview", api_key=key
)

df = pd.read_csv("data/preprocessed/cleaned_merged_movies.csv")

prompt = "\
You are an expert in movie history and Cold War. You will be given the name of the film, the year and the plot of the movie. You first need to analyse if the movie can be identified to the Eastern or Western bloc during the Cold War. If yes come up with the character or group of character impersonating the Western and Eastern bloc and their values as well as their main archetye.\n\
Your output needs to be parsable comma separated without context (the output needs to start directly), use only keyword and very important use new line character after each of the following:\n\
- Cold War side belonging either Easter, Western or None.\n\
- The character or group of character representing Western bloc with their values and archetype comma separated or None.\n\
- The character or group of character representing Eastern bloc with their values and archetype comma separated or None.\n\
- The Western bloc representation main values and characteristics comma separated or None.\n\
- The Eatern bloc representation main values and characteristics comma separated or None.\n\
- The theme of the movies and keywords.\
"

prompt = "\
You are an expert in movie history and Cold War. You will be given the name of the film, the year and the plot of the movie. You first need to analyse if the movie can be identified to the Eastern or Western bloc during the Cold War. If yes come up with the character or group of character impersonating the Western and Eastern bloc and their values as well as their main archetye.\n\
Your output needs to be parsable comma separated without context (the output needs to start directly), use only keyword and very important use new line character after each of the following:\n\
- Cold War side belonging either Easter, Western or None.\n\
- The character or group of character representing Western bloc with their values and archetype comma separated or None.\n\
- The character or group of character representing Eastern bloc with their values and archetype comma separated or None.\n\
- The Western bloc representation main values and characteristics comma separated or None.\n\
- The Eatern bloc representation main values and characteristics comma separated or None.\n\
- The theme of the movies and keywords.\n\
Example:\n\
Bloc represented \n\
Name Western Character, Value1 Western Character, Value2 Western Character, etc.\n\
Name Eastern Character, Value1 Eastern Character, Value2 Eastern Character, etc.\n\
Value1 Western Bloc , Value2 Western Bloc, etc.\n\
Value1 Eastern Bloc, Value2 Eastern Bloc, etc.\n\
Theme1, keyword1, keyword2, etc.\n\
If it does not belong to any of the blocs, put None.\n\
Based on the structure above, please provide the following information for the movie:\n\
"

responses = []

for index, row in df.iterrows():
    query = create_query_movie(
        prompt,
        row["title"],
        row["release_date"].strftime("%Y-%m-%d"),
        row["plot_summary"],
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": query},
        ],
    )

    print(response.model_dump_json(indent=2))

    responses.append(response)

answer_to_be_parsed = [response.choices[0].message.content for response in responses]

parsed_answers = []

for answer in answer_to_be_parsed:
    parsed_answers.append(parse_gpt_answer(answer))

parsed_answers

# create new columns for each key in the parsed answers and assign the values
subset_prompt_engineering_df = df.assign(
    **{key: [d[key] for d in parsed_answers] for key in parsed_answers[0].keys()}
)
subset_prompt_engineering_df
