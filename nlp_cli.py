import argparse

from nlp.utils import detect_language, SUPPORTED_LANGUAGES, get_stylometric_features, rephrase_text, extract_keywords, \
    unify_keywords, generate_pos_tags, generate_sentence_with_keyword
from nlp.wordnet import EnWordNet, RoWordNet


def main():
    parser = argparse.ArgumentParser(description='NLP Command Line Interface')
    parser.add_argument('input', type=str, help='Input to be processed')
    parser.add_argument('--file', action='store_true', help='Treats input as file path')
    parser.add_argument('--verbose', action='store_true', help='Prints additional information')
    args = parser.parse_args()
    if args.file:
        with open(args.input, 'r') as file:
            text = file.read()
    else:
        text = args.input
    language = detect_language(text)
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}. Supported languages: {SUPPORTED_LANGUAGES}")
    else:
        wn = RoWordNet() if language == 'ro' else EnWordNet()
    print(f"Detected language: {language}")
    stylometric_features = get_stylometric_features(text)
    print(f'---Stylometric Features---')
    print(f'Word length: {stylometric_features["word_length"]}')
    print(f'Character length: {stylometric_features["char_length"]}')
    print('--Word Frequency--')
    shown_word_frequencies = len(stylometric_features['word_freq'].items()) if args.verbose else 10
    for word, freq in sorted(stylometric_features['word_freq'].items(), key=lambda x: x[1], reverse=True)[:shown_word_frequencies]:
        print(f'Word: {word}, Frequency: {freq}')
    print('--Character Frequency--')
    shown_char_frequencies = len(stylometric_features['char_freq'].items()) if args.verbose else 10
    for char, freq in sorted(stylometric_features['char_freq'].items(), key=lambda x: x[1], reverse=True)[:shown_char_frequencies]:
        print(f'Character: {char}, Frequency: {freq}')
    print("--Rephrased Text--")
    rephrased_text = rephrase_text(text, wn, syn_ration=0.2, hyper_ration=0, ant_ration=0.1)
    print(rephrased_text)
    print("----Keywords----")
    keyword_len = 10 if args.verbose else 5
    keywords = extract_keywords(text, language=wn.language)
    modified_keywords, modified_text = unify_keywords(keywords, text)
    pos_tags = generate_pos_tags(modified_text)
    for modified_keyword in modified_keywords:
        sentence = generate_sentence_with_keyword(modified_keyword, pos_tags)
        if sentence is not None:
            print(f'Keyword: {modified_keyword}')
            print(sentence)
            keyword_len -= 1
            if keyword_len == 0:
                break


if __name__ == '__main__':
    main()
