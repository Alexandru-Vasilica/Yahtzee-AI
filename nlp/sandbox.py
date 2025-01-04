from nltk.corpus import wordnet
import rowordnet


from nlp.utils import detect_language, get_wordnet_api, get_stylometric_features, extract_keywords, tokenize_text, \
    rephrase_text
from nlp.wordnet import RoWordNet,EnWordNet

ro_wn = RoWordNet()
en_wn = EnWordNet()


eng_sentence = "I am a sentence in English."
ro_sentence = "Eu sunt o propoziție în română."

language = detect_language(ro_sentence)
wn = get_wordnet_api(language)

print(rephrase_text("Ana are mere și pere iar Maria merge acasă la ea aproape.", ro_wn, syn_ration=0.2, hyper_ration=0, ant_ration=0.1))

# print(ro_wn.get_synonyms("aproape"))
# print(ro_wn.get_hypernyms("aproape"))
# print(ro_wn.get_antonyms("aproape"))
#
# print(en_wn.get_synonyms("near"))
# print(en_wn.get_hypernyms("near"))
# print(en_wn.get_antonyms("near"))
