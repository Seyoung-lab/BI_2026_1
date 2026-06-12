# SPEC08: Functional context proxy analysis

## Goal

Binding site count나 binding region만으로는 ribosome density change가 충분히 설명되지 않는다.
Target transcript의 functional context (ER/membrane-associated annotation proxy)가
LIN28A-associated translational derepression 경향과 관련되는지 탐색적으로 분석한다.

> **해석 원칙**: 실제 ER-localized translation data가 없으므로,
> ER/membrane-associated annotation은 **proxy**로만 사용한다.
> "ER-localized mRNA"라고 직접 표현하지 않으며,
> 결론은 "functional context *may* contribute" 수준으로만 해석한다.

---

## Core questions

1. ER/membrane-associated annotation proxy를 가진 transcript가 non-proxy transcript보다
   ribosome density change가 더 positive한가?
2. ER/membrane-associated annotation proxy group에서 high-confidence candidate 비율이 더 높은가?
3. Dominant binding region (CDS vs 3′UTR) × ER/membrane-associated annotation proxy를
   함께 보면 ribosome density change 경향이 더 잘 설명되는가?

---

## Proxy definitions

| Proxy | Subclass columns included |
|---|---|
| `ER_membrane_core` | `is_ER_or_protein_folding` OR `is_membrane_or_transmembrane` OR `is_secretory_or_extracellular` OR `is_Golgi_or_trafficking` |
| `ER_membrane_broad` | `ER_membrane_core` OR `is_transporter_or_channel` OR `is_lysosome_or_endosome` |

> `is_receptor_or_signaling`은 proxy에 포함하지 않음.
> 이 column은 너무 넓으므로 별도 descriptive row로만 보고한다.

---

## Inputs

| File | Description |
|---|---|
| `results/tables/05_s5_with_binding_site_features.csv` | 기반 master table (16,465 transcripts) |
| `results/tables/04_candidate_functional_subclass_annotation.csv` | 56 candidate rows — verification 기준 |
| `results/tables/07_s3_binding_region_classification.csv` | Site-level binding region classification |

---

## Master table construction

### Step 1: SPEC04 rule-based annotation을 S5 전체에 재적용

- `05_s5_with_binding_site_features.csv` base (16,465 rows)
- SPEC04의 동일 SUBCLASSES keyword dict + SYM_PATTERNS으로 `Description` + `Gene Symbol` 컬럼에 적용
- Description null row 수를 보고
- Edem3 override: `NM_001039644` → `is_ER_or_protein_folding = True`
- `is_other_or_unclear`: 모든 is_* 컬럼이 False인 경우에만 True
- **Verification**: 56 candidate rows에서 재적용 결과와 SPEC04 annotation 비교
  - Discrepancy > 5 rows 이면 보고 후 중단

### Step 2: Dominant binding region 계산

- `07_s3_binding_region_classification.csv` site-level rows를 transcript별로 집계
- Valid regions: 5UTR / CDS / 3UTR (ncRNA / out_of_bounds 제외)
- Dominant region = 가장 site 수가 많은 region
- 동점 → 'tie'
- 해당 S3A binding site가 없는 transcript → 'none'
- 5UTR_site_count, CDS_site_count, 3UTR_site_count 컬럼 추가

### Step 3: Merge

```
df_master = df_base (16,465)
  + subclass booleans + ER_membrane_core + ER_membrane_broad
  + left join dominant_binding_region (S3A에 없는 tx → 'none')
  + high_confidence = (candidate_group == 'A_and_B_overlap')
```

### Analysis subsets

| Subset | Definition | Approx n |
|---|---|---|
| `ribo_sub` | Ribosome density change notna | ~5,701 |
| `s3a_sub` | dominant_binding_region != 'none' | ~6,523 |
| `main_sub` | s3a_sub ∩ ribo_sub | ~3,900 |

---

## Analysis design

### Analysis 1: Ribo change distribution — ER/membrane-associated annotation proxy

- Subset: `ribo_sub`
- Compare ER_membrane_core yes vs no: n, median, mean ribosome density change (log2)
- Also report ER_membrane_broad and is_receptor_or_signaling (descriptive only)
- Mann-Whitney U test: exploratory p-value only; effect direction 중심 해석

### Analysis 2: HC fraction — two denominators

