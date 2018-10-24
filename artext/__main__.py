from artext import config
from artext import utils
from artext.artext import Artext

if __name__ == "__main__":
    parser = utils.arg_parser()
    args = parser.parse_args()

    conf = config.Config()
    conf.error_overall = args.error_rate
    conf.path_protected_tokens = args.protected_tokens
    conf.samples = args.samples
    conf.separator = args.separator

    artxt = Artext(config=conf)

    with open(args.source, 'r') as fin, open(args.output, 'w') as fout:
        if args.level == 'sent':
            for line in fin:
                noises = artxt.noise_sentence(line)
                fout.write("{}\n".format(args.separator.join(noises)))
        elif args.level == 'doc':
            for line in fin:
                noises = artxt.noise_document(line)
                fout.write("{}\n".format(args.separator.join(noises)))
