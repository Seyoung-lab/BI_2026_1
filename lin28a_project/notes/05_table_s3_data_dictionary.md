# 05 Table S3 Data Dictionary

## Source

File: `1-s2.0-S0092867412012342-mmc5.xls` (wrong — actually mmc3.xls)
File: `1-s2.0-S0092867412012342-mmc3.xls`

## Sheets

| Sheet | Rows | Cols | Content |
|---|---|---|---|
| Table S3A | 65,534 | 11 | LIN28A binding-site records — **used for analysis** |
| Table S3B | 572 | 6 | Enriched hexameric sequences — not used in SPEC 05 |

## Selected sheet: Table S3A

Loaded with `pd.read_excel(..., sheet_name='Table S3A', skiprows=1)` — row 0 is a long description.

## Column mapping

| Index | Column name | Role | Notes |
|---|---|---|---|
| 0 | `Transcript` | Transcript ID | RefSeq NM_ accession, matches Table S5 `Accession` |
| 1 | `Position` | Nucleotide offset | Integer, position within transcript. NOT used for region inference. |
| 2 | `Gene Symbol` | Gene symbol | Available |
| 3 | `Crosslinked base` | Crosslinked nucleotide | G/A/T/C |
| 4 | `Number of detected libraries` | Library robustness | 1–3 (how many of the 3 CLIP libraries detected this site) |
| 5 | `Detection depth (35L33G)` | Read depth, antibody 35L33G | 43261 non-null |
| 6 | `Score in entropy (35L33G)` | Entropy score, antibody 35L33G | 43261 non-null |
| 7 | `Detection depth (2J3)` | Read depth, antibody 2J3 | 41007 non-null |
| 8 | `Score in entropy (2J3)` | Entropy score, antibody 2J3 | 41007 non-null |
| 9 | `Detection depth (polyclonal)` | Read depth, polyclonal | 42099 non-null |
| 10 | `Score in entropy (polyclonal)` | Entropy score, polyclonal | 42099 non-null |

## Region annotation

**Not available.** Table S3A does NOT contain 5'UTR / CDS / 3'UTR annotations.
The `Position` column alone cannot be used to infer binding region without external GTF data.
See `notes/05_binding_position_unavailable_note.md`.

## Transcript ID matching

- S3A `Transcript` format: `NM_XXXXXX` (no version suffix in data)
- S5 `Accession` format: `NM_XXXXXX` (same format)
- Direct string matching applied; match rate reported in analysis.

## Unique transcripts: 6606
