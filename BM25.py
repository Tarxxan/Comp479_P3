from math import log

from nltk import word_tokenize
from nltk.corpus import stopwords


class BM25:

    def __init__(self, indexer):
        self.indexer = indexer
        self.k1 = 1.2
        self.b = 1
        self.words_idf = []
        self.words_tftd = []
        self.document_rsv = {}

    def idf(self, word):
        N = len(self.indexer.document_lengths)
        dft = len(self.indexer.naive[word])
        return log(N / dft)

    def tftd(self, word):
        tftd = {}
        count = 0
        for val in self.indexer.naive[word]:
            tftd[val] = self.indexer.df_term_data[word][count]
            count += 1
        return tftd

    def calculate_idf_tftd(self, query):
        words_idf = []
        words_tftd = []
        for word in query:
            word_idf = self.idf(word)
            words_idf.append(word_idf)
            word_tftd = self.tftd(word)
            words_tftd.append(word_tftd)
        self.words_idf = words_idf
        self.words_tftd = words_tftd

    def create_rsv(self):
        document_rsv = {}
        for keys in self.words_tftd:
            for key in keys:
                document_rsv[key] = 0
        self.document_rsv = document_rsv

    def calculation(self, query):
        query = word_tokenize(query)
        stopword_list = set(stopwords.words('english'))

        for word in query:
            if word in stopword_list:
                query.remove(word)
        self.calculate_idf_tftd(query)
        self.create_rsv()
        count = 0
        # dictionary corresponding to the word in the query
        for tftd in self.words_tftd:
            # dictionary corresponding to the document
            for document in tftd:
                numerator = (self.k1 + 1) * tftd[document]
                ld = self.indexer.document_lengths[document - 1]
                l_avg = self.indexer.total_doc_length / len(self.indexer.document_lengths)
                denominator = (self.k1 * ((1 - self.b) + self.b * (ld / l_avg)) + tftd[document])
                rsvd = self.words_idf[count] * (numerator / denominator)
                if self.document_rsv[document] == 0:
                    self.document_rsv[document] = rsvd
                else:
                    self.document_rsv[document] += rsvd
            count += 1
        """
        creates a list of tuples dictionary key as first and then score as second element.
        The sorted function then sorts based off the score of each tuple and orders in descending order"""
        self.document_rsv = sorted(self.document_rsv.items(), key=lambda lst: lst[1], reverse=True)
