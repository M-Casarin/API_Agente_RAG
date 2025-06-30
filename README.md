# Agente RAG 


---

## Alcance del Proyecto

* **Consultas de lógica de negocio**: descripción de procesos internos, flujos de trabajo y pasos alternativos.
* **Glosario interactivo**: definiciones de términos y acrónimos del sector asegurador.
* **Cálculos y fórmulas**: explicación de cómo se calculan primas, comisiones y reservas.
* **FAQ dinámico**: preguntas frecuentes actualizadas y sugerencia de documentos relevantes.
* **Multi-proveedor LLM**: integración con OpenAI, Azure OpenAI y Google Vertex AI (configurable).
* **API REST (FastAPI)**: punto de acceso para orquestar recuperación de contexto y llamada al LLM.
* **Canales de mensajería**: integración con Slack/Teams o WhatsApp Business.

**Fuera de alcance:**

* Interfaz de usuario dedicada (web app o dashboard propio).
* Asesoría legal o de cumplimiento.
* Acceso a datos sensibles de clientes.
* Soluciones low-code.

---

## Estructura del Repositorio

```
llm-gkc/
├── .env                     # Variables de entorno
├── .gitignore
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml      # Opcional
│
├── credentials/            # JSON de credenciales (gitignored)
│   └── google-service-account.json
│
├── docs/                   # Documentación original (PDF, DOCX, MD)
│   └── ...
│
├── data/                   # Chunks, embeddings, índices FAISS
│   └── ...
│
├── models/                 # Modelos fine-tuned o checkpoints
│   └── ...
│
└── src/                    # Código fuente organizado por módulos
    ├── ingestion/          # Extracción y chunking de documentos
    ├── indexer/            # Generación de embeddings y FAISS
    ├── rag/                # Lógica RAG y CLI
    ├── api/                # FastAPI y autenticación
    └── llm_backends.py     # Abstracción multi-provider LLM
```

---

## Configuración y Arranque con [uv](https://github.com/astral-sh/uv)

1. **Clonar el repositorio**:

   ```bash
   git clone <tu-repo-url> llm-gkc
   cd llm-gkc
   ```

2. **Crear y activar el entorno con `uv`**:

   ```bash
   uv venv .venv
   source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias**:

   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**: crea un archivo `.env` en la raíz del proyecto con este contenido:

   ```dotenv
   # Proveedor LLM (openai, azure o google)
   LLM_PROVIDER=openai

   # OpenAI
   OPENAI_API_KEY=tu_openai_api_key

    # Azure
    AZURE_OPENAI_ENDPOINT=
    AZURE_OPENAI_API_KEY=
    AZURE_OPENAI_API_VERSION=
    AZURE_OPENAI_RESOURCE_NAME=
    AZURE_OPENAI_DEPLOYMENT_EMBEDDING_NAME=text-embedding-3-small
    AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini-2


   # Google Vertex AI
   GOOGLE_APPLICATION_CREDENTIALS=credentials/google-service-account.json
   GOOGLE_PROJECT_ID=uplifted-nuance-461609-s4
   GOOGLE_LOCATION=us-central1
   GOOGLE_VERTEX_ENDPOINT_ID=tu_endpoint_id
   ```

5. **Arrancar**:

   * **CLI de prueba**:

     ```bash
     uv run python -m src.rag.chat_cli
     ```

   * **API REST con Uvicorn**:

     ```bash
     uv run uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
     ```

6. **Cambiar proveedor LLM (opcional)**:

   Antes de iniciar cualquier servicio, puedes definir el proveedor en terminal:

   ```bash
   export LLM_PROVIDER=azure  # o "google"
   ```

7. **Fase 1: Ingestion y Procesamiento de archivos**
    - Subir todos los archivos que necesarios a docs/


    - Ingestion, Resultante: chunk_raw.json
    ```bash
    uv run python src/ingestion/main_ingest.py
    ``` 


    - Chunker, Resultante: chunk.json
    ```bash
    uv run python src/ingestion/chunker.py   
    ```



8. **Fase 2: Embeddings e indexacion semántica**
    Objetivo: Convertir chunk.json en vectores numericos semanticos usando un modelo de embeddings y almacenarlos en undice FAISS para busquedas eficientes por similitud. 

    ```bash
    Archivos Resultantes de la Fase 2: 
        data/
        ├── embeddings.npy  (Lista de vectores)
        ├── faiss_index/ 
            ├── index.false  (Indice FAISS serializado)
            ├── index_meta.json #  (Metadatos paralelos a los vecotes: source, page, subchunk, etc)
    ```


    - Embedding, por cada chunk en chunks se ha de hacer el embedding: 

    ```bash
    uv run python src/indexer/embed.py
    ```
        Resultante: /data/embeddings.npy   # Matriz vectorial

    - Indexacion. Tomara los embeddings generados en el paso anterior y le asignara un indice unico basado en algun algoritmo, en este caso es el FlatL2 que es tomar la distancia euclideana de cada vector. 

    ```bash
    uv run python src/indexer/faiss_indexer.py
    ```
        Resultante: 
            ├── faiss_index/ 
                ├── index.false  (Indice FAISS serializado)
                ├── index_meta.json #  (Metadatos paralelos a los vecotes: source, page, subchunk, etc)



9. **Fase 3: RAG (Retrieval-Augmented Generation)**
    Objetivo: Construir el sistema de RAG (Retrieval-Augmented Generation), que responde preguntas basadas en conocimiento externo y embebido (tus documentos) en vez de solo depender del conocimiento entrenado del LLM.

    El sistema buscará los fragmentos (chunks) más relevantes del índice semántico, construirá un prompt con ese contexto y se lo enviará a un modelo de lenguaje (Azure OpenAI, Google o OpenAI) para obtener una respuesta precisa.





