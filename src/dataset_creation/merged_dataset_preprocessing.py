import pandas as pd
import numpy as np
import re

from src.utils.helpers import convert_csv
from src.utils.constants import *


def remove_language_suffix(language_set):
    if isinstance(language_set, float):
        return np.nan
    else:
        cleaned_set = {
            re.sub(
                r"[\\\"\']",
                "",  # Remove unwanted characters
                re.sub(
                    r"\blanguages?\b", "", lang, flags=re.IGNORECASE
                ),  # Remove "language"/"languages"
            ).strip()
            for lang in language_set
        }
        return cleaned_set


def preprocess_countries(row):
    countries_representation = {
        "Soviet Union": "Russia",
        "Soviet occupation zone": "Russia",
        "Ukrainian SSR": "Ukraine",
        "Ukranian SSR": "Ukraine",
        "Uzbek SSR": "Uzbekistan",
        "Georgian SSR": "Georgia",
        "West Germany": "Germany",
        "German Democratic Republic": "Germany",
        "East Germany": "Germany",
        "United Kingdom": "United Kingdom",
        "England": "United Kingdom",
        "Wales": "United Kingdom",
        "Scotland": "United Kingdom",
        "Northern Ireland": "United Kingdom",
        "Socialist Federal Republic of Yugoslavia": "Yugoslavia",
        "Federal Republic of Yugoslavia": "Yugoslavia",
        "Republic of China": "Taiwan",
        "South Korea": "Korea",
        "North Korea": "Korea",
        "Kingdom of Italy": "Italy",
        "Republic of Macedonia": "Macedonia",
        "Libyan Arab Jamahiriya": "Libya",
        "Cote DIvoire": "Côte d'Ivoire",
        "Kingdom of Great Britain": "United Kingdom",
        "Malayalam Language": "India",
        "Syrian Arab Republic": "Syria",
        "Kyrgyz Republic": "Kyrgyzstan",
        "Slovak Republic": "Czechoslovakia",
    }
    # row['countries'] = clean_column_values(row['countries'])
    row["countries"] = (
        set(
            [
                countries_representation.get(string, string)
                for string in row["countries"]
            ]
        )
        if isinstance(row["countries"], list)
        else row["countries"]
    )
    # convert back to list
    row["countries"] = (
        list(row["countries"])
        if isinstance(row["countries"], set)
        else row["countries"]
    )
    return row


