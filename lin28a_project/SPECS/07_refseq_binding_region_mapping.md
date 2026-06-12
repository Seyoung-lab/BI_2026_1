# SPEC07: RefSeq-based binding-site region classification

## Goal

Table S3A의 LIN28A binding site position을 UCSC mm9 refGene annotation을 이용해
5′UTR / CDS / 3′UTR로 분류하고, binding region과 ribosome density change의 관계를 분석한다.

---

## External annotation

| Field | Value |
|---|---|
| Source | UCSC Genome Browser mm9 refGene |
| URL | `http://hgdownload.soe.ucsc.edu/goldenPath/mm9/database/refGene.txt.gz` |
| Saved file | `lin28a_project/data/annotations/mm9_refGene.txt.gz` |
| Type | Public external annotation reference (raw sequencing data 아님) |
| Provenance note | `notes/07_annotation_provenance.md` |

---

## Inputs

| Input | Description |
|---|---|
| Table S3A | LIN28A binding-site table (position, transcript ID, gene symbol) |
| Table S5-derived | Candidate group labels and ribosome density change values per transcript |
| mm9 refGene | UCSC RefSeq annotation — transcript boundaries, exon coordinates, CDS ranges |

---

## Key QC

| Check | Result | Status |
|---|---|---|
| refGene match rate | 98.8% (6,524 / 6,606 S3A transcripts) | ✓ Standard analysis |
| out_of_bounds binding sites | 0.14% (91 sites) | ✓ Acceptable |
| Position coordinate assumption | 1-based exonic transcript coordinate from 5′ end | ✓ Validated |

**Example transcript checks** confirming Position compatibility with transcript-level coordinates:

| Gene | RefSeq ID | max S3A Position | Total exonic length |
|---|---|---|---|
| Pgrmc1 | NM_016783 | 1,803 | 1,870 nt |
| Ktn1 | NM_008477 | 4,437 | 4,485 nt |
| Pvrl3 (Nectin3) | NM_021495 | 1,713 | 3,070 nt |

---

## Analysis design

### Site-level region distribution

- 각 binding site를 개별적으로 5′UTR / CDS / 3′UTR / ncRNA로 분류
- 분류 기준: refGene 기반 누적 exonic 길이 (strand-aware)
  - `+` strand: 5′UTR = [txStart, cdsStart), CDS = [cdsStart, cdsEnd), 3′UTR = [cdsEnd, txEnd)
  - `-` strand: 5′UTR = [cdsEnd, txEnd), CDS = [cdsStart, cdsEnd), 3′UTR = [txStart, cdsStart)
- `out_of_bounds` / `ncRNA` / `unmatched` sites는 집계에서 별도 처리

### Transcript-level dominant binding region

- Transcript별로 binding site 수가 가장 많은 region을 dominant region으로 정의
- Ribosome density change (log2)와의 관계를 candidate group별로 비교

### Statistical analysis

- **Spearman correlation**: region별 binding site count vs ribosome density change; sample size n과 함께 보고
- **Chi-square test** (있는 경우): exploratory only; p-value를 주요 결론으로 사용하지 않음
  (sites are nested within transcripts — independence assumption violated)

> **중요**: site-level 분포와 transcript-level dominant region 분석은 별개 단위로 수행하였으며,
> 두 결과를 혼합하여 해석하지 않는다.

---

## Outputs

### Tables

| File | Description |
|---|---|
| `results/tables/07_match_rate_report.csv` | S3A transcript match rate to mm9 refGene |
| `results/tables/07_transcript_feature_lengths.csv` | Per-transcript 5′UTR / CDS / 3′UTR exonic lengths |
| `results/tables/07_s3_binding_region_classification.csv` | Per-site binding region classification |
| `results/tables/07_binding_region_summary_by_candidate_group.csv` | Site-level region fractions by candidate group |
| `results/tables/07_ribo_change_by_dominant_binding_region.csv` | Median ribo change by dominant binding region |

### Figures

| File | Description |
|---|---|
| `results/figures/07_binding_region_distribution.png` | Site-level binding region distribution by candidate group |
| `results/figures/07_ribo_change_by_dominant_binding_region.png` | Ribo density change by transcript-level dominant region |

### Notes

| File | Description |
|---|---|
| `notes/07_annotation_provenance.md` | External annotation download record (URL / command / date / size / md5) |
| `notes/07_binding_region_interpretation.md` | Full interpretation of binding region results |

### Notebook

| File | Description |
|---|---|
| `notebooks/05_binding_region_analysis.ipynb` | SPEC07 analysis notebook (pre-computed results loaded; figures embedded inline) |

---

## Limitations

1. mm9 refGene annotation이 원 논문에서 사용한 annotation 버전과 다를 수 있으며, region boundary가 일치하지 않을 수 있다.
2. S3A Position을 transcript-level exonic coordinate (1-based)로 해석하였으나, 이는 논문에 명시되지 않은 가정이며 QC를 통해 간접 검증하였다.
3. Isoform diversity로 인해 동일 NM_ accession에 여러 refGene entry가 존재할 수 있으며, 가장 긴 exonic transcript를 canonical로 선택하였다.
4. Site-level 분석에서 같은 transcript 내 binding sites는 독립적이지 않으므로 statistical independence 가정이 성립하지 않는다. Site-level 분석은 탐색적 기술 통계로만 사용한다.
5. Region-based ribosome density change 비교는 transcript 수가 적은 subgroup (특히 5′UTR-dominant)에서 해석에 주의가 필요하다.

---

## Status

**Completed** (2026-06-11)

- [x] External annotation downloaded and provenance recorded
- [x] refGene column format verified (16 columns including `bin`; `name` = NM_ accession)
- [x] Match rate QC passed (98.8% ≥ 70% threshold → standard analysis mode)
- [x] Position coordinate assumption validated (out_of_bounds 0.14%; example transcripts confirmed)
- [x] Site-level and transcript-level analyses completed separately
- [x] Spearman correlations reported with n
- [x] Chi-square treated as exploratory only
- [x] All output tables and figures generated
- [x] Notebook executed successfully (14 cells, no errors, figures embedded inline)
- [x] SPEC01–07 all completed
