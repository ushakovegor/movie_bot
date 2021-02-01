import argparse
import os
import requests
import zipfile


MOVIELEN_DOMAIN = 'http://files.grouplens.org/datasets/movielens'
MOVIELEN_SMALL_DS = 'ml-latest-small.zip'
MOVIELEN_FULL_DS = 'ml-latest.zip'


def download_file(url, outputdir, chunk_size=8192):
    '''
    Download file and write it into outputdir

    Args:
        url (str): link to download
        outputdir (str): where to place new file
        chunk_size (int): size of chunks to write on disk default: 4Kb
    Return:
        (str) Name of downloaded File
    '''

    local_filename = url.split('/')[-1]
    local_filename = f'{outputdir}/{local_filename}'
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def unzip_file(filename, outputdir, delete=True):
    '''
    Unzip file and delete it if necessary

    Args:
        filename (str): file to unzip
        outputdir (str): where to unpack
        delete (bool): whatever delete or not after unziping [default: True]

    Return:
        None
    '''
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(outputdir)
    if delete:
        os.remove(filename)


def main():
    parser = argparse.ArgumentParser(
        description='Downloads dataset with movies ratings')
    parser.add_argument('outdir', type=str, help='Output dir for dataset')
    parser.add_argument('--small',
                        action='store_true',
                        help='Download small version of dataset')
    args = parser.parse_args()
    if args.small:
        download_link = f'{MOVIELEN_DOMAIN}/{MOVIELEN_SMALL_DS}'
    else:
        download_link = f'{MOVIELEN_DOMAIN}/{MOVIELEN_FULL_DS}'

    archive_filename = download_file(download_link, outputdir=args.outdir)
    unzip_file(archive_filename, args.outdir)


if __name__ == '__main__':
    main()
