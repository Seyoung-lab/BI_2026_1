# Table S5 Data Dictionary

Source file: `1-s2.0-S0092867412012342-mmc5.xls` (sheet: "Table S5")
Load method: `pd.read_excel(..., skiprows=1)` — row 0 is a long description; row 1 is the header.

Total rows: 16,465 transcripts
Total columns: 22

## Column Mapping

| Column index | Column name (exact) | Biological meaning |
|---|---|---|
| 0 | `Accession` | RefSeq transcript accession (e.g. NM_xxxxxx) |
| 1 | `Gene Symbol` | Gene symbol |
| 2 | `CLIP-seq p-value` | Chi-squared CLIP-seq binding p-value |
| 3 | `CLIP-seq FDR` | CLIP-seq binding false discovery rate |
| 4 | `RNA-seq reads (for normalization)` | RNA-seq read count for CLIP normalization |
| 5 | `CLIP-seq reads (35L33G)` | Raw CLIP read count, antibody 35L33G |
| 6 | `CLIP-seq enrichment (35L33G, log2)` | CLIP enrichment log2, antibody 35L33G |
| 7 | `CLIP-seq reads (2J3)` | Raw CLIP read count, antibody 2J3 |
| 8 | `CLIP-seq enrichment (2J3, log2)` | CLIP enrichment log2, antibody 2J3 |
| 9 | `CLIP-seq reads (polyclonal)` | Raw CLIP read count, polyclonal antibody |
| 10 | `CLIP-seq enrichment (polyclonal, log2)` | CLIP enrichment log2, polyclonal antibody |
| 11 | `Ribosome density change (log2)` | RPF density change upon Lin28a KD (log2) |
| 12 | `Ribosome occupancy change (log2)` | Ribosome occupancy change upon Lin28a KD (log2) |
| 13 | `RPF  reads (siLuc)` | RPF reads, siLuc control |
| 14 | `RNA-seq short tag alignment reads (siLuc)` | RNA-seq reads, siLuc control |
| 15 | `RPF  reads (siLin28a)` | RPF reads, siLin28a knockdown |
| 16 | `RNA-seq short tag alignment reads (siLin28a)` | RNA-seq reads, siLin28a knockdown |
| 17 | `RNA-seq reads (untreated, RPKM)` | Untreated RNA-seq expression (RPKM) |
| 18 | `RNA-seq reads (siLuc, RPKM)` | siLuc RNA-seq expression (RPKM) |
| 19 | `RNA-seq reads (siLin28a, RPKM)` | siLin28a RNA-seq expression (RPKM) |
| 20 | `RNA-seq mRNA change upon Lin28a KD (log2)` | mRNA abundance change upon Lin28a KD (log2) |
| 21 | `Description` | Gene/protein description |

## Key columns for direct target analysis

**CLIP enrichment columns (used for mean_CLIP_enrichment):**
```
CLIP-seq enrichment (35L33G, log2)
CLIP-seq enrichment (2J3, log2)
CLIP-seq enrichment (polyclonal, log2)
```

**NOT used for mean_CLIP_enrichment:**
- `CLIP-let7g`, `CLIP-Mirlet7d`, `CLIP-Mirlet7f-1` — these are miRNA locus names or subset BAM file identifiers, NOT columns in Table S5.

**Ribosome density change:** `Ribosome density change (log2)` (col 11)

**RNA-seq mRNA change:** `RNA-seq mRNA change upon Lin28a KD (log2)` (col 20)

## Missing value summary

| Column | Missing (n) | Note |
|---|---|---|
| CLIP-seq p-value | 5,749 | Transcripts without CLIP binding call |
| CLIP-seq FDR | 5,749 | Same set |
| CLIP enrichment (35L33G, log2) | 5,749 | Same set |
| CLIP enrichment (2J3, log2) | 5,749 | Same set |
| CLIP enrichment (polyclonal, log2) | 5,749 | Same set |
| Ribosome density change (log2) | 10,764 | Low expression or low read count |
| RNA-seq mRNA change upon Lin28a KD (log2) | 9 | |
| Description | 854 | |
