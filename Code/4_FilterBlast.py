"""
DESCRIPTION:
Filter blast file (tabular format).
For each read, retain hits with: 
    (1) lowest e-value
    (2) identity > 75%

ARGUMENTS:
args[1] = <sample>
"""

import os
import main
import sys
import time
import pandas as pd

home = "/rds/general/user/cl3820/"
args = sys.argv

print("Start")
start = time.time()
main.blast_filter(home+"ephemeral/Blast/"+args[1]+"_1.blast",home+"ephemeral/Blast/"+args[1]+"_1_filtered.blast",home+"ephemeral/Blast",tag=args[1])
end = time.time()
print("End: "+str(end-start))

print("Start")
main.blast_filter(home+"ephemeral/Blast/"+args[1]+"_2.blast",home+"ephemeral/Blast/"+args[1]+"_2_filtered.blast",home+"ephemeral/Blast",tag=args[1])
end = time.time()
print("End: "+str(end-start))