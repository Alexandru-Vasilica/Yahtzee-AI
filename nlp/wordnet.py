import nltk
import rowordnet
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet as wn_en

from nlp.utils import get_context_vector, get_synset_vector, vector_similarity


class WordNet:
    language: str
    stopwords: set

    def get_synonyms(self, target_word, sentence=None, threshold=0.0):
        pass

    def get_hypernyms(self, target_word, sentence=None, threshold=0.0):
        pass

    def get_antonyms(self, target_word, sentence=None, threshold=0.0):
        pass


class RoWordNet(WordNet):
    wn: rowordnet.RoWordNet

    def __init__(self):
        self.language = "romanian"
        self.wn = rowordnet.RoWordNet()
        self.stop_words = set(stopwords.words("romanian"))
        self.pos_map = {
            'NN': 'n', 'NNS': 'n', 'NNP': 'n', 'NNPS': 'n',
            'VB': 'v', 'VBD': 'v', 'VBG': 'v', 'VBN': 'v',
            'VBP': 'v', 'VBZ': 'v',
            'JJ': 'a', 'JJR': 'a', 'JJS': 'a',
            'RB': 'r', 'RBR': 'r', 'RBS': 'r'
        }

    def get_synonyms(self, target_word, sentence=None, threshold=0.0):
        if sentence is None:
            sentence = target_word

        context_vec = get_context_vector(sentence, target_word, self.stop_words)

        synonym_scores = {}

        synset_ids = self.wn.synsets(target_word)

        for synset_id in synset_ids:
            synset = self.wn.synset(synset_id)
            synset_vec = get_synset_vector(synset.definition, self.stop_words)
            similarity = vector_similarity(context_vec, synset_vec)

            for literal in synset.literals:
                if literal.lower() != target_word.lower():
                    current_score = synonym_scores.get(literal, 0)
                    synonym_scores[literal] = max(current_score, similarity)

        filtered_synonyms = [(syn, score) for syn, score in synonym_scores.items()
                             if score >= threshold]
        filtered_synonyms.sort(key=lambda x: x[1], reverse=True)
        return [synonym for synonym, _ in filtered_synonyms]

    def get_hypernyms(self, target_word, sentence=None, threshold=0.0):
        if sentence is None:
            sentence = target_word

        context_vec = get_context_vector(sentence, target_word, self.stop_words)

        hypernym_scores = {}

        synset_ids = self.wn.synsets(target_word)

        for synset_id in synset_ids:
            synset = self.wn.synset(synset_id)
            synset_vec = get_synset_vector(synset.definition, self.stop_words)
            similarity = vector_similarity(context_vec, synset_vec)

            synset_hypernym_path = self.wn.synset_to_hypernym_root(synset_id)
            if len(synset_hypernym_path) < 2:
                continue
            synset_hypernym_id = synset_hypernym_path[1]
            synset_hypernyms = self.wn.synset(synset_hypernym_id)

            for hypernym in synset_hypernyms.literals:
                current_score = hypernym_scores.get(hypernym, 0)
                hypernym_scores[hypernym] = max(current_score, similarity)

        filtered_hypernyms = [(hyper, score) for hyper, score in hypernym_scores.items()
                              if score >= threshold]
        filtered_hypernyms.sort(key=lambda x: x[1], reverse=True)
        return [hypernym for hypernym, _ in filtered_hypernyms]

    def get_antonyms(self, target_word, sentence=None, threshold=0.0):
        if sentence is None:
            sentence = target_word

        context_vec = get_context_vector(sentence, target_word, self.stop_words)

        antonym_scores = {}

        synset_ids = self.wn.synsets(target_word)

        for synset_id in synset_ids:
            synset = self.wn.synset(synset_id)
            synset_vec = get_synset_vector(synset.definition, self.stop_words)
            similarity = vector_similarity(context_vec, synset_vec)

            synset_outbound_ids = self.wn.outbound_relations(synset_id)
            synset_antonyms_id = [synset_tuple[0] for synset_tuple in synset_outbound_ids
                                  if synset_tuple[1] == 'near_antonym']

            for antonym_id in synset_antonyms_id:
                synset_antonyms = self.wn.synset(antonym_id)
                antonyms = synset_antonyms.literals
                for antonym in antonyms:
                    current_score = antonym_scores.get(antonym, 0)
                    antonym_scores[antonym] = max(current_score, similarity)

        filtered_antonyms = [(ant, score) for ant, score in antonym_scores.items()
                             if score >= threshold]
        filtered_antonyms.sort(key=lambda x: x[1], reverse=True)
        return [antonym for antonym, _ in filtered_antonyms]


