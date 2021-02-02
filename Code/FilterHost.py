"""
DESCRIPTION:
(1) Map reads to host genome (bowtie2)
(2) Convert sam to bam, sort bam, compute depth (samtools)

ARGUMENTS:
<sample>, host, threads
"""

import os
import sys
import time
import main

home = "/rds/general/user/cl3820/"

args = sys.argv #sample_name, reference_name, threads

file1 = args[1]+"_1"
file2 = args[1]+"_2"

fq_gz1 = home+"home/clean_data/"+file1+".fq.gz"
fq_gz2 = home+"home/clean_data/"+file2+".fq.gz"

print("Reference genome: "+args[2])
print("Start mapping...")

#mapping through bowtie2
start = time.time()
main.bowtie2_map(fasta1=fq_gz1,fasta2=fq_gz2,index=home+"home/reference_genome/"+args[2],sam=home+"home/bowtie2/"+args[1]+".sam",unmap=home+"home/bowtie2/"+args[1]+"_filterhost.fq",threads=args[3])
end = time.time()
print("Filter host:"+str(end-start))

#Sort bam
start = time.time()
main.sort_bam(bam=home+"home/bowtie2/"+args[1]+".sam.bam",out=home+"home/bowtie2/"+args[1]+"_sorted.bam",threads=args[3])
end = time.time()
print("Sort bam:"+str(end-start))

#Compute depth
start = time.time()
main.compute_depth(bam=home+"home/bowtie2/"+args[1]+"_sorted.bam",out=home+"home/bowtie2/depth_"+args[1]+"_"+args[2]+".txt")
end = time.time()
print("Compute depth:"+str(end-start))