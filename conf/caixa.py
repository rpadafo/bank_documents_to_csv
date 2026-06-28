# conf/caixa.py
import os
import pandas as pd

def process(source_path, output_path, file_name):
    """
    Reads La Caixa Bank Files, search the first line of the records (searching by FECHA)
    Then save the EXCEL as CSV and change the name of the file.
    """
    df_raw = pd.read_excel(source_path, header=None)
    
    header_row = None
    
    for i, line in df_raw.iterrows():
        text_line = str(line.iloc[0]).strip().lower()
        if text_line == "fecha":
            header_row = i
            break
            
    if header_row is None:
        raise ValueError("❌ [Caixa] The row containing 'Fecha' was not found in the file.")
        
    print(f"[Caixa] 'Fecha' detected on line: {header_row + 1}")
    
    df_clean = pd.read_excel(source_path, skiprows=header_row)
    df_clean = df_clean.dropna(how='all')

    base_name = os.path.splitext(file_name)[0]
    output_path = os.path.join(output_path, f"CA_{base_name}.csv")
    df_clean.to_csv(output_path, index=False, encoding='utf-8', sep=';')
    print(f"✅ [Caixa] CSV successfully saved to: {output_path}")
