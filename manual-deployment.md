# Deploying Python API to Azure App Service

This document describes how to deploy a Python API to Azure App Service.

## Prerequisites

- Azure CLI
- Docker
- Azure subscription
- Python 3.6 or later


## Steps to Create and Deploy the API for the first time

1. Log in to Azure CLI

```bash
 az login
```
 
2. Create a resource group if it not exists

```bash
 az group create --name inception-api-rg --location eastus2
```

3. Create an Azure Container Registry

```bash
 az acr create --resource-group inception-api-rg --name inceptionapiacr --sku Basic --admin-enabled true
```
 
4. Get the password for the Azure Container Registry

```bash
 ACR_PASSWORD=$(az acr credential show --resource-group inception-api-rg --name inceptionapiacr --query "passwords[?name == 'password'].value" --output tsv)

 echo $ACR_PASSWORD
```

5. Build the Docker image 

```bash
 az acr build --resource-group inception-api-rg --registry inceptionapiacr --image iofmtelogapi:latest .
```

6. Create an App Service Plan

```bash
 az appservice plan create --name apielogplan --resource-group inception-api-rg --sku B1  --is-linux
``` 
 
7. Create a Web App

```bash
 az webapp create --resource-group inception-api-rg --plan apielogplan --name iofmtelogapi --docker-registry-server-password $ACR_PASSWORD --docker-registry-server-user inceptionapiacr --role acrpull --deployment-container-image-name inceptionapiacr.azurecr.io/iofmtelogapi:latest
```
## Deploy updates to the API

1. Build the Docker image

```bash
 az acr build --resource-group inception-api-rg --registry iofmtelogapiacr --image apisimple:latest .
```

2. Update the Web App

```bash
 az webapp update --resource-group inception-api-rg  --name iofmtelogapi
```