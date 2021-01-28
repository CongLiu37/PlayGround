"""
DESCRIPTION:
Toolkit for MRes project.

DEPENDENCIES:
fastqc, trimmomatic, blast+, MEGAN6, bowtie2, diamond
"""

home="/rds/general/user/cl3820/home/"
import os

def file_list(file):
    """
    Read the input file and convert it into a list.
    ith element in the list is corresponded to ith line in the file.

    INPUT
    file (string): A file name.
    
    RETURN
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
    
    INPUT
    file1/2 (string): raw data file (fastq.gz)
    clean1/2 (string): paired clean data file (fastq.gz)
    unpaired1/2 (string): unpaired reads from file1/2 (fastq.gz)
    adaptor (string): fasta file of adaptors (fasta)
    threads (integer): number of threads
    
    OUTPUT
    Paired clean data file (fastq.gz) save in clean1/2
    Unpaired reads from file1/2 (fastq.gz) save in unpaired1/2
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

    INPUT
    clean1/2 (string): input data file (fastqc.gz)
    output (string): directory where QC report is saved
    threads (integer): number of threads

    OUTPUT
    QC report saves in output
    """
   
    qc = "fastqc -o " + output + " " + "-t "+str(threads)+" "+clean1+" "+clean2
    os.system(qc)
    return(0)

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

def run_MEGAN6(blastfile1,blastfile2,output,mdb,threads):
    """
    Run MEGAN6. Convert blast file (format 6) to rma file using weighted LCA.
    
    INPUT
    blastfile1/2 (string): blast files
    output (string): output name
    mdb(string): database

    OUTPUT:
    rma file
    """

    cmd = home+"megan/tools/daa2rma -i "+blastfile1+" "+blastfile2+" --paired -alg weighted -top 50 -mdb "+mdb+" -o "+output
    os.system(cmd)
    return(0)

def rma_extract(rma, output):
    """
    Extract taxon composition from rma file using MEGAN6.
    
    INPUT: 
    rma (string): rma file
    output (string): output file

    OUTPUT:
    File of taxon composition.
    """
    cmd=home+"megan/tools/rma2info -i "+rma+" -o "+output
    cmd=cmd+" -l true -m true -c2c Taxonomy -r2c Taxonomy -r true"
    os.system(cmd)
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

def bowtie2_map(fasta1,fasta2,index,sam,unmap,threads):
    """
    Mapping by bowtie2.
    Convert sam to bam using samtools.
    
    INPUT
    fasta1/2 (string): files of reads (fasta)
    index (string): bowtie2 index of reference
    sam (string): basename of output
    unmap (string): um-mapped reads
    threads (integer): number of threads

    OUTPUT:
    .sam.bam file (bam format)
    """

    cmd = home+"miniconda3/bin/bowtie2 --no-discordant  --no-mixed -p "+str(threads)+" -x "+index+" -1 "+fasta1
    cmd = cmd+" -2 "+fasta2+" -S "+sam+" --un-conc "+unmap
    os.system(cmd)
    os.system(home+"miniconda3/bin/samtools view -b -S "+sam+" > "+sam+".bam")
    os.system("rm "+sam)

def sort_bam(bam,out,threads):
    """
    Sort bam by position.

    INPUT
    bam: bam file
    out: output sorted bam
    threads: number of threads

    OUTPUT:
    sorted bam file
    """
    cmd = home+"miniconda3/bin/samtools sort -o "+out+" -O bam -@ "
    cmd = cmd+str(threads)+" "+bam
    os.system(cmd)
    os.system("rm "+bam)


def compute_depth(bam,out):
    """
    Compute depth of each position.
    
    INPUT
    bam: bam file
    out: output

    OUTPUT:
    Depth of each position
    """
    cmd = home+"miniconda3/bin/samtools depth -aa -o "+out+" "+bam
    os.system(cmd)

def diamond_blastx(query,db,out,threads):
    """
    Run diamond. Output format is Blast tabular. 
    Threshold of e-value is 1e-5.
    Threshold of identity is 50%.

    INPUT:
    query: query sequence file
    db: database
    out: output
    threads: number of threads
    """
    cmd = home+"miniconda3/bin/diamond blastx -p "+str(threads)+" -d "+db
    cmd = cmd + " -q "+query+" --sensitive -e 0.00001 --id 50 -b 15 --daa "+out
    os.system(cmd)

