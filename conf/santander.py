# conf/santander.py
import os
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()

ERROR_RED = "\033[1;31m"
RESET_COLOR = "\033[0m"

def process(source_path, output_path, file_name):
    """
    Reads Santander Bank Files, search the first line of the records (searching by FECHA OPERACION)
    Then save the EXCEL as CSV and change the name of the file.
    """
    df_raw = pd.read_excel(source_path, header=None)
    
    header_row = None
    
    for i, line in df_raw.iterrows():
        text_line = " ".join(line.dropna().astype(str)).lower()
        if "fecha operacion" in text_line or "fecha operación" in text_line:
            header_row = i
            break
            
    if header_row is None:
        raise ValueError("❌ [Santander] The row containing 'FECHA OPERACION' was not found in the file.")
        
    logger.info(f"[Santander] 'Fecha operacion' detected on line: {header_row + 1}")
    
    df_clean = pd.read_excel(source_path, skiprows=header_row)
    df_clean = df_clean.dropna(how='all')

    base_name = os.path.splitext(file_name)[0]
    output_path = os.path.join(output_path, f"SA_{base_name}.csv")
    df_clean.to_csv(output_path, index=False, encoding='utf-8', sep=';')
    logger.info(f"✅ [Santander] CSV successfully saved to: {output_path}")
