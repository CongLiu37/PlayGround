"""
DESCRIPTION:
Python toolkit for MRes project.

DEPENDENCIES:
fastqc, trimmomatic, blast+, MEGAN6, bowtie2, diamond, vsearch
"""

home="/rds/general/user/cl3820/home/"
import os

def file_list(file):
    """
    Read the input file and convert it into a list.
    ith element in the list is corresponded to ith line in the file.

    INPUT:
    file (path): A file name.
    
    RETURN:
    A list
    """

    filea = open(file, "r")
    lis = []
    for line in filea:
        line = line.strip()
        lis.append(line)
    filea.close()
    return(lis)

def run_trimmomatic(file1,file2,clean1,clean2,unpaired1,unpaired2,adaptor,threads):
    """
    Run trimmomatic with following parameters:
    PE -threads 10 -phred33 ILLUMINACLIP:[adaptor]:2:30:10:1:true HEADCROP:15 TRAILING:20 MINLEN:36
    
    INPUT:
    file1/2 (path): raw data file (fastq.gz)
    clean1/2 (path): paired clean data file (fastq.gz)
    unpaired1/2 (path): unpaired reads from file1/2 (fastq.gz)
    adaptor (path): fasta file of adaptors (fasta)
    threads (integer): number of threads
    
    OUTPUT:
    clean1/2: paired clean data file (fastq.gz)
    unpaired1/2: Unpaired reads from file1/2 (fastq.gz)
    """

    cmd = "trimmomatic PE -threads "+str(threads)+" -phred33 "
    cmd = cmd + file1+" "+file2+" "+clean1+" "+unpaired1+" "+clean2
    cmd = cmd + " " + unpaired2
    cmd = cmd + " ILLUMINACLIP:"+adaptor+":2:30:10:1:true HEADCROP:15 TRAILING:20 MINLEN:36"
    os.system(cmd)
    return(0)

def run_fastqc(clean1,clean2,output, threads):
    """
    Run fastqc.

    INPUT:
    clean1/2 (path): input data file (fastqc.gz)
    output (path): directory where QC report is saved
    threads (integer): number of threads

    OUTPUT:
    QC report saves in output
    """
   
    qc = "fastqc -o " + output + " " + "-t "+str(threads)+" "+clean1+" "+clean2
    os.system(qc)
    return(0)

def bowtie2_map(fasta1,fasta2,index,sam,unmap,threads):
    """
    Mapping by bowtie2.
    Convert sam to bam using samtools.
    Remove sam
    
    INPUT:
    fasta1/2 (path): files of reads (fasta)
    index (path): bowtie2 index of reference
    sam (path): basename of output bam
    unmap (path): um-mapped reads
    threads (integer): number of threads

    OUTPUT:
    .sam.bam file (bam format)
    un-mapped reads
    """

    cmd = home+"miniconda3/bin/bowtie2 --no-discordant  --no-mixed -p "+str(threads)+" -x "+index+" -1 "+fasta1
    cmd = cmd+" -2 "+fasta2+" -S "+sam+" --un-conc "+unmap
    os.system(cmd)
    os.system(home+"miniconda3/bin/samtools view -b -S "+sam+" > "+sam+".bam")
    os.system("rm "+sam)

def sort_bam(bam,out,threads):
    """
    Sort bam by position using samtools.
    Remove unsorted bam

    INPUT:
    bam (path): bam file
    out (path): output sorted bam
    threads (integer): number of threads

    OUTPUT:
    out: sorted bam file
    """

    cmd = home+"miniconda3/bin/samtools sort -o "+out+" -O bam -@ "
    cmd = cmd+str(threads)+" "+bam
    os.system(cmd)
    os.system("rm "+bam)


def compute_depth(bam,out):
    """
    Compute depth of each position using samtools.
    
    INPUT:
    bam (path): sorted bam file
    out (path): output

    OUTPUT:
    out: depth of each position
    """

    cmd = home+"miniconda3/bin/samtools depth -aa -o "+out+" "+bam
    os.system(cmd)

def diamond_blastx(query,db,out,threads):
    """
    Run diamond. 
    Output format: Blast tabular. 
    Threshold of e-value: 1e-5.
    Threshold of identity: 50%.

    INPUT:
    query (path): query sequence file
    db (path): database
    out (path): output
    threads (integer): number of threads

    OUTPUT:
    out: blast file in tabular format
    """

    cmd = home+"miniconda3/bin/diamond blastx -p "+str(threads)+" -d "+db
    cmd = cmd + " -q "+query+" --sensitive -e 0.00001 --id 50 -b 15 --out "+out+" -f 6"

    os.system(cmd)


