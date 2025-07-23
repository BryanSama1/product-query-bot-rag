import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

INDEX_PATH = "faiss_index"

# Inicializa el embedding con el modelo de Google Generative AI
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

def index_documents():
    docs = []
    data_dir = "data/products"
    print(f"Cargando documentos desde {data_dir}...")
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            print(f" - Cargando {filepath}")
            loader = TextLoader(filepath, encoding='utf-8')
            loaded_docs = loader.load()
            docs.extend(loaded_docs)

    if not docs:
        raise ValueError("No se encontraron documentos para indexar.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)
    print(f"Documentos divididos en {len(split_docs)} fragmentos para indexar.")

    print("Generando embeddings y creando índice FAISS...")
    db = FAISS.from_documents(split_docs, embedding)

    print(f"Guardando índice local en {INDEX_PATH}...")
    db.save_local(INDEX_PATH)
    print("Indexación completada.")

def search_similar_docs(query: str, k: int = 3):
    print(f"Cargando índice FAISS desde {INDEX_PATH}...")
    db = FAISS.load_local(INDEX_PATH, embedding, allow_dangerous_deserialization=True)
    print(f"Realizando búsqueda de top {k} documentos similares para: {query}")
    results = db.similarity_search(query, k=k)
    return [r.page_content for r in results]
