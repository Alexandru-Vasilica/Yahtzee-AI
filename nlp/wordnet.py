import nltk
import rowordnet


class WordNet:
    def get_synonyms(self, word):
        pass

    def get_hypernyms(self, word):
        pass

    def get_antonyms(self, word):
        pass


class RoWordNet(WordNet):
    wn: rowordnet.RoWordNet

    def __init__(self):
        self.wn = rowordnet.RoWordNet()

    def get_synonyms(self, word):
        synonyms = set()
        synset_ids = self.wn.synsets(word, strict=True)
        for synset_id in synset_ids:
            synset = self.wn.synset(synset_id)
            literals = list(synset.literals)
            synonyms.update(literals)
        synonyms.discard(word)
        return synonyms

    def get_hypernyms(self, word):
        synset_ids = self.wn.synsets(word, strict=True)
        hypernyms = set()
        for synset_id in synset_ids:
            synset_hypernym_path = self.wn.synset_to_hypernym_root(synset_id)
            if len(synset_hypernym_path) < 2:
                continue
            synset_hypernym_id = synset_hypernym_path[1]
            synset_hypernyms = self.wn.synset(synset_hypernym_id)
            hypernyms.update(synset_hypernyms.literals)
        hypernyms.discard(word)
        return hypernyms

    def get_antonyms(self, word):
        synset_ids = self.wn.synsets(word, strict=True)
        antonyms = set()
        for synset_id in synset_ids:
            synset_outbound_ids = self.wn.outbound_relations(synset_id)
            synset_antonyms_id = [synset_tuple[0] for synset_tuple in synset_outbound_ids
                                  if synset_tuple[1] == 'near_antonym']

            for antonym_id in synset_antonyms_id:
                synset_antonyms = self.wn.synset(antonym_id)
                antonyms.update(synset_antonyms.literals)
        return antonyms


class EnWordNet(WordNet):
    wn: nltk.corpus.wordnet

    def __init__(self):
        self.wn = nltk.corpus.wordnet

    def get_synonyms(self, word):
        synonyms = set()
        for synset in self.wn.synsets(word):
            for lemma in synset.lemmas():
                synonyms.add(lemma.name())
        synonyms.discard(word)
        return synonyms

    def get_hypernyms(self, word):
        hypernyms = set()
        for syn in self.wn.synsets(word):
            for hyper in syn.hypernyms():
                for lemma in hyper.lemmas():
                    hypernyms.add(lemma.name())
        return hypernyms

    def get_antonyms(self,word):
        antonyms = set()
        for syn in self.wn.synsets(word):
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    antonyms.add(lemma.antonyms()[0].name())
        return antonyms
