"""
DESCRIPTION:
Taxon profile (MEGAN6)

ARGUMENT:
sample name, threads
"""


import os
import sys
import time
import main

home = "/rds/general/user/cl3820/"

args = sys.argv #[script_name, sample_name, threads]

#MEGAN
start = time.time()
main.run_MEGAN6(blastfile1=home+"ephemeral/Blast/"+args[1]+"_1.blast",blastfile2=home+"ephemeral/Blast/"+args[1]+"_2.blast",output=home+"ephemeral/MEGAN/"+args[1]+".rma",mdb=home+"home/MEGANDatabse/megan-map-Jul2020-2.db",threads=args[2])
end = time.time()
print("Get rma"+str(end-start))

#Taxon composition
start = time.time()
main.rma_extract(rma=home+"ephemeral/MEGAN/"+args[1]+".rma",output=home+"ephemeral/TaxonProfile/"+args[1]+"TaxonProfile.txt")
end = time.time()
print("Deal rma:"+str(end-start))