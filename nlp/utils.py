
from collections import defaultdict

import langdetect
import nltk
import numpy as np
from rake_nltk import Rake


from nlp.wordnet import WordNet

LANGUAGE_THRESHOLD = 0.25
LANGUAGE_PROB_MULTIPLIER = 1.5
SUPPORTED_LANGUAGES = ['en', 'ro']
PUNCTUATION = ['.', ',', '!', '?', ';', ':', '(', ')', '[', ']', '{', '}', '"', "'", '„', '”', '’', '‘', '—', '–', '…']


def detect_language(text):
    languages = langdetect.detect_langs(text)
    for i in range(len(languages)):
        if languages[i].lang in SUPPORTED_LANGUAGES:
            if languages[i].prob > LANGUAGE_THRESHOLD:
                languages[i].prob *= LANGUAGE_PROB_MULTIPLIER
    sorted_languages = sorted(languages, key=lambda x: x.prob, reverse=True)
    return sorted_languages[0].lang


def get_wordnet_api(language):
    match language:
        case "en":
            from nltk.corpus import wordnet as wn
            return wn
        case "ro":
            import rowordnet
            return rowordnet.RoWordNet()
        case _:
            raise ValueError(f"Unsupported language: {language}")


def tokenize_text(text):
    return nltk.word_tokenize(text)


def get_stylometric_features(text):
    words = tokenize_text(text)
    words = [word.lower() for word in words]
    relevant_words = [word for word in words if word not in PUNCTUATION]
    word_length = len(relevant_words)
    char_length = sum(len(word) for word in words)
    char_freq = defaultdict(int)
    word_freq = defaultdict(int)
    for word in relevant_words:
        word_freq[word] += 1
    for word in words:
        for char in word:
            char_freq[char] += 1
    return {
        'word_length': word_length,
        'char_length': char_length,
        'char_freq': char_freq,
        'word_freq': word_freq
    }


def rephrase_text(text, wn: WordNet, syn_ration=0.1, hyper_ration=0.1, ant_ration=0.1):
    words = tokenize_text(text)
    synonym_count = int(len(words) * syn_ration)
    replaced_indexes = set()
    unavailable_indexes = set()
    while synonym_count > 0:
        relevant_indexes = [i for i in range(len(words)) if i not in replaced_indexes and i not in unavailable_indexes]
        if len(relevant_indexes) == 0:
            break
        index = np.random.choice(relevant_indexes)
        word = words[index]
        synonyms = wn.get_synonyms(word)
        if len(synonyms) == 0:
            unavailable_indexes.add(index)
            print(f"No synonyms found for '{word}'")
            continue
        synonym = np.random.choice(list(synonyms))
        words[index] = synonym
        replaced_indexes.add(index)
        synonym_count -= 1
        print(f"Replaced '{word}' with synonym: '{synonym}'")

    antonym_count = int(len(words) * ant_ration)
    unavailable_indexes.clear()
    while antonym_count > 0:
        relevant_indexes = [i for i in range(len(words)) if i not in replaced_indexes and i not in unavailable_indexes]
        if len(relevant_indexes) == 0:
            break
        index = np.random.choice(relevant_indexes)
        word = words[index]
        antonyms = wn.get_antonyms(word)
        if len(antonyms) == 0:
            unavailable_indexes.add(index)
            print(f"No antonyms found for '{word}'")
            continue
        antonym = np.random.choice(list(antonyms))
        words[index] = antonym
        replaced_indexes.add(index)
        antonym_count -= 1
        print(f"Replaced '{word}' with antonym: '{antonym}'")

    hypernym_count = int(len(words) * hyper_ration)
    unavailable_indexes.clear()

    while hypernym_count > 0:
        relevant_indexes = [i for i in range(len(words)) if i not in replaced_indexes and i not in unavailable_indexes]
        if len(relevant_indexes) == 0:
            break
        index = np.random.choice(relevant_indexes)
        word = words[index]
        hypernyms = wn.get_hypernyms(word)
        if len(hypernyms) == 0:
            unavailable_indexes.add(index)
            print(f"No hypernyms found for '{word}'")
            continue
        hypernym = np.random.choice(list(hypernyms))
        words[index] = hypernym
        replaced_indexes.add(index)
        hypernym_count -= 1
        print(f"Replaced '{word}' with hypernym: '{hypernym}'")

    return " ".join(words)


def extract_keywords(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()
