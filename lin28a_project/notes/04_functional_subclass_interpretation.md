# 04 Functional Subclass Interpretation

## High-confidence candidate set

- A∩B overlap candidates: **48 transcripts** (all unique genes, one transcript per gene)
- Source: Threshold A (FDR<0.05, mean CLIP>1, ribo>0, |mRNA|<0.5)
  ∩ Threshold B (FDR<0.05, mean CLIP>top 20%, ribo>0.3, |mRNA|<0.5)

---

## Subclass annotation method

Functional subclass labels were assigned using **rule-based keyword matching** on
the `Description` and `Gene Symbol` columns of `table_s5_cleaned.csv`.

**Important: subclass Boolean labels are NOT mutually exclusive.**
One transcript can belong to multiple subclasses simultaneously
(e.g., a membrane receptor is both `is_membrane_or_transmembrane` and `is_receptor_or_signaling`).
Therefore, the sum of subclass counts can exceed the number of candidate transcripts.

`is_other_or_unclear` is set to `True` **only when ALL other subclasses are False**.

The same annotation rules were applied to ALL transcripts in `table_s5_cleaned.csv`
to enable background comparison across:
1. All analyzable transcripts (n=16465)
2. LIN28A-bound transcripts (CLIP FDR < 0.05, n=266)
3. High-confidence candidates (A∩B, n=48)

---

## Subclass counts (high-confidence candidates, n=48)

| Subclass | Count | % of candidates |
|---|---|---|
| Other / unclear | 23 | 47.9% |
| ER / protein folding | 8 | 16.7% |
| Receptor / signaling | 8 | 16.7% |
| Membrane / transmembrane | 7 | 14.6% |
| Transporter / channel | 3 | 6.2% |
| Secretory / extracellular | 2 | 4.2% |
| Adhesion / ECM | 2 | 4.2% |
| Golgi / trafficking | 1 | 2.1% |
| Lysosome / endosome | 1 | 2.1% |

---

## Which subclasses are enriched in candidates vs. all analyzable transcripts?

| Subclass | HC fraction | All fraction | Enrichment ratio |
|---|---|---|---|
| ER / protein folding | 0.17 | 0.01 | 15.08x |
| Secretory / extracellular | 0.04 | 0.01 | 5.81x |
| Lysosome / endosome | 0.02 | 0.00 | 5.81x |
| Membrane / transmembrane | 0.15 | 0.03 | 5.03x |
| Adhesion / ECM | 0.04 | 0.01 | 3.33x |

---

## Consistency with the original paper's ER-associated translation model

The paper (Cho et al., Cell 2012) argues that LIN28A suppresses ER-associated translation
in mESCs. Table S6 shows the most significantly enriched GO terms in LIN28A CLIP targets are:
- "intrinsic to membrane" (FDR ~6e-149, RPF FDR 0)
- "endoplasmic reticulum part" (CLIP FDR ~4.3e-43, RPF FDR ~4.2e-77)
- "endoplasmic reticulum membrane" (CLIP FDR ~3.0e-29, RPF FDR ~1.9e-55)

The candidate genes in this analysis include several prominent ER-associated proteins
(e.g., Canx/calnexin, Dnajb11, Tmx1, Mfsd1, Pgrmc1), consistent with this model.
The fraction comparison plot (Figure 04-2) shows whether ER/membrane/secretory categories
are enriched in high-confidence candidates relative to the background.

---

## Limitations

1. **Annotation is rule-based and preliminary.** Keywords matched in `Description` or
   `Gene Symbol` do not guarantee correct biological subclass assignment.
2. **This does not prove direct biological function.** These are candidate translational
   repression targets based on CLIP enrichment and ribosome density change.
3. **Data are from mESCs**, not cancer or differentiated cells.
4. **Table S6 is GO-level**, not gene-level; it cannot be used to assign GO terms to
   individual transcripts in this candidate list.
5. **Subclasses are not mutually exclusive.** Fraction sums across subclasses exceed 1.

---

## Suggested next steps (not executed in this spec)

1. **Binding-site position analysis (Spec 05):** Use Table S3 (if available) or BAM-level
   CLIP data to determine whether LIN28A binds 5'UTR, CDS, or 3'UTR of top candidates.
2. **BAM-level validation:** Check CLIP read coverage for top candidates (e.g., Pgrmc1,
   Tmx1, Slc30a1) using the provided `CLIP-35L33G.bam` file.

---

## Annotation patch (2026-05-28): Edem3 ER reclassification

### What changed

`Edem3` (NM_001039644) was reclassified:
- `is_ER_or_protein_folding`: `False` → **`True`**
- `is_other_or_unclear`: `True` → **`False`**

### Why

The `Description` column for Edem3 is:
> "ER degradation-enhancing alpha-mannosidase-like"

The keyword `'ER'` is explicitly present, but the regex pattern `' er '`
(with surrounding spaces) did not match because `ER` appears at the start
of the matched text without a leading space — a keyword matching bug.

This was identified via `04_unclear_candidate_review.md` (Level A evidence).

### Why Level B candidates remain unclear

The 12 Level B candidates (e.g., Hsp90b1, Ppib, Sel1l, Mfsd1, Tmem57 …) were
reviewed from Description/Gene Symbol text only. Their descriptions do not contain
an exact keyword from the current subclass rule list. Reclassifying them would
require either (a) expanding the keyword list with new terms (a policy decision)
or (b) using domain knowledge / external databases — which is out of scope for
this rule-based annotation step. They are intentionally kept as `is_other_or_unclear`.

### Files updated by this patch

- `results/tables/04_candidate_functional_subclass_annotation.csv`
- `results/tables/04_candidate_annotation_manual_review.csv`
- `results/tables/04_subclass_fraction_summary.csv`
- `results/tables/04_high_confidence_candidates_for_spec05.csv`
- `results/figures/04_high_confidence_subclass_counts.png`
- `results/figures/04_subclass_fraction_comparison.png`
- `results/figures/04_ribosome_change_by_subclass.png`

### Files preserved (not modified)

- `results/tables/04_unclear_candidates_for_review.csv`
- `notes/04_unclear_candidate_review.md`
