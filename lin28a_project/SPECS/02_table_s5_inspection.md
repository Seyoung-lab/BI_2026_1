# 02_table_s5_inspection.md

## Goal

Inspect Table S5 and create a data dictionary for transcript-level analysis.

## Scope

Only inspect Table S5.

Do not define direct targets yet.
Do not apply biological thresholds yet.

## Inputs

Supplementary Table S5 in:

`lin28a_project/data/supplementary_tables/`

## Tasks

1. Load Table S5 using Python.
2. Report:
   - number of rows
   - number of columns
   - sheet names if Excel file has multiple sheets
   - column names
   - missing value counts
   - numeric columns
3. Identify likely columns for:
   - transcript accession
   - gene symbol
   - CLIP-seq p-value
   - CLIP-seq FDR
   - CLIP enrichment from each antibody
   - ribosome density change after Lin28a knockdown
   - RNA-seq mRNA change after Lin28a knockdown
   - gene description
4. Do not rename columns in the raw table.
5. Create a cleaned working CSV only if column parsing is successful.

## Expected outputs

- `lin28a_project/notes/table_s5_data_dictionary.md`
- `lin28a_project/data/processed/table_s5_cleaned.csv`

## Do not

- Do not choose thresholds.
- Do not filter genes.
- Do not make biological conclusions.
