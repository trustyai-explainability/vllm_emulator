import random
import numpy as np
import json

PUNCTUATION = ".!?"
LETTERS = list("abcdefghijklmnopqrstuvwxyz")

# frequency of starting letters, from https://en.wikipedia.org/wiki/Letter_frequency
WORD_START_FREQ = [.1154, .043, .052, .032, .028, .04, .016, .042, .073, .0051, .0086, .024, .038, .023, .076, .043,
                   .0022, .028, .067, .16, .012, .0082, .055, .00045, .0076, .00045]

# word length distribution, from https://math.wvu.edu/~hdiamond/Math222F17/Sigurd_et_al-2004-Studia_Linguistica.pdf
WORD_LEN_DISTRIBUTION = [0.031500223549973574, 0.1717270251595334, 0.21533959273259357, 0.15851725399341543,
                         0.10974271430313375, 0.08657480795024995, 0.07316180953542249, 0.05690362963866195,
                         0.04064544974190139, 0.027435678575783436, 0.01524204365321302, 0.009145226191927812,
                         0.004064544974190139]
WORD_LENS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


# === WORD GENERATION MARKOV MODEL =================================================================
def proc_bigrams():
    """Load the English bigram frequency table
    downloaded from https://gist.github.com/lydell/c439049abac2c9226e53
    """
    with open("bigrams.json", "r") as f:
        bigrams = json.load(f)
    return bigrams


bigrams = proc_bigrams()


def specific_bigram_freq(start_letter):
    """Given a specific start letter, get the probability of subsequent letters appearing"""
    specific_bigrams = [(bg, f) for bg, f in bigrams if bg[0] == start_letter]
    specific_bigrams, freqs = zip(*specific_bigrams)
    freqs = np.array(freqs) / sum(freqs)
    return specific_bigrams, freqs


def gen_word():
    """Generates english-y words according to a bi-gram Markov chain """
    start_letter = np.random.choice(LETTERS, size=1, p=WORD_START_FREQ)[0]
    word = start_letter

    word_len = np.random.choice(WORD_LENS, size=1, p=WORD_LEN_DISTRIBUTION)[0]
    for _ in range(word_len):
        specific_bigrams, freqs = specific_bigram_freq(word[-1])
        new_letters = np.random.choice(specific_bigrams, size=1, p=freqs)[0]
        word += new_letters[-1]
    return word


# === PARAGRAPH GENERATION =========================================================================
def gen_paragraph(max_len, sentence_bounds=(4, 8), word_bounds=(5, 15)):
    """Generate a random paragraph according to sentence_bounds and word_bounds

    * max_len: maximum length of paragraph in characters
    * sentence_bounds: tuple of (min_sentences, max_sentences), a random number of sentences between min_sentences
        and max_sentences will be generated.
    * word_bounds: tuple of (min_words, max_words), a random number of words between min_words and
        max_words will be generated in each sentence.

    returns a tuple of (string, bool), where the string is the generated "english-y" paragraph, and the bool indicates
    whether the max_len threshold was hit.
    """

    out = ""
    n_sent = random.randint(*sentence_bounds)
    since_last_break = 0;

    for _ in range(n_sent):
        n_words = random.randint(*word_bounds)
        for word_idx in range(n_words):

            if max_len and len(out) > max_len:
                return out.strip(), True

            word = gen_word()
            if word_idx == 0:  # capitalize first word
                word = word[0].upper() + word[1:]
            out += word

            if word_idx < n_words - 1:
                if (len(out) - since_last_break) < 80:
                    out += " "
                else:
                    out += " \n"
                    since_last_break = len(out)
        out += random.choice(PUNCTUATION)
        out += " "
    return out.strip(), False