def run_MEGAN6(blastfile1,blastfile2,output,mdb,threads):
    """
    Run MEGAN6. 
    Convert blast file (format 6, tabular) to rma file.
    Weighted LCA.
    NCBI Taxonomy.
    
    INPUT:
    blastfile1/2 (path): blast files
    output (path): output name
    mdb (path): database

    OUTPUT:
    output: rma file
    """

    cmd = home+"megan/tools/blast2rma -i "+blastfile1+" "+blastfile2+" -f BlastTab --paired -alg weighted -top 50 -mdb "+mdb+" -o "+output
    os.system(cmd)
    return(0)

def rma_extract(rma, output):
    """
    Extract taxon composition from rma file using MEGAN6.
    
    INPUT: 
    rma (path): rma file
    output (path): output file

    OUTPUT:
    output: file of taxon composition.
    """

    cmd=home+"megan/tools/rma2info -i "+rma+" -o "+output
    cmd=cmd+" -l true -m true -c2c Taxonomy -r2c Taxonomy -r true"
    os.system(cmd)
    return(0)

def subsampling_fastq(fastq,percentage,output):
    """
    Subsample fastq file with given percentage.

    INPUT:
    fastq (path): input fastq/a file
    percentage (float from 0-100): sampling percentage
    output (path): subsampled file, fasta

    OUTPUT:
    output
    """

    cmd = home+"miniconda3/bin/vsearch --fastx_subsample "+fastq+" --fastaout "+output+" --sample_pct "+str(percentage)
    os.system(cmd)

def extract_fastaIDs(fasta):
    """
    Extract IDs of sequences from fasta file.

    INPUT
    fasta (path): input fasta file

    RETURN:
    a list composed of sequence IDs
    """

    f = open(fasta,"r")
    l = []
    for line in f:
        if line[0] == ">":
            line = line.strip()
            l.append(line[1:])
    return l

def extract_blast(IDs,blastfile,output):
    """
    Extract hits of given query IDs from a blast tabular file.

    INPUT:
    IDs (list): ID of query sequences
    blastfile (path): blast file of tabular format
    output (path): output blast file

    OUTPUT:
    output
    """

    os.system("touch "+output)
    out = open(output, "w")
    blast = open(blastfile, "r")
    for line in blast:
        for ID in IDs:
            if ID in line:
                out.write(line)


##########################################################################
def makeblastdb(fasta, out, dbtype):
    """
    Make blast database from fasta file.
    
    INPUT
    fasta (string): fasta file
    out (string): database name
    dbtype (string): database type, nucl/prot

    OUTPUT
    blast database named as out
    """
    cmd = home+"Software/ncbi-blast-2.11.1+/bin/makeblastdb -in "+fasta+" -input_type fasta -dbtype "+dbtype
    cmd = cmd+" -title "+out+".db -parse_seqids -out "+out
    os.system(cmd)
    return(0)

def run_blastx(fasta,out,database,threads):
    """
    Run blastx.
    Threshold of e-value is 1e-10.

    INPUT
    fasta (string): query file (fasta)
    out (string): output file (blast)
    database (string): database for search
    outfmt (string): output format (6: tabular, no column name; 
                      7: tabular with column name). Default value is 6.
    
    OUTPUT:
    blast file 
    """
    
    cmd = home+"Software/ncbi-blast-2.11.1+/bin/blastx -query "+fasta+" -out "+out+" -db "+database
    cmd = cmd+" -outfmt 6 -evalue 1e-10 -num_threads "+str(threads)
    
    os.system(cmd)
    return(0)

def merge_file(file, output):
    """
    Create output.
    Merge file to output
    
    INPUT
    file (string): a file
    output (string): another file

    OUTPUT
    output file
    """
    os.system("touch "+output)
    cmd = "cat "+file+" >> "+output
    os.system(cmd)
    return(0)

def blast_filter(blastfile, output):
    """
    Filter blast results with thresholds:
       identity >= 50%
       
    INPUT:
    blastfile (string): blast file in format 6/7
    output (string): output file

    OUTPUT:
    Filtered blast file
    """
    os.system("touch "+output)
    out = open(output, "w")
    fil = open(blastfile, "r")
    for line in fil:
        a = line.strip().split("\t")
        if float(a[2]) >= 50:
            out.write(line)
    fil.close()
    out.close()
    return(0)



def bowtie2_index(fasta, base):
    """
    Build bowtie index.
    
    INPUT
    fasta (string): a fasta file
    base (string): base name of index

    OUTPUT:
    bowtie2 index
    """

    cmd = home+"miniconda3/bin/bowtie2-build "+fasta+" "+base
    os.system(cmd)




