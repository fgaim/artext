import random

from artext import utils
from artext.utils import log



class WordNoiser():
    """
    Handles word level noise injection.
    """

    def __init__(self):
        self.lang = 'en'
        self.keyboard = 'qwerty'


    def noise_word(self, word):
        rand = random.random()
        if rand <= 0.20:
            injections = 3
        elif rand <= 0.55:
            injections = 2
        else:
            injections = 1
        uword = word

        # handle capitalization separately
        rand = random.random()
        if rand >= 75:
            rand = random.random()
            if rand <= 75:
                uword = uword.lower()
            else:
                uword = uword.capitalize()

        # add other errors
        for _ in range(injections):
            rand = random.random()
            if rand <= 0.20:
                uword = self.drop_char(uword)
            elif rand <= 0.50:
                uword = self.add_char(uword)
            elif rand <= 0.65:
                uword = self.swap_char(uword)
            elif rand <= 0.75:
                uword = self.flip_char(uword)
            elif rand <= 0.90:
                uword = self.repeat_char(uword)
            elif rand <= 0.95:
                uword = self.swap_char(uword)
            else:
                #uword = self.keyboard_typo(uword)
                pass

        return uword


    def drop_char(self, word):
        """
        Drop char in a word.
        TODO test [vowel or double] only.
        """

        log.debug("drop change---before: %s" % word)
        pos = utils.rand_index(word)
        if pos == 0:
            pos += 1  # don't drop first letter of a word
        uword = word[:pos] + word[pos+1:]
        log.debug("drop change---after: %s" % word)
        return uword


    def add_char(self, word):
        """
        Randomly add vowel to word.
        """

        log.debug("addition change---before: %s" % word)
        pos = utils.rand_index(word)
        addition = random.choice(list(word+'aeiou'))
        word = word[:pos] + addition + word[pos:]
        log.debug("addition change---after: %s" % word)
        return word


    def swap_char(self, word):
        """
        Randomly swap two neighboring letters in a word.
        """

        log.debug("swap change---before: %s" % word)
        pos = utils.rand_index(word)
        i, j = (pos - 1, pos) if pos > 0 else (pos, pos + 1)
        word = word[:i] + word[j] + word[i] + word[j + 1:]
        log.debug("swap change---after: %s" %  word)
        return word


    def flip_char(self, word):
        """
        Randomly flip letters between two positions in a word.
        """

        log.debug("flip change---before: %s" % word)
        i, j = utils.rand_index(word), utils.rand_index(word)
        if i > j:
            i, j = j, i  # swaps i and j
        word = word[:i] + word[j] + word[i + 1:j] + word[i] + word[j + 1:]
        log.debug("flip change---after: %s" % word)
        return word


    def repeat_char(self, word):
        """
        Randomly repeat a letter in a word.
        """

        log.debug("repeat change---before: %s" % word)
        pos = utils.rand_index(word)
        word = word[:pos] + word[pos] + word[pos:]
        log.debug("repeat change---after: %s" % word)
        return word
