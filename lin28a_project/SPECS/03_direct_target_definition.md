# 03_direct_target_definition.md

## Goal

Define preliminary direct LIN28A translational repression candidates using Table S5.

## Biological question

Which transcripts are bound by LIN28A and show increased ribosome density after Lin28a knockdown without major mRNA abundance change?

## Inputs

- `lin28a_project/data/processed/table_s5_cleaned.csv`

## Tasks

1. Compute mean CLIP enrichment across available CLIP enrichment columns.
2. Summarize distributions of:
   - mean CLIP enrichment
   - CLIP FDR
   - ribosome density change
   - RNA-seq mRNA change
3. Propose at least two threshold sets.
4. For each threshold set, report:
   - number of selected transcripts
   - number of unique gene symbols
   - top 20 candidates by mean CLIP enrichment and ribosome density change
5. Create the main scatter plot:
   - x-axis: mean CLIP enrichment
   - y-axis: ribosome density change
   - color: small vs large mRNA abundance change
   - highlight direct repression candidates
6. Save candidate tables.

## Suggested initial threshold candidates

Do not treat these as final without checking distributions.

Threshold set A:
- CLIP FDR < 0.05
- mean CLIP enrichment > 1
- ribosome density change > 0
- abs(mRNA change) < 0.5

Threshold set B:
- CLIP FDR < 0.05
- mean CLIP enrichment in top 20%
- ribosome density change > 0.3
- abs(mRNA change) < 0.5

## Expected outputs

- `lin28a_project/results/figures/03_clip_vs_ribosome_scatter.png`
- `lin28a_project/results/tables/03_direct_candidates_threshold_A.csv`
- `lin28a_project/results/tables/03_direct_candidates_threshold_B.csv`
- `lin28a_project/notes/03_threshold_summary.md`

## Do not

- Do not overwrite Table S5.
- Do not decide final threshold silently.
- Do not make more than 3 plots.
