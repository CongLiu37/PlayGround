"""
Visualize depth.
Each pdf, horizontal axis represents chromosome/scaffold/contig, 
vertical axis represents depth.

ARUGUMENT:
depth file computed by samtools, sample, species (reference genome)
"""

import pandas as pd
import matplotlib.pylab as p
import sys

args = sys.argv #[script_name, depth_file, sample, species]

f = pd.read_csv(args[1], sep="\t", header= None)

chrs = list(f[0].drop_duplicates())

for chr in chrs:
    fi = f[f[0] == chr]
    f1 = p.figure()
    p.plot(fi[1], fi[2], 'r-')
    p.grid()
    p.xlabel(chr)
    p.ylabel("Depth")
    p.suptitle(args[2]+"_"+args[3])
    f1.savefig("../Figures/VisualizationMappingDepth"+args[2]+"_"+args[3]+chr+".pdf")
