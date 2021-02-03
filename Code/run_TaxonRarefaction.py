"""
DESCRIPTION:
Taxon rarefaction
"""

import os
import sys
usr = "/rds/general/user/cl3820/"

iteration = os.getenv("PBS_ARRAY_INDEX")
iteration = int(iteration)

def iter_percentage(itera):
    """
    Convert iteration number to subsampling percentage.

    itera (int): [1,190]
    """
    if itera <= 10:
        return(5)
    elif itera <= 20:
        return(10)
    elif itera <= 30:
        return(15)
    elif itera <= 40:
        return(20)
    elif itera <= 50:
        return(25)
    elif itera <= 60:
        return(30)
    elif itera <= 70:
        return(35)
    elif itera <= 80:
        return(40)
    elif itera <= 90:
        return(45)
    elif itera <= 100:
        return(50)
    elif itera <=110:
        return(55)
    elif itera <= 120:
        return(60)
    elif itera <= 130:
        return(65)
    elif itera <= 140:
        return(70)
    elif itera <= 150:
        return(75)
    elif itera <= 160:
        return(80)
    elif itera <= 170:
        return(85)
    elif itera <= 180:
        return(90)
    elif itera <= 190:
        return(95)

args = sys.argv#[script_name, sample_name,threads]
os.system("python3 "+usr+"home/Code/TaxonRarefaction.py "+args[1]+" "+str(iter_percentage(iteration))+" 8 "+str(iteration))