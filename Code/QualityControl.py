"""
DESCRIPTION:
(1) Quality report of raw data (fastqc)
(2) Data filter (trimmomatic)
    remove nextera adaptor
	crop 15 bases from heads
	crop bases with quality score lower than 20 from tails
	filter reads shorter than 36 bp
(3) Quality report of clean data (fastqc)

ARGUMENTS:
<sample>, threads
"""

import os
import main
import sys
import time

home="/rds/general/user/cl3820/home/"
args = sys.argv #sample name, threads

start = time.time()
main.run_fastqc(clean1=home+"raw_data/"+args[1]+"_1.fq.gz",clean2=home+"raw_data/"+args[1]+"_2.fq.gz",output=home+"QualityControl/raw/",threads=args[2])
end = time.time()
print("Quality report of raw data: "+str(end-start))

start = time.time()
main.run_trimmomatic(file1=home+"raw_data/"+args[1]+"_1.fq.gz",file2=home+"raw_data/"+args[1]+"_2.fq.gz",clean1=home+"clean_data/"+args[1]+"_1.fq.gz",clean2=home+"clean_data/"+args[1]+"_2.fq.gz",unpaired1=home+"clean_data/unpaired_"+args[1]+"_1.fq.gz",unpaired2=home+"clean_data/unpaired_"+args[1]+"_2.fq.gz",adaptor=home+"DataFile.txt",threads=args[2])
end = time.time()
print("Data filtering: "+str(end-start))

start = time.time()
main.run_fastqc(clean1=home+"clean_data/"+args[1]+"_1.fq.gz",clean2=home+"clean_data/"+args[1]+"_2.fq.gz",output=home+"QualityControl/clean",threads=args[2])
end = time.time()
print("Quality report of clean data: "+str(end-start))