import pandas as pd
import glob
print("Running inspection...")
for f in sorted(glob.glob('lin28a_project/data/supplementary_tables/*.xls')):
    try:
        print(f'=== {f} ===')
        df = pd.read_excel(f, sheet_name=0, nrows=2)
        print('Cols:', list(df.columns))
    except Exception as e:
        print(f"Error reading: {e}")
