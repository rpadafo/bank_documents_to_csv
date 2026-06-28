# conf/caixa.py
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
        
    logger.info(f"[Caixa] 'Fecha' detected on line: {header_row + 1}")
    
    df_clean = pd.read_excel(source_path, skiprows=header_row)
    df_clean = df_clean.dropna(how='all')

    date_columns = ['Fecha', 'Fecha valor']
    for column in date_columns:
        if column in df_clean.columns:
            df_clean[column] = pd.to_datetime(df_clean[column], errors='coerce')
            df_clean[column] = df_clean[column].dt.strftime('%d/%m/%Y')


    base_name = os.path.splitext(file_name)[0]
    output_path = os.path.join(output_path, f"CA_{base_name}.csv")
    df_clean.to_csv(output_path, index=False, encoding='utf-8', sep=';')
    logger.info(f"✅ [Caixa] CSV successfully saved to: {output_path}")
