
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import json
from src.ingestion.text_extractor import extract_all_documents
from pathlib import Path
from colorama import Fore as Fr
import os 



# Generar los chunks, se debe correr el script directamente 
if __name__ == '__main__': 
    print(Fr.YELLOW, "\nIniciando la extraccion de texto de los documentos en /docs/")
    chunks = extract_all_documents()
    
    
    print(Fr.GREEN, f"Se extrajeron {len(chunks)} chunks de los documentos")

    os.makedirs("data", exist_ok=True)

    output_path =  Path("data") / "chunks_raw.json"

    with open(output_path, "w", encoding="utf-8") as file: 
        json.dump(
            chunks,
            file, 
            indent=2, 
            ensure_ascii=False
        )

    print(f"├── Chunks han sido guardados en {output_path.resolve()}")
    print(Fr.RESET, " ")
    
