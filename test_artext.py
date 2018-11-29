"""
Unit tests for artext
"""


class TestArtext():

    def test_args(self):
        from artext import utils
        parser = utils.arg_parser()
        args = parser.parse_args('-src test -out test -n 5'.split())
        assert args.source == 'test'
        assert args.output == 'test'
        assert args.samples == 5

    def test_noise_sentence(self):
        from artext import config, Artext
        conf = config.Config()
        artxt = Artext(config=conf)

        # Sentence Level
        sent = "This person tried to keep an eye on the president while "
        "doing his work."
        noises = artxt.noise_sentence(sent)
        assert noises is not None
        assert len(noises) == conf.samples

    def test_noise_document(self):
        from artext import config, Artext
        conf = config.Config()
        artxt = Artext(config=conf)

        # Document Level
        doc = "I went to Iceland for vacation. The top of the mountain was "
        "very cold. Fortunately, I was wearing snowboard gear."
        noises = artxt.noise_document(doc)
        assert noises is not None
        assert len(noises) == conf.samples

    def test_word_noise(self):
        from artext.word_level import WordNoiser
        wnoiser = WordNoiser()
        word = 'Mountain'
        uword = wnoiser.noise_word(word)
        assert uword is not None
        assert uword != word
