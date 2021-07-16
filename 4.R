#!/usr/bin/env Rscript


# bash
# vcftools --gzvcf CPCT02220079.annotated.processed.vcf.gz\ 10-38-53-743.gz \
# --recode --recode-INFO-all --keep-only-indels --out filtered_indels 

library(vcfR)
vcf = read.vcfR(file.choose())
df = vcfR2tidy(vcf)
