#PBS -lselect=1:ncpus=100:ompthreads=100:mem=1200gb
#PBS -lwalltime=71:30:00
module load anaconda3/personal

echo "Start"

time python3 /rds/general/user/cl3820/home/Code/TaxonProfile_PGcomcol3_Bimp.py LF_F18 Bombus_impatiens 100

echo "Done"