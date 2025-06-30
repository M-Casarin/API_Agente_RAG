"""
El modulo tiene como objetivo tomar al chunks_raw.json y sepeararlo en subchunks si es que el contenido de el primero rebasa cierta cantidad de caracteres. 
Busca transformar los fragmentos de texto extraidos desde docs,  en chunks semanticos más adecuados para el modelo LLM y bases vectoriales.

¿Que hace? 
- carga el archivo *data/chunks_raw.json* generado por src/ingestion/main_ingest
- recorre cada fragmento de texto y: 
    -> si es muy largo lo divide en sub-chunks manejables, dado un maximo acotado y fijo MAX_CHARS. 
    -> si es corto lo conserva
- normaliza el nexto 
- agrega metadatos de contexto 
- guarda el resultado final en data/chunks.json 


Por lo tanto, chunker acota los fragmentos de cada texto en a lo mas n caracteres dados por la variable MAX_CHARS, sanitiza el contenido de cada fragmento y enriquece 
el fragmento con metadatos.

"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import json 
import textwrap 

# Fijese la cota maxima de caracteres por chunk 
MAX_CHARS = 1500

def merge_chunks(raw_chunks: list[dict]) -> list[dict]: 

    finaL_chunks = []

    for fragmento in raw_chunks: 
        content = fragmento["content"] # obteenr el fragmento del chunk 
        # Recuperar los otros dos metadatos que no son el contenido del chunk 
        metadata = {
            key_metadata: value_metadata for key_metadata, value_metadata in fragmento.items() if key_metadata != 'content' 
        }

        if len(content) > MAX_CHARS: 
            sub_chunks = textwrap.wrap(content, MAX_CHARS) # Hacer particiones de longitud MAX_CHARS al chunk
            for i, sub in enumerate(sub_chunks): 
                dict_subchunk = {"content": sub.strip()}
                dict_subchunk.update(metadata)
                dict_subchunk.update({"subchunk": i})
                finaL_chunks.append(dict_subchunk)

        else: 
            finaL_chunks.append(
                fragmento
            )

    return finaL_chunks




def main():

    print("Cargando chunks crudos desde 'data/chunks_raw.json'")
    with open("data/chunks_raw.json", "r", encoding="utf-8") as f:
        raw_chunks = json.load(f)

    print(f"Procesando {len(raw_chunks)} fragmentos...")
    clean_chunks = merge_chunks(raw_chunks)

    print(f"{len(clean_chunks)} chunks finales generados.")
    os.makedirs("data", exist_ok=True)
    with open("data/chunks.json", "w", encoding="utf-8") as f:
        json.dump(clean_chunks, f, indent=2, ensure_ascii=False)

    print("├── Guardado en 'data/chunks.json'")


if __name__ == "__main__":
    main()
