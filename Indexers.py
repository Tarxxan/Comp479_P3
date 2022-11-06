from itertools import groupby
import time
from nltk import word_tokenize
from reuters import get_files, raw_text


class Indexers:
    def __init__(self, timed="naive"):
        if timed == "naive":
            self.naive, self.document_lengths, self.total_doc_length, self.df_term_data = self.naive_indexer()
        elif timed == "p2":
            self.p2, self.start_time = self.timed_indexer_p2()
        else:
            self.SPIMI, self.start_time = self.timed_indexer_spimi()

    def term_document_frequency(self, data):
        tdF = {}
        for key in data:
            tdF[key] = []
            """
            https://stackoverflow.com/questions/2161752/how-to-count-the-frequency-of-the-elements-in-an-unordered-list
            only works because the numbers are already sorted. Functional approach quicker and cleaner than this long
            loop with many if checks. The functional approach uses sorted which is optimized comapred to raw loops.
            This got me to start looking at the sorted function for lists which ended up being used often in my code
            
            count = 1
            for i in range(len(data[key]) - 1):
                if i == data[key][i + 1]:
                    count += 1
                else:
                    if count >1:
                        print(count)
                    tdF[key].append(int(count))
                    count = 1
            """
            tdF[key].extend([len(list(group)) for key, group in groupby(data[key])])
        return tdF

    def remove_posting_dup(self, data):
        for key in data:
            list_set = list(set(data[key]))
            data[key] = list_set
        return data

    def create_indexer(self, rt, naive_dict):
        total_doc_length = 0
        document_lengths = []
        document_length = 0
        remove = ["lt", ",", ".", ">", "<", "-", ";", ":", "&", "#", "?", "!"]
        for reuters in rt:
            for lists in reuters:
                (id, title, body) = lists
                if title:
                    words = word_tokenize(title[0])
                    document_length += len(words)
                    for word in words:
                        if word not in remove:
                            if word not in naive_dict:
                                naive_dict[word] = [id]
                            else:
                                naive_dict[word].append(id)
                else:
                    pass

                if body:
                    words = word_tokenize(body[0])
                    document_length += len(words)
                    for word in words:
                        if word not in remove:
                            if word not in naive_dict:
                                naive_dict[word] = [id]
                            else:
                                naive_dict[word].append(id)
                else:
                    pass
                document_lengths.append(document_length)
                total_doc_length += document_length
                document_length = 0
        return naive_dict, document_lengths, total_doc_length,

    def naive_indexer(self):
        naive = {}
        new = {}
        document_lengths = []
        total_doc_length = 0
        fileList = get_files()
        for file in fileList:
            new = naive
            rt = raw_text(file)
            naive, document_length, total_doc = self.create_indexer(rt, new)
            document_lengths.extend(document_length)
            total_doc_length += total_doc
        df_term_data = self.term_document_frequency(naive)
        naive = self.remove_posting_dup(naive)
        return naive, document_lengths, total_doc_length, df_term_data

    def create_timed_spimi(self, token_list):
        spimi = {}
        for articles in token_list:
            for words in articles[1:]:
                if words in spimi:
                    spimi[words].append(articles[0])
                else:
                    spimi[words] = [articles[0]]
        return spimi

    def create_timed_p2(self, token_list):
        f = []
        for articles in token_list:
            for words in articles[1:]:
                f.append([articles[0], words])
        return f

    def timed_indexer_spimi(self):
        timed_spimi = {}
        count = 0
        new = {}
        fileList = get_files()
        for file in fileList:
            rt = raw_text(file)
            tokens = self.create_10k_tokens(rt)
            start_time = time.perf_counter()
            timed_spimi = self.create_timed_spimi(tokens)
            break
        return timed_spimi, start_time

    def timed_indexer_p2(self):
        count = 0
        f = []
        fileList = get_files()
        for file in fileList:
            new = f
            rt = raw_text(file)
            tokens = self.create_10k_tokens(rt)
            start_time = time.perf_counter()
            f = self.create_timed_p2(tokens)
        no_dupes = self.remove_dup(f)
        postings = self.postings_list(no_dupes)
        return postings, start_time

    def remove_dup(self, f):
        dict = {}
        for tups in f:
            (key, value) = tups
            if key not in dict:
                dict[key] = list()
                dict[key].append(value)
            else:
                if value in dict.get(key):
                    pass
                else:
                    dict[key].append(value)
        return dict

    def postings_list(self, no_dupes):
        postings = {}
        for key in no_dupes.keys():
            for val in no_dupes[key]:
                if val in postings.keys():
                    postings[val].append(key)
                else:
                    postings[val] = list()
                    postings[val].append(key)
                postings[val].sort()
        return postings

    def create_10k_tokens(self, raw_list=None, naive_dict=None):
        count = 0
        remove = ["lt", ",", ".", ">", "<", "-", ";", ":", "&", "#", "?", "!"]
        list_10k_terms = []
        doc_terms = []
        for reuters in raw_list:
            for lists in reuters:
                doc_terms.clear()
                (id, title, body) = lists
                doc_terms.append(id)
                if title:
                    words = word_tokenize(title[0])
                    for word in words:
                        if word not in remove:
                            doc_terms.append(word)
                            count += 1
                            if count == 10000:
                                list_10k_terms.append(doc_terms[:])
                                return list_10k_terms
                if body:
                    words = word_tokenize(body[0])
                    for word in words:
                        if word not in remove:
                            doc_terms.append(word)
                            count += 1
                            if count == 10000:
                                list_10k_terms.append(doc_terms[:])
                                return list_10k_terms
                list_10k_terms.append(doc_terms[:])
            return list_10k_terms
