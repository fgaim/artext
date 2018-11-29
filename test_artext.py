"""
Unit tests for artext
"""


def test_args():
    from artext import utils
    parser = utils.arg_parser()
    args = parser.parse_args('-src test -out test -n 5'.split())
    assert args.source == 'test'
    assert args.output == 'test'
    assert args.samples == 5


def test_noise_sentence(benchmark):
    from artext import config, Artext
    conf = config.Config()
    artxt = Artext(config=conf)

    sent = "This person tried to keep an eye on the president while doing his work."
    noises = benchmark(artxt.noise_sentence, sent)
    assert noises is not None
    assert len(noises) == conf.samples


def test_noise_document(benchmark):
    from artext import config, Artext
    conf = config.Config()
    artxt = Artext(config=conf)

    doc = "I went to Iceland for vacation. The top of the mountain was very cold."
    noises = benchmark(artxt.noise_document, doc)
    assert noises is not None
    assert len(noises) == conf.samples


def test_word_noise(benchmark):
    from artext.word_level import WordNoiser
    wnoiser = WordNoiser()
    word = 'Mountain'
    uword = benchmark(wnoiser.noise_word, word)
    assert uword is not None
    assert uword != word
