import numpy as np
import pandas as pd
import re
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity

data_of_words = {}
data_of_films = pd.DataFrame()
data_of_links = pd.DataFrame()


def pre_actions():
    global data_of_words, data_of_films, data_of_links

    f = open('../datasets/crawl-300d-2M-subword.vec', encoding='utf-8')
    for line in tqdm(f):
        values = line.strip().rsplit(' ')
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        data_of_words[word] = coefs
    f.close()
    data_of_films = pd.read_csv('../datasets/movies.csv', dtype={'movieId': 'object'})
    data_of_links = pd.read_csv('../datasets/links.csv',
                                dtype={'movieId': 'object', 'imdbId': 'object', 'tmdbId': 'object'})
    return 0


def get_title(text):
    global data_of_films

    SHAPE = data_of_films.shape[0]
    best_destination = 0
    number = 0

    l_v = title_to_vector(text)
    for i in range(SHAPE):
        r_v = title_to_vector(data_of_films.loc[i, 'title'])
        destination = get_similarity(l_v, r_v)
        if destination > best_destination:
            best_destination = destination
            number = i
    title = data_of_films.loc[number, 'title']
    return title, number


def get_link(title_id):
    global data_of_links

    return data_of_links.loc[title_id, 'imdbId']


def clear_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = text.split()
    return text


def get_vector(word):
    global data_of_words

    if word in data_of_words:
        return data_of_words[word]
    else:
        return np.zeros(300, )


def title_to_vector(title):
    vector = np.zeros(300, )

    list_of_word = clear_text(title)
    for j in list_of_word:
        vector += get_vector(j)
    vector = vector.reshape(1, -1)
    return vector


def get_similarity(l_v, r_v):
    return cosine_similarity(l_v, r_v)
