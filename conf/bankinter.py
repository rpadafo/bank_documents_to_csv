# bancos/bankinter.py
import os
import pandas as pd

def process(source_path, output_path, file_name):
    """Reads Bankinter files, search the firts line of the records (searchin by FECHA CONTABLE)
    Then save the EXCEL as CSV and change the name of the file.
    """
    df_raw = pd.read_excel(source_path, header=None)
    
    header_row = None

    for i, line in df_raw.iterrows():
        text_line = str(line.iloc[0]).strip().lower()
        if "fecha contable" in text_line:
            header_row = i
            break
            
    if header_row is None:
        raise ValueError("❌ [Bankinter] The row containing 'Fecha contable' was not found in the file.")
        
    print(f"[Bankinter] ¡Fecha contable' detected on line: {header_row + 1}")
    
    df_clean = pd.read_excel(source_path, skiprows=header_row)
    df_clean = df_clean.dropna(how='all')

    base_name = os.path.splitext(file_name)[0]
    output_path = os.path.join(output_path, f"BK_{base_name}.csv")
    df_clean.to_csv(output_path, index=False, encoding='utf-8', sep=';', decimal=',')
    print(f"✅ [Bankinter] CSV successfully saved to: {output_path}")
