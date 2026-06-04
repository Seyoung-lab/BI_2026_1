# 06 BAM Candidate Validation Interpretation

## 1. Gene selection

Genes loaded from `results/tables/05_candidate_genes_for_BAM_validation.csv` (SPEC05).

- **Positive candidates (A∩B high-confidence)**: Pgrmc1, Ktn1, Pvrl3
  Selected based on highest mean CLIP enrichment × ribosome density increase
  (limited mRNA change) among the 48 A∩B overlap candidates.
- **Negative / comparison gene**: Unc45a
  Not_candidate group; binding_site_count = 0; has ribosome data.

### Pvrl3 → Nectin3 alias mapping

`Pvrl3` in Table S5 corresponds to `Nectin3` in GENCODE vM27 (official gene rename, 2018).

- candidate_gene_symbol = Pvrl3
- gtf_gene_name = Nectin3
- alias_mapping_used = True

All GTF coordinate lookups for Pvrl3 used the alias `Nectin3`.

## 2. BAM files used

| Sample key | Label | BAM file |
|---|---|---|
| CLIP_35L33G | CLIP (35L33G) | CLIP-35L33G.bam |
| RPF_siLuc | RPF siLuc | RPF-siLuc.bam |
| RPF_siLin28a | RPF siLin28a | RPF-siLin28a.bam |
| RNA_siLuc | RNA-seq siLuc | RNA-siLuc.bam |
| RNA_siLin28a | RNA-seq siLin28a | RNA-siLin28a.bam |

All BAMs used as read-only from `tools/binfo1-datapack1/`. No BAM files copied.

## 3. Coverage extraction

```
conda run -n samtools samtools depth -aa -r <chrom:start-end> <bam>
```

- `-aa`: outputs ALL positions in region, including zero-coverage
- Region: gene body ± 1000 bp flank
- Python 0-fills any residual missing positions
- Region-level summary computed from 0-filled coverage

## 4. RPM normalization

```
RPM depth = raw_depth / (total_mapped_reads / 1,000,000)
```

Approximate normalization for visual comparison only. No replicates; no statistical test.

### Library sizes

| Sample | Label | Mapped reads | RPM factor |
|---|---|---|---|
| CLIP_35L33G | CLIP (35L33G) | 36,589,778 | 36.59 |
| RPF_siLuc | RPF siLuc | 41,007,348 | 41.01 |
| RPF_siLin28a | RPF siLin28a | 29,178,323 | 29.18 |
| RNA_siLuc | RNA-seq siLuc | 25,785,774 | 25.79 |
| RNA_siLin28a | RNA-seq siLin28a | 32,938,700 | 32.94 |

## 5. Gene coordinates (GENCODE vM27, gene body ± 1000 bp flank)

| Gene Symbol | GTF gene_name | Alias used | Region | Gene length |
|---|---|---|---|---|
| Pgrmc1 | Pgrmc1 |  | chrX:35860859-35870732 | 7,874 |
| Ktn1 | Ktn1 |  | chr14:47884905-47978351 | 91,447 |
| Pvrl3 | Nectin3 | ✓ | chr16:46207069-46319888 | 110,820 |
| Unc45a | Unc45a |  | chr7:79974040-79998741 | 22,702 |

## 6. Qualitative assessment criteria

### CLIP signal threshold
- **yes**: max_rpm > 5.0 (strong focal CLIP peak)
- **weak**: max_rpm > 1.0 AND mean_rpm > 0.02 (low-level enrichment)
- **no**: otherwise (consistent with background / no LIN28A binding)

*Note: max_rpm alone is sensitive to a single high-coverage position.
A combined max + mean criterion is used to reduce false positives from
isolated read pileups.*

### RPF pattern
- **higher_siLin28a**: mean_rpm_siLin28a / mean_rpm_siLuc > 1.3
  → consistent with translational derepression after Lin28a KD
- **similar**: ratio 0.77–1.3
- **lower_siLin28a**: ratio < 0.77

### RNA pattern
- **stable**: mean RNA ratio 0.77–1.3 (translational, not transcriptional regulation)
- **changed**: ratio outside 0.77–1.3

## 7. Interpretation summary

| Gene | Candidate type | CLIP enrich | ribo Δ | mRNA Δ | BS count | CLIP signal | RPF pattern | RNA pattern | Summary |
|---|---|---|---|---|---|---|---|---|---|
| Pgrmc1 | A_and_B_overlap | 4.031 | 0.315 | -0.220 | 21 | yes | higher_siLin28a (consistent with derepression | stable | consistent with direct translational repression target |
| Ktn1 | A_and_B_overlap | 2.913 | 0.605 | -0.399 | 62 | yes | similar | changed | partially consistent — see caveats |
| Pvrl3 | A_and_B_overlap | 2.882 | 0.867 | -0.324 | 17 | yes | higher_siLin28a (consistent with derepression | changed | partially consistent — see caveats |
| Unc45a | Not_candidate | -1.861 | -1.965 | 0.016 | 0 | no | lower_siLin28a | stable | negative control: no CLIP signal; RPF lower after Lin28 |

## 8. Limitations

1. **Locus-level only**: Coverage spans full gene body (introns included).
   Not equivalent to transcript-level quantification.
2. **No biological replicates**: Each condition is a single BAM. No replicate-level
   statistical testing. Results are qualitative.
3. **RPM normalization is approximate**: Not corrected for GC content, mappability,
   or gene length.
4. **GENCODE vs RefSeq boundary mismatch**: Gene coordinates from GENCODE vM27 may
   differ from RefSeq transcript boundaries used in Table S5 and Table S3.
5. **Pvrl3/Nectin3 alias**: `Nectin3` alias used for coordinate lookup in GENCODE vM27.
6. **samtools in separate conda env**: `conda run -n samtools samtools` used for
   all BAM operations. No BAM/BAI files were modified.

## 9. Recommended next steps

1. **RefSeq-based binding-region mapping**: Map Table S3 `Position` offsets to
   5′UTR/CDS/3′UTR using GENCODE UTR/CDS annotations (requires scope extension).
2. **Final report figure selection**: Choose 1–2 representative figures for the
   final project report.
3. **let-7 pathway control**: Compare patterns for let-7 target genes as an
   additional comparison group.
