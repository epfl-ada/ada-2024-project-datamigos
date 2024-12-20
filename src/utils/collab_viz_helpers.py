import numpy as np
from collections import Counter
from itertools import combinations
from src.utils.constants import *

# Have been generated with GPT
COUNTRY_COORDS = {
    'United States of America': (37.0902, -95.7129),
    'Italy': (41.8719, 12.5674),
    'Germany': (51.1657, 10.4515),
    'Russia': (61.5240, 105.3188),
    'Hungary': (47.1625, 19.5033),
    'Estonia': (58.5953, 25.0136),
    'Ukraine': (48.3794, 31.1656),
    'Switzerland': (46.8182, 8.2275),
    'Puerto Rico': (18.2208, -66.5901),
    'France': (46.6034, 1.8883),
    'Egypt': (26.8206, 30.8025),
    'Netherlands': (52.1326, 5.2913),
    'Japan': (36.2048, 138.2529),
    'United Kingdom': (55.3781, -3.4360),
    'Hong Kong': (22.3193, 114.1694),
    'India': (20.5937, 78.9629),
    'Spain': (40.4637, -3.7492),
    'Costa Rica': (9.7489, -83.7534),
    'Vietnam': (14.0583, 108.2772),
    'Taiwan': (23.6978, 120.9605),
    'Australia': (-25.2744, 133.7751),
    'Canada': (56.1304, -106.3468),
    'Latvia': (56.8796, 24.6032),
    'Brazil': (-14.2350, -51.9253),
    'Turkey': (38.9637, 35.2433),
    'Denmark': (56.2639, 9.5018),
    'Poland': (51.9194, 19.1451),
    'Korea': (35.9078, 127.7669),
    'Norway': (60.4720, 8.4689),
    'Croatia': (45.1, 15.2),
    'Bulgaria': (42.7339, 25.4858),
    'Austria': (47.5162, 14.5501),
    'Philippines': (12.8797, 121.7740),
    'Lithuania': (55.1694, 23.8813),
    'Portugal': (39.3999, -8.2245),
    'China': (35.8617, 104.1954),
    'Romania': (45.9432, 24.9668),
    'Georgia': (42.3154, 43.3569),
    'Yugoslavia': (44.0165, 21.0059),
    'New Zealand': (-40.9006, 174.8860),
    'Czechoslovakia': (49.8175, 15.4729),
    'Argentina': (-38.4161, -63.6167),
    'Greece': (39.0742, 21.8243),
    'South Africa': (-30.5595, 22.9375),
    'Luxembourg': (49.8153, 6.1296),
    'Sweden': (60.1282, 18.6435),
    'Ireland': (53.1424, -7.6921),
    'Colombia': (4.5709, -74.2973),
    'Uruguay': (-32.5228, -55.7658),
    'Belgium': (50.5039, 4.4699),
    'Czech Republic': (49.8175, 15.4729),
    'Bangladesh': (23.6850, 90.3563),
    'Tunisia': (33.8869, 9.5375),
    'Albania': (41.1533, 20.1683),
    'Finland': (61.9241, 25.7482),
    'Iceland': (64.9631, -19.0208),
    'Liechtenstein': (47.1660, 9.5554),
    'Mexico': (23.6345, -102.5528),
    'Iran': (32.4279, 53.6880),
    'Zimbabwe': (-19.0154, 29.1549),
    'Nepal': (28.3949, 84.1240),
    'Uzbekistan': (41.3775, 64.5853),
    'Venezuela': (6.4238, -66.5897),
    'Bosnia and Herzegovina': (43.9159, 17.6791),
    'Cuba': (21.5218, -77.7812),
    'Peru': (-9.1899, -75.0152),
    'Malaysia': (4.2105, 101.9758),
    'Pakistan': (30.3753, 69.3451),
    'Sri Lanka': (7.8731, 80.7718),
    'Algeria': (28.0339, 1.6596),
    'Israel': (31.0461, 34.8516),
    'Singapore': (1.3521, 103.8198),
    'Morocco': (31.7917, -7.0926),
    'Azerbaijan': (40.1431, 47.5769),
    'Bolivia': (-16.2902, -63.5887),
    'Cameroon': (7.3697, 12.3547),
    'Serbia': (44.0165, 21.0059),
    'Mali': (17.5707, -3.9962),
    'Macedonia': (41.6086, 21.7453),
    'Monaco': (43.7384, 7.4246),
    'Slovakia': (48.6690, 19.6990),
    'Senegal': (14.4974, -14.4524),
    'Qatar': (25.2760, 51.2148),
    'Thailand': (15.8700, 100.9925),
    "Cote D'Ivoire": (7.5399, -5.5471),
    'Belarus': (53.7098, 27.9534),
    'Armenia': (40.0691, 45.0382),
    'Chile': (-35.6751, -71.5430),
    'Cambodia': (12.5657, 104.9910),
    'Ghana': (7.9465, -1.0232),
    'Jamaica': (18.1096, -77.2975),
    'Slovenia': (46.1512, 14.9955),
    'Guinea': (9.9456, -9.6966),
    'Afghanistan': (33.9391, 67.7100),
    'Democratic Republic of the Congo': (-4.0383, 21.7587),
    'Indonesia': (-0.7893, 113.9213),
    'Montenegro': (42.7087, 19.3744),
    'Namibia': (-22.9576, 18.4904),
    'Moldova': (47.4116, 28.3699),
    'Panama': (8.5379, -80.7821),
    'Burkina Faso': (12.2383, -1.5616),
    'Aruba': (12.5211, -69.9683),
    'Ethiopia': (9.145, 40.4897),
    'Jordan': (30.5852, 36.2384),
    'Kazakhstan': (48.0196, 66.9237),
    'Nigeria': (9.0820, 8.6753),
    'Libya': (26.3351, 17.2283),
    'Congo': (-0.2280, 15.8277),
    'Turkmenistan': (38.9697, 59.5563),
    'Bhutan': (27.5142, 90.4336),
    'Kuwait': (29.3117, 47.4818),
    'Lebanon': (33.8547, 35.8623),
    'Guinea-Bissau': (11.8037, -15.1804),
    'Mauritania': (21.0079, -10.9408),
    'Angola': (-11.2027, 17.8739),
    'Burma': (21.9162, 95.9560),
    'Martinique': (14.6415, -61.0242),
    'Trinidad and Tobago': (10.6918, -61.2225),
    'Bahrain': (26.0667, 50.5577),
    'Syria': (34.8021, 38.9968),
    'Kyrgyzstan': (41.2044, 74.7661),
    'Botswana': (-22.3285, 24.6849),
    'Zambia': (-13.1339, 27.8493),
    'Bahamas': (25.0343, -77.3963),
    'Papua New Guinea': (-6.3149, 143.9555),
    'Ecuador': (-1.8312, -78.1834),
    'Palestinian Territory': (31.9522, 35.2332)
}

