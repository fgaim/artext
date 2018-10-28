import unittest


class ArtextTestCase(unittest.TestCase):

    def test_args(self):
        from artext import utils
        parser = utils.arg_parser()
        args = parser.parse_args('-src test -out test -n 5'.split())
        self.assertEqual(args.source, 'test')
        self.assertEqual(args.output, 'test')
        self.assertEqual(args.samples, 5)

    def test_noise_sentence(self):
        from artext import config, Artext
        conf = config.Config()
        artxt = Artext(config=conf)

        # Sentence Level
        sent = "This person tried to keep an eye on the president while doing his work."
        noises = artxt.noise_sentence(sent)
        self.assertNotEqual(noises, None)
        self.assertEqual(len(noises), conf.samples)

    def test_noise_document(self):
        from artext import config, Artext
        conf = config.Config()
        artxt = Artext(config=conf)

        # Document Level
        doc = "I went to Iceland for vacation. The top of the mountain was very cold. Fortunately, I was wearing snowboard gear."
        noises = artxt.noise_document(doc)
        self.assertNotEqual(noises, None)
        self.assertEqual(len(noises), conf.samples)

    def test(self):
        # TODO: Write proper test here
        pass
