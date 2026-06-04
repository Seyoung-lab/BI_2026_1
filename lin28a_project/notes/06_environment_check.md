# 06 Environment Check

## Python (jupyter_env)

- Python: 3.10.20 (main, Mar 11 2026, 17:46:40) [GCC 14.3.0]
- Executable: /home/sezero/miniconda3/envs/jupyter_env/bin/python
- conda env: jupyter_env
- Note: `python` used (not `python3`). `python3` on this system points to the
  system Python at /usr/bin/python3.

## samtools

`samtools` is NOT installed in `jupyter_env`.
It is installed in a separate conda environment named `samtools`.

All samtools calls are executed via:

```
conda run -n samtools samtools <args>
```

- samtools version: samtools 1.23

## BAM files and indices

- CLIP (35L33G): BAM ✓, BAI ✓, 1.37 GB
- RPF siLuc: BAM ✓, BAI ✓, 1.06 GB
- RPF siLin28a: BAM ✓, BAI ✓, 0.74 GB
- RNA-seq siLuc: BAM ✓, BAI ✓, 0.98 GB
- RNA-seq siLin28a: BAM ✓, BAI ✓, 1.26 GB

## GTF annotation

- Path: /home/sezero/data/BI_2026-1/Guided_Mission_1/colab-biolab/tools/binfo1-datapack1/gencode.vM27.annotation.gtf.gz
- Exists: ✓
- Size: 28.4 MB

## Chromosome naming compatibility

Both BAM (checked via samtools idxstats) and GTF use `chr`-prefixed chromosome
names (e.g., `chr1`, `chrX`). Chromosome naming is COMPATIBLE.

## Pvrl3 → Nectin3 alias mapping

Table S5 uses the gene symbol `Pvrl3`.
GENCODE vM27 annotation uses the current official gene name `Nectin3` for this locus
(the gene was officially renamed Pvrl3 → Nectin3 in 2018).

- candidate_gene_symbol = Pvrl3
- gtf_gene_name = Nectin3
- alias_mapping_used = True

All GTF coordinate lookups and region strings for Pvrl3 use the alias `Nectin3`.
Results tables record both the original symbol (Pvrl3) and the GTF name (Nectin3).

## samtools depth -aa and zero-filling

Coverage is extracted with:

```
samtools depth -aa -r <chrom:start-end> <bam>
```

The `-aa` flag outputs ALL reference positions including zero-coverage ones,
preventing mean depth from being biased by only reporting covered positions.

As an additional safety step, Python fills any remaining missing positions to 0
by merging depth data against the full genomic range.

Region-level coverage summaries are computed from these 0-filled arrays.

## Note on intron-spanning regions

Gene-level regions span the full gene body (introns included) ± 1000 bp flank.
Coverage summaries are locus-level visualization aids only — NOT differential
expression or translational efficiency estimates.
