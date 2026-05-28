# 05 Binding-Position Analysis: Unavailable

## What was checked

Table S3A contains a `Position` column with nucleotide positions within each transcript.

## Why region analysis was not performed

Table S3A does **not** include region annotation columns (e.g., 5'UTR, CDS, 3'UTR, exon, intron).
The `Position` value alone is a bare nucleotide offset within the transcript sequence.
To convert it to a region label (5'UTR / CDS / 3'UTR), the exact UTR/CDS boundary coordinates
for each transcript would be required from an external annotation source (e.g., GENCODE GTF).

Parsing and joining GTF-level CDS/UTR coordinates is outside the scope of SPEC 05.
The `Position` column was therefore intentionally NOT used to infer region labels.
No 5'UTR / CDS / 3'UTR categories were created.

## What was done instead

All SPEC 05 analyses focus on:
- binding-site count (binding_site_count)
- binding-site robustness (multi-library detection, entropy scores, detection depth)

## Possible future extension

In a future spec, transcript-level UTR/CDS boundaries could be obtained from
`tools/binfo1-datapack1/gencode.vM27.annotation.gtf.gz` and joined to the `Position`
column to enable 5'UTR / CDS / 3'UTR region-level analysis.
