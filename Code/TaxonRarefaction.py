"""
DESCRIPTION:
(1) Sample the raw_raw_data (un-filtered by BGI)
(2) Extract sampled sequence IDs
(3) Extract hits from blast file
(4) Taxon profile (MEGAN6)

ARGUMENT:
sample name, sample percentage, threads
"""

import os
import sys
import main

usr = "/rds/general/user/cl3820/"
args = sys.argv ##[script_name, sample_name, percentage, threads]

fq1 = usr+"home/bowtie2/"+args[1]+"_filterhost.1.fq"
fq2 = usr+"home/bowtie2/"+args[1]+"_filterhost.2.fq"

main.subsampling_fastq(fastq=fq1,percentage=float(args[2]),output=usr+"ephemeral/TaxonRarefaction/"+args[1]+"_"+args[2]+".fasta")

ID_s = main.extract_fastaIDs(usr+"ephemeral/TaxonRarefaction/"+args[1]+"_"+args[2]+".fasta")

main.extract_blast(IDs=ID_s,blastfile=usr+"ephemeral/Blast/"+args[1]+"_1.blast",output=usr+"ephemeral/TaxonRarefaction/"+args[1]+"_"+args[2]+"_1.blast")
main.extract_blast(IDs=ID_s,blastfile=usr+"ephemeral/Blast/"+args[1]+"_2.blast",output=usr+"ephemeral/TaxonRarefaction/"+args[1]+"_"+args[2]+"_2.blast")

main.run_MEGAN6(blastfile1=usr+"ephemeral/TaxonRarefaction/"+args[1]+"_"+args[2]+"_1.blast",blastfile2=usr+"ephemeral/TaxonRarefaction/"+args[1]+"_"+args[2]+"_2.blast",output=usr+"ephemeral/TaxonRarefaction/"+args[1]+"_"+args[2]+".rma",mdb=home+"home/MEGANDatabse/megan-map-Jul2020-2.db",threads=args[3])

main.rma_extract(rma=usr+"ephemeral/TaxonRarefaction/"+args[1]+"_"+args[2]+".rma",output=home+"ephemeral/TaxonRarefaction/"+args[1]+"_"+args[2]+"TaxonProfile.txt")
