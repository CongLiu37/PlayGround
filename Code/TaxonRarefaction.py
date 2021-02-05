"""
DESCRIPTION:
(1) Sample the raw_raw_data (un-filtered by BGI)
(2) Extract sampled sequence IDs
(3) Extract hits from blast file
(4) Extract corresponded host-filtered reads
(5) Taxon profile (MEGAN6)

i in 1:10

ARGUMENT:
sample name, sample percentage, threads, i
"""

import os
import sys
import main
import time
import pandas as pd

usr = "/rds/general/user/cl3820/"
args = sys.argv ##[script_name, sample_name, percentage, threads, i]
i = args[4]

fq1 = usr+"home/bowtie2/"+args[1]+"_filterhost.1.fq"
fq2 = usr+"home/bowtie2/"+args[1]+"_filterhost.2.fq"

#Subsample raw_raw data, spit fasta
main.subsampling_fastq(fastq=usr+"home/raw_raw_data/"+args[1]+"_1.fq.gz",percentage=float(args[2]),output=usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+".fasta")

#Extract sampled IDs
print("Start extract IDs")
start = time.time()
ID_s = main.extract_fastaIDs(usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+".fasta",usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+"_IDs.txt")
end = time.time()
print("Done: "+str(end-start))

#Extract corresponded blast
print("Start extract blast 1")
start = time.time()
blast = pd.read_table(usr+"ephemeral/Blast/"+args[1]+"_1.blast",sep="\t",header=None)
sub = blast[blast[0].isin(ID_s)]
sub.to_csv(usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+"_1.blast",index=False,header=False,sep="\t")
end = time.time()
print("Done: "+str(end-start))

print("Start extract blast 2")
start = time.time()
blast = pd.read_table(usr+"ephemeral/Blast/"+args[1]+"_2.blast",sep="\t",header=None)
sub = blast[blast[0].isin(ID_s)]
sub.to_csv(usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+"_2.blast",index=False,header=False,sep="\t")
end = time.time()
print("Done: "+str(end-start))
#Extract corresponded clean reads (host-filtered)
#main.extract_fastq(IDs=ID_s,fastq=usr+"home/bowtie2/"+args[1]+"_filterhost.1.fq",output=usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+"_1.fasta")
#main.extract_fastq(IDs=ID_s,fastq=usr+"home/bowtie2/"+args[1]+"_filterhost.2.fq",output=usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+"_2.fasta")

#Taxon profile
main.run_MEGAN6(blastfile1=usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+"_1.blast",blastfile2=usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+"_2.blast",output=usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+".rma",mdb=usr+"home/MEGANDatabse/megan-map-Jul2020-2.db",threads=args[3])

main.rma_extract(rma=usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+".rma",output=usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+"TaxonProfile.txt")

os.system("rm "+usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+".fasta")
os.system("rm "+usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+"_1.blast")
os.system("rm "+usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+"_2.blast")
os.system("rm "+usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+".rma")
os.system("rm "+usr+"ephemeral/TaxonRarefaction/"+str(i)+args[1]+"_"+args[2]+"_IDs.txt")
