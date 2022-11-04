from itertools import groupby

from nltk import word_tokenize

from reuters import get_files, raw_text


class Indexers:

    def __init__(self):
        self.naive, \
        self.document_lengths, \
        self.total_doc_length, \
        self.df_term_data = Indexers.naive_indexer(self)

    def term_document_frequency(self, data):
        tdF = {}
        for key in data:
            tdF[key] = []
            # https://stackoverflow.com/questions/2161752/how-to-count-the-frequency-of-the-elements-in-an-unordered-list
            # only works because the numbers are already sorted
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

    def naive_indexer(self, timed=False):
        naive = {}
        new = {}
        document_lengths = []
        total_doc_length = 0
        fileList = get_files()
        for file in fileList:
            new = naive
            rt = raw_text(file)
            naive, document_length, total_doc = Indexers.create_indexer(self, rt, new)
            document_lengths.extend(document_length)
            total_doc_length += total_doc
        df_term_data = Indexers.term_document_frequency(self, naive)
        naive = Indexers.remove_posting_dup(self, naive)
        return naive, document_lengths, total_doc_length, df_term_data

    def timed_indexer(self):
        pass

