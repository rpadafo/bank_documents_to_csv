import os
import time
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Bank module >>
import bankinter 
import sabadell
import caixa
import santander

IN_FOLDER = "/excel"
OUT_FOLDER = "/csv"
RETENTION_HOUR = int(os.environ.get("RETENTION_HOUR", 12))

def clean_old_csv():
    # Delete all files in OUT_FOLDER when RETENTION_HOUR is over
    now = time.time()
    # Hours to seconds (RETENTION_HOUR * 60 * 60 = x seconds)
    limit_seconds = RETENTION_HOUR * 3600
    
    print(f"🧹 Running automatic cleanup of files older than {RETENTION_HOUR} hours")
    
    try:
        for file_name in os.listdir(OUT_FOLDER):
            full_path_file = os.path.join(OUT_FOLDER, file_name)
            
            if os.path.isfile(full_path_file) and file_name.endswith('.csv'):
                modification_date = os.path.getmtime(full_path_file)
                if (now - modification_date) > limit_seconds:
                    os.remove(full_path_file)
                    print(f"🗑️ Deleted {file_name} file")
    except Exception as e:
        print(f"⚠️ Error while deleting files: {e}")

class FilesMonitor(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or os.path.basename(event.src_path).startswith("~$"):
            return
            
        file_name = os.path.basename(event.src_path)
        file_name_lower = file_name.lower()

        if file_name_lower.endswith(('.xlsx', '.xls', '.txt')):
            print(f"\n⚡ Find: {file_name}")
            time.sleep(2) # Wait for complete copy
            
            try:
                # 1. SANTANDER (Files starts with transactions)
                if file_name_lower.startswith("transactions"):
                    print("-> Using [Santander] module")
                    santander.process(event.src_path,OUT_FOLDER,file_name)

                # 2. LA CAIXA
                elif file_name_lower.startswith("movimientos_cuenta"):
                    print("-> Using [Caixa] module")
                    caixa.process(event.src_path,OUT_FOLDER,file_name)

                # 3. BANKINTER
                elif file_name_lower.startswith("movimientos"):
                    print("-> Using [Bankinter] module")
                    bankinter.process(event.src_path,OUT_FOLDER,file_name)

                # 4. CASO SABADELL
                elif file_name_lower.endswith('.txt') or re.match(r'^[\d_]+\.[a-zA-Z0-9]+$', file_name_lower):
                    print("-> Using [Sabadell] module")
                    sabadell.process(event.src_path, OUT_FOLDER, file_name)
                
                else:
                    print(f"❌ This file is not asociated to any bank: {file_name}")
                    return

                # Delete the original file from /excel
                os.remove(event.src_path)
                
                # Cleaning
                clean_old_csv()

            except Exception as e:
                print(f"💥 Error processing {file_name}: {e}")

if __name__ == "__main__":
    os.makedirs(IN_FOLDER, exist_ok=True)
    os.makedirs(OUT_FOLDER, exist_ok=True)
    
    observer = Observer()
    observer.schedule(FilesMonitor(), path=IN_FOLDER, recursive=False)
    observer.start()
    print(f"🤖 Watching {IN_FOLDER} (Excel/TXT), exporting to {OUT_FOLDER}...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()