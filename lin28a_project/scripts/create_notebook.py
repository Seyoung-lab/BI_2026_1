import nbformat as nbf

nb = nbf.v4.new_notebook()

# 1. Project setup and paths
cell_1_md = nbf.v4.new_markdown_cell("## 1. Project setup and paths")
cell_1_code = nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set paths
TABLE_S5_PATH = '../data/supplementary_tables/1-s2.0-S0092867412012342-mmc5.xls'
PROCESSED_DATA_PATH = '../data/processed/table_s5_cleaned.csv'
FIGURE_PATH = '../results/figures/03_clip_vs_ribosome_scatter.png'
TABLE_A_PATH = '../results/tables/03_direct_candidates_threshold_A.csv'
TABLE_B_PATH = '../results/tables/03_direct_candidates_threshold_B.csv'
""")

# 2. Load Table S5
cell_2_md = nbf.v4.new_markdown_cell("## 2. Load Table S5")
cell_2_code = nbf.v4.new_code_cell("""# Load Table S5
# skipping the first row because it contains a long text description
df = pd.read_excel(TABLE_S5_PATH, sheet_name=0, skiprows=1)
df.head()
""")

# 3. Inspect columns and missing values
cell_3_md = nbf.v4.new_markdown_cell("## 3. Inspect columns and missing values")
cell_3_code = nbf.v4.new_code_cell("""print(f"Shape: {df.shape}")
print("\\nColumns:")
print(list(df.columns))

print("\\nMissing values count:")
print(df.isnull().sum())
""")

# 4. Identify key columns
cell_4_md = nbf.v4.new_markdown_cell("## 4. Identify key columns")
cell_4_code = nbf.v4.new_code_cell("""# The key columns based on inspection:
# Transcript accession: 'Accession'
# Gene symbol: 'Gene'
# CLIP-seq p-value: 'CLIP p-value'
# CLIP-seq FDR: 'CLIP FDR'
# CLIP enrichment from each antibody: 'CLIP-35L33G', 'CLIP-let7g', 'CLIP-Mirlet7d', 'CLIP-Mirlet7f-1'
# Ribosome density change: 'Ribosome density change (siLin28a / siLuc)'
# RNA-seq mRNA change: 'RNA level change (siLin28a / siLuc)'
# Gene description: 'Description'

# Save the cleaned table without biological thresholds
df.to_csv(PROCESSED_DATA_PATH, index=False)
print(f"Saved cleaned table to {PROCESSED_DATA_PATH}")

# Now write to note file 
with open('../notes/table_s5_data_dictionary.md', 'w') as f:
    f.write("# Table S5 Data Dictionary\\n\\n")
    f.write("- **Accession**: Transcript accession\\n")
    f.write("- **Gene**: Gene symbol\\n")
    f.write("- **CLIP p-value**: CLIP-seq p-value\\n")
    f.write("- **CLIP FDR**: CLIP-seq False Discovery Rate\\n")
    f.write("- **CLIP-35L33G, CLIP-let7g, CLIP-Mirlet7d, CLIP-Mirlet7f-1**: CLIP enrichment from each antibody\\n")
    f.write("- **Ribosome density change...**: Ribosome density change after Lin28a knockdown\\n")
    f.write("- **RNA level change...**: RNA-seq mRNA change after Lin28a knockdown\\n")
    f.write("- **Description**: Gene description\\n")
""")

# 5. Calculate mean CLIP enrichment
cell_5_md = nbf.v4.new_markdown_cell("## 5. Calculate mean CLIP enrichment")
cell_5_code = nbf.v4.new_code_cell("""clip_enrichment_cols = ['CLIP-35L33G', 'CLIP-let7g', 'CLIP-Mirlet7d', 'CLIP-Mirlet7f-1']
# Convert columns to numeric, replacing non-numeric with NaN if any
for col in clip_enrichment_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['mean_CLIP_enrichment'] = df[clip_enrichment_cols].mean(axis=1)
print(df[['Gene', 'mean_CLIP_enrichment']].head())
""")

# 6. Inspect distributions
cell_6_md = nbf.v4.new_markdown_cell("## 6. Inspect distributions")
cell_6_code = nbf.v4.new_code_cell("""# Rename some long columns for ease of use
ribo_col = [col for col in df.columns if 'Ribosome' in col and 'change' in col][0]
rna_col = [col for col in df.columns if 'RNA' in col and 'change' in col][0]

df[ribo_col] = pd.to_numeric(df[ribo_col], errors='coerce')
df[rna_col] = pd.to_numeric(df[rna_col], errors='coerce')
df['CLIP FDR'] = pd.to_numeric(df['CLIP FDR'], errors='coerce')

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
sns.histplot(df['mean_CLIP_enrichment'].dropna(), bins=50, ax=axes[0, 0])
axes[0, 0].set_title('Mean CLIP Enrichment')

sns.histplot(df['CLIP FDR'].dropna(), bins=50, ax=axes[0, 1])
axes[0, 1].set_title('CLIP FDR')

sns.histplot(df[ribo_col].dropna(), bins=50, ax=axes[1, 0])
axes[1, 0].set_title('Ribosome Density Change')

