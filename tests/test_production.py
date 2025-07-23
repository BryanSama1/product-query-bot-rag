#!/usr/bin/env python3
"""
Script para probar el Product Query Bot deployado en GCP
Este script verifica que la API en producción funcione correctamente
"""

import requests
import json
import sys
import os

# Agregar el directorio raíz al path para importar módulos si es necesario
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# URL del bot en producción
PRODUCTION_URL = "https://product-query-bot-127465468754.us-central1.run.app"

def test_production_bot():
    print("🚀 Probando Product Query Bot en GCP...")
    print(f"📡 URL: {PRODUCTION_URL}")
    print("="*60)
    
    # Test queries
    test_queries = [
        {
            "user_id": "gcp_test_1",
            "query": "¿Qué shampoo me recomiendas?",
            "description": "Test básico de shampoo"
        },
        {
            "user_id": "gcp_test_2", 
            "query": "Necesito detergente para ropa delicada",
            "description": "Test de detergente especializado"
        },
        {
            "user_id": "gcp_test_3",
            "query": "¿Tienes pasta dental?",
            "description": "Test de pasta dental"
        }
    ]
    
    for i, test_data in enumerate(test_queries, 1):
        print(f"\n[Test {i}/3] {test_data['description']}")
        print(f"👤 Usuario: {test_data['user_id']}")
        print(f"❓ Query: {test_data['query']}")
        
        try:
            response = requests.post(
                f"{PRODUCTION_URL}/query",
                json={
                    "user_id": test_data["user_id"],
                    "query": test_data["query"]
                },
                timeout=60  # 60 segundos para cold start
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"🤖 Respuesta: {data.get('answer', 'Sin respuesta')}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"📄 Details: {response.text}")
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout - El servidor está iniciando (cold start)")
            print("💡 Esto es normal en la primera llamada")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 40)
    
    print("\n🌐 Tu bot está disponible públicamente en:")
    print(f"   {PRODUCTION_URL}")
    print("\n📖 Documentación interactiva:")
    print(f"   {PRODUCTION_URL}/docs")
    
    print("\n🧪 Ejemplo de uso con curl:")
    print(f'''curl -X POST "{PRODUCTION_URL}/query" \\
  -H "Content-Type: application/json" \\
  -d '{{"user_id":"test","query":"¿Qué productos tienes?"}}'
''')

if __name__ == "__main__":
    test_production_bot()
