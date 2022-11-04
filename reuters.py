# This is a sample Python script.
import os
import re
from copy import deepcopy

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, regexp_tokenize

tokenized_title = []
tokenized_body = []
tokenized_IDs = []
lower_case = []
stemmed_list = []
removed_list = []
ps = PorterStemmer()


# copies two lists by values and merges them together. Takes first from list1 and puts it in a tuple with the first
# index of the second list. It will then return the merged list
def merge(list1, list2):
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list


def merge3(list1, list2, list3):
    merged_list = [(list1[i], list2[i], list3[i],) for i in range(0, len(list1))]
    return merged_list


# Asks the directory for the files and will change the current directory to this so all future files will be created in
# this directory. This also allows it to search for the files in the directory
def get_files():
    reuters_files = []
    path = input("Enter Path to reuters")
    os.chdir(path)
    for file in os.listdir():
        if file.endswith('sgm'):
            reuters_files.append(file)
    return reuters_files


# function called after every module responsible for printing all the contents of a list to the approriate file
def print_reuters(filename, lists):
    count = 0
    if filename == "raw":
        for l in lists:
            with open(filename + "_reuters" + str(count), 'w') as f:
                for tup in l:
                    (title, body) = tup
                    f.write(title + "\t" + body + "\n")
            count += 1
    elif filename == "tokenized":
        for filegroups in lists:
            with open(filename + "_reuters" + str(count), 'w') as f:
                for group in filegroups:
                    for tup in group:
                        for words in tup:
                            f.write(words + " ")
                    f.write("\n")
                count += 1
    elif filename == "lowercase":
        for l in lists:
            with open(filename + "_reuters" + str(count), 'w') as f:
                for file in l:
                    f.write(file + " ")
                f.write("\n")
            count += 1
    elif filename == "porter":
        for l in lists:
            with open(filename + "_reuters" + str(count), 'w') as f:
                for file in l:
                    f.write(file + " ")
                f.write("\n")
            count += 1
    else:
        for l in lists:
            with open("remove_reuters" + str(count), 'w') as f:
                for file in l:
                    for words in file:
                        f.write(words + " ")
                    f.write("\n")
            count += 1


#Changed the tokenize text to work for only 10000 pairs
def tokenize_text(raw_list):
    count = 0
    tokenized_reuters = []
    remove = ["lt", ",", ".", ">", "<", "-", ";", ":", "&", "#", "?", "!"]
    for reuters in raw_list:
        for r in reuters:
            for lists in r:
                (id, title, body) = lists
                if title:
                    words = word_tokenize(title[0])
                    for word in words:
                        if word not in remove:
                            tokenized_reuters.append((id, word))
                            count += 1
                            if count == 10000:
                                return tokenized_reuters
                else:
                    pass
                if body:
                    words = word_tokenize(body[0])
                    for word in words:
                        if word not in remove:
                            tokenized_reuters.append((id, word))
                            count += 1
                            if count == 10000:
                                return tokenized_reuters
                else:
                    pass
        return tokenized_reuters


# parses the raw text of the file (title and body) using regex. This will happen for every article in the file
def raw_text(files):
    raw_list = []
    body = []
    title = []
    newIDs = []
    text_file = open(files)
    data = text_file.read()
    regex = r"NEWID=\"(\d{1,})([\s\S]+?)<\/REUTERS>"
    matches = re.findall(regex, data, re.MULTILINE)

    for match in matches:
        (topics, everything) = match
        newIDs.append(int(topics))
        title.append(regexp_tokenize(everything, '<TITLE>([\s\S]+?)<\/TITLE>'))
        body.append(regexp_tokenize(everything, '<BODY>([\s\S]+?)<\/BODY>'))
    raw_list.append(merge3(newIDs, title, body))
# print_reuters("raw", raw_list)
    return raw_list


# self-explanatory, makes every word in the list lowercase
def to_lower_case(tokenized_reuters):
    l = []
    for i in tokenized_reuters:
        for file in i:
            for lists in file:
                for words in lists:
                    l.append(words.lower())
        a = deepcopy(l)
        lower_case.append(a)
        l.clear()
    print_reuters("lowercase", lower_case)
    return lower_case


# stemmer function from nltk. Logic is added in order to seperate the words of each file
def porter_stemmer(lower_case):
    l = []
    for lc_files in lower_case:
        for words in lc_files:
            l.append(ps.stem(words))
        a = deepcopy(l)
        l.clear()
        stemmed_list.append(a)
    print_reuters("porter", stemmed_list)
    return stemmed_list


# responsible for taking out all stop words in the list from the list of your choice.
def remove_words(stem, remove):
    for files in stem:
        for stop in remove:
            while stop in files:
                files.remove(stop)
        a = deepcopy(files)
        removed_list.append(a)
        files.clear()
    print_reuters("removed", removed_list)

def setup(files):
    rt=[]
    for file in files:
        rt.append(raw_text(file))
    return tokenize_text(rt)
