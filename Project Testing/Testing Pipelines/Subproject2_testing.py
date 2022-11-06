from BM25 import *
from Indexers import *
from Query import *

# Creates an instance of the Indexer class which is used to create the inverted index
indexer = Indexers()

query = input("What is your query?")
BM25 = BM25(indexer)
BM25.calculation(query)

print("Document ranked by BM25 in descending order")
# print(BM25.document_rsv)
with open(query + ' ranked.txt', 'w') as f:
    f.write(str(BM25.document_rsv))

query = input("What is your query?")
Query = Query(indexer)

Query.query_operation(query, "and")
Query.query_operation(query, "or")

with open(query + '.txt', 'w') as convert_file:
    convert_file.write("And\n")
    convert_file.writelines(str(Query.result_and))
    convert_file.write("\nOr\n")
    convert_file.writelines(str(Query.result_or))
