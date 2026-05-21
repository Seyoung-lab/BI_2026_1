import pandas as pd
import numpy as np
import os

TABLE_S5_PATH = 'lin28a_project/data/supplementary_tables/1-s2.0-S0092867412012342-mmc5.xls'
PROCESSED_DATA_PATH = 'lin28a_project/data/processed/table_s5_cleaned.csv'

df = pd.read_excel(TABLE_S5_PATH, sheet_name=0, skiprows=1)

print(f"Shape: {df.shape}")
print("\nColumns:")
print(list(df.columns))

print("\nMissing values count:")
print(df.isnull().sum())

df.to_csv(PROCESSED_DATA_PATH, index=False)
print(f"\nSaved cleaned table to {PROCESSED_DATA_PATH}")

with open('lin28a_project/notes/table_s5_data_dictionary.md', 'w') as f:
    f.write("# Table S5 Data Dictionary\n\n")
    f.write("- **Accession**: Transcript accession\n")
    f.write("- **Gene**: Gene symbol\n")
    f.write("- **CLIP p-value**: CLIP-seq p-value\n")
    f.write("- **CLIP FDR**: CLIP-seq False Discovery Rate\n")
    f.write("- **CLIP-35L33G, CLIP-let7g, CLIP-Mirlet7d, CLIP-Mirlet7f-1**: CLIP enrichment from each antibody\n")
    f.write("- **Ribosome density change (siLin28a / siLuc)**: Ribosome density change after Lin28a knockdown\n")
    f.write("- **RNA level change (siLin28a / siLuc)**: RNA-seq mRNA change after Lin28a knockdown\n")
    f.write("- **Description**: Gene description\n")
print("Saved data dictionary to notes/table_s5_data_dictionary.md")
