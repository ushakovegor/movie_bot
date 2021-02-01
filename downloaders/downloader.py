import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import argparse
import json


def descr_cleaner(storyline):
    storyline = re.sub(r'\nWritten by\n.+', ' ', storyline)
    storyline = re.sub('\n', ' ', storyline)
    storyline = storyline.split()
    storyline = " ".join(storyline)
    return storyline


def descr_download(row):
    resp = requests.get(str('https://www.imdb.com/title/tt' + row['imdbId']))
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    storyline_soup = soup(name='div', class_='inline canwrap')
    storyline = descr_cleaner(storyline_soup[0].text)
    return storyline


def description(data_to, data_from):
    data = pd.read_csv(str('datasets/' + data_from),
                       dtype={'movieId': np.object, 'imdbId': np.object, 'tmdbId': np.object})
    data = data.loc[0:30, :]
    data['description'] = data.apply(descr_download, axis=1)
    print(data['description'])
    data.loc[:, ['imdbId', 'description']].to_csv(str('datasets/' + data_to), index=False)


def poster_download(row, data_to):
    resp = requests.get(str('https://www.imdb.com/title/tt' + row[1]))
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    s = soup.find('script', type='application/ld+json')
    poster_link = json.loads(s.text)['image']
    p = requests.get(poster_link)
    out = open(str(data_to + "/" + row[0] + ".jpg"), "wb")
    out.write(p.content)
    out.close()


def poster(data_to, data_from):
    data = pd.read_csv(str('datasets/' + data_from),
                       dtype={'movieId': np.object, 'imdbId': np.object, 'tmdbId': np.object})
    data = data.loc[0:30, :]
    for row in data.loc[:, ['movieId', 'imdbId']].values.tolist():
        print(row)
        poster_download(row, data_to)


def main():
    ##########################################
    # Args parser #
    parser = argparse.ArgumentParser(description='description parser')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--description", action='store_true', help='Decription')
    group.add_argument("--poster", action='store_true', help='Poster')
    parser.add_argument('indir', type=str, help='Where to put description')
    parser.add_argument('outdir', type=str, help='Dataset of films')
    args = parser.parse_args()
    ##########################################

    if args.description:
        description(args.indir, args.outdir)
    elif args.poster:
        poster(args.indir, args.outdir)


if __name__ == '__main__':
    main()
