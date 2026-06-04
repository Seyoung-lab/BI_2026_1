
# SPEC06: Representative BAM-level validation of LIN28A candidate targets

## Goal

Perform representative BAM-level validation for selected candidate LIN28A direct translational repression targets.

The main biological question is:

> Do representative candidate genes identified from Table S5 and Table S3 show read-level patterns consistent with LIN28A binding and translational derepression after Lin28a knockdown?

This analysis is not intended to reproduce the full original sequencing pipeline.
Instead, it is a small locus-level validation step using already-aligned BAM files.

---

## Background

Previous specs generated the following results:

* **SPEC03**: Defined candidate direct LIN28A-mediated translational repression targets using Table S5.
* **SPEC04**: Classified high-confidence candidates into functional subclasses.
* **SPEC05**: Reprocessed Table S3 binding-site data and showed that high-confidence candidates have higher LIN28A binding-site burden than non-candidates.

SPEC06 adds a read-level validation layer by inspecting representative candidate loci in:

* LIN28A CLIP-seq BAM
* ribosome footprinting BAM
* RNA-seq BAM

This validation should be interpreted cautiously. It is qualitative or semi-quantitative locus-level inspection, not a full differential expression or differential translation analysis.

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

Also check whether `samtools` is available:

```bash
which samtools
samtools --version
```

Important notes:

* Use `python`, not `python3`, because `python3` may point to the system Python instead of the conda environment.
* Do not create a new conda environment.
* Do not install or update packages without explicit approval.
* If a required package or command is missing, stop and report it first.
* Record the environment check in:

`lin28a_project/notes/06_environment_check.md`

---

## Inputs

### Candidate table

Preferred input:

* `lin28a_project/results/tables/05_candidate_genes_for_BAM_validation.csv`

If unavailable, use candidate information from:

* `lin28a_project/results/tables/04_high_confidence_candidates_for_spec05.csv`
* `lin28a_project/results/tables/05_s5_with_binding_site_features.csv`
* `lin28a_project/results/tables/03_direct_candidates_threshold_A.csv`
* `lin28a_project/results/tables/03_direct_candidates_threshold_B.csv`

Suggested representative genes from SPEC05:

Positive candidate genes:

* `Pgrmc1`
* `Ktn1`
* `Pvrl3`

Negative or comparison gene:

* `Unc45a`

If any of these genes cannot be mapped to the annotation file or BAM coordinate system, report the issue and choose another candidate from the high-confidence candidate table.

---

### BAM files

Use the existing BAM files as read-only input.

Do not copy, move, rename, modify, delete, or re-index these files unless explicitly approved.

Input BAMs:

* `tools/binfo1-datapack1/CLIP-35L33G.bam`
* `tools/binfo1-datapack1/RPF-siLuc.bam`
* `tools/binfo1-datapack1/RPF-siLin28a.bam`
* `tools/binfo1-datapack1/RNA-siLuc.bam`
* `tools/binfo1-datapack1/RNA-siLin28a.bam`

Expected BAM index files:

* `tools/binfo1-datapack1/CLIP-35L33G.bam.bai`
* `tools/binfo1-datapack1/RPF-siLuc.bam.bai`
* `tools/binfo1-datapack1/RPF-siLin28a.bam.bai`
* `tools/binfo1-datapack1/RNA-siLuc.bam.bai`
* `tools/binfo1-datapack1/RNA-siLin28a.bam.bai`

If a required `.bai` index is missing, stop and report it. Do not create a new index without approval.

---

### Annotation file

Use the available GENCODE annotation for gene-level coordinate lookup:

* `tools/binfo1-datapack1/gencode.vM27.annotation.gtf.gz`

This annotation is used only for locating gene coordinates for BAM coverage visualization.

Important:

* This spec does not attempt to map Table S3 transcript-level positions to 5′UTR/CDS/3′UTR.
* This spec does not require RefSeq transcript-boundary mapping.
* If GENCODE gene names do not match selected candidate gene symbols, report the mismatch and choose alternative candidates if needed.

---

## Output directories

Save output tables to:

* `lin28a_project/results/tables/`

Save output figures to:

* `lin28a_project/results/figures/`

Save notes to:

* `lin28a_project/notes/`

Save small derived coverage files to:

* `lin28a_project/results/coverage/`

Notebook should be created or updated at:

* `lin28a_project/notebooks/04_bam_candidate_validation.ipynb`

