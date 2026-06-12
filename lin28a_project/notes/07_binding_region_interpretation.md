# 07 Binding-Site Region Analysis Interpretation

## Analysis mode: Standard

## 1. External annotation

Source: UCSC Genome Browser mm9 refGene
URL: http://hgdownload.soe.ucsc.edu/goldenPath/mm9/database/refGene.txt.gz
See `notes/07_annotation_provenance.md` for full provenance details.

## 2. RefSeq ID matching

- S3A unique transcripts: 6606
- Matched to mm9 refGene: 6524 (98.8%)
- Sites in matched transcripts: 64,760 / 65,534 (98.8%)

## 3. Position coordinate validation

`Position` in Table S3A is assumed to be **1-based exonic transcript coordinate**
(counting from the 5′ end of the transcript, exons only).

- Position min: 1, max: 78699
- out_of_bounds rate: 0.14% (sites where Position > total exonic length)
- Validation with example transcripts:

### Example transcripts

| Transcript | Gene | n sites | pos range | total exonic | in bounds? |
|---|---|---|---|---|---|
| NM_016783 | Pgrmc1 | 21 | 74–1803 | 1870 | yes |
| NM_008477 | Ktn1 | 62 | 33–4437 | 4485 | yes |
| NM_021495 | Pvrl3(Nectin3) | 17 | 376–1713 | 3070 | yes |

## 4. Site-level region distribution (distinct from transcript-level)

*Note: Site-level and transcript-level dominant region analyses are kept separate.*

| Candidate group | n sites | 5′UTR | CDS | 3′UTR | ncRNA |
|---|---|---|---|---|---|
| Not_candidate | 63,239 | 2.3% | 65.3% | 31.6% | 0.7% |
| A_only | 443 | 0.7% | 86.2% | 13.1% | 0.0% |
| B_only | 0 | nan% | nan% | nan% | nan% |
| A_and_B_overlap | 987 | 1.9% | 58.5% | 39.6% | 0.0% |
| ALL_matched | 64,669 | 2.3% | 65.4% | 31.6% | 0.7% |

**Key pattern**: CDS tends to be the most common binding region across all groups.
3′UTR binding is also prominent.

## 5. Transcript-level dominant binding region vs ribosome density change

Each transcript is assigned the region with the **most binding sites** as its
dominant binding region. This is a separate analysis from the site-level distribution.

Results are in `results/tables/07_ribo_change_by_dominant_binding_region.csv` and
`results/figures/07_ribo_change_by_dominant_binding_region.png`.

## 6. Spearman correlations (with n)

Per-region binding site count vs ribosome density change (log2):

| Region | Subset | n | Spearman rho | p-value |
|---|---|---|---|---|
| 5UTR | all_with_ribo | 775 | 0.014 | 0.6977 |
| 5UTR | HC_candidates_A_union_B | 14 | -0.5161 | 0.0588 |
| CDS | all_with_ribo | 3810 | -0.0713 | 0.0 |
| CDS | HC_candidates_A_union_B | 41 | 0.0395 | 0.8062 |
| 3UTR | all_with_ribo | 2978 | 0.1122 | 0.0 |
| 3UTR | HC_candidates_A_union_B | 38 | 0.1095 | 0.5129 |

*Note: n = transcripts with ≥1 site in the region AND ribo data available.*
*Do not use p-values as primary conclusions — see Chi-square note below.*

## 7. Chi-square (exploratory only)

Chi-square test on site-level region distribution (HC vs Not_candidate) is
reported as an exploratory analysis only. Binding sites within the same
transcript are not independent observations, so this p-value should NOT be
used as a primary conclusion.

## 8. Limitations

1. **Position coordinate assumption**: Assumed 1-based exonic transcript coordinate
   from 5′ end. This assumption is NOT explicitly documented in the supplementary
   methods of Cho et al. 2012. Validated by out_of_bounds rate and example
   transcript checks, but could not be fully verified without original alignment
   pipeline details.

2. **mm9 refGene vs original alignment**: The original PAR-CLIP pipeline may have
   used a different transcript database or splice-junction model. mm9 refGene is
   the best available public approximation.

3. **Multiple isoforms**: Duplicate NM_ entries in refGene were resolved by keeping
   the longest transcript per NM_ accession. Some NM_ accessions may have different
   exon structures at different genomic loci.

4. **Non-coding RNA**: Transcripts with cdsStart == cdsEnd are labeled ncRNA;
   their sites cannot be classified into 5′UTR/CDS/3′UTR.

5. **Unmatched transcripts**: 82 transcripts (1.2%) in S3A
   could not be found in mm9 refGene. These may include withdrawn NM_ accessions,
   splice variants, or annotation version differences.

6. **Site-level vs transcript-level**: Site-level distribution and transcript-level
   dominant region analyses were kept strictly separate and should not be mixed
   in interpretation.

## 9. Recommended next steps

1. Confirm Position coordinate system with the original authors if possible.
2. Cross-check with mm10 refGene (if accession versions are updated).
3. Consider 3′UTR-specific analysis: are 3′UTR binding sites in HC candidates
   particularly enriched relative to background?
