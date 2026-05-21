import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

TABLE_S5_PATH = '../data/supplementary_tables/1-s2.0-S0092867412012342-mmc5.xls'
PROCESSED_DATA_PATH = '../data/processed/table_s5_cleaned.csv'
FIGURE_PATH = '../results/figures/03_clip_vs_ribosome_scatter.png'
TABLE_A_PATH = '../results/tables/03_direct_candidates_threshold_A.csv'
TABLE_B_PATH = '../results/tables/03_direct_candidates_threshold_B.csv'
SUMMARY_PATH = '../notes/03_threshold_summary.md'

print("Loading cleaned table...")
df = pd.read_csv(PROCESSED_DATA_PATH)

# Set columns
clip_enrichment_cols = ['CLIP-seq enrichment (35L33G, log2)', 'CLIP-seq enrichment (2J3, log2)', 'CLIP-seq enrichment (polyclonal, log2)']
ribo_col = 'Ribosome density change (log2)'
rna_col = 'RNA-seq mRNA change upon Lin28a KD (log2)'

for col in clip_enrichment_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df['mean_CLIP_enrichment'] = df[clip_enrichment_cols].mean(axis=1)

df[ribo_col] = pd.to_numeric(df[ribo_col], errors='coerce')
df[rna_col] = pd.to_numeric(df[rna_col], errors='coerce')
df['CLIP-seq FDR'] = pd.to_numeric(df['CLIP-seq FDR'], errors='coerce')

# Threshold set A:
# - CLIP FDR < 0.05
# - mean CLIP enrichment > 1
# - ribosome density change > 0
# - abs(mRNA change) < 0.5
cond_A = (df['CLIP-seq FDR'] < 0.05) & \
         (df['mean_CLIP_enrichment'] > 1) & \
         (df[ribo_col] > 0) & \
         (df[rna_col].abs() < 0.5)

# Threshold set B:
# - CLIP FDR < 0.05
# - mean CLIP enrichment in top 20%
# - ribosome density change > 0.3
# - abs(mRNA change) < 0.5
top20_clip = df['mean_CLIP_enrichment'].quantile(0.8)
cond_B = (df['CLIP-seq FDR'] < 0.05) & \
         (df['mean_CLIP_enrichment'] > top20_clip) & \
         (df[ribo_col] > 0.3) & \
         (df[rna_col].abs() < 0.5)

df_A = df[cond_A].copy()
df_B = df[cond_B].copy()

# Ensure destination directories exist
os.makedirs(os.path.dirname(TABLE_A_PATH), exist_ok=True)
os.makedirs(os.path.dirname(FIGURE_PATH), exist_ok=True)
os.makedirs(os.path.dirname(SUMMARY_PATH), exist_ok=True)

df_A.to_csv(TABLE_A_PATH, index=False)
df_B.to_csv(TABLE_B_PATH, index=False)
print("Saved candidate tables.")

# Generate Scatter Plot
df['mRNA_change_category'] = np.where(df[rna_col].abs() < 0.5, 'Small Change (< 0.5)', 'Large Change (>= 0.5)')
df['Direct Repression Candidate'] = np.where(cond_B, 'Candidate (Set B)', 'Not Candidate')

plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x='mean_CLIP_enrichment', y=ribo_col, hue='mRNA_change_category', style='Direct Repression Candidate', alpha=0.7)
plt.axhline(0, color='grey', linestyle='--')
plt.axvline(0, color='grey', linestyle='--')
plt.xlabel('Mean CLIP Enrichment (35L33G, 2J3, polyclonal)')
plt.ylabel('Ribosome Density Change (log2)')
plt.title('CLIP Enrichment vs Ribosome Density Change')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(FIGURE_PATH, dpi=300)
print(f"Saved figure to {FIGURE_PATH}")

# Summary
with open(SUMMARY_PATH, 'w') as f:
    f.write("# Threshold Summary\n\n")
    f.write("## Threshold Set A\n")
    f.write(f"- Selected transcripts: {len(df_A)}\n")
    f.write(f"- Unique genes: {df_A['Gene Symbol'].nunique()}\n\n")
    f.write("## Threshold Set B\n")
    f.write(f"- Selected transcripts: {len(df_B)}\n")
    f.write(f"- Unique genes: {df_B['Gene Symbol'].nunique()}\n\n")
    f.write("## Conclusion\n")
    f.write("Set B applies a more stringent threshold for ribosome density change (>0.3) and selects the top 20% of CLIP enrichment, resulting in a more refined set of direct targets.\n")

print("Created 03_threshold_summary.md")

# Output to console
print(f"\n[Threshold Set A]\nTranscripts: {len(df_A)}\nUnique Genes: {df_A['Gene Symbol'].nunique()}")
print(f"\n[Threshold Set B]\nTranscripts: {len(df_B)}\nUnique Genes: {df_B['Gene Symbol'].nunique()}")
