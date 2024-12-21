# 🌐 **llm Integration Hub**

A cloud-native, scalable API service designed to interact with advanced language models like **Groq's Llama3**, with plans to extend support for AWS Bedrock, NVIDIA Nim, and other cutting-edge AI frameworks.  


## 🛠️ **Project Overview**

This project enables querying large language models through a simple, secure API.  
It includes authentication, flexible deployment options, and support for future model integrations.  

**Core Features**:  
- Authentication with OAuth2.  
- Query the **Groq Cloud Llama3 model** and return results.  
- Future-proof architecture designed for multi-model integration.  
- Planned support for AWS Bedrock and NVIDIA NeMo models.  
- Deployment-ready for Kubernetes via Amazon EKS.

## 🚀 **Getting Started**

### **1. Clone the Repository**

```bash
git clone https://github.com/Achanandhi-M/llm-integration-hub.git
cd llm-integration-hub
```

### **2. Set Up Environment Variables**  

Create a `.env` file in the root directory with the following variables:  

```env
GROQ_API_KEY=your-groq-api-key
SECRET_KEY=your-secret-key-for-authentication
```

### **3. Install Dependencies**  

Ensure Python 3.9+ is installed, then run:

```bash
pip install -r requirements.txt
```

### **4. Run the Application**

Start the FastAPI development server:  

```bash
uvicorn main:app --reload
```

The server will be available at `http://localhost:8000`.

---

## 🔌 **API Endpoints**

### 1. **POST /login**
Authenticate and retrieve an access token.

#### Request:
```bash
curl -X POST "http://localhost:8000/login" \
-H "Content-Type: application/json" \
-d '{
    "username": "your-username",
    "password": "your-password"
}'
```

#### Response:
```json
{
    "access_token": "your-access-token"
}
```

---

### 2. **POST /query_model**
Query the Groq Cloud Llama3 model.  

#### Request:
```bash
curl -X POST "http://localhost:8000/query_model" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your-access-token" \
-d '{
    "query": "Explain the importance of large language models"
}'
```

#### Response:
```json
{
    "answer": " large Language models enable fast and efficient..."
}
```

---

## 🚧 **Current Progress and Future Plans**

### **Current Progress**
- Successfully integrated Groq Cloud API with a `/query_model` endpoint.
- Developed a secure authentication layer using OAuth2.

---

### **Future Updates**

1. **AWS Bedrock Integration**:
   - Add support for other AI models available via AWS Bedrock.
   - Enable dynamic backend switching for multi-model queries.

2. **NVIDIA Nim Integration**:
   - Explore NVIDIA Nim’s capabilities for conversational AI and other applications.
   - Implement APIs for Nim-based workflows.

3. **Cloud-Native Deployment**:
   - Deploy to **Amazon EKS** for scalability and reliability.
   - Integrate CI/CD pipelines for seamless updates.

4. **Enhanced Features**:
   - Caching for frequent queries.
   - Query analytics for performance monitoring.
   - Support for saving and managing user preferences.

---

## 📋 **Development Stack**

| Technology         | Purpose                           |
|---------------------|-----------------------------------|
| **FastAPI**         | API framework                   |
| **Python 3.9+**     | Core programming language        |
| **Groq Cloud API**  | Language model querying          |
| **OAuth2**          | Authentication mechanism         |
| **Kubernetes (EKS)**| Future deployment platform       |


## Author

Developed by Your Achanandhi M