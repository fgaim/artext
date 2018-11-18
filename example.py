import sys
from artext import config, utils, Artext


if __name__ == "__main__":
    parser = utils.arg_parser()
    args = parser.parse_args('-src test -out test -n 5'.split() + sys.argv[1:])

    conf = config.Config()
    conf.error_rate = args.error_rate
    conf.path_protected_tokens = args.protected_tokens
    conf.samples = args.samples
    conf.separator = args.separator

    artxt = Artext(config=conf)

    # Sentence Level
    print('Sentence Level')
    sent = "This person tried to keep an eye on the president while doing his work."
    print('Input:\n{}\n'.format(sent))
    noises = artxt.noise_sentence(sent)
    print('Noises:')
    for noise in noises:
        print('-', noise)

    # Document Level
    print('\nDocument Level')
    doc = "I went to Iceland for vacation. The top of the mountain was very cold. Fortunately, I was wearing snowboard gear."
    print('Input:\n{}\n'.format(doc))
    noises = artxt.noise_document(doc)
    print('Noises:')
    for noise in noises:
        print('-', noise)
