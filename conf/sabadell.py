# conf/sabadell.py
import os
import logging

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
    Change the file extension from TXT to CSV from Sabadell File.
    """
    # Generamos el nombre final cambiando .txt por .csv
    base_name = os.path.splitext(file_name)[0]
    prefix = os.environ.get("PREFIX_SABADELL", "BS")
    csv_path = os.path.join(output_path, f"{prefix}_{base_name}.csv")
    
    with open(source_path, 'rb') as f_source:
        content = f_source.read()
        
    with open(csv_path, 'wb') as f_destination:
        f_destination.write(content)
        
    logger.info(f"[Sabadell] ✅ Extension successfully changed to CSV: {output_path}")