"""
Contiene la clase encargada de la extraccion del texto en crudo de cada documento

"""
import os 
from pathlib import Path
import pdfplumber 
import docx
from colorama import Fore as Fr
import json

class TextExtractor: 

    extensions_alloweds = [".pdf", ".docx", ".txt", ".md"]

    def __init__(self, file_path: str):
        self.file_path = file_path
        # Verificar la existencia 
        if not Path(file_path).exists(): 
            raise FileNotFoundError(f"[Error:TextExtractor] El archivo {file_path} no existe")
        self.extension = Path(file_path).suffix.lower()
        self.filename = os.path.basename(file_path)

    
    def extract(self): 
        """
        Extrae el texto del archivo segun el tipo de formato
        """
        if not self.extension in self.extensions_alloweds: 
            raise ValueError(f"[Error:TextExtractor.Extract] Tipo de extension no soportado: {self.file_path}")
        
        match self.extension: 
            case ".pdf": 
                return self._extract_pdf() 
            case ".docx": 
                return self._extract_docx()
            case ".txt" | ".md": 
                return self._extract_txt()
            


    def _extract_pdf(self) -> list[dict]: 
        chunks = []
        with pdfplumber.open(self.file_path) as pdf: 
            for i, page in enumerate(pdf.pages, start=1):
                texto = page.extract_text()
                if texto: 
                    # Hay que darles este formato pues los embeddings se enriquecen de proporcionar metadatos de cada archivo 
                    chunks.append({
                        "content": texto.strip(), 
                        "source": self.filename, 
                        "page": i
                    })
        return chunks
    

    def _extract_docx(self) -> list[dict]:
        chunks = []
        doc = docx.Document(self.file_path)

        for i, parrafo in enumerate(doc.paragraphs): 
            texto = parrafo.text.strip()
            if texto: 
                chunks.append({
                    "content": texto, 
                    "source": self.filename, 
                    "paragraph": i
                }) 
        return chunks
    
    def _extract_txt(self) -> list[dict]: 
        
        with open(self.file_path, "r", encoding="utf-8") as file: 
            lineas = file.readlines()

        return [
            {
                "content": linea.strip(),
                "source": self.filename, 
                "line": i + 1
            }
                for i, linea in enumerate(lineas)
                if linea.strip()
        ]

def extract_all_documents(directory: str = "docs") -> list[dict]: 

    all_chunks = []
    for i, file in enumerate(os.listdir(directory)): 
        try: 
            path  = Path(directory) / file 
            print(f"\t[{i}] {path}")
            if path.is_file():
                extractor = TextExtractor(path)
                chunks = extractor.extract()
                all_chunks.extend(chunks)

        except Exception as e: 
            print(f"[Error] al obtener todos los chunks de {path.resolve()}: {e}")

    return all_chunks
        

