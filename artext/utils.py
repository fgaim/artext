import string
import random
import logging
import operator
import argparse



# Log to console
log = logging.getLogger('ARTEXT')
fmt = '%(name)s %(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%Y:%m:%d %I:%M:%S')
ch = logging.StreamHandler()
log.addHandler(ch)


def arg_parser():
    """
    CLI options for inject.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-src', '--source', type=str, required=True,
                        help='Path to source text file')
    parser.add_argument('-out', '--output', type=str, required=True,
                        help='Path to ouput text file')
    parser.add_argument('-n', '--samples', type=int, default=1,
                        help='Number of noise samples to generate per sentence')
    parser.add_argument('-sep', '--separator', type=str, default='\n',
                        help='String to separate noise samples of a sentence')
    parser.add_argument('-er', '--error_rate', type=float, default=0.25,
                        help='Error rate in decimal, eg. 0.25')
    parser.add_argument('-l', '--level', choices=['sent', 'doc'], default='sent',
                        help='Level at which to generate noises')
    parser.add_argument('-pt', '--protected_tokens', type=str, default=None,
                        help='A file listing tokens to be excluded from noising')

    return parser


def rand_index(word):
    """
    Returns a random index in a given text.
    """

    return random.randint(0, len(word)-1)
