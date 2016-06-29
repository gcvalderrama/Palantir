import nltk


class BigramController:
    def __init__(self):
        """

        """

    def BuildBigrams(self, words):
        bigrams = nltk.bigrams(words)
        return bigrams

    def BuildBrigramFeatures(self, words):
        bigrams = self.BuildBigrams(words)
        bigrams = sorted(set(bigrams), key=lambda c: c[0])
        return bigrams

    def BuildBigramFeaturesSet(self, CorpusBigrams, DocumentBigrams):
        features = {}
        for w in CorpusBigrams:
            features[w] = any(w[0] == d[0] and w[1] == d[1] for d in DocumentBigrams)
        return features

    def BigramStatistics(self, bigrams):
        bigramdist = nltk.FreqDist(bigrams)
        print("Bigram distribution")
        print(bigramdist.most_common(20))