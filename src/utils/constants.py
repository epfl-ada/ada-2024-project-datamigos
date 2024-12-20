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
NEUTRAL_COLORS = [
    "#000010",  # Darkest Neutral
    "#59585B",
    "#BBB9B9",
    "#F2F2F2"   # Lightest Neutral
]

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

# COLOR SETS in RGB
# Scale West to East
COLOR_SCALE_RGB = {
    "Deep Red": (189, 0, 50),
    "Red": (247, 81, 75),
    "Light Red": (254, 179, 166),
    "Neutral Middle": (242, 242, 242),
    "Light Blue": (160, 203, 232),
    "Blue": (92, 141, 184),
    "Deep Blue": (28, 94, 169)
}

# Neutral colors
NEUTRAL_COLORS_RGB = {
    "Darkest Neutral": (0, 0, 16),
    "Neutral Dark": (89, 88, 91),
    "Neutral Light": (187, 185, 185),
    "Lightest Neutral": (242, 242, 242)
}

# Distinct colors
DISTINCT_COLORS_RGB = {
    "Black": (0, 0, 0),
    "Green": (6, 221, 149),
    "Yellow Green": (152, 225, 68),
    "Yellow": (255, 233, 137),
    "Light Orange": (241, 171, 121),
    "Teal": (75, 174, 154),
    "Olive": (127, 177, 18),
    "Lime": (240, 254, 65),
    "Gold": (250, 200, 43),
    "Orange": (245, 134, 52)
}