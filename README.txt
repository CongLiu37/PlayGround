# MResProject

########################################################################################
Pipeline
Command line produced by functions in Code/main.py
########################################################################################
I Quality control
(1) fastqc check
	input: raw_data/<sample>_[12].fq.gz
	output: QualityControl/raw.html
(2) trimmomatic filter
	input: raw_data/<sample._[12].fq.gz
	remove nextera adaptor
	crop 15 bases from heads
	crop bases with quality score lower than 20 from tails
	filter reads shorter than 36 bp
	output: clean_data/<sample>_[12].fq.gz
(3) fastqc check
	input: clean_data/<sample>_[12].fq.gz
	output: QualityControl/raw.html

####Summary of results####
QualityControl/raw.html
QualityControl/clean.html

II Filter host reads (Code/TaxonProfile.py)
(1) bowtie2 index
	input: reference_genome/<host>.fasta (genomic)
	output: reference_genome/<host>.*.bt2 (referred as <host>)
(2) bowtie2 map
	input: clean_data/<sample>.fq.gz
	       reference_genome/<host>.*.bt2 (referred as <host>)
	only take concordantly alignment into consideration, split un-mapped reads (bowtie2)
	convert sam to bam, sort bam, compute depth
	output: bowtie2/<sample>_filterhost.[12].fq
	        bowtie2/<sample>_sorted.bam
	        bowtie2/depth_<sample>_<host>.txt

####Summary of results####
<sample>	<host>	percentage_align
PGcomcol3_Bimp	Bombus_impatiens	14.81

III Diamond alignment (Code/TaxonProfile.py)
(1) diamond database
	nr_diamond/*.dmnd (build from nr database)
(2) alignment
	input: nr_diamond/*.dmnd
	       bowtie2/<sample>_filterhost.[12].fq
	e-value < 1e-5, identity > 50%, --very-sensitive
	output: Blast/<sample>_[12].daa

IV Taxon profile by MEGAN6 (Code/TaxonProfile.py)
(1) daa to rma (daa2rma)
	input: Blast/<sample>_[12].daa
	weighted LCA
	databse: MEGANDatabase/megan-map-Jul2020-2.db (nr -> Taxonomy)
	output: MEGAN/<sample>.rma
(2) rma to taxon profile (rma2info)
	input: MEGAN/<sample>.rma
	Taxonomy database
	output: TaxonProfile/<sample>TaxonProfile.txt

*** Modeling rarefaction curve
(1) subsampling
(2) re-analysis
	depth, number of species, number of genus, number of genes
	saves in Rarefaction_analysis/
(3) modeling: number of species, number of genus, number of genes(y) ~ sequencing depth (x)
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


(6) MEGAN
#https://software-ab.informatik.uni-tuebingen.de/download/megan6/welcome.html
$ wget https://software-ab.informatik.uni-tuebingen.de/download/megan6/MEGAN_Community_unix_6_18_4.sh
$ bash MEGAN_Community_unix_6_18_4.sh
# set megan/tools as environmental variable
#Download MEGAN database: nr -> taxon
$wget https://software-ab.informatik.uni-tuebingen.de/download/megan6/megan-map-Jul2020-2.db.zip
$unzip megan-map-Jul2020-2.db.zip
