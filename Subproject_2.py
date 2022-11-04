import json
from collections import Counter

from nltk import word_tokenize
from nltk.corpus import stopwords


def load_indexer():

    with open('C:/Users/christian.henneveld/PycharmProjects/Comp479_P3/Reuters/BM25.txt', 'r') as fp:
        data = json.load(fp)
        return data

""" Responsible for all the calculation and logic of BM25.
    Creates another indexer in here instead of using the one on file because
    we need total terms and each documents length (terms). The actual inverted
    index is never used from this function
"""


def intersect(result):
    final_intersection = result[0]
    for i in result[0:]:
        new_list= set(final_intersection).intersection(i)
        final_intersection = new_list
    return sorted(final_intersection)


def union(result):
    or_list = []
    for i in range(len(result)):
        or_list.extend(result[i])
    # https://stackoverflow.com/questions/23429426/sorting-a-list-by-frequency-of-occurrence-in-a-list
    sorted_dup = sorted(or_list, key=Counter(or_list).get, reverse=True)
    result = []
    for num in sorted_dup:
        if num not in result:
            result.append(num)
    return result


def query_operation(data, query, operation):
    list_of_dictionary = []
    stopword_list = set(stopwords.words('english'))
    query_tokenized = word_tokenize(query)
    for word in query_tokenized:
        if word not in stopword_list:
            if word in data:
                list_of_dictionary.append(data[word])
        result = sorted(list_of_dictionary, key=len)
    if operation == "and":
        return intersect(result)
    else:
        return union(result)
