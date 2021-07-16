import io
import os
import pandas as pd

import matplotlib.pyplot as plt

# bash
# vcftools --gzvcf CPCT02220079.annotated.processed.vcf.gz\ 10-38-53-743.gz \
# --recode --recode-INFO-all --keep-only-indels --out filtered_indels 

def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype = {'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep = '\t'
    ).rename(columns={'#CHROM': 'CHROM'})

df = read_vcf("filtered_indels.recode.vcf")

df = df[df.CHROM != "#CHROM"]
df["LEN"] = [len(alt) - len(ref) for alt, ref in zip(df.ALT, df.REF)]

fig, axes = plt.subplots(6,4, figsize=(10,10))

for (chrom, group), ax in zip(df.groupby("CHROM")["LEN"], axes.flatten()):
    group.plot(kind='hist', ax=ax, title=chrom)

plt.savefig("hist.png")