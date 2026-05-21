import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Project setup and paths"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import os\n",
    "\n",
    "# Set paths\n",
    "TABLE_S5_PATH = '../data/supplementary_tables/1-s2.0-S0092867412012342-mmc5.xls'\n",
    "PROCESSED_DATA_PATH = '../data/processed/table_s5_cleaned.csv'\n",
    "FIGURE_PATH = '../results/figures/03_clip_vs_ribosome_scatter.png'\n",
    "TABLE_A_PATH = '../results/tables/03_direct_candidates_threshold_A.csv'\n",
    "TABLE_B_PATH = '../results/tables/03_direct_candidates_threshold_B.csv'\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Load Table S5"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load Table S5\n",
    "# skipping the first row because it contains a long text description\n",
    "df = pd.read_excel(TABLE_S5_PATH, sheet_name=0, skiprows=1)\n",
    "df.head()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Inspect columns and missing values"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(f\"Shape: {df.shape}\")\n",
    "print(\"\\nColumns:\")\n",
    "print(list(df.columns))\n",
    "\n",
    "print(\"\\nMissing values count:\")\n",
    "print(df.isnull().sum())\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Identify key columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# The key columns based on inspection:\n",
    "# Transcript accession: 'Accession'\n",
    "# Gene symbol: 'Gene Symbol'\n",
    "# CLIP-seq p-value: 'CLIP-seq p-value'\n",
    "# CLIP-seq FDR: 'CLIP-seq FDR'\n",
    "# CLIP enrichment from each antibody: 'CLIP-seq enrichment (35L33G, log2)', 'CLIP-seq enrichment (2J3, log2)', 'CLIP-seq enrichment (polyclonal, log2)'\n",
    "# Ribosome density change: 'Ribosome density change (log2)'\n",
    "# RNA-seq mRNA change: 'RNA-seq mRNA change upon Lin28a KD (log2)'\n",
    "# Gene description: 'Description'\n",
    "\n",
    "# Save the cleaned table without biological thresholds\n",
    "df.to_csv(PROCESSED_DATA_PATH, index=False)\n",
    "print(f\"Saved cleaned table to {PROCESSED_DATA_PATH}\")\n",
    "\n",
    "# Write to note file\n",
    "with open('../notes/table_s5_data_dictionary.md', 'w') as f:\n",
    "    f.write(\"# Table S5 Data Dictionary\\n\\n\")\n",
    "    f.write(\"- **Accession**: Transcript accession\\n\")\n",
    "    f.write(\"- **Gene Symbol**: Gene symbol\\n\")\n",
    "    f.write(\"- **CLIP-seq p-value**: CLIP-seq p-value\\n\")\n",
    "    f.write(\"- **CLIP-seq FDR**: CLIP-seq False Discovery Rate\\n\")\n",
    "    f.write(\"- **CLIP-seq enrichment (35L33G, log2), CLIP-seq enrichment (2J3, log2), CLIP-seq enrichment (polyclonal, log2)**: CLIP enrichment from each antibody\\n\")\n",
    "    f.write(\"- **Ribosome density change (log2)**: Ribosome density change after Lin28a knockdown\\n\")\n",
    "    f.write(\"- **RNA-seq mRNA change upon Lin28a KD (log2)**: RNA-seq mRNA change after Lin28a knockdown\\n\")\n",
    "    f.write(\"- **Description**: Gene description\\n\")\n",
    "\n",
    "print(\"Saved data dictionary to notes/table_s5_data_dictionary.md\")\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Calculate mean CLIP enrichment"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "clip_enrichment_cols = ['CLIP-seq enrichment (35L33G, log2)', 'CLIP-seq enrichment (2J3, log2)', 'CLIP-seq enrichment (polyclonal, log2)']\n",
    "# Convert columns to numeric, replacing non-numeric with NaN if any\n",
    "for col in clip_enrichment_cols:\n",
    "    df[col] = pd.to_numeric(df[col], errors='coerce')\n",
    "\n",
    "df['mean_CLIP_enrichment'] = df[clip_enrichment_cols].mean(axis=1)\n",
    "print(df[['Gene Symbol', 'mean_CLIP_enrichment']].head())\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Inspect distributions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Set column names explicitly based on the validated mappings\n",
    "ribo_col = 'Ribosome density change (log2)'\n",
    "rna_col = 'RNA-seq mRNA change upon Lin28a KD (log2)'\n",
    "\n",
    "df[ribo_col] = pd.to_numeric(df[ribo_col], errors='coerce')\n",
    "df[rna_col] = pd.to_numeric(df[rna_col], errors='coerce')\n",
    "df['CLIP-seq FDR'] = pd.to_numeric(df['CLIP-seq FDR'], errors='coerce')\n",
    "\n",
    "fig, axes = plt.subplots(2, 2, figsize=(12, 10))\n",
    "sns.histplot(df['mean_CLIP_enrichment'].dropna(), bins=50, ax=axes[0, 0])\n",
    "axes[0, 0].set_title('Mean CLIP Enrichment')\n",
    "\n",
    "sns.histplot(df['CLIP-seq FDR'].dropna(), bins=50, ax=axes[0, 1])\n",
    "axes[0, 1].set_title('CLIP-seq FDR')\n",
    "\n",
    "sns.histplot(df[ribo_col].dropna(), bins=50, ax=axes[1, 0])\n",
    "axes[1, 0].set_title('Ribosome Density Change')\n",
    "\n",
    "sns.histplot(df[rna_col].dropna(), bins=50, ax=axes[1, 1])\n",
    "axes[1, 1].set_title('RNA-seq mRNA Change')\n",
    "plt.tight_layout()\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7. Compare threshold set A and B"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Threshold set A:\n",
    "# - CLIP-seq FDR < 0.05\n",
    "# - mean CLIP enrichment > 1\n",
    "# - ribosome density change > 0\n",
    "# - abs(mRNA change) < 0.5\n",
    "cond_A = (df['CLIP-seq FDR'] < 0.05) & \\\n",
    "         (df['mean_CLIP_enrichment'] > 1) & \\\n",
    "         (df[ribo_col] > 0) & \\\n",
    "         (df[rna_col].abs() < 0.5)\n",
    "\n",
    "# Threshold set B:\n",
    "# - CLIP-seq FDR < 0.05\n",
    "# - mean CLIP enrichment in top 20%\n",
    "# - ribosome density change > 0.3\n",
    "# - abs(mRNA change) < 0.5\n",
    "top20_clip = df['mean_CLIP_enrichment'].quantile(0.8)\n",
    "cond_B = (df['CLIP-seq FDR'] < 0.05) & \\\n",
    "         (df['mean_CLIP_enrichment'] > top20_clip) & \\\n",
    "         (df[ribo_col] > 0.3) & \\\n",
    "         (df[rna_col].abs() < 0.5)\n",
    "\n",
    "df_A = df[cond_A].copy()\n",
    "df_B = df[cond_B].copy()\n",
    "\n",
    "print(f\"Threshold Set A selected {len(df_A)} transcripts, {df_A['Gene Symbol'].nunique()} unique genes.\")\n",
    "print(f\"Threshold Set B selected {len(df_B)} transcripts, {df_B['Gene Symbol'].nunique()} unique genes.\")\n",
    "\n",
    "# Top 20 for A\n",
    "print(\"\\nTop 20 candidates (Threshold A) by mean CLIP enrichment and ribosome density change:\")\n",
    "print(df_A.sort_values(by=['mean_CLIP_enrichment', ribo_col], ascending=[False, False])[['Gene Symbol', 'mean_CLIP_enrichment', ribo_col]].head(20))\n",
    "\n",
    "# Top 20 for B\n",
    "print(\"\\nTop 20 candidates (Threshold B) by mean CLIP enrichment and ribosome density change:\")\n",
    "print(df_B.sort_values(by=['mean_CLIP_enrichment', ribo_col], ascending=[False, False])[['Gene Symbol', 'mean_CLIP_enrichment', ribo_col]].head(20))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 8. Generate main scatter plot"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Scatter plot: x=mean CLIP enrichment, y=ribosome density change\n",
    "# Color: small vs large mRNA abundance change (Threshold: abs(mRNA change) < 0.5)\n",
    "\n",
    "df['mRNA_change_category'] = np.where(df[rna_col].abs() < 0.5, 'Small Change (< 0.5)', 'Large Change (>= 0.5)')\n",
    "df['Direct Repression Candidate'] = np.where(cond_B, 'Candidate (Set B)', 'Not Candidate')\n",
    "\n",
    "plt.figure(figsize=(10, 8))\n",
    "sns.scatterplot(data=df, x='mean_CLIP_enrichment', y=ribo_col, hue='mRNA_change_category', style='Direct Repression Candidate', alpha=0.7)\n",
    "plt.axhline(0, color='grey', linestyle='--')\n",
    "plt.axvline(0, color='grey', linestyle='--')\n",
    "plt.xlabel('Mean CLIP Enrichment (35L33G, 2J3, polyclonal)')\n",
    "plt.ylabel('Ribosome Density Change (log2)')\n",
    "plt.title('CLIP Enrichment vs Ribosome Density Change')\n",
    "plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')\n",
    "plt.tight_layout()\n",
    "plt.savefig(FIGURE_PATH, dpi=300)\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 9. Save candidate tables"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_A.to_csv(TABLE_A_PATH, index=False)\n",
    "df_B.to_csv(TABLE_B_PATH, index=False)\n",
    "print(\"Saved candidate tables.\")\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 10. Summary and next steps"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "with open('../notes/03_threshold_summary.md', 'w') as f:\n",
    "    f.write(\"# Threshold Summary\\n\\n\")\n",
    "    f.write(\"## Threshold Set A\\n\")\n",
    "    f.write(f\"- Selected transcripts: {len(df_A)}\\n\")\n",
    "    f.write(f\"- Unique genes: {df_A['Gene Symbol'].nunique()}\\n\\n\")\n",
    "    f.write(\"## Threshold Set B\\n\")\n",
    "    f.write(f\"- Selected transcripts: {len(df_B)}\\n\")\n",
    "    f.write(f\"- Unique genes: {df_B['Gene Symbol'].nunique()}\\n\\n\")\n",
    "    f.write(\"## Conclusion\\n\")\n",
    "    f.write(\"Set B applies a more stringent threshold for ribosome density change (>0.3) and selects the top 20% of CLIP enrichment, resulting in a more refined set of direct targets.\\n\")\n",
    "\n",
    "print(\"Created 03_threshold_summary.md\")\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open("lin28a_project/notebooks/01_s5_direct_target_analysis.ipynb", "w") as f:
    json.dump(notebook_content, f, indent=1)

print("Notebook generated directly via json.")
