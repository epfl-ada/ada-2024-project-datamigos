import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

import spacy
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from collections import Counter

VOC_MAPPING = {
    'anti-': 'anti',
    'anti ': 'anti',
    'anti hero': 'antihero',
    'archetypes': 'archetype',
    'archetype:': 'archetype',
    'archetypal': 'archetype',
    'authoritarianism': 'authoritarian'
}

# Function to split the row list into character name and character representation
def extract_character_name_and_attributes(row):
    if isinstance(row, list) and len(row) > 0 and row[0] is not None:
        character_name = row[0]
        character_representation = row[1:]
        return pd.Series([character_name, character_representation])
    else:
        return pd.Series([None, None])

# Function to apply the mapping with substring matching
def apply_mapping_with_substrings(string_list, mapping):
    updated = []
    for s in string_list:
        new_s = s
        for key, value in mapping.items():
            if key in s:
                new_s = s.replace(key, value)
        updated.append(new_s.lower())
    return updated

def create_character_df(original_df, character_column, character_side):
    """
    Create a dataframe that will be used for the analysis of movies' characters

    Parameters:
    - original_df: the original dataframe containing the movies' information
    - character_column: the column containing the characters' information
    - character_side: the side which the character chacter represent (East or West)

    Returns:
    - new_df: the dataframe that will be used for the analysis of movies' characters
    """

    # create the new dataframe
    new_df = original_df[[character_column, 'cold_war_side', 'title', 'release_date']]
    new_df = new_df.rename(columns={'cold_war_side': 'movie_side'})
    new_df[['character_name', 'character_representation']] = \
        new_df[character_column].apply(extract_character_name_and_attributes)
    new_df = new_df.drop(columns=[character_column])
    new_df['character_side'] = character_side

    # clean the obtained dataframe
    new_df = new_df.drop_duplicates(subset=['character_name'])
    new_df = new_df[new_df['character_representation'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False)]
    new_df = new_df[new_df['character_name'].apply(lambda x: len(x.split()) if isinstance(x, str) else 0) <= 5]
    new_df['character_representation'] = new_df['character_representation'].apply(
        lambda x: apply_mapping_with_substrings(x, VOC_MAPPING)
    )
    return new_df

def preprocess_char_repres(string_list, nlp, words_to_remove):
    """
    Preprocess character representations to use them in the topic detection model

    Parameters:
    - string_list: the list of character representations
    - nlp: the spacy nlp model
    - words_to_remove: the list of words to remove from the character representations

    Returns:
    - tokens: the list of tokens obtained after preprocessing
    """
    # personalize the stop words
    stop_words = set(stopwords.words('english')).union(words_to_remove)

    docs = [nlp(s) for s in string_list]
    tokens = []
    for doc in docs:
        tokens.extend([token.lemma_ for token in doc if not token.is_punct and token.lemma_ not in stop_words])
    return tokens

def topic_detection(df, nb_topics, nb_passes):
    """
    Detect topics in the character representations

    Parameters:
    - df: the dataframe containing the character representations
    - nb_topics: the number of topics to detect
    - nb_passes: the number of passes for the LDA model

    Returns:
    - lda_model: the trained LDA model
    - corpus: the corpus used to train the LDA model
    - dictionary: the dictionary used to train the LDA model
    """
    dictionary = corpora.Dictionary(df)
    corpus = [dictionary.doc2bow(text) for text in df]
    
    lda_model = LdaModel(corpus, num_topics=nb_topics, id2word=dictionary, passes=nb_passes)
    
    for idx, topic in lda_model.print_topics(-1, 10):
        print(f'Topic: {idx}\nWords: {topic}\n')
    
    return lda_model, corpus, dictionary

def get_dominant_topic(lda_model, corpus):
    """
    Get the dominant topic for each document (characters in our case) in the corpus
    """
    topics = []
    for doc in corpus:
        # Get topic distribution for the document
        topic_distribution = lda_model[doc]
        if topic_distribution:
            proportions = [prop_topic for _, prop_topic in topic_distribution]
            # Dominant topic
            dominant_topic = np.argmax(proportions)
            # Variance of proportions to see if the topic is really dominant
            variance = np.var(proportions) 
            topics.append((dominant_topic, variance))

    return topics

def get_main_character_archetypes(df, nb_topics, nb_passes, nlp, words_to_remove):
    df['processed_repres'] = df['character_representation'].apply(preprocess_char_repres, args=(nlp, words_to_remove))
    topic_detection_res = topic_detection(df['processed_repres'], nb_topics, nb_passes)
    df['topic'] = get_dominant_topic(topic_detection_res[0], topic_detection_res[1])
    # Keep only the "relevant" dominant topics that is the characters for which the
    # variance in the topic distribution was large enough to have a "dominant" topic
    df = df[df['topic'].apply(lambda x: x[1] > 0.1)] 
    return df, topic_detection_res

def compute_overall_term_freq(corpus, dictionary):
    """
    Computes the overall term frequency for all words in the corpus.

    Parameters:
    - corpus: BoW representation of the corpus (list of lists of (word_id, count)).
    - dictionary: Gensim Dictionary object mapping word IDs to words.

    Returns:
    - A Counter object mapping each word to its overall frequency in the corpus.
    """
    term_freq = Counter()
    for doc in corpus:
        term_freq.update(dictionary[term_id] for term_id, _ in doc if term_id in dictionary)
    return term_freq

def compute_estimated_term_freq(lda_model, corpus, dictionary, top_n=15):
    """
    Computes the estimated term frequency for the top N words in each topic.
    
    Parameters:
    - lda_model: Trained Gensim LDA model.
    - corpus: BoW representation of the corpus (list of lists of (word_id, count)).
    - dictionary: Gensim Dictionary object mapping word IDs to words.
    - top_n: Number of top words per topic to compute the frequencies for (default: 15).
    
    Returns:
    - A dictionary where each topic ID maps to another dictionary of top words and their estimated frequencies.
    """
    doc_topic_distrib = [dict(lda_model.get_document_topics(doc, minimum_probability=0.0)) for doc in corpus]
    topic_term_frequencies = {}
    
    for topic_id in range(lda_model.num_topics):
        top_words = lda_model.get_topic_terms(topic_id, topn=top_n)
        word_frequencies = {}

        for word_id, _ in top_words:
            word = dictionary[word_id]
            estimated_frequency = 0.0

            # Accumulate contributions from all doc for this word
            for doc_id, doc in enumerate(corpus):
                word_count = dict(doc).get(word_id, 0) # Get word count in the document
                topic_contribution = doc_topic_distrib[doc_id].get(topic_id, 0) # Topic proportion for this doc
                estimated_frequency += topic_contribution * word_count

            word_frequencies[word] = estimated_frequency

        topic_term_frequencies[topic_id] = word_frequencies

    return topic_term_frequencies
