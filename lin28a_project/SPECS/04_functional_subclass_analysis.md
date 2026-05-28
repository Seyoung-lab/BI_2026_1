# SPEC04: Functional subclass analysis of LIN28A direct translational repression candidates

## Goal

Analyze the functional subclasses of candidate direct LIN28A-mediated translational repression targets identified in Spec 03.

The main biological question is:

> Among candidate LIN28A-repressed transcripts, which functional subclasses are most represented?

This analysis should focus on interpreting the candidate genes defined from Table S5 using LIN28A CLIP enrichment, ribosome density change, and RNA-seq mRNA change.

This spec should not simply repeat the original paper's broad GO enrichment analysis. Instead, it should classify the candidate genes into more interpretable functional subclasses, especially within ER/membrane/secretory-related categories.

---

## Background

Spec 03 identified candidate direct LIN28A-mediated translational repression targets using two threshold sets.

* Threshold A candidates: strong LIN28A binding and increased ribosome density after Lin28a knockdown
* Threshold B candidates: top 20% LIN28A binding and stronger ribosome density increase
* The overlap between Threshold A and B should be treated as the high-confidence candidate group

The high-confidence candidates are interpreted as preliminary candidate transcripts where:

1. LIN28A binding is enriched,
2. ribosome density increases after Lin28a knockdown,
3. mRNA abundance does not change strongly.

These are candidate direct translational repression targets, not experimentally confirmed direct functional targets.

---

## Environment

Use the existing conda environment:

`jupyter_env`

Before running any Python code or notebook, confirm the environment with:

```bash
conda info --envs
which python
python --version
python -c "import pandas, numpy, matplotlib; print('basic packages ok')"
```

Important notes:

* Use `python`, not `python3`, because `python3` may point to the system Python instead of the conda environment.
* Do not create a new conda environment.
* Do not install or update packages without explicit approval.
* If a required package is missing, stop and report the missing package first.
* Record the environment check in:

`lin28a_project/notes/04_environment_check.md`

---

## Inputs

Use the following existing files:

* `lin28a_project/results/tables/03_direct_candidates_threshold_A.csv`
* `lin28a_project/results/tables/03_direct_candidates_threshold_B.csv`
* `lin28a_project/data/processed/table_s5_cleaned.csv`

Optional reference:

* `lin28a_project/data/supplementary_tables/1-s2.0-S0092867412012342-mmc6.xls`

Do not use BAM files in this spec.

---

## Output directory

Save output tables to:

* `lin28a_project/results/tables/`

Save output figures to:

* `lin28a_project/results/figures/`

Save notes to:

* `lin28a_project/notes/`

Notebook should be created or updated at:

* `lin28a_project/notebooks/02_functional_subclass_analysis.ipynb`

---

## Annotation strategy

This spec does not require sequence similarity search.

Do not run:

* BLAST
* blastn
* blastp
* InterProScan
* Foldseek
* any sequence alignment or structure-search tools

Functional subclass labels should be assigned using existing gene-level information from:

* `Gene Symbol`
* `Description`
* available columns in Table S5
* Table S6 as a reference for broad GO categories, if useful

The annotation should be rule-based and exploratory, not definitive.

Required Python packages should be limited to simple data-analysis packages:

* pandas
* numpy
* matplotlib
* optional: seaborn, xlrd, openpyxl

If additional packages are required, stop and ask for approval before installing anything.

---

## Use of Table S6

Table S6 should be used as a reference for the original paper's GO-level interpretation.

However, Table S6 should not be treated as a gene-level annotation table unless its structure clearly supports gene-level mapping.

Use Table S6 to:

1. identify which GO categories were enriched in the original study,
2. compare the candidate-level subclass analysis with the original GO-level results,
3. support interpretation of ER, membrane, Golgi, lumen, secretory, and cell-surface categories.

Do not simply repeat the original GO enrichment analysis.

The main goal of this spec is to classify the Spec 03 candidate genes into interpretable functional subclasses.

---

## Tasks

### 1. Load candidate tables

