# 08 Functional Context Proxy Analysis Interpretation

## 1. Proxy definition and scope

ER/membrane-associated annotation proxies are defined by keyword matching on the RefSeq
`Description` field (same logic as SPEC04). They represent protein functional context
inferred from annotation, NOT direct ER-localized translation measurements.

- `ER_membrane_core`: is_ER_or_protein_folding | is_membrane_or_transmembrane |
                       is_secretory_or_extracellular | is_Golgi_or_trafficking
- `ER_membrane_broad`: core | is_transporter_or_channel | is_lysosome_or_endosome
- `is_receptor_or_signaling`: reported separately (too broad for core/broad proxy)

**Description null rows**: 854 / 16465 — all assigned `is_other_or_unclear=True`.
**Edem3 override** (NM_001039644): `is_ER_or_protein_folding=True` (keyword 'endoplasmic reticulum'
misses the abbreviation "ER " at description start).

## 2. SPEC04 verification

Re-applied keyword logic matched SPEC04 annotation for 55 / 56 candidate transcripts.
Discrepancies: 1 transcripts.

## 3. Analysis subsets

| Subset | n | Description |
|---|---|---|
| df_master | 16465 | All S5 transcripts |
| ribo_sub | 5701 | With ribosome density data |
| s3a_sub | 6437 | With ≥1 S3A binding site (dominant region available) |
| main_sub | 3974 | s3a_sub ∩ ribo_sub (primary analysis subset) |

## 4. Analysis 1 — Ribo change by ER/membrane-associated annotation proxy

**ER_membrane_core** (ribo_sub, n=5701):
- yes (n=341): median ribo = +0.129
- no  (n=5360): median ribo = -0.314
- Mann-Whitney U (one-sided, greater): p = 0.0000 (exploratory)

**Interpretation**: The direction of effect (whether ER/membrane-associated annotation proxy
transcripts show more positive or negative ribosome density change upon Lin28a KD) should
be interpreted as exploratory and hypothesis-generating only. The magnitude of the
difference and the effect direction are the primary reporting metrics; p-value is
secondary given the large n and the annotation proxy nature of the grouping.

## 5. Analysis 2 — HC fraction (two denominators)

**Why two denominators?**

Denominator A (S5 total): measures co-occurrence of ER/membrane-associated annotation and HC
annotation status across the full S5 universe. This denominator includes transcripts with
no LIN28A binding evidence, so it tests whether the functional context is broadly associated
with HC status independent of binding.

Denominator B (S3A-bound): restricts to transcripts that have at least one detected LIN28A
binding site. This is more directly relevant to binding-mediated effects, but carries a
selection bias: the S3A-bound transcript population is already enriched for CLIP signal,
which overlaps with HC criteria.

| Proxy / Denominator | Proxy=yes HC% | Proxy=no HC% |
|---|---|---|
| ER_membrane_core / S5_total | 1.8% (n=16/910) | 0.2% (n=32/15555) |
| ER_membrane_core / S3A_bound | 4.1% (n=11/271) | 0.4% (n=23/6166) |

## 6. Analysis 3 — 2D summary (dominant region × ER proxy)

Subset: main_sub (s3a_sub ∩ ribo_sub).
Cells with n < 5 are flagged as "n too small" and excluded from quantitative interpretation.

Key patterns to note (if observed):
- Whether CDS-dominant + ER proxy = yes shows higher ribo Δ than CDS-dominant + no
- Whether 3′UTR-dominant transcripts show differential ER proxy effect
- These are exploratory observations; no causal inference is warranted.

## 7. Analysis 4 — Exploratory regression

Regression subset: main_sub (S3A-bound ∩ ribo data, dominant region ∈ CDS/3UTR/5UTR/tie).
Sensitivity analysis includes dominant_binding_region='none' (all ribo_sub).

**Interpretation principle**: Coefficient direction (positive/negative) and sample size are
the primary metrics. p-values are not used to claim significance. The low explained variance
(expected R² < 0.1 given the noisy biological data) is not itself a negative finding.

Predictors were chosen a priori based on biological hypotheses:
- mean_CLIP_enrichment: proxy for LIN28A binding affinity
- log1p(binding_site_count): proxy for binding site burden
- dominant_binding_region: site topology
- ER_membrane_core: functional context proxy

VIF > 5 would indicate problematic multicollinearity; VIF < 3 is acceptable.

## 8. Limitations

1. ER/membrane-associated annotation proxy is keyword-based; it is NOT a direct measurement
   of ER-localized translation. Avoid stating "ER-localized mRNA" as a conclusion.
2. HC subset (n=48) is too small for reliable regression or Fisher p-value interpretation.
   Effect direction and n should be the primary metrics.
3. Dominant binding region for S3A-unbound transcripts is 'none'; these are excluded from
   region-based regression (main_sub). Sensitivity analysis includes them.
4. The same functional annotation proxy may be associated with both higher CLIP enrichment
   (correlated predictor) and higher HC fraction, creating collinearity in regression.
5. Analysis 2 Denominator B has selection bias: S3A-bound transcripts are already enriched
   for features that define HC candidates (CLIP enrichment, ribo change).

## 9. Conclusion

Functional context (ER/membrane-associated annotation proxy) may contribute to the
pattern of LIN28A-associated translational derepression, but direct causal interpretation
is not warranted. These results are exploratory and should inform future hypothesis-driven
experiments rather than standalone conclusions.
