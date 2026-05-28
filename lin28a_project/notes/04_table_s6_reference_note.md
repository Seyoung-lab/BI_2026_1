# Table S6 Reference Note

## Structure
- Sheet: 'Table S6'  |  2860 GO terms  x  11 columns
- Columns: GO accession, GO term, CLIP-seq number of valid members, CLIP-seq FDR,
  CLIP-seq log2 enrichment, RPF number of valid members, RPF FDR,
  RPF Ribosome density change (log2), RNA-seq number of valid members,
  RNA-seq FDR, RNA-seq mRNA abundance change (log2)

## What Table S6 is and is NOT
- GO-level enrichment summary for LIN28A-bound transcripts — NOT a gene-level annotation table.
- Cannot be used to assign GO terms to individual genes.
- Used here only to verify which GO categories were enriched in the original study.

## Relevant GO categories (most significant hits)

| Category | Example GO term | CLIP-seq FDR | RPF FDR |
|---|---|---|---|
| — | intrinsic to membrane | 6.05e-149 | 0.00e+00 |
| — | endoplasmic reticulum part | 4.31e-43 | 4.17e-77 |
| — | endoplasmic reticulum | 3.62e-41 | 5.34e-74 |
| — | endoplasmic reticulum membrane | 2.99e-29 | 1.94e-55 |
| — | lumen | 4.71e-26 | 4.23e-57 |
| — | Golgi apparatus | 1.35e-11 | 8.93e-17 |
| — | extracellular region | 2.68e-08 | 2.71e-03 |
| — | cell surface | 4.03e-06 | 1.52e-03 |

## Interpretation
The most significantly enriched CLIP-seq GO terms are membrane-intrinsic and ER-related,
consistent with the paper's ER-associated translation model.
These GO-level findings support using ER, membrane, Golgi, and secretory pathway keywords
for the rule-based functional subclass annotation in this spec.
