import pytest
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.vector_store import search_similar_docs
from agents.responder_agent import generate_response
from core.prompts import build_prompt
import tempfile
import shutil


class TestVectorStore:
    """Tests para el vector store y retrieval logic"""
    
    def test_search_similar_docs_returns_results(self):
        """Test que la búsqueda retorna resultados"""
        query = "detergente para ropa"
        results = search_similar_docs(query, k=2)
        
        assert len(results) > 0, "Debería retornar al menos un resultado"
        assert len(results) <= 2, "No debería retornar más de k resultados"
        assert all(isinstance(r, str) for r in results), "Todos los resultados deben ser strings"
    
    def test_search_similar_docs_relevant_content(self):
        """Test que la búsqueda retorna contenido relevante"""
        query = "shampoo para cabello"
        results = search_similar_docs(query, k=3)
        
        # Al menos uno de los resultados debería mencionar shampoo o cabello
        relevant_found = any(
            'shampoo' in result.lower() or 'cabello' in result.lower() 
            for result in results
        )
        assert relevant_found, "Los resultados deberían ser relevantes a la consulta"
    
    def test_search_similar_docs_different_k_values(self):
        """Test que el parámetro k funciona correctamente"""
        query = "productos de limpieza"
        
        results_k1 = search_similar_docs(query, k=1)
        results_k3 = search_similar_docs(query, k=3)
        
        assert len(results_k1) <= 1, "k=1 debería retornar máximo 1 resultado"
        assert len(results_k3) <= 3, "k=3 debería retornar máximo 3 resultados"


class TestPrompts:
    """Tests para la construcción de prompts"""
    
    def test_build_prompt_structure(self):
        """Test que el prompt se construye correctamente"""
        query = "¿Qué detergente me recomiendas?"
        docs = ["Detergente UltraClean es efectivo", "Jabón SoftCare para piel sensible"]
        
        prompt = build_prompt(query, docs)
        
        assert query in prompt, "El prompt debe incluir la consulta del usuario"
        assert all(doc in prompt for doc in docs), "El prompt debe incluir todos los documentos"
        assert "Responde" in prompt, "El prompt debe incluir instrucciones claras"


class TestResponderAgent:
    """Tests para el agente responder"""
    
    def test_generate_response_returns_string(self):
        """Test que el agente genera una respuesta en formato string"""
        query = "¿Qué productos tienes?"
        docs = ["Detergente líquido para ropa", "Shampoo para cabello"]
        
        response = generate_response(query, docs)
        
        assert isinstance(response, str), "La respuesta debe ser un string"
        assert len(response) > 0, "La respuesta no debe estar vacía"
    
    def test_generate_response_uses_context(self):
        """Test que la respuesta usa el contexto proporcionado"""
        query = "¿Tienes detergente?"
        docs = ["Detergente UltraClean es una fórmula avanzada"]
        
        response = generate_response(query, docs)
        
        # La respuesta debería mencionar algo relacionado con detergente
        assert any(word in response.lower() for word in ['detergente', 'ultraclean', 'limpieza'])


# Fixture para tests de integración
@pytest.fixture
def sample_query_data():
    return {
        "user_id": "test_user_123",
        "query": "¿Qué shampoo me recomiendas para cabello graso?"
    }


class TestIntegration:
    """Tests de integración end-to-end"""
    
    def test_full_rag_pipeline(self, sample_query_data):
        """Test del pipeline completo RAG"""
        query = sample_query_data["query"]
        
        # 1. Retrieval
        docs = search_similar_docs(query, k=3)
        assert len(docs) > 0, "El retrieval debe encontrar documentos"
        
        # 2. Generation
        response = generate_response(query, docs)
        assert isinstance(response, str), "Debe generar una respuesta"
        assert len(response) > 10, "La respuesta debe tener contenido sustancial"


if __name__ == "__main__":
    pytest.main([__file__])
