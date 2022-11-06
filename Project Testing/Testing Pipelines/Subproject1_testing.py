import json
import time

import Indexer_P2
from Indexer_P2 import *
from Indexers import *

# Time to create the indexer with 10000 doc pairs
print("10 000 Term-DocID pairs for the SPIMI inspired indexer")
indexer = Indexers("spimi")
print("--- %s seconds --- \n" % (time.perf_counter() - indexer.start_time))

with open('SPIMI_int_10k.txt', 'w') as convert_file:
    convert_file.write(json.dumps(indexer.SPIMI))

print("10 000 Term-DocID pairs for the P2 indexer")
indexer2 = Indexers("p2")
print("--- %s seconds ---" % (time.perf_counter() - indexer2.start_time))

with open('P2_int_10k.txt', 'w') as convert_file:
    convert_file.write(json.dumps(indexer.SPIMI))

# create index from p2 just have to figure out what to import

# For fun checks how long it takes to create the whole corpus

start_time = time.time()
indexer = Indexers()
print("--- %s seconds ---" % (time.time() - start_time))
with open('SPIMI_int.txt', 'w') as convert_file:
    convert_file.write(json.dumps(indexer.naive))
