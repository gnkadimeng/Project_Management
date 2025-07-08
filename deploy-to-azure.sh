#!/bin/bash

# 🚀 Complete Azure Deployment Script for Your Django App
# Run this from your terminal after installing Azure CLI

set -e

echo "🌐 Azure Django App Deployment"
echo "=============================="

# Configuration - CHANGE THESE VALUES
RESOURCE_GROUP="django-app-rg"
LOCATION="South Africa North"
CONTAINER_ENV="django-container-env"
CONTAINER_APP="django-project-app"
POSTGRES_SERVER="django-postgres-$(date +%s)"
POSTGRES_ADMIN="dbadmin"
POSTGRES_PASSWORD="DjangoApp$(date +%s)!"
DATABASE_NAME="project_management"

# Get your GitHub username
read -p "📝 Enter your GitHub username: " GITHUB_USERNAME
if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required!"
    exit 1
fi

echo ""
echo "📋 Deployment Configuration:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  Container App: $CONTAINER_APP"
echo "  Database: $POSTGRES_SERVER"
echo "  GitHub Image: ghcr.io/$GITHUB_USERNAME/project_management:latest"
echo ""

read -p "🚀 Continue with deployment? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Deployment cancelled."
    exit 0
fi

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed!"
    echo "Please install it first:"
    echo "  macOS: brew install azure-cli"
    echo "  Ubuntu: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
    echo "  Windows: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows"
    exit 1
fi

# Login to Azure
echo "🔐 Logging into Azure..."
az login

# Create resource group
echo "📦 Creating resource group..."
az group create \
    --name $RESOURCE_GROUP \
    --location "$LOCATION"

# Create PostgreSQL database
echo "🗄️ Creating PostgreSQL database..."
az postgres flexible-server create \
    --resource-group $RESOURCE_GROUP \
    --name $POSTGRES_SERVER \
    --location "$LOCATION" \
    --admin-user $POSTGRES_ADMIN \
    --admin-password "$POSTGRES_PASSWORD" \
    --sku-name Standard_B1ms \
    --tier Burstable \
    --public-access 0.0.0.0 \
    --storage-size 32 \
    --version 15

echo "🗃️ Creating database..."
az postgres flexible-server db create \
    --resource-group $RESOURCE_GROUP \
    --server-name $POSTGRES_SERVER \
    --database-name $DATABASE_NAME

# Create Container Apps environment
echo "🏗️ Creating Container Apps environment..."
az containerapp env create \
    --name $CONTAINER_ENV \
    --resource-group $RESOURCE_GROUP \
    --location "$LOCATION"

# Build the database URL
DATABASE_URL="postgres://$POSTGRES_ADMIN:$POSTGRES_PASSWORD@$POSTGRES_SERVER.postgres.database.azure.com:5432/$DATABASE_NAME"

# Generate Django secret key
echo "🔐 Generating Django secret key..."
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')

# Deploy the container app
echo "🚀 Deploying your Django app..."
az containerapp create \
    --name $CONTAINER_APP \
    --resource-group $RESOURCE_GROUP \
    --environment $CONTAINER_ENV \
    --image "ghcr.io/$GITHUB_USERNAME/project_management:latest" \
    --target-port 8000 \
    --ingress external \
    --min-replicas 0 \
    --max-replicas 3 \
    --cpu 0.5 \
    --memory 1Gi \
    --env-vars \
        "DATABASE_URL=$DATABASE_URL" \
        "DEBUG=False" \
        "SECRET_KEY=$SECRET_KEY"

# Get the app URL
APP_URL=$(az containerapp show \
    --name $CONTAINER_APP \
    --resource-group $RESOURCE_GROUP \
    --query "properties.configuration.ingress.fqdn" \
    --output tsv)

echo ""
echo "🎉 Deployment completed successfully!"
echo "====================================="
echo "🌐 Your app: https://$APP_URL"
echo "🗄️ Database: $POSTGRES_SERVER.postgres.database.azure.com"
echo "📊 Resource Group: $RESOURCE_GROUP"
echo ""
echo "🔐 SAVE THESE CREDENTIALS:"
echo "  Database User: $POSTGRES_ADMIN"
echo "  Database Password: $POSTGRES_PASSWORD"
echo "  Secret Key: $SECRET_KEY"
echo ""
echo "🔧 To update your app:"
echo "1. Push changes to GitHub"
echo "2. GitHub Actions will build new image"
echo "3. Update container app:"
echo "   az containerapp update \\"
echo "     --name $CONTAINER_APP \\"
echo "     --resource-group $RESOURCE_GROUP \\"
echo "     --image ghcr.io/$GITHUB_USERNAME/project_management:latest"
echo ""
echo "🎯 Your Django Project Management app is now live on Azure!"
