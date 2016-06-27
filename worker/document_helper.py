import  nltk


def get_features(words, word_features):
    """
    Given a string with a word_features as universe,
    it will return their respective features
    : param words: String to generate the features to
    : param word_features: Universe of words
    : return: Dictionary with the features for document string
    """
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features
