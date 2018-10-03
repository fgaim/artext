import sys
import os
import random
import argparse
import configparser as ConfigParser

from artext import utils, Artext


if __name__ == "__main__":
    parser = utils.arg_parser()
    args = parser.parse_args()

    artxt = Artext(args)

    with open(args.source, 'r') as fin, open(args.output, 'w') as fout:
        if args.level == 'sent':
            for line in fin:
                noises = artxt.noise_sentence(line)
                fout.write("{}\n".format(args.separator.join(noises)))
        elif args.level == 'doc':
            for line in fin:
                noises = artxt.noise_document(line)
                fout.write("{}\n".format(args.separator.join(noises)))
