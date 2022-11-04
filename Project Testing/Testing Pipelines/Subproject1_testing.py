import json
import time

from Indexers import *

# Time to create the indexer with 10000 doc pairs
print("10 000 Term-DocID pairs for the SPIMI inspired indexer")
naive, start_time = indexer()
print("--- %s seconds --- \n" % (time.time() - start_time))
print("10 000 Term-DocID pairs for the P2 indexer")
start_time,indp2 = indexer_p2()
print("--- %s seconds ---" % (time.time() - start_time))
start_time = (time.time())

#create index from p2 just have to figure out what to import

# For fun checks how long it takes to create the whole corpus

start_time=time.time()
indexer = Indexers()
print("--- %s seconds ---" % (time.time() - start_time))
with open('SPIMI_int.txt', 'w') as convert_file:
    convert_file.write(json.dumps(indexer.naive))
