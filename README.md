
# The Iron Curtain's Dirty Movie Secrets!

*During the Cold War, both the Western and Eastern blocs relied on soft power to spread ideological messages and influence global opinion, with cinema emerging as a key medium for this influence. Our project is driven by a desire to explore how cinema served as a subtle but potent tool for political messaging during this period. We are particularly interested in how cinema can not only entertain but also embed ideologies, shape public views, and reflect the values and power dynamics of its time. By analyzing Cold War-era films, we aim to reveal how character archetypes, narratives, and themes were crafted to convey and promote specific ideologies, as well as to understand whether these films mirrored societal beliefs or aimed to actively mold public opinion. To what extent did Cold War cinema serve as a tool for ideological persuasion?*

## Data Story

Find our data story with the final analysis and visualizations on the  website [here](https://m-rollet.github.io).

## Research Questions

**1. Global and National Trends**

- Are the different stakeholders distributing their films nationaly or also internationally? If so, to which countries and in what languages? Can this distribution reveal spheres of influence for the Eastern and Western Blocs?

**2. Genre and Narrative Trends**

- How did the popularity of genres and narrative themes change throughout the Cold War? What can it tell us about the cultural and political climate of the time?
- To what extent did these shifts mirror specific historical events or changes in the political landscape?

**3. Character Archetypes**

- Are new character archetypes emerging, are there recurring types? Do they communicate particular ideologies? In which productions are they most prevalent?
- In what ways do their ideological messaging differ between Blocs?

## Datasets

- [The CMU Movie Corpus](https://www.cs.cmu.edu/~ark/personas/): Our initial dataset consisting of 42,306 movies extracted from Wikipedia and aligned metadata extracted from Freebase.
- [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset): Metadata for 45,000 films listed in the Full MovieLens Dataset, all of which were released on or before July 2017. We will use this dataset, specifically the movies_metadata.csv file, primarily to fill in missing revenue values. Additionally, this dataset includes plot keywords (keywords.csv), which could be helpful for analyzing and clustering movie plots.
- [IMDB Non-Commercial Dataset](https://developer.imdb.com/non-commercial-datasets/) is a database containing over 50 Million movies from different regions, which allows us to complement our initial dataset specifically with movies created in the Soviet Union during the cold war. In addition, using the IMDB API and the IMDbPY Package, we can extract the plot to fix the issues of imbalance (The CMU Movie Summaries data being largely focused on the US).

## Methods

**1. Data Integration & Cleaning**

- Integrate the additional datasets.
- Adjust certain columns to a compatible format (converting time-related data to a consistent format).
- Exclude extreme or inconsistent entries.
- Handling NaN:
    When possible, populate NaN using data from the supplementary datasets. 
- Perform film selection by focusing on the Cold War period. 

**2. Prompt engineering**

- Use prompt engineering based on title and plot to get info such as:
    - Main characters and their archetypes.
    - If the movie promotes values from the Eastern or Western bloc.
    - Themes represented in the movie.
- After crafting the prompt we would give it to the OpenAI GPT 4o API to get a parsable output to create new columns in our dataset.

**3. Visualizations:**

- Illustrate regions with the highest concentration of film releases using a heatmap.
- Utilize a tool like [Leaflet.js](https://leafletjs.com) to create interactive maps that visualize our data analysis, allowing users to explore geographical trends in film distribution.
- Create a network graph to visualize the connections between countries based on the number of collaborations in film production.
- Map language distribution to highlight dominant languages across regions, potentially revealing patterns of cultural or political influence.

**4. Themes and genres analysis:**

- Study the differences in genre popularity between the Eastern and Western blocs by plotting the number of movies released per genre across both blocs and how they evolved over time. 
- Study themes present specifically in War Movies to find the differences in the portrayal of war between the two blocs.
- Relative difference was used to point out genres and themes that appear much more frequently in one side over the other.
- Theme topic detection: Use Latent Dirichelet Allocation to identify recurring themes in movies from each bloc. Identifying the influence of political events as well as cultural differences between the two blocs.

**5. Characters analysis:**

- Character archetype detection: Use Latent Dirichelet Allocation to identify recurring character archetypes in movies from each bloc, potentially revealing differences in how friendly and antagonistic characters were portrayal between the Eastern and Western blocs.
- Sementical analysis to study th evolution of the themes embodied by the characters accross the Cold War.


## Team organization

|Member | Contribution |
|--------|--------------|
|Mehdi | <ol><li>Data Integration & Cleaning</li><li>Visualization</li><li>Clustering for Influence Zones</li></ol>|
|Mattéo | <ol><li>Data Integration & Cleaning</li><li>Prompt Engineering</li><li>Theme Topic Detection</li></ol>|
|Fanny     | <ol><li>Data Integration & Cleaning</li><li>Visualization</li><li>Characters Analysis</li><li>Data Story</li><ol>|
|Karim     |<ol><li>Data Integration & Cleaning</li><li>Themes and genre Analysis</li><ol>|
|Martin | <ol><li>Data Integration & Cleaning</li><li>Visualizations</li><li>Website</li></ol>|

## Project Structure

- 📂`data`:
    - 📂`preprocessed`: datasets after each step of merging resulting in `preprocessed_movies.csv` as the final cleaned and augmented dataset. 
    -  📂`raw`:
          - 📂 `MovieSummaries`:
            - `character.metadata.tsv`: Original character metadata.
            - `movie.metadata.tsv`: Initial movie metadata file.
            - `name.clusters.txt`: Text file containing name clusters.
            - `plot_summaries.txt`: Raw text files of movie plot summaries.
            - `README.txt`: Descriptive file providing details about the CMU Dataset.
            - `tvtropes.clusters.txt`: Cluster data related to TV tropes.
          - 📂`TMDb`:
              - `keywords.csv`
              - `movies_metadata.csv`
          - 📂 `IMDb`: File Sizes too Large, manually install from https://datasets.imdbws.com/
            - `title.akas.tsv`
            - `basics.akas.tsv`
    - 📂`PNGs`
    - 📂`web_export`: the HTML files used to make the website
- 📂`src`:
    - 📂`analysis`: All scripts for the whole data analysis called in the main notebook
    - 📂`dataset_creation`: All scripts to merge, clean and augment the data to create the final dataset `preprocessed_movies.csv`
    - 📂`prompt_engineering`: Script and prompt to call the API and create new columns in our dataset with OpenAI GPT
    - 📂`utils`: Utilities files containing constants and recurrent functions used across the project.
- `results.ipynb`: Main notebook containing the whole data analysis and visualizations.
- `README.md`: Main documentation file of the repository
- `requirements.txt`: File containing all the dependencies needed to run the project.
