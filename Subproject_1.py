import time

from nltk import word_tokenize

from reuters import get_files, raw_text


def tokenize_text_10000(raw_list, count):
    naive_dict = {}
    remove = ["lt", ",", ".", ">", "<", "-", ";", ":", "&", "#", "?", "!"]
    for reuters in raw_list:
        for lists in reuters:
            (id, title, body) = lists
            if title:
                words = word_tokenize(title[0])
                for word in words:
                    if word not in remove:
                        if word not in naive_dict:
                            naive_dict[word] = [id]
                        elif word in naive_dict:
                            if id not in naive_dict[word]:
                                naive_dict[word].append(id)
                            else:
                                pass
                        count += 1
                        if count == 10000:
                            return naive_dict, -1
            else:
                pass

            if body:
                words = word_tokenize(body[0])
                for word in words:
                    if word not in remove:
                        if word not in naive_dict:
                            naive_dict[word] = [id]
                        elif word in naive_dict:
                            if id not in naive_dict[word]:
                                naive_dict[word].append(id)
                            else:
                                pass
                        count += 1
                    if count == 10000:
                        return naive_dict, -1
            else:
                pass

    return naive_dict, count


def tokenize_text(rt, naive_dict):
    remove = ["lt", ",", ".", ">", "<", "-", ";", ":", "&", "#", "?", "!"]
    for reuters in rt:
        #by-product of how I separated each article
        for lists in reuters:
            (id, title, body) = lists
            #Chekc if title exists
            if title:
                words = word_tokenize(title[0])
                for word in words:
                    if word not in remove:
                        if word not in naive_dict:
                            naive_dict[word] = [id]
                        elif word in naive_dict:
                            if id not in naive_dict[word]:
                                naive_dict[word].append(id)
                            else:
                                pass
            else:
                pass
            #check if body exists
            if body:
                words = word_tokenize(body[0])
                for word in words:
                    if word not in remove:
                        if word not in naive_dict:
                            naive_dict[word] = [id]
                        elif word in naive_dict:
                            if id not in naive_dict[word]:
                                naive_dict[word].append(id)
                            else:
                                pass
            else:
                pass

    return naive_dict


def indexer():
    count = 0
    fileList = get_files()
    start_time = time.time()
    for file in fileList:
        if count != -1:
            rt = raw_text(file)
            naive, count = tokenize_text_10000(rt, count)
    return naive, start_time


def naive_indexer():
    naive = {}
    new = {}
    fileList = get_files()
    for file in fileList:
        new = naive
        rt = raw_text(file)
        naive = tokenize_text(rt, new)
    return naive
