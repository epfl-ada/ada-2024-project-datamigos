DATA_FOLDER = "data/"
DATA_FOLDER_RAW = DATA_FOLDER + "raw/"
DATA_FOLDER_PREPROCESSED = DATA_FOLDER + "preprocessed/"

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

EASTERN_COLOR = '#DD3C32'
WESTERN_COLOR = '#0F89E6'
NEUTRAL_COLOR = '#C2C7D6'