sns.histplot(df[rna_col].dropna(), bins=50, ax=axes[1, 1])
axes[1, 1].set_title('RNA-seq mRNA Change')
plt.tight_layout()
plt.show()
""")

# 7. Compare threshold set A and B
cell_7_md = nbf.v4.new_markdown_cell("## 7. Compare threshold set A and B")
cell_7_code = nbf.v4.new_code_cell("""# Threshold set A:
# - CLIP FDR < 0.05
# - mean CLIP enrichment > 1
# - ribosome density change > 0
# - abs(mRNA change) < 0.5
cond_A = (df['CLIP FDR'] < 0.05) & \\
         (df['mean_CLIP_enrichment'] > 1) & \\
         (df[ribo_col] > 0) & \\
         (df[rna_col].abs() < 0.5)

# Threshold set B:
# - CLIP FDR < 0.05
# - mean CLIP enrichment in top 20%
# - ribosome density change > 0.3
# - abs(mRNA change) < 0.5
top20_clip = df['mean_CLIP_enrichment'].quantile(0.8)
cond_B = (df['CLIP FDR'] < 0.05) & \\
         (df['mean_CLIP_enrichment'] > top20_clip) & \\
         (df[ribo_col] > 0.3) & \\
         (df[rna_col].abs() < 0.5)

df_A = df[cond_A].copy()
df_B = df[cond_B].copy()

print(f"Threshold Set A selected {len(df_A)} transcripts, {df_A['Gene'].nunique()} unique genes.")
print(f"Threshold Set B selected {len(df_B)} transcripts, {df_B['Gene'].nunique()} unique genes.")

# Top 20 for A
print("\\nTop 20 candidates (Threshold A) by mean CLIP enrichment and ribosome density change:")
print(df_A.sort_values(by=['mean_CLIP_enrichment', ribo_col], ascending=[False, False])[['Gene', 'mean_CLIP_enrichment', ribo_col]].head(20))

# Top 20 for B
print("\\nTop 20 candidates (Threshold B) by mean CLIP enrichment and ribosome density change:")
print(df_B.sort_values(by=['mean_CLIP_enrichment', ribo_col], ascending=[False, False])[['Gene', 'mean_CLIP_enrichment', ribo_col]].head(20))
""")

# 8. Generate main scatter plot
cell_8_md = nbf.v4.new_markdown_cell("## 8. Generate main scatter plot")
cell_8_code = nbf.v4.new_code_cell("""# Scatter plot: x=mean CLIP enrichment, y=ribosome density change
# Color: small vs large mRNA abundance change (Threshold: abs(mRNA change) < 0.5)

df['mRNA_change_category'] = np.where(df[rna_col].abs() < 0.5, 'Small Change (< 0.5)', 'Large Change (>= 0.5)')
df['Direct Repression Candidate'] = np.where(cond_B, 'Candidate (Set B)', 'Not Candidate')

plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x='mean_CLIP_enrichment', y=ribo_col, hue='mRNA_change_category', style='Direct Repression Candidate', alpha=0.7)
plt.axhline(0, color='grey', linestyle='--')
plt.axvline(0, color='grey', linestyle='--')
plt.xlabel('Mean CLIP Enrichment')
plt.ylabel('Ribosome Density Change (siLin28a / siLuc)')
plt.title('CLIP Enrichment vs Ribosome Density Change')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(FIGURE_PATH, dpi=300)
plt.show()
""")

# 9. Save candidate tables
cell_9_md = nbf.v4.new_markdown_cell("## 9. Save candidate tables")
cell_9_code = nbf.v4.new_code_cell("""df_A.to_csv(TABLE_A_PATH, index=False)
df_B.to_csv(TABLE_B_PATH, index=False)
print("Saved candidate tables.")
""")

# 10. Summary and next steps
cell_10_md = nbf.v4.new_markdown_cell("## 10. Summary and next steps")
cell_10_code = nbf.v4.new_code_cell("""with open('../notes/03_threshold_summary.md', 'w') as f:
    f.write("# Threshold Summary\\n\\n")
    f.write("## Threshold Set A\\n")
    f.write(f"- Selected transcripts: {len(df_A)}\\n")
    f.write(f"- Unique genes: {df_A['Gene'].nunique()}\\n\\n")
    f.write("## Threshold Set B\\n")
    f.write(f"- Selected transcripts: {len(df_B)}\\n")
    f.write(f"- Unique genes: {df_B['Gene'].nunique()}\\n\\n")
    f.write("## Conclusion\\n")
    f.write("Set B applies a more stringent threshold for ribosome density change (>0.3) and selects the top 20% of CLIP enrichment, resulting in a more refined set of direct targets.\\n")

print("Created 03_threshold_summary.md")
""")

nb['cells'] = [
    cell_1_md, cell_1_code,
    cell_2_md, cell_2_code,
    cell_3_md, cell_3_code,
    cell_4_md, cell_4_code,
    cell_5_md, cell_5_code,
    cell_6_md, cell_6_code,
    cell_7_md, cell_7_code,
    cell_8_md, cell_8_code,
    cell_9_md, cell_9_code,
    cell_10_md, cell_10_code
]

with open('lin28a_project/notebooks/01_s5_direct_target_analysis.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook created successfully!")
