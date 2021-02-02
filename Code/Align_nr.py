"""
DESCRIPTION:
Align un-mapped reads with non-redundant database (diamond).

ARGUMENT:
sequence file, threads
"""

import os
import sys
import time
import main

home = "/rds/general/user/cl3820/"
args = sys.argv #sequence file, threads

start = time.time()
main.diamond_blastx(query=args[1],db=home+"home/nr_diamond/nr.dmnd",out=home+"ephemeral/Blast/"+args[1]+"_1.blast",threads=args[2])
end = time.time()
print("Alignment:"+str(end-start))