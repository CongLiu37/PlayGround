

import os
import sys
usr = "/rds/general/user/cl3820/"
args = sys.argv #<sample> <percentage> <threads>

for i in range(1,6):
    os.system("python3 "+usr+"home/Code/TaxonRarefaction.py "+args[1]+" "+str(args[2])+" 8 "+str(i))