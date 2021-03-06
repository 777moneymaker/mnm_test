import io
import os
import pandas as pd

import matplotlib.pyplot as plt
import gzip

# Task 4
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

def read_vcf_gz(path):
    with gzip.open(path, 'rt') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype = {'#CHROM': str, 'POS': str, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep = '\t'
    ).rename(columns={'#CHROM': 'CHROM'})


df = read_vcf("filtered_indels.recode.vcf")
df = df[df.CHROM != "#CHROM"]
df["LEN"] = [len(alt) - len(ref) for alt, ref in zip(df.ALT, df.REF)]

# Plot grid
fig, axes = plt.subplots(6,4, figsize=(10,10))
for (chrom, group), ax in zip(df.groupby("CHROM")["LEN"], axes.flatten()):
    group.plot(kind='hist', ax=ax, title=chrom)

plt.savefig("hist.png")
df = df[["CHROM", 'ID', 'REF', 'ALT', 'LEN']]
df.to_csv("indel_lengths.csv", index=False)

# Task 5
df = read_vcf_gz("CPCT02220079.annotated.processed.vcf.gz 10-38-53-743.gz")
df = df[df.CHROM != "#CHROM"]
df = df[df.FILTER == "PASS"]
interest = df[(df["INFO"].str.contains("GoNLv5_AF") & df["INFO"].str.contains("GT"))]

res = pd.DataFrame()
res["GT"] = interest.CPCT02220079R.str.split(':').str[0]
res["AF"] = interest.INFO.str.extract("(.*GoNLv5_AF=)([0-9]*\.[0-9]*)")[1]

res["GT"] = res["GT"].astype(str)
res["AF"] = pd.to_numeric(res['AF'])

counts = len(res[(res['GT'] == "0/1") & (res["AF"] < 0.01)])
print(counts) # 1

# Task 6
df = read_vcf_gz("CPCT02220079.annotated.processed.vcf.gz 10-38-53-743.gz")
interest = df[df.INFO.str.contains("DP")]
dps = interest.CPCT02220079R.str.split(':').str[2]

res = pd.DataFrame()
res["CHROM"] = df.loc[dps.index]["CHROM"]
res['mean_DP'] = pd.to_numeric(dps)

res = res[~res['CHROM'].isin(['X', 'Y', 'MT'])]
res['CHROM'] = pd.to_numeric(res['CHROM'])
final = res.groupby("CHROM").mean()
final = final.sort_values(by='CHROM')

final.plot.bar()
final.to_csv("avg_DP.csv")
plt.savefig("bar6.png")