---

## Important restrictions

* Do not modify files outside `lin28a_project/`.
* Do not modify `tools/binfo1-datapack1/`.
* Do not copy BAM files into the project directory.
* Do not run FASTQ processing, trimming, mapping, or alignment.
* Do not perform genome-wide differential analysis.
* Do not perform full read-count quantification for all genes.
* Do not run BLAST, InterProScan, Foldseek, or sequence-search tools.
* Do not run `git add`, `git commit`, or `git push`.
* Do not delete existing files unless explicitly approved.
* Do not create excessive plots.
* Keep this analysis focused on a small number of representative loci.

---

## Tasks

### 1. Confirm inputs and environment

Check and report:

* conda environment
* Python path and version
* `samtools` availability
* existence of all required BAM and BAI files
* existence of `gencode.vM27.annotation.gtf.gz`
* existence of candidate gene table

Write environment and input check to:

* `lin28a_project/notes/06_environment_check.md`

---

### 2. Select candidate genes

Load:

* `lin28a_project/results/tables/05_candidate_genes_for_BAM_validation.csv`

If this file exists, use it as the primary candidate list.

If not, reconstruct candidate selection using previous result tables.

Select:

* 2 to 3 positive candidate genes
* 1 negative or comparison gene

Preferred positive candidates:

* `Pgrmc1`
* `Ktn1`
* `Pvrl3`

Preferred comparison gene:

* `Unc45a`

Create and save the final selected gene list:

* `lin28a_project/results/tables/06_selected_genes_for_bam_validation.csv`

This table should include:

* `Gene Symbol`
* `Accession`, if available
* `Description`, if available
* `candidate_group`
* `mean_CLIP_enrichment`, if available
* `Ribosome density change (log2)`, if available
* `RNA-seq mRNA change upon Lin28a KD (log2)`, if available
* `binding_site_count`, if available
* `reason_for_selection`

---

### 3. Extract gene coordinates from GENCODE GTF

Parse `gencode.vM27.annotation.gtf.gz`.

For each selected gene, identify gene-level coordinates using `gene_name`.

For each selected gene, extract:

* chromosome
* start
* end
* strand
* gene_id
* gene_name
* transcript IDs, if easily available

Extend each region by a small flank for visualization.

Suggested flank:

* 1,000 bp upstream and downstream

Create region string:

```text
chr:start-end
```

Save gene coordinate table as:

* `lin28a_project/results/tables/06_selected_gene_coordinates.csv`

Important checks:

* Confirm chromosome naming style in GTF and BAM are compatible.

  * Example: `chr1` vs `1`
* Use `samtools idxstats` to inspect BAM chromosome names.
* If chromosome naming is incompatible, report the issue and do not force analysis.

---

### 4. Estimate library sizes for simple coverage normalization

For each BAM, use `samtools idxstats` or equivalent to estimate mapped reads.

Save library size table as:

* `lin28a_project/results/tables/06_bam_library_size_summary.csv`

Use simple RPM-style normalization for coverage visualization:

```text
RPM coverage = raw depth / mapped reads * 1,000,000
```

Important:

* This is only for approximate visual comparison.
* Do not treat this as a full differential analysis.
* Mention this limitation in the interpretation note.

---

### 5. Extract coverage for selected regions

For each selected gene region and each BAM file, extract per-base coverage using `samtools depth`.

Use read-only input BAMs.

Save small derived coverage files under:

* `lin28a_project/results/coverage/`

Suggested file naming:

```text
06_<GeneSymbol>_<sample>_depth.tsv
```

For example:

* `06_Pgrmc1_CLIP_35L33G_depth.tsv`
* `06_Pgrmc1_RPF_siLuc_depth.tsv`
* `06_Pgrmc1_RPF_siLin28a_depth.tsv`
* `06_Pgrmc1_RNA_siLuc_depth.tsv`
* `06_Pgrmc1_RNA_siLin28a_depth.tsv`

Coverage table columns should include:

* chromosome
* position
* raw_depth
* sample
* gene_symbol
* rpm_depth

If coverage extraction fails for a gene, report the reason and continue with other genes if possible.

---

### 6. Create locus-level coverage plots

For each selected gene, create a multi-track coverage plot.

Each gene figure should include:

1. LIN28A CLIP-seq coverage

   * `CLIP-35L33G.bam`
2. RPF coverage comparison

   * `RPF-siLuc.bam`
   * `RPF-siLin28a.bam`
