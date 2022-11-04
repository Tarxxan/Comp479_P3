import time

from reuters import setup, get_files


def remove_dup(f, dict):
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


def term_doc(tokenized_list, f=[]):
    for doc in tokenized_list:
        for tup in doc:
            (id, title, body) = tup
            for t in title:
                f.append(tuple([id, t.lower()]))
            for b in body:
                f.append(tuple([id, b.lower()]))


def term_doc_case(tokenized_list, f=[]):
    for doc in tokenized_list:
        for tup in doc:
            (id, title, body) = tup
            id = int(id[0])
            for t in title:
                f.append(tuple([id, t]))
            for b in body:
                f.append(tuple([id, b]))

    # HAVE ALL THE TOKENIZED TEXT HERE NEED TO MAP IT NOW


def postings_list(no_dupes, postings):
    for key in no_dupes.keys():
        for val in no_dupes[key]:
            if val in postings.keys():
                postings[val].append(key)
            else:
                postings[val] = list()
                postings[val].append(key)
            postings[val].sort()


def indexer():
    count = 0
    f = []
    noDupes, postings = {}, {}
    fileList = get_files()
    start_time = time.time()
    f = setup(fileList)
    remove_dup(f, noDupes)
    postings_list(noDupes, postings)
    return start_time, postings
