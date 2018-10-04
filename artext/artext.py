import sys
import os
import random
import string
import configparser as ConfigParser
from nltk.tokenize.treebank import TreebankWordDetokenizer
import spacy

from artext.utils import log
from artext import inflect
from artext.word_level import WordNoiser


nlp = spacy.load('en_core_web_sm')


class Artext:
    """
    Natural Language Noise Generator.
    TODO: Implement Punctuation errors
    TODO: Implement Semantic (synonym) errors
    """

    def __init__(self, args):
        # Config
        self.config = ConfigParser.RawConfigParser()
        self.config.read(args.config)
        if args.error_rate:
            self.config.set("general", "error_overall", 'True')
            self.config.set("general", "error_rate_overall", args.error_rate)

        # for k in self.config.sections():
        #    for _item in self.config.items(k):
        #        print(_item)

        self.error_overall = self.config.getboolean("general", "error_overall")
        self.error_typo = self.config.getfloat("spelling", "error_rate_typo")
        self.error_swap = self.config.getfloat("swap", "error_rate_swap")
        self.prep_list = self.config.get("preposition", "target_preposition").split('|')
        self.determiner_list = self.config.get("determiner", "target_determiner").split('|')
        self.punc_list = self.config.get("punctuation", "target_punc").split('|')
        self.pos_det = "DT"
        self.pos_prep = "IN"
        self.pos_noun = self.config.get("noun-number", "target_noun").split('|')
        self.pos_verb = self.config.get("verb-form", "target_verb").split('|')
        self.pos_adj = self.config.get("adjective", "target_adj").split('|')

        self.samples = args.samples
        self.separator = args.separator
        self.word_noiser = WordNoiser()
        self.inf = inflect.Inflect()
        self.detok = TreebankWordDetokenizer().detokenize


    def noise_document(self, doc):
        """
        Generates 'samples' number of noises for a document.

        Returns:
            tuple: noises
        """
        parsed_doc = nlp(doc.strip())

        doc_noises = list()
        for sent in parsed_doc.sents:
            samples = self.samples

            # Keep some (10%) sentences clean
            cln = []
            rand = random.random()
            if samples > 1 and rand >= 0.90:
                cln_samples = random.randint(0, samples-1)
                cln = [sent.text] * cln_samples
                samples -= cln_samples

            # Inject noise
            noises = set()
            while len(noises) < samples:
                noises.add(self._inject_noise(sent))

            # Collect and shuffle
            noises = list(noises) + cln
            random.shuffle(noises)

            doc_noises.append(noises)

        return tuple(' '.join(ns) for ns in zip(*doc_noises))

    def noise_sentence(self, sent):
        """
        Generates 'samples' number of noises for a sentence.

        Returns:
            tuple: noises
        """
        parsed_sent = nlp(sent.strip())

        noises = set()
        while len(noises) < self.samples:
            noises.add(self._inject_noise(parsed_sent))

        return tuple(noises)

    def _inject_noise(self, parsed_sent):
        """
        Inject errors according to an overall probability.
        """
        ug_src = []
        prob = 1. - self.config.getfloat("general", "error_rate_overall")

        for _i, tok in enumerate(parsed_sent):
            rand1, rand2 = random.random(), random.random()

            # Orthographic errors
            if rand1 >= prob and rand2 <= self.error_typo and len(tok.text) > 4:
                typo = self.word_noiser.noise_word(tok.text)
                ug_src.append(typo)

            # Swap current and last words
            elif rand1 >= prob and rand2 <= self.error_swap and len(ug_src) > 0 and 1 < _i < len(parsed_sent)-1:
                ug_pop = ug_src.pop()
                ug_src.append(tok.text)
                ug_src.append(ug_pop)

            # Determiners/Articles
            elif rand1 >= prob and tok.tag_ == self.pos_det:
                if tok.text.lower() in self.determiner_list:
                    if rand2 <= 0.15:
                        ug_src.append('a')
                    elif rand2 <= 0.30:
                        ug_src.append('an')
                    elif rand2 <= 0.45:
                        ug_src.append('the')
                    elif rand2 <= 0.80 or len(ug_src) == 0:
                        ug_src.append(tok.text)
                    elif len(ug_src) > 0:
                        pass
                else:
                    if rand2 <= 0.35:
                        ug_src.append(self.pluralize(tok.text))
                    elif rand2 <= 0.85 or len(ug_src) == 0:
                        ug_src.append(tok.text)
                    elif len(ug_src) > 0:
                        pass

            # Prepositions
            elif rand1 >= prob and tok.tag_ == self.pos_prep and tok.text.lower() in self.prep_list:
                if rand2 <= 0.10:
                    ug_src.append('in')
                elif rand2 <= 0.20:
                    ug_src.append('on')
                elif rand2 <= 0.30:
                    ug_src.append('to')
                elif rand2 <= 0.40:
                    ug_src.append('for')
                elif rand2 <= 0.80:
                    ug_src.append(random.sample(self.prep_list, 1)[0])
                else:
                    pass

            # Nouns
            elif rand1 >= prob and tok.tag_ in self.pos_noun:
                if rand2 <= 0.5:
                    ug_src.append(self.singularize_noun(tok.text))
                else:
                    ug_src.append(self.pluralize(tok.text))

            # Verbs
            elif rand1 >= prob and tok.tag_ in self.pos_verb:
                if rand2 <= 0.20:
                    ug_src.append(tok.lemma_)
                elif rand2 <= 0.30:
                    ug_src.append(self.pluralize_verb(tok.text))
                elif rand2 <= 0.50:
                    ug_src.append(self.present_participle(tok.text))
                else:
                    ug_src.append(tok.text)

            # Adjectives
            elif rand1 >= prob and tok.tag_ in self.pos_adj:
                if rand2 <= 0.5:
                    ug_src.append(self.pluralize_adj(tok.text))
                else:
                    ug_src.append(tok.text)

            # Punctuation
            elif tok.text in self.punc_list:
                if rand2 <= 0.70:
                    ug_src.append(tok.text)
                elif rand1 <= 0.80:
                    ug_src.append(random.sample(self.punc_list, 1)[0])
                else:
                    pass

            else:
                ug_src.append(tok.text)
                log.debug('Skipped: ' + tok.tag_)

        return self.detok([t for t in ug_src if t])


    def singularize_noun(self, word):
        uw = self.inf.singular_noun(word)
        return uw if uw else word

    def pluralize(self, word):
        uw = self.inf.plural(word)
        return uw if uw else word

    def pluralize_verb(self, word):
        uw = self.inf.plural_verb(word)
        return uw if uw else word

    def pluralize_adj(self, word):
        uw = self.inf.plural_adj(word)
        return uw if uw else word

    def present_participle(self, word):
        uw = self.inf.present_participle(word)
        return uw if uw else word
