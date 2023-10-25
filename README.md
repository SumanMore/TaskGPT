# TaskGPT

## Introduction

This is a [Streamlit](https://streamlit.io/)-based ToDo application that incorporates:

1. CRUD functionalities
2. Chat feature integrated with Azure Open AI

## Prerequisites

1. [Log in to Azure using Azure CLI](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli#sign-in-interactively)

   ```bash
   az login
   ```

2. Ensure you are on the right Azure subscription before provisioning resources

   ```bash
   az account show --output table
   ```

   To switch to a different Azure subscription, run the following command:

   ```bash
   az account set --subscription "<REPLACE_WITH_AZURE_SUBSCRIPTION_NAME_OR_ID>"
   ```

3. Create an Azure Resource Group

    ```bash
    az group create --name $RESOURCE_GROUP_NAME --location $AZURE_REGION
    ```

    Follow [this](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-cli#create-resource-groups) for more information.

4. Create an Azure SQL Database resource

    4.1 Create a server

    ```bash
    az sql server create --name $server --resource-group $resourceGroup --location "$location" --admin-user $login --admin-password $password
    ```

    4.2 Create a database

    ```bash
    az sql db create --resource-group $resourceGroup --server $server --name $database --sample-name AdventureWorksLT --edition GeneralPurpose --compute-model Serverless --family Gen5 --capacity 2
    ```

    Once the Azure SQL Database is created: Note the value of database server, database name, database username, database password for later use.

5. [Create an Azure Open AI Resource](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource)

    Once Azure Open AI resource is created: Note the value of Open AI key and Open AI endpoint for later use.

## Architecture flow of the Application

### ToDo Flow

![Todo Flow image](./images/Picture1.png)

### Chat Flow with Open AI

![Chat Flow image](./images/Picture2.png)

## Technologies used

1. Streamlit
2. Azure Container Registry
3. Azure App Service
4. Azure SQL Database
5. Azure Open AI

## Getting Started

### Steps

1. Clone this github repository into your local machine and open it in VS code.

2. Setup environment variables:

    - Create an environment file ".env" file by copying the contents from [env_template](.env_template) file.
    - Fill in the values for Azure SQL Database credentials and Azure Open AI credentials in ".env" file that you noted down while creating Azure SQL Database and Azure Open AI earlier.

3. To run the application locally, follow the command:

    ```streamlit run main.py```

4. You will see that the application starts running on the local host with port number "8501":  

    ```http://localhost:8501```


### You can also deploy the application using various ways:

- Streamlit community cloud
- Azure App Service
- Docker
- Kubernetes
