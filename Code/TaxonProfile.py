"""
DESCRIPTION:
(1) Map reads to host genome (bowtie2, pre-built index)
(2) Convert sam to bam, sort bam, compute depth (samtools)
(3) Align un-mapped reads with non-redundant database (diamond)
(4) Taxon profile (MEGAN6)

ARGUMENT:
sample name, Genus_Species/*_*, threads
"""


import os
import sys
import time
import main

home = "/rds/general/user/cl3820/"

args = sys.argv #[script_name, sample_name, reference_name, threads]

file1 = args[1]+"_1"
file2 = args[1]+"_2"

fq_gz1 = home+"home/clean_data/"+file1+".fq.gz"
fq_gz2 = home+"home/clean_data/"+file2+".fq.gz"

if args[2] != "*_*":
    print("Reference genome: "+args[2])
    print("Start removing reference reads...")
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
    #Alignment
    start = time.time()
    main.diamond_blastx(query=home+"home/bowtie2/"+args[1]+"_filterhost.1.fq",db=home+"home/nr_diamond/nr.dmnd",out=home+"ephemeral/Blast/"+args[1]+"_1.daa",threads=args[3])
    end = time.time()
    print("Alignment 1:"+str(end-start))

    start = time.time()
    main.diamond_blastx(query=home+"home/bowtie2/"+args[1]+"_filterhost.2.fq",db=home+"home/nr_diamond/nr.dmnd",out=home+"ephemeral/Blast/"+args[1]+"_2.daa",threads=args[3])
    end = time.time()
    print("Alignment 2:"+str(end-start))

    #MEGAN
    start = time.time()
    main.run_MEGAN6(blastfile1=home+"ephemeral/Blast/"+args[1]+"_1.daa",blastfile2=home+"ephemeral/Blast/"+args[1]+"_2.daa",output=home+"ephemeral/MEGAN/"+args[1]+".rma",mdb=home+"home/MEGANDatabse/megan-map-Jul2020-2.db",threads=args[3])
    end = time.time()
    print("Get rma"+str(end-start))

    #Taxon composition
    start = time.time()
    main.rma_extract(rma=home+"ephemeral/MEGAN/"+args[1]+".rma",output=home+"ephemeral/TaxonProfile/"+args[1]+"TaxonProfile.txt")
    end = time.time()
    print("Deal rma:"+str(end-start))
else:
    print("No reference genome provided.")
    print("Start aligning...")
    #Alignment
    start = time.time()
    main.diamond_blastx(query=fq_gz1,db=home+"home/nr_diamond/nr.dmnd",out=home+"ephemeral/Blast/"+args[1]+"_1.daa",threads=args[3])
    end = time.time()
    print("Alignment 1:"+str(end-start))

    start = time.time()
    main.diamond_blastx(query=fq_gz2,db=home+"home/nr_diamond/nr.dmnd",out=home+"ephemeral/Blast/"+args[1]+"_2.daa",threads=args[3])
    end = time.time()
    print("Alignment 2:"+str(end-start))

    #MEGAN
    start = time.time()
    main.run_MEGAN6(blastfile1=home+"ephemeral/Blast/"+args[1]+"_1.daa",blastfile2=home+"ephemeral/Blast/"+args[1]+"_2.daa",output=home+"ephemeral/MEGAN/"+args[1]+".rma",mdb=home+"home/MEGANDatabse/megan-map-Jul2020-2.db",threads=args[3])
    end = time.time()
    print("Get rma"+str(end-start))

    #Taxon composition
    start = time.time()
    main.rma_extract(rma=home+"ephemeral/MEGAN/"+args[1]+".rma",output=home+"ephemeral/TaxonProfile/"+args[1]+"TaxonProfile.txt")
    end = time.time()
    print("Deal rma:"+str(end-start))
