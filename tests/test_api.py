import pytest
import sys
import os
from fastapi.testclient import TestClient

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

client = TestClient(app)


class TestAPI:
    """Tests para los endpoints de la API"""
    
    def test_query_endpoint_success(self):
        """Test del endpoint /query con datos válidos"""
        test_data = {
            "user_id": "test_user_123",
            "query": "¿Qué detergente me recomiendas?"
        }
        
        response = client.post("/query", json=test_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "user_id" in data
        assert "answer" in data
        assert "status" in data
        assert data["user_id"] == test_data["user_id"]
        assert data["status"] == "success"
        assert len(data["answer"]) > 0
    
    def test_query_endpoint_empty_query(self):
        """Test del endpoint con query vacía"""
        test_data = {
            "user_id": "test_user_123",
            "query": ""
        }
        
        response = client.post("/query", json=test_data)
        assert response.status_code == 400
    
    def test_query_endpoint_whitespace_query(self):
        """Test del endpoint con query solo espacios"""
        test_data = {
            "user_id": "test_user_123",
            "query": "   "
        }
        
        response = client.post("/query", json=test_data)
        assert response.status_code == 400
    
    def test_query_endpoint_missing_fields(self):
        """Test del endpoint con campos faltantes"""
        # Falta user_id
        test_data = {
            "query": "¿Qué productos tienes?"
        }
        
        response = client.post("/query", json=test_data)
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_query_endpoint_invalid_json(self):
        """Test del endpoint con JSON inválido"""
        response = client.post("/query", data="invalid json")
        assert response.status_code == 422
    
    def test_query_endpoint_different_queries(self):
        """Test con diferentes tipos de queries"""
        queries = [
            "¿Tienes shampoo?",
            "Necesito algo para lavar ropa",
            "¿Qué pasta dental me recomiendas?",
            "Productos para cabello graso"
        ]
        
        for query in queries:
            test_data = {
                "user_id": f"test_user_{hash(query)}",
                "query": query
            }
            
            response = client.post("/query", json=test_data)
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "success"
            assert len(data["answer"]) > 0


if __name__ == "__main__":
    pytest.main([__file__])
