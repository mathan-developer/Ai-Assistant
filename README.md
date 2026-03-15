# AI Assistant Android App

An Android application that integrates **Artificial Intelligence using a RAG (Retrieval-Augmented Generation) pipeline**.
The project demonstrates how an Android app can interact with a **local AI backend** to answer technical interview questions.

The system combines an **Android frontend**, a **FastAPI backend**, and a **local LLM running with Ollama**.

---

# 🚀 Features

* Modern Android UI built with **Jetpack Compose**
* AI-powered responses using a **local LLM**
* **RAG pipeline** for retrieving relevant interview questions
* Semantic search using **Sentence Transformers**
* Clean Android architecture with **Redux-style state management**
* Backend API built with **FastAPI**

---

# 🏗 Architecture

```
User Question
      ↓
Android App
      ↓
FastAPI Backend (/ask)
      ↓
Embedding Model
      ↓
Vector Similarity Search
      ↓
Retrieve Context
      ↓
Local LLM (Ollama - Mistral)
      ↓
AI Response
```

The system retrieves relevant questions from a dataset and sends them as context to the LLM to generate better answers.

---

# 🛠 Tech Stack

### Android

* Kotlin
* Jetpack Compose
* Redux + ViewModel
* Hilt
* Retrofit
* OkHttp

### Backend

* FastAPI
* Ollama (Mistral model)
* Sentence Transformers
* Cosine similarity vector search

---

# 📂 Project Structure

```
project
│
├ android-app
├ backend
│   └ api_server.py
│
├ dataset
│   ├ questions.json
│   └ embeddings.json
│
├ scripts
│   └ generate_embeddings.py
```

---

# ⚙️ Setup

## 1. Install Ollama

Install Ollama and download the model:

```
ollama pull mistral
```

Run the model:

```
ollama run mistral
```

---

## 2. Start Backend

Install dependencies:

```
pip install fastapi sentence-transformers requests numpy uvicorn
```

Start the server:

```
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

---

## 3. Run Android App

1. Open the project in **Android Studio**
2. Run the app on an **Android Emulator**

The emulator connects to the backend using:

```
http://10.0.2.2:8000
```

---

# 📸 Screenshots

![img.png](img.png)

---

# 📄 License

MIT License
