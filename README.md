
# The Iron Curtain's Dirty Movie Secrets!

*During the Cold War, both the Western and Eastern blocs relied on soft power to spread ideological messages and influence global opinion, with cinema emerging as a key medium for this influence. Our project is driven by a desire to explore how cinema served as a subtle but potent tool for political messaging during this period. We are particularly interested in how cinema can not only entertain but also embed ideologies, shape public views, and reflect the values and power dynamics of its time. By analyzing Cold War-era films, we aim to reveal how character archetypes, narratives, and themes were crafted to convey and promote specific ideologies, as well as to understand whether these films mirrored societal beliefs or aimed to actively mold public opinion. To what extent did Cold War cinema serve as a tool for ideological persuasion?*

## Research Questions

**1. Global and National Trends**

- Are the different stakeholders distributing their films nationaly or also internationally? If so, to which countries and in what languages? Can this distribution reveal spheres of influence for the Eastern and Western Blocs?
- How did the popularity of genres and narrative themes change throughout the Cold War? Did new concepts or styles emerge?
- To what extent did these shifts mirror specific historical events or changes in the political landscape climate?

**2. Character Archetypes**

- Are new character archetypes emerging, are there recurring types? Do these archetypes communicate particular ideologies? In which productions are they most prevalent?
- In what ways do the portrayal and ideological messaging of these archetypes differ between the Eastern and Western Blocs?


## Datasets

- [The CMU Movie Corpus](https://www.cs.cmu.edu/~ark/personas/) is the dataset around which we are building our project. It has been created by David Bamman, Brendan O'Connor, and Noah Smith at the Language Technologies Institute and Machine Learning Department at Carnegie Mellon University.

- [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) contains metadata for 45,000 films listed in the Full MovieLens Dataset, all of which were released on or before July 2017. We will use this dataset, specifically the movies_metadata.csv file, primarily to fill in missing revenue values, as approximately 90% of revenue data is absent in the CMU movie dataset. Additionally, this dataset includes plot keywords (in the keywords.csv file), which could be helpful for analyzing and clustering movie plots.
- [IMDB Non-Commercial Dataset](https://developer.imdb.com/non-commercial-datasets/) is a giant database containing over 50 Million movies from different regions, which allows us to complement our initial dataset specifically with movies created in the Soviet Union during the cold war. In addition, using the IMDB API and the IMDbPY Package, we can extract the plot to fix the issues of imbalance (The CMU Movie Summaries data being largely focused on the United States)

## Methods

**1. Data Integration & Cleaning**

- Integrate the additional datasets to enrich our primary dataset.
- Adjust certain columns to a compatible format, such as converting time-related data to a consistent date format.
- Exclude extreme or inconsistent data entries, such as movies with durations exceeding 5 hours.
- Handling Missing Data:
    - Where possible, populate missing values using data from the supplementary datasets.
    - Perform value imputation when it is pertienent, such as the duration column with the median, as film lengths within a given historical period are generally stable.
    - Omit records with missing values to preserve analytical accuracy, such as the revenue, due to it's high variability and the estimation challenges.
    - Omit problematic features if they aren't that much relevant for our study case. 
- Perform film selection by focusing on the Cold War period. We'll also examining pre-Cold War productions to identify potential evolutions by the onset of the Cold War.

**2. Prompt engineering**

- Use prompt engineering based on title and plot to get info such as:
    - Main characters and their archetype
    - If the movie promotes values from the Easter or Western bloc
    - What part of the population is targeted? Age? Social class?
    - Some keywords about the movies (genre, themes represented)
- After crafting the prompt we would give it to the OpenAI GPT 4o API to get a parsable output to create new columns in our dataset.

**3. Visualizations:**

- Illustrate regions with the highest concentration of film releases from each bloc’s origin country, segmented by genre to show preferences and trends, using a heatmap.
- Map language distribution to highlight dominant languages across regions, potentially revealing patterns of cultural or political influence.

**4. Clustering for Influence Zones:**

- Apply soft clustering algorithms based on language, country, and film origin to group countries with similar release patterns or language preferences. This approach will help identify influence zones or cultural clusters associated with each bloc.
- Perform Network Analysis by treating each country as a node and each movie release as an edge. This could help highlight which countries served as cultural bridges or showed dual influences from both blocs.
- Statistical Analysis: use revenue value to assess movies popularity. Understanding a film's popularity will help us assess its impact on audiences, allowing us to develop an "influence metric."

**5. Trend analysis:**

- Track the development of movie themes to observe how popular genres or topics shifted in response to Cold War events.
- Using movie release dates, we can identify periods where specific genres surged. We can map genre trends to historical events using time series analysis. We could also look at the number of movies released internationally versus nationally by each bloc. This may reveal periods when one bloc attempted to expand its influence (e.g., the Space Race, the Vietnam War).

## Timeline

## Team organization

|Member | Contribution |
|--------|--------------|
|Mehdi | <ol><li>Data Integration & Cleaning</li></ol>|
|Mattéo | <ol><li>Data Integration & Cleaning</li></ol>|
|Fanny     | <ol><li>Data Integration & Cleaning</li><ol>|
|Karim     |<ol><li>Data Integration & Cleaning</li><ol>|
|Martin | <ol><li>Data Integration & Cleaning</li></ol>|

## Question

What do you think about our title 👉👈 ?

## Project Structure

- 📂`data`:
     - `character.metadata.tsv`: Original character metadata.
    - `movie.metadata.tsv`: Initial movie metadata file.
    - `name.clusters.txt`: Text file containing name clusters.
    - `plot_summaries.txt`: Raw text files of movie plot summaries.
    - `README.txt`: Descriptive file providing details about the CMU Dataset.
    - `tvtropes.clusters.txt`: Cluster data related to TV tropes.
- 📂`src`:
    - 📂`models`: Model directory
    - 📂`utils`: Directory for the utilities files containing functions used in the notebooks.
- 📂`tests`: Tests of any kind
- `milestone_2.ipynb`: Main notebook for Milestone 2.
- `README.md`: Main documentation file of the repository
