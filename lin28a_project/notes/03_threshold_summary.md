# 03 Threshold Summary

## Analysis: Direct LIN28A Translational Repression Candidates (Spec 03)

Mean CLIP enrichment = average of 3 CLIP enrichment columns:
- `CLIP-seq enrichment (35L33G, log2)`
- `CLIP-seq enrichment (2J3, log2)`
- `CLIP-seq enrichment (polyclonal, log2)`

## Threshold Set A

| Criterion | Column | Cutoff | Justification |
|---|---|---|---|
| CLIP binding | CLIP-seq FDR | < 0.05 | Standard FDR cutoff |
| CLIP enrichment | mean_CLIP_enrichment | > 1 (log2) | >2-fold enrichment |
| Translational repression | Ribosome density change (log2) | > 0 | Any increase upon KD |
| Translational specificity | RNA-seq mRNA change (log2) | |x| < 0.5 | Exclude mRNA abundance changes |

**Selected: 56 transcripts, 56 unique genes**

## Threshold Set B (more stringent)

| Criterion | Column | Cutoff | Justification |
|---|---|---|---|
| CLIP binding | CLIP-seq FDR | < 0.05 | Standard FDR cutoff |
| CLIP enrichment | mean_CLIP_enrichment | > top 20% (>0.493) | Top quintile |
| Translational repression | Ribosome density change (log2) | > 0.3 | More than minimal change |
| Translational specificity | RNA-seq mRNA change (log2) | |x| < 0.5 | Exclude mRNA abundance changes |

**Selected: 48 transcripts, 48 unique genes**

## Comparison

| | Threshold A | Threshold B |
|---|---|---|
| Transcripts | 56 | 48 |
| Unique genes | 56 | 48 |
| CLIP cutoff | > 1 | top 20% (>0.493) |
| Ribosome density cutoff | > 0 | > 0.3 |
