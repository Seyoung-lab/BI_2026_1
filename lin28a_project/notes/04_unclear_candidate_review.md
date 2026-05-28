# 04 Unclear Candidate Review

## Purpose

This note reviews the 23 high-confidence candidates (A∩B overlap)
classified as `is_other_or_unclear == True` by the rule-based annotation in Spec 04.

Review is based **solely on Description and Gene Symbol text** — no external
database queries, BLAST, or InterProScan were used.

Ambiguous genes are kept as `unclear`. Only cases where the description text
directly contains a missed keyword (evidence level A) are flagged for reclassification.

## Evidence levels

| Level | Meaning | Action |
|---|---|---|
| A | Description text clearly contains a functional keyword that was missed by regex | **Recommend reclassification** |
| B | Description suggests a likely subclass but requires interpretation beyond text matching | Keep as unclear; note for future manual review |
| C | Description is uninformative — no functional subclass signal | Keep as unclear |

---

## Level A — Keyword matching gap (recommend reclassify)

These genes have a recognizable keyword in their Description that our regex failed to capture. The annotation rules should have caught them. Recommend updating the keyword list or manually setting the subclass flag.

| Gene Symbol | mean_CLIP | ribo Δ | mRNA Δ | Description | Note |
|---|---|---|---|---|---|
| Edem3 | 2.408 | 0.626 | -0.249 | ER degradation-enhancing alpha-mannosidase-like | "ER degradation-enhancing alpha-mannosidase-like" — "ER" is explicitly present i |

---

## Level B — Suggestive description (keep unclear)

These genes have descriptions that imply a functional category based on domain knowledge, but do not contain an exact keyword match. Kept as unclear; listed here for optional future manual review.

| Gene Symbol | mean_CLIP | ribo Δ | mRNA Δ | Description | Note |
|---|---|---|---|---|---|
| Ktn1 | 2.913 | 0.605 | -0.399 | kinectin | "kinectin" — cytoplasmic face of rough ER in published literature, but descripti |
| Mfsd1 | 2.512 | 0.961 | -0.443 | major facilitator superfamily domain-containing | "major facilitator superfamily domain-containing" — MFS (major facilitator super |
| Zmpste24 | 2.417 | 0.344 | -0.151 | CAAX prenyl protease 1 homolog | "CAAX prenyl protease 1 homolog" — CAAX motif processing occurs at ER/inner nucl |
| Manf | 2.307 | 0.367 | -0.120 | mesencephalic astrocyte-derived neurotrophic factor precursor | "mesencephalic astrocyte-derived neurotrophic factor precursor" — "precursor" ma |
| Serinc1 | 2.288 | 0.735 | -0.147 | serine incorporator 1 precursor | "serine incorporator 1 precursor" — SERINC family proteins are multi-pass membra |
| Hsp90b1 | 2.264 | 0.853 | -0.311 | endoplasmin precursor | "endoplasmin precursor" — Endoplasmin is the common name for GRP94, an Hsp90-fam |
| Tmem57 | 2.210 | 0.490 | -0.432 | macoilin | "macoilin" — common name for a multi-pass transmembrane protein, but "macoilin"  |
| Mia3 | 2.186 | 0.841 | -0.105 | melanoma inhibitory activity protein 3 precursor | "melanoma inhibitory activity protein 3 precursor" — MIA3/TANGO1 mediates collag |
| Ppib | 2.030 | 0.585 | -0.473 | peptidyl-prolyl cis-trans isomerase B precursor | "peptidyl-prolyl cis-trans isomerase B precursor" — cyclophilin B, an ER-residen |
| Tmem30a | 1.959 | 1.181 | 0.206 | cell cycle control protein 50A | "cell cycle control protein 50A" — alternative name for TMEM30A/CDC50A, a transm |
| Sel1l | 1.958 | 0.449 | 0.070 | protein sel-1 homolog 1 isoform a | "protein sel-1 homolog 1 isoform a" — SEL1L is a key ER-associated degradation ( |
| Ccdc47 | 1.948 | 0.547 | -0.386 | coiled-coil domain-containing protein 47 precursor | "coiled-coil domain-containing protein 47 precursor" — CCDC47 is an ER transmemb |

---

## Level C — Uninformative description (keep unclear)

These genes have descriptions that give no functional subclass signal (e.g., "protein FAM18B1", generic domain names, or metabolic enzymes without pathway-level keywords). Keep as unclear.

| Gene Symbol | mean_CLIP | ribo Δ | mRNA Δ | Description | Note |
|---|---|---|---|---|---|
| Yipf4 | 2.566 | 0.845 | -0.038 | protein YIPF4 | "protein YIPF4" — description is uninformative. Cannot assign subclass from desc |
| Acsl3 | 2.433 | 0.375 | -0.466 | long-chain-fatty-acid--CoA ligase 3 isoform a | "long-chain-fatty-acid--CoA ligase 3 isoform a" — acyl-CoA synthetase, lipid met |
| Impad1 | 2.429 | 0.880 | -0.259 | inositol monophosphatase 3 | "inositol monophosphatase 3" — phosphatase, inositol metabolism. No subclass key |
| Ppp1r15b | 2.277 | 0.792 | -0.239 | protein phosphatase 1 regulatory subunit 15B | "protein phosphatase 1 regulatory subunit 15B" — phosphatase regulatory protein. |
| Ndufa5 | 2.215 | 0.488 | -0.015 | NADH dehydrogenase [ubiquinone] 1 alpha subcomplex subunit 5 | "NADH dehydrogenase [ubiquinone] 1 alpha subcomplex subunit 5" — mitochondrial C |
| Hsd17b11 | 2.178 | 0.839 | -0.208 | estradiol 17-beta-dehydrogenase 11 | "estradiol 17-beta-dehydrogenase 11" — ER-resident lipid-metabolizing enzyme, bu |
| Sptlc2 | 2.153 | 0.569 | -0.336 | serine palmitoyltransferase 2 | "serine palmitoyltransferase 2" — ER-membrane enzyme for sphingolipid biosynthes |
| Hmgcr | 1.999 | 0.421 | -0.311 | 3-hydroxy-3-methylglutaryl-coenzyme A reductase | "3-hydroxy-3-methylglutaryl-coenzyme A reductase" — HMG-CoA reductase, ER membra |
| Fam18b | 1.985 | 1.046 | -0.448 | protein FAM18B1 | "protein FAM18B1" — uninformative description. Cannot assign subclass from descr |
| Elmod2 | 1.964 | 0.703 | -0.004 | ELMO domain-containing protein 2 | "ELMO domain-containing protein 2" — ELMO domain is involved in Arf GTPase regul |

---

## Summary

| Level | n | Action |
|---|---|---|
| A — recommend reclassify | 1 | Edem3: add `is_ER_or_protein_folding = True` |
| B — suggestive, keep unclear | 12 | No change; note candidates |
| C — uninformative | 10 | No change |
| **Total unclear reviewed** | **23** | |

## Important notes

- `is_other_or_unclear` is `True` only when ALL other subclass Boolean columns are `False`.
  Reclassifying Edem3 would flip its `is_other_or_unclear` to `False`.
- Existing annotation tables (`04_candidate_annotation_manual_review.csv`,
  `04_candidate_functional_subclass_annotation.csv`) were NOT modified.
- If Level A recommendations are accepted, update the annotation tables
  or add `'er '` / `'^er '` to the ER keyword list and re-run Step 4.

## Output files

- `results/tables/04_unclear_candidates_for_review.csv`
- `notes/04_unclear_candidate_review.md` (this file)
