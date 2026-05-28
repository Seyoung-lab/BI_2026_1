# 05 Binding-Site Analysis Interpretation

## Dataset used

- **Table S3A**: 65534 binding-site records, 6606 unique transcripts
- **Table S5 (all)**: 16465 transcripts
- Transcripts in S5 with ≥1 binding site: 6603 / 16465 (40.1%)
- High-confidence candidates (A∩B, n=48) with ≥1 binding site: 35 / 48 (72.9%)

## Binding-site features aggregated

Per transcript from Table S3A:
- `binding_site_count`, `has_binding_site`
- `n_sites_detected_2plus_libraries`, `n_sites_detected_3_libraries`
- `max_detected_libraries`, `mean_detected_libraries`
- depth: max/mean for each of 35L33G, 2J3, polyclonal (NaN excluded in aggregation)
- entropy score: max/mean for each of 35L33G, 2J3, polyclonal (NaN excluded)

Transcripts absent from S3A assigned `binding_site_count = 0`, `has_binding_site = False`.

## Do high-confidence candidates have more binding sites?

High-confidence candidates have 21.62 binding sites
on average vs 3.90
for Non-candidates. 72.9% of HC candidates have ≥1 binding site.

## Binding-site count vs ribosome density change

Spearman ρ = 0.0037  (p = 7.813e-01, n = 5649)
(among transcripts with binding sites only: ρ = 0.0137, p = 3.889e-01, n = 3976)

## Binding-site burden categories

| Category | n (total) | median ribo Δ | mean ribo Δ |
|---|---|---|---|
| 0_sites | 9862 | -0.295 | -0.277 |
| 1_site | 1039 | -0.372 | -0.328 |
| 2_to_3_sites | 1288 | -0.353 | -0.341 |
| 4_or_more_sites | 4276 | -0.282 | -0.275 |

## Binding-position analysis

Not performed. Table S3A does not contain 5'UTR/CDS/3'UTR region annotations.
See `notes/05_binding_position_unavailable_note.md`.

## Limitations

1. **Table S3A is already processed data.** Binding sites represent detected crosslinking
   events above a threshold; very low-coverage sites may be absent.
2. **Transcript ID matching** is direct NM_ accession matching; any version-suffix
   discrepancy would reduce the match rate silently.
3. **Transcripts absent from S3A** are assigned binding_site_count = 0, but this
   includes transcripts that may have been excluded from S3A due to low read counts
   (not necessarily LIN28A-unbound).
4. **Binding-site count does not prove causality.** Higher binding site burden may
   reflect LIN28A binding density but does not directly demonstrate translational
   repression.
5. **Region analysis is not available** from Table S3 alone.

## Recommended next steps

1. **BAM-level validation** for top candidates (Pgrmc1, Ktn1, Pvrl3) using
   `CLIP-35L33G.bam` — visualize CLIP read coverage at the transcript level.
2. **Binding-position analysis** using `gencode.vM27.annotation.gtf.gz` to map
   `Position` offsets to 5'UTR / CDS / 3'UTR regions.
3. **let-7 control analysis** — compare binding-site features between direct
   translational repression candidates and let-7 pathway targets.

---

## Sensitivity check: zero-inflated background

Transcripts absent from Table S3A are assigned `binding_site_count = 0`.
Because background (Not_candidate) transcripts are largely absent from S3A,
including zero-count transcripts inflates the apparent difference between
candidate and background groups.

**Non-zero subset** (`binding_site_count > 0`): 6603 / 16465 S5 transcripts (40.1%)

| Candidate group | n (≥1 site) | total n | % with binding site | median count |
|---|---|---|---|---|
| Not_candidate | 6561 | 16409 | 40.0% | 6.0 |
| A_only | 7 | 8 | 87.5% | 40.0 |
| B_only | 0 | 0 | nan% | nan |
| A_and_B_overlap | 35 | 48 | 72.9% | 25.0 |

**Interpretation**: Even when restricting to transcripts with ≥1 binding site,
A∩B high-confidence candidates show a substantially higher median binding-site count
than background transcripts.
The enrichment is not an artifact of zero-inflation alone.

Output files:
- `results/tables/05_binding_site_count_by_candidate_group_nonzero_summary.csv`
- `results/figures/05_binding_site_count_by_candidate_group_nonzero.png`
