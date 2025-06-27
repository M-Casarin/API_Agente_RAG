## Agente IP 

Agente LLM de Individual Privado. 
**Grupo KC Agente de Seguros**. 


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

   # Azure OpenAI
   AZURE_OPENAI_ENDPOINT=https://<tu-recurso>.openai.azure.com/
   AZURE_OPENAI_KEY=tu_azure_key
   AZURE_OPENAI_DEPLOYMENT_NAME=emeth-deploy

   # Google Vertex AI
   GOOGLE_APPLICATION_CREDENTIALS=credentials/google-service-account.json
   GOOGLE_PROJECT_ID=uplifted-nuance-461609-s4
   GOOGLE_LOCATION=us-central1
   GOOGLE_VERTEX_ENDPOINT_ID=tu_endpoint_id
   ```

5. **Arrancar Emeth**:

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

---

## Próximos Pasos

1. **Fase 1: Ingestión y Chunking** – extraer texto de `docs/` y generar `data/chunks.json`.
2. **Fase 2: Indexación semántica** – producir `data/embeddings.npy` y construir índice FAISS.
3. **Fase 3: Mejora de prompt** – iterar plantillas y parámetros.
4. **Fase 4: Despliegue** – contenerizar con Docker y habilitar CI/CD.

---

**Emeth** – Tu asistente LLM de confianza para el sector asegurador. ¡Manos a la obra!
