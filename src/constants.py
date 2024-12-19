DATA_FOLDER = "data/"
DATA_FOLDER_RAW = DATA_FOLDER + "raw/"
DATA_FOLDER_PREPROCESSED = DATA_FOLDER + "preprocessed/"

PREPROCESSED_MOVIES = DATA_FOLDER_PREPROCESSED + "preprocessed_movies.csv"

PROMPT_ENGINEERING = DATA_FOLDER_RAW + "PromptEngineering/"

DATA_FOLDER_CMU = DATA_FOLDER_RAW + "MovieSummaries/"
DATA_FOLDER_TMDB = DATA_FOLDER_RAW + "TMDb/"
DATA_FOLDER_IMDB = DATA_FOLDER_RAW + "IMDb/"

CMU_CHARACTER = DATA_FOLDER_CMU + "character.metadata.tsv"
CMU_MOVIE = DATA_FOLDER_CMU + "movie.metadata.tsv"
PLOT_SUMMARIES = DATA_FOLDER_CMU + "plot_summaries.txt"

TMDB_MOVIE = DATA_FOLDER_TMDB + "movies_metadata.csv"
TMDB_KEYWORDS = DATA_FOLDER_TMDB + "keywords.csv"

# Download them on: https://datasets.imdbws.com/
IMDB_AKA = DATA_FOLDER_IMDB + "title.akas.tsv"
IMDB_BASIC = DATA_FOLDER_IMDB + "title.basics.tsv"

# COLOR SETS
# Scale West to East
COLOR_SCALE = [
    "#BD0032",  #Deep Red - East Side
    "#F7514B",  #Red
    "#FEB3A6",  #Light Red
    "#F2F2F2",  #Neutral Middle
    "#A0CBE8",  #Light Blue
    "#5C8DB8",  #Blue
    "#1C5EA9"   #Deep Blue - West Side
]

# Neutral colors
NEUTRAL_COLORS = {
    "#000010",  # Darkest Neutral
    "#59585B",
    "#BBB9B9",
    "#F2F2F2"   # Lightest Neutral
}

# Distinct colors
DISTINCT_COLORS = [
    "#000000",
    "#06DD95",
    "#98E144",
    "#FFE989",
    "#F1AB79",
    "#4BAE9A",
    "#7FB112",
    "#F0FE41",
    "#FAC82B",
    "#F58634"
]