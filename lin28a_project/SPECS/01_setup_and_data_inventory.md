# 01_setup_and_data_inventory.md

## Goal

Set up the LIN28A project directory and inspect available input files.

## Scope

Only perform setup and file inventory.

Do not run biological analysis.
Do not apply thresholds.
Do not generate biological plots.

## Inputs

Existing read-only data directory:

`tools/binfo1-datapack1/`

Expected supplementary table directory:

`lin28a_project/data/supplementary_tables/`

## Tasks

1. Confirm current git repository root.
2. Confirm or create the following directories:
   - `lin28a_project/data/supplementary_tables/`
   - `lin28a_project/data/processed/`
   - `lin28a_project/notebooks/`
   - `lin28a_project/scripts/`
   - `lin28a_project/results/figures/`
   - `lin28a_project/results/tables/`
   - `lin28a_project/notes/`
3. List files in `tools/binfo1-datapack1/`.
4. Classify available files into:
   - aligned read-level data
   - index files
   - intermediate processed files
   - annotation/reference files
   - notebooks/results
5. List files in `lin28a_project/data/supplementary_tables/`.
6. Write a note file:
   - `lin28a_project/notes/data_inventory.md`

## Expected outputs

- `lin28a_project/notes/data_inventory.md`

## Do not

- Do not modify files in `tools/binfo1-datapack1/`.
- Do not copy BAM files.
- Do not run analysis.
- Do not create plots.
- Do not commit or push.
