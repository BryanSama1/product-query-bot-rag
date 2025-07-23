# Product Query Bot - RAG Pipeline

Un microservicio inteligente que responde preguntas sobre productos usando un pipeline RAG (Retrieval-Augmented Generation) con arquitectura multi-agente.

## Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │  Retriever      │    │  Responder      │
│   Endpoint      │───▶│  Agent          │───▶│  Agent          │
│  POST /query    │    │  (Vector Store) │    │  (Gemini AI)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Componentes:

- **Vector Store**: FAISS con embeddings de Google AI
- **Retriever Agent**: Búsqueda semántica de documentos relevantes
- **Responder Agent**: Generación de respuestas usando Gemini 1.5-flash
- **Multi-Agent Pipeline**: Comunicación entre agentes para respuestas contextuales

## Setup y Instalación

### Prerrequisitos

- Python 3.11+
- Google AI API Key
- Docker (opcional)

### 1. Instalación Local

```bash
# Clonar repositorio
git clone <repository-url>
cd product-query-bot

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tu GOOGLE_API_KEY
```

### 2. Indexar Documentos

```bash
# Indexar productos (necesario antes del primer uso)
python index.py
```

### 3. Ejecutar Servidor

```bash
# Desarrollo
uvicorn app:app --reload

# Producción
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Docker

### Build y Run

```bash
# Build imagen
docker build -t product-query-bot .

# Run container
docker run -p 8000:8000 --env-file .env product-query-bot

# O usar docker-compose
docker-compose up --build
```

### Desarrollo con Docker

```bash
# Modo desarrollo con hot reload
docker-compose --profile dev up
```

## 📡 API Usage

### Endpoint Principal

```bash
POST /query
Content-Type: application/json

{
  "user_id": "string",
  "query": "string" 
}
```

### Ejemplos de Uso

```bash
# Consulta sobre shampoo
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "query": "¿Qué shampoo me recomiendas para cabello graso?"
  }'

# Consulta sobre detergente
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user456", 
    "query": "Necesito algo para lavar ropa delicada"
  }'
```

### Respuesta

```json
{
  "user_id": "user123",
  "answer": "Te recomiendo el Shampoo RevitalHair...",
  "status": "success"
}
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_rag_pipeline.py
pytest tests/test_api.py

# Con coverage
pytest --cov=. --cov-report=html
```

### Tests Incluidos

- **test_rag_pipeline.py**: Tests del pipeline RAG (vector store, prompts, agentes)
- **test_api.py**: Tests de endpoints FastAPI (validaciones, formato, errores)
- **test_production.py**: Tests de la API deployada en GCP
- Tests de integración end-to-end

## Estructura del Proyecto

product-query-bot/
├── app.py                 # Aplicación FastAPI
├── index.py               # Script de indexación de documentos
├── agents/
│   ├── retriever_agent.py # Lógica de recuperación de documentos
│   └── responder_agent.py # Generación de respuestas
├── core/
│   ├── vector_store.py    # Almacén vectorial FAISS
│   └── prompts.py         # Plantillas de prompts
├── data/
│   └── products/          # Documentos de productos
├── tests/                 # Conjunto de pruebas
├── faiss_index/           # Índice vectorial generado
├── Dockerfile
├── docker-compose.yml
└── requirements.txt


## Configuración

### Variables de Entorno

```bash
GOOGLE_API_KEY=your_api_key_here
TOP_K=3  # Número de documentos a recuperar (opcional)
```

### Agregar Nuevos Productos

1. Crear archivo `.txt` en `data/products/`
2. Ejecutar `python index.py` para re-indexar
3. El bot automáticamente incluirá el nuevo producto

## Tecnologías Utilizadas

- **FastAPI**: API REST framework
- **LangChain**: RAG pipeline y agent orchestration  
- **FAISS**: Vector similarity search
- **Google AI**: Embeddings y generación de texto
- **Python 3.11**: Runtime
- **Docker**: Containerización
- **Pytest**: Testing framework

## Performance

- **Indexación**: ~5-10 documentos en <30 segundos
- **Query Response**: <3 segundos promedio
- **Vector Search**: Sub-segundo con FAISS


## Deployment a GCP

### Cloud Run (Producción)

**API en vivo:** `https://product-query-bot-127465468754.us-central1.run.app`

**Documentación interactiva:** `https://product-query-bot-127465468754.us-central1.run.app/docs`

### Comandos de deployment:

```bash
# 1. Build y push a Container Registry
gcloud builds submit --tag gcr.io/prototipado-ia-robotica/product-query-bot

# 2. Deploy a Cloud Run
gcloud run deploy product-query-bot \
  --image gcr.io/prototipado-ia-robotica/product-query-bot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY
```

### Probar API en producción:

```bash
curl -X POST "https://product-query-bot-127465468754.us-central1.run.app/query" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","query":"¿Qué productos tienes?"}'
```


## 📄 Licencia

MIT License - ver archivo LICENSE para detalles


