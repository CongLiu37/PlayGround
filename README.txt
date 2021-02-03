# MResProject

########################################################################################
Scripts
########################################################################################
(1) main.py
(2) main.R

(3) QualityControl.py
USAGE:
	$python QualityControl.py <sample> <threads>
DEPENDENCIES:
	main.py, fastqc, trimmomatic
INPUT:
	raw_data/<sample>_[12].fq.gz
FUNCTIONS & OUTPUT:
	fastqc check of raw data (QualityControl/raw/*)
	trimmomatic filter: (clean_data/<sample>_[12].fq.gz)
		remove nextera adaptor
		crop 15 bases from heads
		crop bases with quality score lower than 20 from tails
		filter reads shorter than 36 bp
	fastqc check of clean data (QualityControl/clean/*)

(4) FilterHost.py
USAGE:
	$python FilterHost.py <sample> <host> <threads>
DEPENDENCIES:
	main.py, bowtie2, samtools
INPUT:
	clean_data/<sample>_[12].fq.gz
	reference_genome/<host> (bowtie2 index)
FUNCTIONS & OUTPUT:
	bowtie2 mapping (bowtie2/<sample>__filterhost.[12].fq)
	convert sam to bam, sort bam (bowtie2/<sample>_sorted.bam)
	compute depth (bowtie2/depth_<sample>_<host>.txt)

(5) Align_nr.py
USAGE:
	$python Align_nr.py <sample> <threads>
DEPENDENCIES:
	main.py, diamond
INPUT:
	bowtie2/<sample>_filterhost.[12].fq
	nr_diamond/nr.dmnd
FUNCTIONS & OUTPUT:
	align reads to nr database (Blast/<sample>_[12].blast)

(6) MEGAN.py
USAGE:
	$python MEGAN.py <sample> <threads>
DEPENDENCIES:
	main.py, MEGAN6
INPUT:
	Blast/<sample>_[12].blast
	MEGANDatabse/megan-map-Jul2020-2.db
FUNCTIONS & OUTPUT:
	MEGAN/<sample>.rma
	TaxonProfile/<sample>TaxonProfile.txt
	
(7) TaxonRarefaction.py
USAGE:
	$python TaxonRarefaction.py <sample> <percentage> <threads> <i>
INPUT:
	raw_raw_data/<sample>_1.fq.gz
	Blast/<sample>_[12].blast
FUNCTIONS & OUTPUT:
	subsample raw_raw_data/<sample>_1.fq.gz by vsearch (TaxonRarefaction/<i><sample>_<percentage>.fasta)
	extract sequence IDs from TaxonRarefaction/<i><sample>_<percentage>.fasta, find corresponding blast results (TaxonRarefaction/<i><sample>_<percentage>_[12].blast)
	MEGAN6 profiling (TaxonRarefaction/<i><sample>_<percentage>.rma, TaxonRarefaction/<i><sample>_<percentage>TaxonProfile.txt)



########################################################################################
Pipeline
Command line produced by functions in Code/main.py
########################################################################################
I Quality control (Code/QualityControl.py)
(1) fastqc check
	input: raw_data/<sample>_[12].fq.gz
	output: QualityControl/raw.html
(2) trimmomatic filter
	input: raw_data/<sample>._[12].fq.gz
	remove nextera adaptor
	crop 15 bases from heads
	crop bases with quality score lower than 20 from tails
	filter reads shorter than 36 bp
	output: clean_data/<sample>_[12].fq.gz
(3) fastqc check
	input: clean_data/<sample>_[12].fq.gz
	output: QualityControl/raw.html

####Summary of results####
QualityControl/raw/raw.html
QualityControl/clean/clean.html

II Filter host reads (Code/FilterHost.py)
(1) bowtie2 index
	input: reference_genome/<host>.fasta (genomic)
	output: reference_genome/<host>.*.bt2 (referred as <host>)
(2) bowtie2 map
	input: clean_data/<sample>.fq.gz
	       reference_genome/<host>.*.bt2 (referred as <host>)
	only take concordantly alignment into consideration, spit un-mapped reads (bowtie2)
	convert sam to bam, sort bam, compute depth (samtools)
	output: bowtie2/<sample>_filterhost.[12].fq
	        bowtie2/<sample>_sorted.bam
	        bowtie2/depth_<sample>_<host>.txt

##########################Summary of results##########################
PGcomcol3_Bimp
59532563 reads; of these:
  59532563 (100.00%) were paired; of these:
    50717312 (85.19%) aligned concordantly 0 times
    6252486 (10.50%) aligned concordantly exactly 1 time
    2562765 (4.30%) aligned concordantly >1 times
14.81% overall alignment rate

PGcomcol4a_Bimp
54493550 reads; of these:
  54493550 (100.00%) were paired; of these:
    49274544 (90.42%) aligned concordantly 0 times
    3159394 (5.80%) aligned concordantly exactly 1 time
    2059612 (3.78%) aligned concordantly >1 times
9.58% overall alignment rate

PGcomcol4b_Bimp
50950233 reads; of these:
  50950233 (100.00%) were paired; of these:
    44197093 (86.75%) aligned concordantly 0 times
    4644360 (9.12%) aligned concordantly exactly 1 time
    2108780 (4.14%) aligned concordantly >1 times
13.25% overall alignment rate

PGnos_high_hv13-1
975761 reads; of these:
  975761 (100.00%) were paired; of these:
    938132 (96.14%) aligned concordantly 0 times
    3009 (0.31%) aligned concordantly exactly 1 time
    34620 (3.55%) aligned concordantly >1 times
3.86% overall alignment rate

PGnos_high_hv13-2
45776057 reads; of these:
  45776057 (100.00%) were paired; of these:
    41664402 (91.02%) aligned concordantly 0 times
    191968 (0.42%) aligned concordantly exactly 1 time
    3919687 (8.56%) aligned concordantly >1 times
8.98% overall alignment rate

PGnos_inter_hv15
<pre>53648951 reads; of these:
  53648951 (100.00%) were paired; of these:
    46682350 (87.01%) aligned concordantly 0 times
    9007 (0.02%) aligned concordantly exactly 1 time
    6957594 (12.97%) aligned concordantly &gt;1 times
12.99% overall alignment rate</pre>

PGpollen_fresh
52072942 reads; of these:
  52072942 (100.00%) were paired; of these:
    50199144 (96.40%) aligned concordantly 0 times
    745418 (1.43%) aligned concordantly exactly 1 time
    1128380 (2.17%) aligned concordantly >1 times
3.60% overall alignment rate

##########################End##########################

III Diamond alignment (Code/Align_nr.py)
(1) diamond database
	nr_diamond/*.dmnd (build from nr database)
(2) alignment
	input: nr_diamond/*.dmnd
	       bowtie2/<sample>_filterhost.[12].fq
	e-value < 1e-5, identity > 50%, --sensitive, -b 100, -c 1, -p 150, -f 6 (out format: blast tabular)
	output: Blast/<sample>_[12].blast

IV Taxon profile by MEGAN6 (Code/MEGAN.py)
(1) blast to rma (daa2rma)
	input: Blast/<sample>_[12].blast
	weighted LCA
	databse: MEGANDatabase/megan-map-Jul2020-2.db (nr -> Taxonomy)
	output: MEGAN/<sample>.rma
(2) rma to taxon profile (rma2info)
	input: MEGAN/<sample>.rma
	Taxonomy database
	output: TaxonProfile/<sample>TaxonProfile.txt
(3) statistics and visualization
	phylogenetic tree + abundance ...

V Filter reference reads
(1) reference genomes
	input: TaxonProfile/<sample>TaxonProfile.txt
	extract taxid
	download genome/nucleotide
	build bowtie2 index
(2) bowtie2 map
	map, compute depth
	


*** Modeling rarefaction curve
(1) subsampling (vsearch --fastx_subsample) (<i> in 1:10)
	input: raw_raw_data/<sample>_1.fq.gz
	subsample, extract sampled sequence IDs
	Extract corresponded blast hits
	Extract corresponded clean reads (host filtered): TaxonRarefaction/<i>_<sample>_<percentage>_[12].fasta
	Taxon profile: TaxonRarefaction/i_<sample>_<percentage>TaxonProfile.txt
(2) 
(3) modeling: number of species, number of genus, number of genes (y) ~ sequencing depth (x)
	results save in Rarefaction_analysis/
	y = y(x), y(0) = 0
	model 1: y(x) = B_0+B_1*x+B_2*x^2 (Code/Rarefaction_1.R)
	model 2: y(x) = B_0+B_1*x+B_2*x^2+B_3*x^3 (Code/Rarefaction_2.R)
	model 3: y(x) = a*x^b, a>0, 0<b<1 (Code/Rarefaction_3.R)
	model 4: y(x) = a+b/x, a>0, b<0, ylim = a (Code/Rarefaction_4.R)
	model 5: y(x) = a*x/(1+b*x), ylim = a/b (Code/Rarefaction_5.R)

	model 6: y(x) = b-b*a^x, 0<a<1, b>0, ylim = b (Code/Rarefaction_6.R)
	model 7: y(x) = log_b(ax+1), a>0, b>1 (Code/Rarefaction_7.R)
 

########################################################################################
Some details about software
########################################################################################
#Link to cluster
$ssh cl3820@login.cx1.hpc.ic.ac.uk
$sftp cl3820@login.cx1.hpc.ic.ac.uk

I. Environmental variable set
$ vi ~/.bashrc
export PATH=<Your Path>:$PATH #add this line to the end of file
$ source ~/.bashrc

II. Install conda
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ bash Miniconda3-latest-Linux-x86_64.sh
$ source ~/.bashrc
$ conda config --add channels bioconda
$ conda config --add channels conda-forge

III. Java
$ wget https://www.oracle.com/webapps/redirect/signon?nexturl=https://download.oracle.com/otn/java/jdk/8u271-b09/61ae65e088624f5aaa0b1d2d801acb16/jdk-8u271-linux-x64.tar.gz
# or check this: https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html
$ tar -zxvf jdk-8u271-linux-x64.tar.gz
$ sudo -i #
$ vi /etc/profile
#add this line to the end of file
JAVA_HOME=/usr/java/jdk-15.0.1
CLASSPATH=$JAVA_HOME/lib/
PATH=$PATH:$JAVA_HOME/bin
export PATH JAVA_HOME CLASSPATH
$ source /etc/profile
$java -version

IV. Softwares
(1) Fastqc
https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
(2) Trimmomatic
conda install
(3) Blast+
OUTFMT6: Tabular
Fields: query acc.ver, subject acc.ver, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score

(4) nr database

(5) Diamond
conda install

(6) MEGAN
#on HPC, first run
$export _JAVA_OPTIONS='-Djava.io.tmpdir=$TMPDIR'
#https://software-ab.informatik.uni-tuebingen.de/download/megan6/welcome.html
$ wget https://software-ab.informatik.uni-tuebingen.de/download/megan6/MEGAN_Community_unix_6_18_4.sh
$ bash MEGAN_Community_unix_6_18_4.sh
# set megan/tools as environmental variable
#Download MEGAN database: nr -> taxon
$wget https://software-ab.informatik.uni-tuebingen.de/download/megan6/megan-map-Jul2020-2.db.zip
$unzip megan-map-Jul2020-2.db.zip

(7) vsearch
conda install
