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
    sent = "So, I think if we have to go somewhere on foot, we must put on our hat."
    learner = "So, I think if we have to go somewhere on foot, we must put our hat."

    print('Input (Lang-8 target):\n{}\n'.format(sent))
    print('Human (Lang-8 source):\n{}\n'.format(learner))
    noises = artxt.noise_sentence(sent)
    print('Artext:')
    for noise in noises:
        print('-', noise)

    # Document Level
    print('\nDocument Level')
    doc = """This morning I found out that one of my favourite bands released a new album.
I already forgot about Rise Against and it is a great surprise for me, because I haven't listened to them for 2 years.
I hope this band didn't become worse, like many others big ones did, and I 'll enjoy listening to it.
Well, I just have to get it and check it out."""
    learner = """This morning I found out that one of my favourite band released his new album.
I already forgot about Rise Against an it is a great surprise for me, because I didn't return to them for 2 years.
I hope this band did n't become worse yet like many others big ones and I'll enjoy listening it.
Well , there remains to get it and check it out."""

    print('Input (Lang-8 target):\n{}\n'.format(doc))
    print('Human (Lang-8 source):\n{}\n'.format(earner))
    noises = artxt.noise_document(doc)
    print('Artext:')
    for noise in noises:
        print('-', noise)