3. RNA-seq coverage comparison

   * `RNA-siLuc.bam`
   * `RNA-siLin28a.bam`

Recommended plot structure:

* One figure per gene
* Three vertical tracks:

  1. CLIP
  2. RPF siLuc vs siLin28a
  3. RNA siLuc vs siLin28a
* x-axis: genomic position
* y-axis: RPM-normalized coverage

Save figures as:

* `lin28a_project/results/figures/06_<GeneSymbol>_bam_coverage_validation.png`

Example:

* `lin28a_project/results/figures/06_Pgrmc1_bam_coverage_validation.png`

Do not generate more than one main coverage figure per gene unless explicitly approved.

---

### 7. Create simple region-level coverage summary

For each selected gene and each BAM sample, summarize coverage across the selected gene region.

Calculate:

* total raw coverage sum
* mean raw depth
* max raw depth
* total RPM-normalized coverage sum
* mean RPM-normalized depth
* max RPM-normalized depth

Save as:

* `lin28a_project/results/tables/06_gene_region_coverage_summary.csv`

Important:

* Interpret these summaries cautiously because gene length, isoform structure, mappability, and local coverage patterns can affect values.
* Do not use these as definitive differential expression or translation estimates.

---

### 8. Compare BAM-level pattern with Table S5 pattern

For each selected gene, compare the visual and summary pattern to Table S5 values.

Specifically check:

1. Does the gene show visible CLIP signal?
2. Is RPF siLin28a coverage visually or regionally higher than RPF siLuc?
3. Is RNA siLin28a coverage relatively similar to RNA siLuc compared with the RPF change?
4. Is this pattern consistent with a candidate direct translational repression target?

Create a summary table:

* `lin28a_project/results/tables/06_bam_validation_interpretation_table.csv`

Columns:

* `Gene Symbol`
* `candidate_type`
* `TableS5_mean_CLIP_enrichment`
* `TableS5_ribosome_density_change`
* `TableS5_mRNA_change`
* `binding_site_count`
* `visible_CLIP_signal`
* `RPF_pattern`
* `RNA_pattern`
* `BAM_validation_summary`
* `caveats`

Use qualitative categories such as:

* `yes`
* `weak`
* `no`
* `ambiguous`

Do not overclaim.

---

### 9. Notes and interpretation

Write an interpretation note:

* `lin28a_project/notes/06_bam_candidate_validation_interpretation.md`

This note should include:

1. which genes were selected and why,
2. which BAM files were used,
3. how coverage was extracted,
4. how coverage was normalized,
5. whether representative candidate loci show visible CLIP signal,
6. whether RPF/RNA patterns are broadly consistent with Table S5,
7. limitations:

   * locus-level validation only,
   * no full differential analysis,
   * no biological replicate-level statistical test,
   * coverage depends on gene length, isoforms, and mappability,
   * GENCODE annotation may not perfectly match RefSeq transcript IDs used in Table S5/Table S3,
8. recommended next step:

   * RefSeq-based binding-region mapping, if external annotation is approved,
   * final report figure selection and writing.

---

## Expected outputs

### Notebook

* `lin28a_project/notebooks/04_bam_candidate_validation.ipynb`

### Notes

* `lin28a_project/notes/06_environment_check.md`
* `lin28a_project/notes/06_bam_candidate_validation_interpretation.md`

### Tables

* `lin28a_project/results/tables/06_selected_genes_for_bam_validation.csv`
* `lin28a_project/results/tables/06_selected_gene_coordinates.csv`
* `lin28a_project/results/tables/06_bam_library_size_summary.csv`
* `lin28a_project/results/tables/06_gene_region_coverage_summary.csv`
* `lin28a_project/results/tables/06_bam_validation_interpretation_table.csv`

### Coverage files

* `lin28a_project/results/coverage/06_<GeneSymbol>_<sample>_depth.tsv`

### Figures

* `lin28a_project/results/figures/06_<GeneSymbol>_bam_coverage_validation.png`

---

## Final report

After completing this spec, report:

1. files created or modified,
2. conda environment and Python version used,
3. whether `samtools` was available,
4. selected candidate genes and reasons for selection,
5. coordinate lookup results,
6. BAM library size summary,
7. coverage files generated,
8. coverage figures generated,
9. BAM-level interpretation for each gene,
10. limitations and assumptions,
11. recommended next step, without executing it.
