#!/bin/bash
#PBS -l walltime=71:30:00
#PBS -l select=1:ncpus=8:mem=10gb
module load anaconda3/personal
echo "Start"
python3 /rds/general/user/cl3820/home/Code/run_TaxonRarefaction.py LF_F18 8
echo "Done" 