import pandas as pd
import numpy as np
import torch
import transformers as ppb
#from sklearn.metrics.pairwise import cosine_similarity


def main():
    movies = pd.read_csv('../datasets/movies.csv',
                         dtype={'movieId': np.object, 'title': np.object, 'genres': np.object})
    model_class, tokenizer_class, pretrained_weights = (ppb.BertModel, ppb.BertTokenizer, 'bert-base-uncased')
    tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights)
    tokenized = movies['title'].apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))
    max_len = 0
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)
    padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized.values])
    attention_mask = np.where(padded != 0, 1, 0)
    input_ids = torch.tensor(padded)
    attention_mask = torch.tensor(attention_mask)

    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)
    print(last_hidden_states[0][:, 0, :].numpy())


if __name__ == '__main__':
    main()