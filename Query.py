from collections import Counter

from nltk.corpus import stopwords


class Query:

    def __init__(self, indexer):
        self.result = None
        self.indexer = indexer
        self.result_and = None
        self.result_or = None

    def intersect(self):
        if self.result:
            final_intersection = self.result[0]
            for i in self.result[1:]:
                new_list = set(final_intersection).intersection(i)
                final_intersection = new_list
            self.result_and = sorted(final_intersection)

    def union(self):
        or_list = []
        or_dict = {}
        result = []
        for i in range(len(self.result)):
            or_list.extend(self.result[i])

        for i in or_list:
            if i in or_dict:
                or_dict[i] += 1
            else:
                or_dict[i] = 1

        or_list = sorted(or_dict.items(), key=lambda lst: lst[1], reverse=True)

        for i in or_list:
            result.append(i[0])

        self.result_or = result


    def query_operation(self, query, operation):
        list_of_dictionary = []
        stopword_list = set(stopwords.words('english'))
        query_tokenized = query.split(" ")
        for word in query_tokenized:
            if word not in stopword_list:
                if word in self.indexer.naive:
                    list_of_dictionary.append(self.indexer.naive[word])
            self.result = sorted(list_of_dictionary, key=len)
        if operation == "and":
            return self.intersect()
        else:
            return self.union()