class EnWordNet(WordNet):
    wn: wn_en

    def __init__(self):
        self.wn = wn_en
        self.language = "english"
        self.stop_words = set(stopwords.words("english"))
        self.pos_map = {
            'NN': 'n', 'NNS': 'n', 'NNP': 'n', 'NNPS': 'n',
            'VB': 'v', 'VBD': 'v', 'VBG': 'v', 'VBN': 'v',
            'VBP': 'v', 'VBZ': 'v',
            'JJ': 'a', 'JJR': 'a', 'JJS': 'a',
            'RB': 'r', 'RBR': 'r', 'RBS': 'r'
        }

    def get_synonyms(self, target_word, sentence=None, threshold=0.0):
        if sentence is None:
            sentence = target_word
        tokens = word_tokenize(sentence)
        pos_tags = pos_tag(tokens)
        target_pos = None

        for word, pos in pos_tags:
            if word.lower() == target_word.lower():
                target_pos = self.pos_map.get(pos)
                break

        context_vec = get_context_vector(sentence, target_word, self.stop_words)

        synonym_scores = {}

        synsets = self.wn.synsets(target_word)
        if target_pos:
            synsets = [s for s in synsets if s.pos() == target_pos]

        for synset in synsets:
            synset_vec = get_synset_vector(synset.definition(), self.stop_words)
            similarity = vector_similarity(context_vec, synset_vec)

            for lemma in synset.lemmas():
                synonym = lemma.name()
                if synonym.lower() != target_word.lower():
                    current_score = synonym_scores.get(synonym, 0)
                    synonym_scores[synonym] = max(current_score, similarity)

        filtered_synonyms = [(syn, score) for syn, score in synonym_scores.items()
                             if score >= threshold]
        filtered_synonyms.sort(key=lambda x: x[1], reverse=True)
        return [synonym for synonym, _ in filtered_synonyms]

    def get_antonyms(self, target_word, sentence=None, threshold=0.0):
        if sentence is None:
            sentence = target_word
        tokens = word_tokenize(sentence)
        pos_tags = pos_tag(tokens)
        target_pos = None

        for word, pos in pos_tags:
            if word.lower() == target_word.lower():
                target_pos = self.pos_map.get(pos)
                break

        context_vec = get_context_vector(sentence, target_word, self.stop_words)

        antonym_scores = {}

        synsets = self.wn.synsets(target_word)
        if target_pos:
            synsets = [s for s in synsets if s.pos() == target_pos]

        for synset in synsets:
            synset_vec = get_synset_vector(synset.definition(), self.stop_words)
            similarity = vector_similarity(context_vec, synset_vec)

            for lemma in synset.lemmas():
                antonym = lemma.antonyms()
                if antonym:
                    antonym = antonym[0].name()
                    current_score = antonym_scores.get(antonym, 0)
                    antonym_scores[antonym] = max(current_score, similarity)

        filtered_antonyms = [(ant, score) for ant, score in antonym_scores.items()
                             if score >= threshold]
        filtered_antonyms.sort(key=lambda x: x[1], reverse=True)
        return [antonym for antonym, _ in filtered_antonyms]

    def get_hypernyms(self, target_word, sentence=None, threshold=0.0):
        if sentence is None:
            sentence = target_word
        tokens = word_tokenize(sentence)
        pos_tags = pos_tag(tokens)
        target_pos = None

        for word, pos in pos_tags:
            if word.lower() == target_word.lower():
                target_pos = self.pos_map.get(pos)
                break

        context_vec = get_context_vector(sentence, target_word, self.stop_words)

        hypernym_scores = {}
        synsets = self.wn.synsets(target_word)
        if target_pos:
            synsets = [s for s in synsets if s.pos() == target_pos]

        for synset in synsets:
            synset_vec = get_synset_vector(synset.definition(), self.stop_words)
            similarity = vector_similarity(context_vec, synset_vec)

            for hypernym in synset.hypernyms():
                for lemma in hypernym.lemmas():
                    hypernym = lemma.name()
                    current_score = hypernym_scores.get(hypernym, 0)
                    hypernym_scores[hypernym] = max(current_score, similarity)

        filtered_hypernyms = [(hyper, score) for hyper, score in hypernym_scores.items()
                              if score >= threshold]
        filtered_hypernyms.sort(key=lambda x: x[1], reverse=True)
        return [hypernym for hypernym, _ in filtered_hypernyms]
