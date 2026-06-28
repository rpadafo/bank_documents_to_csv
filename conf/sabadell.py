# conf/sabadell.py
import os

def process(source_path, output_path, file_name):
    """
    Change the file extension from TXT to CSV from Sabadell File.
    """
    # Generamos el nombre final cambiando .txt por .csv
    base_name = os.path.splitext(file_name)[0]
    csv_path = os.path.join(output_path, f"BS_{base_name}.csv")
    
    with open(source_path, 'rb') as f_source:
        content = f_source.read()
        
    with open(csv_path, 'wb') as f_destination:
        f_destination.write(content)
        
    print(f"✅ [Sabadell] Extension successfully changed to CSV: {output_path}")