def create_preprocessed_movies():
    movies = pd.read_csv(DATA_FOLDER_PREPROCESSED + "v2_movies_cleaned.csv")

    movies = convert_csv(movies)

    movies = movies.apply(preprocess_countries, axis=1)

    languages_translation = {
        "广州话/廣州話": "Chinese",
        "广州话 / 廣州話": "Chinese",
        "日本語": "Japanese",
        "Japan": "Japanese",
        "普通话": "Chinese",
        "한국어/조선말": "Korean",
        "ภาษาไทย": "Thai",
        "हिन्दी": "Indian",
        "தமிழ்": "Indian",
        "TiếngViệt": "Vietnamese",
        "Tiếng Việt": "Vietnamese",
        "العربية": "Arabic",
        "اردو": "Indian",
        "българскиезик": "Bulgarian",
        "Pусский": "Russian",
        "беларускаямова": "Belarusian",
        "Український": "Ukrainian",
        "Srpski": "Serbian",
        "Slovenčina": "Slovak",
        "Français": "French",
        "France": "French",
        "Deutsch": "German",
        "Italiano": "Italian",
        "Español": "Spanish",
        "Polski": "Polish",
        "Standard Mandarin": "Chinese",
        "Mandarin Chinese": "Chinese",
        "Mandarin": "Chinese",
        "Português": "Portuguese",
        "Standard Cantonese": "Chinese",
        "Cantonese": "Chinese",
        "suomi": "Finnish",
        "Magyar": "Hungarian",
        "Bosanski": "Bosnian",
        "svenska": "Swedish",
        "ελληνικά": "Greek",
        "Český": "Czech",
        "Dansk": "Danish",
        "Nederlands": "Dutch",
        "עִבְרִית": "Hebrew",
        "American English": "English",
        "Türkçe": "Turkish",
        "Tagalog": "Filipino",
        "Khmer": "Cambodian",
        "Hindi": "Indian",
        "Tamil": "Indian",
        "Telugu": "Indian",
        "Urdu": "Indian",
        "Oriya": "Indian",
        "Eesti": "Estonian",
        "Română": "Romanian",
        "Romani": "Romanian",
        "Norsk": "Norwegian",
        "No": "Norwegian",
        "Íslenska": "Icelandic",
        "Bahasa indonesia": "Indonesian",
        "Català": "Spanish",
        "Inuktitut": "Inuit",
        "Hakka": "Chinese",
        "Sicilian": "Italian",
        "Marathi": "Indian",
        "Hrvatski": "Croatian",
        "shqip": "Albanian",
        "isiZulu": "Zulu",
        "Latviešu": "Latvian",
        "ქართული": "Georgian",
        "Australian English": "English",
        "Bahasamelayu": "Malay",
        "Lietuvi\\x9akai".encode("latin1").decode(
            "unicode_escape"
        ): "Lithuanian",  # \x9a is an escape sequence
        "Farsi, Western": "Persian",
        "فارسی": "Persian",
        "беларуская мова": "Belarusian",
        "български език": "Bulgarian",
        "Swiss German": "German",
        "Brazilian Portuguese": "Portuguese",
        "euskera": "Basque",
        "қазақ": "Kazakh",
        "Bahasa melayu": "Malay",
        "French Sign": "Sign Language",
        "American Sign": "Sign Language",
        "Hokkien": "Chinese",
        "Min Nan": "Chinese",
        "Chinese, Hakka": "Chinese",
        "Ancient Greek": "Greek",
        "Gaelic": "Scottish Gaelic",
        "Scottish Gaelic": "Scottish Gaelic",
        "Zulu": "Zulu",
        "Lithuanian": "Lithuanian",
        "Standard Tibetan": "Tibetan",
        "Saami, North": "Sami",
        "Bamanankan": "Bambara",
        "Fulfulde, Adamawa": "Fula",
        "Brazilian Portuguese": "Portuguese",
        "South African English": "English",
        "Jamaican Creole English": "Jamaican Creole",
        "Classical Arabic": "Arabic",
        "Frisian, Western": "Frisian",
        "Yolngu Matha": "Yolngu Matha",
        "Cheyenne": "Cheyenne",
        "Crow": "Crow",
        "Scanian": "Swedish",
        "Palawa kani": "Palawa kani",
        "Kiswahili": "Swahili",
        "Māori": "Maori",
        "বাংলা": "Bengali",
        "తెలుగు": "Indian",
        "Taiwanese": "Chinese",
        "Shanghainese": "Chinese",
        "Azərbaycan": "Azerbaijani",
        "Cymraeg": "Welsh",
        "Hariyani": "Indian",
        "Slovenščina": "Slovenian",
        "Maya, Yucatán": "Maya",
        "Egyptian Arabic": "Arabic",
        "Assyrian Neo-Aramaic": "Aramaic",
        "Crow": "Native American languages",
        "Cheyenne": "Native American languages",
        "Hopi": "Native American languages",
        "Pawnee": "Native American languages",
        "Mohawk": "Native American languages",
        "Algonquin": "Native American languages",
        "Cree": "Native American languages",
        "Navajo": "Native American languages",
        "Sioux": "Native American languages",
        "Khmer, Central": "Cambodian",
    }

    movies["languages"] = movies["languages"].apply(remove_language_suffix)

    movies["languages"] = movies["languages"].apply(
        lambda x: (
            set([languages_translation.get(string, string) for string in x])
            if isinstance(x, set)
            else x
        )
    )

    movies["languages"] = movies["languages"].apply(
        lambda x: (
            [lang for lang in x if lang != "" and pd.notna(lang) and lang != "??????"]
            if isinstance(x, set)
            else x
        )
    )

    movies = movies.drop(
        columns=["wikipedia_id", "freebase_id", "keywords", "runtime", "plot_summary"]
    )

    movies["cold_war_side"] = movies["cold_war_side"].apply(lambda x: f'"{x}"')

    movies.to_csv(PREPROCESSED_MOVIES, index=False)

    return movies


if __name__ == "__main__":
    create_preprocessed_movies()
