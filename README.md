
# The Iron Curtain's Dirty Movie Secrets!

*During the Cold War, both the Western and Eastern blocs relied on soft power to spread ideological messages and influence global opinion, with cinema emerging as a key medium for this influence. Our project is driven by a desire to explore how cinema served as a subtle but potent tool for political messaging during this period. We are particularly interested in how cinema can not only entertain but also embed ideologies, shape public views, and reflect the values and power dynamics of its time. By analyzing Cold War-era films, we aim to reveal how character archetypes, narratives, and themes were crafted to convey and promote specific ideologies, as well as to understand whether these films mirrored societal beliefs or aimed to actively mold public opinion. To what extent did Cold War cinema serve as a tool for ideological persuasion?*

## Research Questions

**1. Global and National Trends**

- Are the different stakeholders distributing their films nationaly or also internationally? If so, to which countries and in what languages? Can this distribution reveal spheres of influence for the Eastern and Western Blocs?
- How did the popularity of genres and narrative themes change throughout the Cold War? Did new concepts or styles emerge?
- To what extent did these shifts mirror specific historical events or changes in the political landscape?

**2. Character Archetypes**

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
    - When possible, populate NaN using data from the supplementary datasets.
    - Do median imputation or drop certain rows depending on NaN.
- Perform film selection by focusing on the Cold War period. We'll also examining pre-Cold War productions to identify potential evolutions.

**2. Prompt engineering**

- Use prompt engineering based on title and plot to get info such as:
    - Main characters and their archetype.
    - If the movie promotes values from the Easter or Western bloc.
    - Which part of the population is targeted?
    - Themes represented in the movie.
- After crafting the prompt we would give it to the OpenAI GPT 4o API to get a parsable output to create new columns in our dataset.

**3. Visualizations:**

- Illustrate regions with the highest concentration of film releases using a heatmap.
- Map language distribution to highlight dominant languages across regions, potentially revealing patterns of cultural or political influence.
- Utilize a tool like [Leaflet.js](https://leafletjs.com) to create interactive maps that visualize our data analysis, allowing users to explore geographical trends in film distribution.

**4. Clustering for Influence Zones:**

- Apply soft clustering algorithms based on language, country, and film origin to group countries with similar release patterns or language preferences. This approach will help identify influence zones or cultural clusters associated with each bloc.
- Statistical Analysis: use revenue value to assess movies popularity. Understanding a film's popularity will help us assess its impact on audiences, allowing us to develop an "influence metric."

**5. Trend analysis:**

- Track the development of movie themes to observe how popular genres or topics shifted in response to Cold War events.
- Using movie release dates, we can identify periods where specific genres surged. We can map genre trends to historical events using time series analysis. We could also look at the number of movies released internationally versus nationally by each bloc. This may reveal periods when one bloc attempted to expand its influence (e.g., the Space Race, the Vietnam War).

## Timeline

2024.11.15 (1) Data Preprocessing & Initial Exploratory Data Analysis

2024.11.22 (2) Finish enriching our dataset with prompt engeneering

2024.11.29 (3) Visulaization + (5.1) Track Evolution of movie genres/topics

2024.12.06 (4) Clustering task + (5.2) time series analysis 

2024.12.20 Website and Data Story 

## Team organization

|Member | Contribution |
|--------|--------------|
|Mehdi | <ol><li>Data Integration & Cleaning</li><li>Prompt Engineering</li><li>Clustering for Influence Zones</li></ol>|
|Mattéo | <ol><li>Data Integration & Cleaning</li><li>Prompt Engineering</li><li>Trend analysis</li></ol>|
|Fanny     | <ol><li>Data Integration & Cleaning</li><li>Visualizations</li><li>Trend analysis</li><ol>|
|Karim     |<ol><li>Data Integration & Cleaning</li><li>Clustering for Influence Zones</li><ol>|
|Martin | <ol><li>Data Integration & Cleaning</li><li>Visualizations</li><li>Website</li></ol>|

## Project Structure

- 📂`data`:
    - 📂`preprocessed`: 
      - `soviet_movies.tsv`: generated in milestone_2.ipynb
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

- 📂`src`:
    - 📂`utils`: Directory for the utilities files containing functions used in the notebooks.
- `milestone_2.ipynb`: Main notebook for Milestone 2.
- `README.md`: Main documentation file of the repository
