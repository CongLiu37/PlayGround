"""
DESCRIPTION:
Align un-mapped reads with non-redundant database (diamond).
Thresholds:
	e-value < 1e-5
	identity > 50%

ARGUMENT:
args[1] = <sample>
args[2] = <threads>
"""

import os
import sys
import time
import main

home = "/rds/general/user/cl3820/"
args = sys.argv

start = time.time()
main.diamond_blastx(query=home+"home/bowtie2/"+args[1]+"_filterhost.1.fq",db=home+"home/nr_diamond/nr.dmnd",out=home+"ephemeral/Blast/"+args[1]+"_1.blast",threads=args[2])
end = time.time()
print("Alignment 1:"+str(end-start))

start = time.time()
main.diamond_blastx(query=home+"home/bowtie2/"+args[1]+"_filterhost.2.fq",db=home+"home/nr_diamond/nr.dmnd",out=home+"ephemeral/Blast/"+args[1]+"_2.blast",threads=args[2])
end = time.time()
print("Alignment 2:"+str(end-start))
