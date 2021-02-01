import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
import re
import torch
import transformers as ppb
from sklearn.metrics.pairwise import cosine_similarity


def get_title(text):
    dest = 0
    best_dest = 0
    number = 0

    l_v = title_to_vector(text)
    for i in range(df.shape[0]):
        r_v = title_to_vector(df.loc[i, 'title'])
        dest = get_similarity(l_v, r_v)
        if dest > best_dest:
            best_dest = dest
            number = i
    return number


def clear_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = text.split()
    return text


def get_vector(word, data):
    if word in data:
        return data[word]
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