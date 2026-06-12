# 07 External Annotation Provenance

## Source

- Name: UCSC Genome Browser mm9 refGene track
- Description: RefSeq curated gene annotation for mouse genome assembly mm9 (NCBI build 37)
- Type: **Public external annotation reference** (NOT raw sequencing data)
- Used for: mapping transcript-level binding-site positions (Table S3A) to
  5′UTR / CDS / 3′UTR regions

## Download details

- URL: http://hgdownload.soe.ucsc.edu/goldenPath/mm9/database/refGene.txt.gz
- Download command:
  ```
  wget -O lin28a_project/data/annotations/mm9_refGene.txt.gz \
    "http://hgdownload.soe.ucsc.edu/goldenPath/mm9/database/refGene.txt.gz"
  ```
- Download date: 2026-06-11 05:42 UTC
- Saved to: `lin28a_project/data/annotations/mm9_refGene.txt.gz`
- File size: 4,813,469 bytes (4.8 MB)
- md5sum: 029bc7d0c31f4dc2fc2ce6dbdfb3ffbe

## Format

Tab-delimited, no header row. 16 columns:

| Index | Column | Description |
|---|---|---|
| 0 | bin | UCSC bin index (ignore) |
| 1 | name | RefSeq transcript ID (NM_...) |
| 2 | chrom | Chromosome |
| 3 | strand | Strand (+/-) |
| 4 | txStart | Transcript start, 0-based |
| 5 | txEnd | Transcript end, 0-based half-open |
| 6 | cdsStart | CDS start, 0-based |
| 7 | cdsEnd | CDS end, 0-based half-open |
| 8 | exonCount | Number of exons |
| 9 | exonStarts | Comma-separated exon starts, 0-based |
| 10 | exonEnds | Comma-separated exon ends, 0-based half-open |
| 11 | score | Score (unused) |
| 12 | name2 | Gene symbol |
| 13 | cdsStartStat | CDS start status |
| 14 | cdsEndStat | CDS end status |
| 15 | exonFrames | Exon reading frames |

## Note on mm9 / assembly choice

The Lin28a PAR-CLIP paper (Cho et al., 2012, Cell) used mouse genome assembly mm9.
UCSC mm9 refGene is therefore the appropriate annotation for matching
Table S3A transcript IDs and positions.

## Usage restriction

This file is used read-only as a coordinate reference.
It has NOT been copied to `tools/binfo1-datapack1/` or any other protected directory.
