#!/bin/bash
# Script de deployment para Google Cloud Platform
# Reemplaza TU_PROJECT_ID con tu ID real de proyecto

set -e  # Salir si hay algún error

# Configuración
PROJECT_ID="TU_PROJECT_ID"  # ⚠️ CAMBIA ESTO
SERVICE_NAME="product-query-bot"
REGION="us-central1"
GOOGLE_API_KEY="TU_GOOGLE_API_KEY"  # ⚠️ CAMBIA ESTO

echo "🚀 Iniciando deployment a Google Cloud Platform..."

# 1. Configurar proyecto
echo "📋 Configurando proyecto: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# 2. Habilitar APIs necesarias
echo "🔧 Habilitando APIs necesarias..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 3. Build y push de la imagen Docker
echo "🐳 Construyendo imagen Docker..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# 4. Deploy a Cloud Run
echo "☁️ Desplegando a Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY

echo "✅ ¡Deployment completado!"
echo "🌐 Tu API está disponible en:"
gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"

echo ""
echo "🧪 Para probar tu API:"
echo "curl -X POST \"<URL>/query\" -H \"Content-Type: application/json\" -d '{\"user_id\":\"test\",\"query\":\"¿Qué productos tienes?\"}'"