Load Threshold A and Threshold B candidate tables.

Confirm:

* number of candidate transcripts in A
* number of candidate transcripts in B
* number of overlapping transcripts
* number of overlapping unique genes

Create a candidate group label:

* `A_and_B_overlap`
* `A_only`
* `B_only`

Save the combined candidate table as:

* `lin28a_project/results/tables/04_candidate_groups.csv`

---

### 2. Define high-confidence candidates

Use the `A_and_B_overlap` group as the primary high-confidence candidate group.

Do not change the threshold definitions from Spec 03.

Do not silently redefine candidate criteria.

---

### 3. Inspect gene descriptions

For high-confidence candidates, inspect the following columns if available:

* `Accession`
* `Gene Symbol`
* `Description`
* `mean_CLIP_enrichment`
* `CLIP-seq FDR`
* `Ribosome density change (log2)`
* `RNA-seq mRNA change upon Lin28a KD (log2)`

Create a top candidate summary table sorted by:

1. high mean CLIP enrichment
2. high ribosome density increase

Save as:

* `lin28a_project/results/tables/04_high_confidence_candidate_summary.csv`

---

### 4. Functional subclass annotation

Create functional subclass labels using gene description and gene symbol information.

Use Boolean columns, because one gene can belong to more than one subclass.

Suggested subclass columns:

* `is_ER_or_protein_folding`
* `is_membrane_or_transmembrane`
* `is_secretory_or_extracellular`
* `is_Golgi_or_trafficking`
* `is_lysosome_or_endosome`
* `is_receptor_or_signaling`
* `is_transporter_or_channel`
* `is_adhesion_or_ECM`
* `is_other_or_unclear`

Start with rule-based annotation using keywords from `Description` and `Gene Symbol`.

Example keywords:

### ER or protein folding

* ER
* endoplasmic reticulum
* chaperone
* folding
* calnexin
* disulfide
* translocon
* DnaJ
* heat shock
* protein processing
* endoplasmic-reticulum
* oxidoreductase
* thioredoxin

### Membrane or transmembrane

* membrane
* transmembrane
* integral membrane
* plasma membrane
* membrane protein
* TM
* receptor
* transporter
* channel

### Secretory or extracellular

* secreted
* secretion
* extracellular
* signal peptide
* lumen
* secretory
* glycoprotein

### Golgi or trafficking

* Golgi
* ERGIC
* vesicle
* trafficking
* coatomer
* transport vesicle
* endomembrane
* sorting

### Lysosome or endosome

* lysosome
* lysosomal
* endosome
* endosomal
* vacuolar
* ATPase
* acidification

### Receptor or signaling

* receptor
* signaling
* kinase
* Wnt
* Lrp
* Adam
* growth factor
* signaling pathway

### Transporter or channel

* transporter
* channel
* solute carrier
* SLC
* pump
* ATPase
* ion
* zinc
* calcium

### Adhesion or ECM

* adhesion
* cadherin
* integrin
* matrix
* collagen
* ECM
* extracellular matrix

Important:

* Do not claim these annotations are definitive.
* Clearly describe them as rule-based preliminary functional subclass labels.
* If a gene has ambiguous annotation, mark it as `is_other_or_unclear`.
* One gene can have multiple `True` subclass labels.

Save annotated table as:

* `lin28a_project/results/tables/04_candidate_functional_subclass_annotation.csv`

---

### 5. Manual review table

After rule-based annotation, create a table for manual review:

* `lin28a_project/results/tables/04_candidate_annotation_manual_review.csv`

This table should include:

* `Accession`
* `Gene Symbol`
* `Description`
* all subclass Boolean columns
* `mean_CLIP_enrichment`
* `CLIP-seq FDR`
* `Ribosome density change (log2)`
* `RNA-seq mRNA change upon Lin28a KD (log2)`
* `annotation_notes`

Do not overclaim ambiguous classifications.

If a gene cannot be confidently classified from the description, mark it as:

* `is_other_or_unclear = True`

---

### 6. Compare candidate groups with background

Compare functional subclass proportions across:

