#PBS -lselect=1:ncpus=10:ompthreads=10:mem=120gb
#PBS -lwalltime=71:30:00

module load anaconda3/personal
cd /rds/general/user/cl3820/home/Code
source ~/.bashrc
echo "Start"
python VisualizationMappingDepth.py ../bowtie2/depth_PGcomcol3_Bimp_Bombus_impatiens.txt PGcomcol3_Bimp Bombus_impatiens
echo "Done"