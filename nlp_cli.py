import argparse

from nlp.utils import detect_language, SUPPORTED_LANGUAGES, get_stylometric_features, rephrase_text, extract_keywords
from nlp.wordnet import EnWordNet, RoWordNet


def main():
    parser = argparse.ArgumentParser(description='NLP Command Line Interface')
    parser.add_argument('input', type=str, help='Input to be processed')
    parser.add_argument('--file', action='store_true', help='Treats input as file path')

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
    for word, freq in sorted(stylometric_features['word_freq'].items(), key=lambda x: x[1], reverse=True):
        print(f'Word: {word}, Frequency: {freq}')
    print('--Character Frequency--')
    for char, freq in sorted(stylometric_features['char_freq'].items(), key=lambda x: x[1], reverse=True):
        print(f'Character: {char}, Frequency: {freq}')
    print("--Rephrased Text--")
    rephrased_text = rephrase_text(text, wn, syn_ration=0.2, hyper_ration=0, ant_ration=0.1)
    print(rephrased_text)
    print("----Keywords----")
    keywords = extract_keywords(text)
    for keyword in keywords:
        print(keyword)


if __name__ == '__main__':
    main()
