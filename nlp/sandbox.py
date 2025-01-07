from nltk.corpus import wordnet
import rowordnet

from nlp.utils import detect_language, get_wordnet_api, get_stylometric_features, extract_keywords, tokenize_text, \
    rephrase_text, generate_ngrams
from nlp.wordnet import RoWordNet, EnWordNet, WordNet

ro_wn = rowordnet.RoWordNet()
en_wn = EnWordNet()

text = "The climate of change on the global is significant.warming is a major factor in impact.The environment is affected by climate.Many studies have shown the change of global on warming."
keywords = extract_keywords(text, max_length=5)
print(keywords)

sentences = generate_ngrams(text, 20)
print(sentences)

# eng_sentence = "I am a sentence in English."
# ro_sentence = "Eu sunt o propoziție în română."
#
# language = detect_language(ro_sentence)
# wn = get_wordnet_api(language)
#
# print(rephrase_text("Ana are mere și pere iar Maria merge acasă la ea aproape.", ro_wn, syn_ration=0.2, hyper_ration=0, ant_ration=0.1))

# print(ro_wn.get_synonyms("aproape"))
# print(ro_wn.get_hypernyms("aproape"))
# print(ro_wn.get_antonyms("aproape"))
#
# print(en_wn.get_synonyms("near"))
# print(en_wn.get_hypernyms("near"))
# print(en_wn.get_antonyms("near"))
