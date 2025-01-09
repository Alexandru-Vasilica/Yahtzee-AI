from __future__ import annotations

from collections import defaultdict

import langdetect
import nltk
import numpy as np
from nltk import word_tokenize, ngrams
from numpy import random
from rake_nltk import Rake

from typing import TYPE_CHECKING

if TYPE_CHECKING:
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


def get_context_vector(sentence, target_word, stop_words):
    words = [w.lower() for w in word_tokenize(sentence)
             if w.lower() not in stop_words]
    context_vector = defaultdict(int)

    for word in words:
        if word != target_word.lower():
            context_vector[word] += 1
    return context_vector


def get_synset_vector(synset_definition, stop_words):
    vector = defaultdict(int)
    for word in word_tokenize(synset_definition):
        word = word.lower()
        if word not in stop_words:
            vector[word] += 1
    return vector


def vector_similarity(vec1, vec2):
    words = set(vec1.keys()) | set(vec2.keys())
    vec1_array = np.array([vec1.get(word, 0) for word in words])
    vec2_array = np.array([vec2.get(word, 0) for word in words])

    norm1 = np.linalg.norm(vec1_array)
    norm2 = np.linalg.norm(vec2_array)

    if norm1 == 0 or norm2 == 0:
        return 0

    return np.dot(vec1_array, vec2_array) / (norm1 * norm2)


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
    sentences = nltk.sent_tokenize(text)
    sentence_indexes = []
    words = []
    for idx, sentence in enumerate(sentences):
        tokens = nltk.word_tokenize(sentence)
        sentence_indexes.extend([idx] * len(tokens))
        words.extend(tokens)
    synonym_count = int(len(words) * syn_ration)
    replaced_indexes = set()
    unavailable_indexes = set()
    while synonym_count > 0:
        relevant_indexes = [i for i in range(len(words)) if i not in replaced_indexes and i not in unavailable_indexes]
        if len(relevant_indexes) == 0:
            break
        index = np.random.choice(relevant_indexes)
        word = words[index]
        sentence_index = sentence_indexes[index]
        sentence = sentences[sentence_index]
        synonyms = wn.get_synonyms(word, sentence)
        if len(synonyms) == 0:
            unavailable_indexes.add(index)
            # print(f"No synonyms found for '{word}' in sentence: '{sentence}'")
            continue
        synonym = np.random.choice(list(synonyms))
        synonym = remove_snake_case(synonym)
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
        sentence_index = sentence_indexes[index]
        sentence = sentences[sentence_index]
        antonyms = wn.get_antonyms(word, sentence)
        if len(antonyms) == 0:
            unavailable_indexes.add(index)
            # print(f"No antonyms found for '{word}' in sentence: '{sentence}'")
            continue
        antonym = np.random.choice(list(antonyms))
        antonym = remove_snake_case(antonym)
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
        sentence_index = sentence_indexes[index]
        sentence = sentences[sentence_index]
        hypernyms = wn.get_hypernyms(word, sentence)
        if len(hypernyms) == 0:
            unavailable_indexes.add(index)
            # print(f"No hypernyms found for '{word}' in sentence: '{sentence}'")
            continue
        hypernym = np.random.choice(list(hypernyms))
        hypernym = remove_snake_case(hypernym)
        words[index] = hypernym
        replaced_indexes.add(index)
        hypernym_count -= 1
        print(f"Replaced '{word}' with hypernym: '{hypernym}'")

    return " ".join(words)


def extract_keywords(text, language="english", max_length=None):
    r = Rake(language=language)
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()
    if max_length is not None:
        keywords = keywords[:max_length]
    return keywords


def unify_keywords(keywords, text):
    modified_keywords = []
    for keyword in keywords:
        if ' ' in keyword:
            new_keyword = keyword.replace(' ', '_')
            text = text.replace(keyword, new_keyword)
            modified_keywords.append(new_keyword)
        else:
            modified_keywords.append(keyword)
    return modified_keywords, text


def generate_pos_tags(text):
    words = word_tokenize(text.lower())
    return nltk.pos_tag(words)


def generate_sentence_with_keyword(keyword, pos_tags):
    structure = "{subject} {verb} {adjective} {object}."

    roles = {
        'NN': ['subject', 'object'],
        'NNS': ['subject', 'object'],
        'NNP': ['subject', 'object'],
        'NNPS': ['subject', 'object'],
        'JJ': ['adjective'],
        'JJS': ['adjective'],
        'JJR': ['adjective'],
        'VB': ['verb'],
        'VBN': ['verb'],
        'VBG': ['verb'],
        'VBD': ['verb'],
        'VBP': ['verb'],
    }
    found = False
    assigned_roles = {}
    for word, pos in pos_tags:
        if word == keyword:

            if pos not in roles:
                continue
            role = random.choice(roles[pos])
            assigned_roles[role] = remove_snake_case(word)
            found = True
            break
    if not found:
        return None
    random.shuffle(pos_tags)
    for word, pos in pos_tags:
        if pos in roles:
            for role in roles[pos]:
                if role not in assigned_roles:
                    assigned_roles[role] = remove_snake_case(word)
                    break
        if len(assigned_roles) == 4:
            break

    sentence = structure.format(**assigned_roles)

    return sentence.capitalize()


def remove_snake_case(text):
    return ' '.join(text.split('_'))