1. all analyzable transcripts from `table_s5_cleaned.csv`
2. LIN28A-bound transcripts
3. high-confidence candidate transcripts

Suggested definition for LIN28A-bound transcripts:

* `CLIP-seq FDR < 0.05`

Do not create new biological thresholds beyond this unless explicitly justified.

Create a summary table:

* rows: functional subclasses
* columns: group, number of transcripts, fraction of transcripts

Save as:

* `lin28a_project/results/tables/04_subclass_fraction_summary.csv`

---

### 7. Figures

Create only the following figures.

#### Figure 04-1: Candidate subclass count bar plot

For high-confidence candidates only.

* x-axis: functional subclass
* y-axis: number of high-confidence candidate genes

Save as:

* `lin28a_project/results/figures/04_high_confidence_subclass_counts.png`

#### Figure 04-2: Subclass fraction comparison plot

Compare subclass fractions among:

* all analyzable transcripts
* LIN28A-bound transcripts
* high-confidence candidates

Save as:

* `lin28a_project/results/figures/04_subclass_fraction_comparison.png`

#### Figure 04-3: Ribosome density change by subclass

For high-confidence candidates.

* x-axis: functional subclass
* y-axis: ribosome density change after Lin28a knockdown

Save as:

* `lin28a_project/results/figures/04_ribosome_change_by_subclass.png`

Do not generate additional plots unless explicitly approved.

---

### 8. Notes and interpretation

Write a short interpretation note:

* `lin28a_project/notes/04_functional_subclass_interpretation.md`

This note should include:

1. how many high-confidence candidates were analyzed,
2. which subclasses were most common,
3. whether ER/membrane/secretory-related categories appear common among candidates,
4. whether the subclass pattern is consistent with the original paper's ER-associated translation model,
5. important limitations:

   * annotation is rule-based and preliminary,
   * this does not prove direct biological function,
   * this analysis is based on mESC data, not cancer or differentiated cells,
   * Table S6 is GO-level information and may not provide gene-level subclass annotation,
6. suggested next step:

   * binding-site count or binding-position analysis using Table S3,
   * optional BAM-level validation for representative top candidates.

---

### 9. Output for next spec

At the end of this spec, prepare a clean input table for Spec 05:

* `lin28a_project/results/tables/04_high_confidence_candidates_for_spec05.csv`

This table should contain the A/B overlap high-confidence candidates and the key columns needed for binding-site analysis:

* `Accession`
* `Gene Symbol`
* `Description`
* `mean_CLIP_enrichment`
* `CLIP-seq FDR`
* `Ribosome density change (log2)`
* `RNA-seq mRNA change upon Lin28a KD (log2)`
* all functional subclass Boolean columns

Do not perform binding-site analysis in Spec 04.

---

## Constraints

* Do not modify files outside `lin28a_project/`.
* Do not modify `tools/binfo1-datapack1/`.
* Do not copy BAM, BAI, FASTQ, SAM, pileup, bedgraph, bigWig files.
* Do not run `git add`, `git commit`, or `git push`.
* Do not delete existing files unless explicitly approved.
* Do not change Spec 03 threshold definitions.
* Do not perform BAM validation in this spec.
* Do not perform let-7 target analysis in this spec.
* Do not perform binding-site count or binding-position analysis in this spec; prepare input for Spec 05 only.
* Use the existing `jupyter_env` conda environment.
* Use `python`, not `python3`.
* Do not install packages or modify conda environments without explicit approval.
* Do not run BLAST, InterProScan, Foldseek, or any sequence-search tool.
* Treat functional subclass labels as preliminary rule-based annotations.
* Do not generate extra plots beyond the three requested figures unless explicitly approved.

---

## Final report

After completing this spec, report:

1. files created or modified,
2. conda environment and Python version used,
3. number of Threshold A candidates,
4. number of Threshold B candidates,
5. number of A/B overlap candidates,
6. subclass count summary,
7. saved figure paths,
8. saved table paths,
9. limitations and assumptions,
10. recommended next step, without executing it.
