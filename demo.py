#!/usr/bin/env python3
"""
Script de demostración para el Product Query Bot
Ejecuta ejemplos de consultas para mostrar el funcionamiento del sistema
"""

import requests
import json
import time
from typing import Dict, Any

# Configuración
BASE_URL = "http://localhost:8000"
ENDPOINT = f"{BASE_URL}/query"

# Ejemplos de consultas
EXAMPLE_QUERIES = [
    {
        "user_id": "demo_user_1",
        "query": "¿Qué shampoo me recomiendas para cabello graso?",
        "description": "Consulta específica sobre shampoo"
    },
    {
        "user_id": "demo_user_2", 
        "query": "Necesito algo para lavar ropa delicada",
        "description": "Consulta sobre detergente para ropa delicada"
    },
    {
        "user_id": "demo_user_3",
        "query": "¿Tienes pasta dental para dientes sensibles?",
        "description": "Consulta sobre pasta dental especializada"
    },
    {
        "user_id": "demo_user_4",
        "query": "¿Qué productos tienes para el cuidado personal?",
        "description": "Consulta general sobre productos"
    },
    {
        "user_id": "demo_user_5",
        "query": "¿Hay algún jabón para piel sensible?",
        "description": "Consulta sobre jabón especializado"
    }
]

def make_query(data: Dict[str, str]) -> Dict[str, Any]:
    """Hacer una consulta al bot"""
    try:
        response = requests.post(ENDPOINT, json=data, timeout=30)
        return {
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text,
            "success": response.status_code == 200
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": None,
            "response": f"Error de conexión: {str(e)}",
            "success": False
        }

def print_separator():
    print("="*80)

def print_query_result(query_data: Dict[str, str], result: Dict[str, Any]):
    """Imprimir resultado de una consulta de forma legible"""
    print(f"📋 {query_data['description']}")
    print(f"👤 Usuario: {query_data['user_id']}")
    print(f"❓ Consulta: {query_data['query']}")
    print()
    
    if result['success']:
        response_data = result['response']
        print(f"✅ Status: {result['status_code']} - {response_data.get('status', 'N/A')}")
        print(f"🤖 Respuesta:")
        print(f"   {response_data.get('answer', 'Sin respuesta')}")
    else:
        print(f"❌ Error: {result['status_code']}")
        print(f"📄 Detalles: {result['response']}")
    
    print()

def check_server_health():
    """Verificar que el servidor esté disponible"""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 Product Query Bot - Script de Demostración")
    print_separator()
    
    # Verificar conectividad
    print("🔍 Verificando conectividad del servidor...")
    if not check_server_health():
        print("❌ Error: No se puede conectar al servidor")
        print(f"   Asegúrate de que el servidor esté ejecutándose en {BASE_URL}")
        print("   Ejecuta: uvicorn app:app --reload")
        return
    
    print("✅ Servidor disponible!")
    print()
    
    # Ejecutar consultas de ejemplo
    print("📝 Ejecutando consultas de demostración...")
    print_separator()
    
    for i, query_data in enumerate(EXAMPLE_QUERIES, 1):
        print(f"[{i}/{len(EXAMPLE_QUERIES)}]")
        
        # Hacer la consulta
        result = make_query(query_data)
        
        # Mostrar resultado
        print_query_result(query_data, result)
        
        # Pausa entre consultas
        if i < len(EXAMPLE_QUERIES):
            print("⏳ Esperando 2 segundos...\n")
            time.sleep(2)
        
        print_separator()
    
    print("✨ Demostración completada!")
    print()
    print("💡 Comandos útiles:")
    print("   - Ejecutar tests: pytest")
    print("   - Ver documentación: http://localhost:8000/docs")
    print("   - Re-indexar productos: python index.py")

if __name__ == "__main__":
    main()