COLOR_MAPPING = {'Western': f'rgb({COLOR_SCALE_RGB["Deep Blue"][0]}, {COLOR_SCALE_RGB["Deep Blue"][1]}, {COLOR_SCALE_RGB["Deep Blue"][2]})',
                 'Eastern': f'rgb({COLOR_SCALE_RGB["Deep Red"][0]}, {COLOR_SCALE_RGB["Deep Red"][1]}, {COLOR_SCALE_RGB["Deep Red"][2]})',
                 'None': f'rgb({NEUTRAL_COLORS_RGB["Neutral Light"][0]}, {NEUTRAL_COLORS_RGB["Neutral Light"][1]}, {NEUTRAL_COLORS_RGB["Neutral Light"][2]})', 
                 'Lack of data': f'rgb({DISTINCT_COLORS_RGB["Yellow"][0]}, {DISTINCT_COLORS_RGB["Yellow"][1]}, {DISTINCT_COLORS_RGB["Yellow"][2]})'}

def compute_counts(movies_df, min_nb_movies=0, min_nb_collab=0):
    country_film_count = Counter()
    collaboration_count = Counter()

    # Count for the number of movies produced by each country and the number of collaboration 
    # between every tuple of countries if their is.
    for countries in movies_df['countries']:
        country_film_count.update(countries)
        for pair in combinations(countries, 2):
            collaboration_count[tuple(sorted(pair))] += 1
    
    # Filter to keep only the countries that have produced a minimum number of movies
    country_film_count = {k: v for k, v in country_film_count.items() if v > min_nb_movies}

    # Apply a root scale to reduce the divergence between the values
    root_film_count = {country: np.sqrt(count) for country, count in country_film_count.items()}

    # Get the remaining countries
    countries = list(root_film_count.keys())

    # Filter to keep only the collaboration that have happened more than a minimum number of time
    # and we make sure we have the same countries than the one in our `countries` list 
    collaboration_count = {k: v for k, v in collaboration_count.items() if v > min_nb_collab}
    collaboration_count = {k: v for k, v in collaboration_count.items() if k[0] in countries and k[1] in countries}

    return countries, root_film_count, collaboration_count
