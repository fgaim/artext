import sys
import os
import random
import string

from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import wordnet as wn
import spacy
from spacy.symbols import ORTH

from artext.config import Config
from artext.utils import log
from artext import inflect
from artext.word_level import WordNoiser


nlp = spacy.load('en_core_web_sm')


class Artext:
    """
    Artificial noise generation of Natural Language.
    """

    def __init__(self, config=Config()):
        self.config = config

        self.error_overall = self.config.error_overall
        self.error_typo = self.config.error_rate_typo
        self.error_swap = self.config.error_rate_swap
        self.prep_list = self.config.target_preposition
        self.determiner_list = self.config.target_determiner
        self.punc_list = self.config.target_punc
        self.pos_det = self.config.pos_determiner
        self.pos_prep = self.config.pos_preposition
        self.pos_noun = self.config.pos_noun
        self.pos_verb = self.config.pos_verb
        self.pos_adv = self.config.pos_adv
        self.pos_adj = self.config.pos_adj

        self.samples = self.config.samples
        self.separator = self.config.separator

        # load protected list
        self.protected_tokens = set()
        if self.config.path_protected_tokens:
            with open(self.config.path_protected_tokens, 'r') as fin:
                self.protected_tokens = set(
                    [line.lower().strip() for line in fin])
        for pt in self.protected_tokens:
            nlp.tokenizer.add_special_case(pt, [{ORTH: pt}])

        self.word_noiser = WordNoiser()
        self.inf = inflect.Inflect()
        self.detok = TreebankWordDetokenizer().detokenize

    def noise_document(self, doc):
        """
        Generates 'samples' number of noises for a document.

        Args:
            doc: str, multi-sentence text

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

        Args:
            sent: str, a sentence

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
        Inject errors according to an overall rate.

        Returns:
            str: noised sentence
        """
        noised_sent = []
        prob = 1. - self.config.error_rate_overall

        for tok in parsed_sent:
            rand1, rand2 = random.random(), random.random()

            if rand1 < prob or tok.text.lower() in self.protected_tokens:
                # do not noise token
                noised_sent.append(tok.text)
                continue

            # Orthographic errors
            if rand2 <= self.error_typo and len(tok.text) > 4:
                typo = self.word_noiser.noise_word(tok.text)
                noised_sent.append(typo)

            # Swap current and previous words
            elif rand2 <= self.error_swap and len(noised_sent) > 1:
                prev_tok = noised_sent.pop()
                noised_sent.append(tok.text)
                noised_sent.append(prev_tok)

            # Determiners/Articles
            elif tok.tag_ == self.pos_det:
                if tok.text.lower() in self.determiner_list:
                    if rand2 <= 0.15:
                        noised_sent.append('a')
                    elif rand2 <= 0.30:
                        noised_sent.append('an')
                    elif rand2 <= 0.45:
                        noised_sent.append('the')
                    elif rand2 <= 0.80 or len(noised_sent) == 0:
                        noised_sent.append(tok.text)
                    elif len(noised_sent) > 0:
                        pass
                else:
                    if rand2 <= 0.35:
                        noised_sent.append(self.pluralize(tok.text))
                    elif rand2 <= 0.85 or len(noised_sent) == 0:
                        noised_sent.append(tok.text)
                    elif len(noised_sent) > 0:
                        pass

            # Prepositions
            elif tok.tag_ == self.pos_prep and tok.text.lower() in self.prep_list:
                if rand2 <= 0.10:
                    noised_sent.append('in')
                elif rand2 <= 0.20:
                    noised_sent.append('on')
                elif rand2 <= 0.30:
                    noised_sent.append('to')
                elif rand2 <= 0.40:
                    noised_sent.append('for')
                elif rand2 <= 0.80:
                    noised_sent.append(random.sample(self.prep_list, 1)[0])
                else:
                    pass

            # Nouns
            elif tok.tag_ in self.pos_noun:
                if rand2 <= 0.45:
                    noised_sent.append(self.singularize_noun(tok.text))
                elif rand2 <= 0.80:
                    noised_sent.append(self.pluralize(tok.text))
                elif rand2 <= 0.90:
                    synonyms = self.synonyms_noun(tok.text)
                    if not len(synonyms):
                        synonyms = [tok.text]
                    noised_sent.append(random.sample(synonyms, 1)[0])
                else:
                    noised_sent.append(tok.text)

            # Verbs
            elif tok.tag_ in self.pos_verb:
                if rand2 <= 0.20:
                    noised_sent.append(tok.lemma_)
                elif rand2 <= 0.45:
                    noised_sent.append(self.pluralize_verb(tok.text))
                elif rand2 <= 0.75:
                    noised_sent.append(self.present_participle(tok.text))
                elif rand2 <= 0.90:
                    synonyms = self.synonyms_verb(tok.text)
                    if not len(synonyms):
                        synonyms = [tok.text]
                    noised_sent.append(random.sample(synonyms, 1)[0])
                else:
                    noised_sent.append(tok.text)

            # Adverbs
            elif tok.tag_ in self.pos_adv:
                if rand2 <= 0.35:
                    synonyms = self.synonyms_adv(tok.text)
                    if not len(synonyms):
                        synonyms = [tok.text]
                    noised_sent.append(random.sample(synonyms, 1)[0])
                else:
                    noised_sent.append(tok.text)

            # Adjectives
            elif tok.tag_ in self.pos_adj:
                if rand2 <= 0.40:
                    noised_sent.append(self.pluralize_adj(tok.text))
                elif rand2 <= 0.60:
                    synonyms = self.synonyms_adj(tok.text)
                    if not len(synonyms):
                        synonyms = [tok.text]
                    noised_sent.append(random.sample(synonyms, 1)[0])
                elif rand2 <= 0.95:
                    noised_sent.append(tok.text)
                else:
                    pass

            # Punctuation
            elif tok.tag_ in self.punc_list:
                if rand2 <= 0.60:
                    noised_sent.append(tok.text)
                elif rand2 <= 0.80:
                    noised_sent.append(random.sample(self.punc_list, 1)[0])
                else:
                    pass

            else:
                log.debug('UNK POS [{}]'.format(tok.tag_))

            # After exhausting other schemes double-up for Orthographic errors
            if (rand2/2) <= self.error_typo and len(tok.text) > 3:
                typo = self.word_noiser.noise_word(tok.text)
                noised_sent.append(typo)
            else:
                noised_sent.append(tok.text)

            # Add redundant punctuation
            if tok.tag_ not in self.punc_list:
                if rand2 <= 0.01:
                    noised_sent.append(random.sample(self.punc_list, 1)[0])

        return self.detok([t for t in noised_sent if t])

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

    def get_sysnonyms(self, word, pos):
        assert word, 'No word!'
        assert pos, 'No POS!'

        synsets = wn.synsets(word, pos)
        synonyms = set()
        for synset in synsets:
            for synonym in synset.lemmas():
                synonym = synonym.name()
                if synonym.isalpha() and word != synonym:
                    synonyms.add(synonym)
        return list(synonyms)

    def synonyms_noun(self, word):
        return self.get_sysnonyms(word, wn.NOUN)

    def synonyms_verb(self, word):
        return self.get_sysnonyms(word, wn.VERB)

    def synonyms_adv(self, word):
        return self.get_sysnonyms(word, wn.ADV)

    def synonyms_adj(self, word):
        return self.get_sysnonyms(word, wn.ADJ)
