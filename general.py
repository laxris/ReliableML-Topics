# git clone https://github.com/zelandiya/RAKE-tutorial
import rake
import operator
import nltk
from nltk.stem import *
from nltk.tokenize import RegexpTokenizer

STOPPATH = 'SmartStoplist.txt'
STOPWORDS = rake.load_stop_words(STOPPATH)


def get_keywords_of_single_abstract_grams(abstract):
    abstract = abstract.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(abstract)
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens if t not in STOPWORDS]
    bigrams = nltk.bigrams(tokens)
    trigrams = nltk.trigrams(tokens)
    keyword_candidates = nltk.FreqDist(bigrams) + nltk.FreqDist(trigrams)

    keywords = keyword_candidates.iteritems()
    keywords = [(' '.join(w for w in k), score) for k, score in keywords]

    sorted_keywords = sorted(keywords, key=operator.itemgetter(1), reverse=True)
    total_keywords = len(sorted_keywords)
    return [k[0] for k in sorted_keywords[0:total_keywords / 3]]


def get_keywords_of_single_abstract_RAKE(abstract):
    sentence_list = rake.split_sentences(abstract)
    stopword_pattern = rake.build_stop_word_regex(STOPPATH)
    phrase_list = rake.generate_candidate_keywords(sentence_list, stopword_pattern)
    word_scores = rake.calculate_word_scores(phrase_list)
    keyword_candidates = rake.generate_candidate_keyword_scores(phrase_list, word_scores)

    keywords = keyword_candidates.iteritems()
    keywords = list(keywords)
    stemmer = PorterStemmer()
    keywords = [(' '.join(stemmer.stem(w) for w in k.split(' ')), score) for k, score in keywords]

    sorted_keywords = sorted(keywords, key=operator.itemgetter(1), reverse=True)
    total_keywords = len(sorted_keywords)
    return [k[0] for k in sorted_keywords[0:total_keywords / 3]]