- **Denominator A** — S5 전체 (`df_master`, 16,465)
  - ER_membrane_core yes/no별 high_confidence 비율
  - "전체 S5 transcript 중에서"
- **Denominator B** — S3A-bound transcript (`s3a_sub`, ~6,523)
  - ER_membrane_core yes/no별 high_confidence 비율
  - "최소 1개 이상의 LIN28A binding site를 가진 transcript 중에서"
- Fisher's exact test: exploratory p-value만 보고; n / HC fraction / effect direction 중심 해석

> **두 denominator의 의미 차이**:
> Denominator A는 S5에 포함된 모든 transcript 중 ER proxy와 HC annotation의 공존 빈도를 측정한다.
> Denominator B는 실제 LIN28A binding이 확인된 transcript 중에서 ER proxy가 HC 비율을 높이는지를 측정한다.
> Denominator B가 binding-mediated 효과에 더 적합하지만 선택 편향(binding이 있는 transcript 자체가 HC candidate 기준과 연동)에 주의해야 한다.

### Analysis 3: 2D summary — dominant binding region × ER_membrane_core

- Subset: `main_sub` (s3a_sub ∩ ribo_sub)
- Rows: dominant_binding_region (CDS / 3UTR / 5UTR / tie)
- Cols: ER_membrane_core yes / no
- Cell: n, median ribo change, mean ribo change, HC count, HC fraction
- n < 5인 cell은 통계 생략, "n too small" 표시

### Analysis 4: Exploratory OLS regression

- Subset: `main_sub`
- Outcome: Ribosome density change (log2)
- Predictors:
  - `mean_CLIP_enrichment`
  - `log1p(total_binding_site_count)`
  - `dominant_binding_region` (dummy; reference = 'CDS')
  - `ER_membrane_core` (0/1)
- Optional model 2: + `dominant_binding_region × ER_membrane_core` interaction term
- VIF 확인; multicollinearity 보고
- **해석 원칙**: coefficient direction + n 중심; p-value exploratory로만 보고
- S3A binding이 없는 transcript는 region-based regression에서 제외
  (sensitivity: 'none' category 포함 모델을 별도 보고)

---

## Expected outputs

### Tables

| File | Description |
|---|---|
| `results/tables/08_functional_context_master_table.csv` | Transcript-level master table |
| `results/tables/08_ribo_change_by_er_membrane_proxy.csv` | Ribo change summary by proxy group |
| `results/tables/08_hc_fraction_by_er_membrane_proxy.csv` | HC fraction — two denominators |
| `results/tables/08_binding_region_by_er_membrane_proxy_summary.csv` | 2D binding region × proxy summary |
| `results/tables/08_exploratory_regression_summary.csv` | Regression coefficient table |

### Figures

| File | Description |
|---|---|
| `results/figures/08_ribo_change_by_er_membrane_proxy.png` | Boxplot: ribo change by ER/membrane proxy |
| `results/figures/08_hc_fraction_by_er_membrane_proxy.png` | HC fraction bar chart (two denominators) |
| `results/figures/08_binding_region_er_proxy_interaction.png` | 2D summary heatmap |

### Notes

| File | Description |
|---|---|
| `notes/08_functional_context_proxy_interpretation.md` | Full interpretation |

### Notebook

| File | Description |
|---|---|
| `notebooks/06_functional_context_proxy_analysis.ipynb` | SPEC08 notebook |

---

## Limitations

1. ER/membrane-associated annotation proxy는 Description keyword matching 기반이므로
   실제 ER-localized translation을 직접 측정한 결과가 아니다.
2. 동일 transcript의 multiple binding sites는 독립적이지 않다 (site-level 분석 금지 이유).
3. SPEC04 keyword logic은 자동화된 rule-based annotation이며, 수동 검증 없이는
   annotation noise가 있을 수 있다.
4. HC subset은 n=48로 작으므로 regression/Fisher 결과를 주요 결론으로 사용하지 않는다.
5. Description null transcript (854/16,465)는 모두 `is_other_or_unclear=True`로 처리된다.

---

## Constraints

- 기존 SPEC01–07 결과 수정 금지
- raw BAM/FASTQ 재처리 금지
- 외부 데이터 추가 다운로드 금지
- git add/commit/push 금지
- 새 파일은 SPEC08 / notebook 06 / results/tables/08_* / results/figures/08_* / notes/08_* 로만
