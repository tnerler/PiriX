# 🤖 PiriX Chatbot 
![Project Logo](static/images/denizci-yunus-maskot.webp)

**PiriX** is an advanced **RAG-based chatbot** designed to structured MD formatted datasets. 
It can understand context, provide accurate responses, and operate securely using a OpenAI's LLM.

---

## ⚙️ Installation

```bash
# Clone repository
git clone https://github.com/your-username/pirix-chatbot.git
cd pirix-chatbot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```
**After, installing the requirements.txt file you need to install the right pytorch libraries for your required cuda version.
[You can check from here](https://pytorch.org/).Since my CUDA version is 12.9, I installed the version of CUDA 12.9
If you don't have CUDA in your pc: You can install from [***here***](https://developer.nvidia.com/cuda-downloads)**


### .env files
```bash
OPENAI_API_KEY=...
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=...
MONGO_URI=mongodb://localhost:27017/pirix_chatbot
DATABASE=pirix_chatbot
```
Of course, you need to install mongoDB in your pc to track user's log.

# How PiriX-Chatbot Works

This page explains the inner workings of **PiriX**, the information assistant for Piri Reis University. You don’t need to be an expert—just a little curiosity will do!

We’ll cover:

- How PiriX processes different types of data (PDFs, images, markdown, etc.)
- How it organizes and stores information
- How it uses AI to answer your questions
- Tips and tricks that make it faster and more efficient

By the end, you’ll have a clear understanding of what happens behind the scenes without diving too deep into technical details.

---

## Pre-Trained Models

PiriX doesn’t train its own models. Instead, it uses **pre-trained models** such as:

- **BGE-M3** and **text-embedding-3-large** for embeddings  
- **GPT-4o** for natural language generation

We rely on these models to save time, computing resources, and ensure high-quality answers. But using pre-trained models alone isn’t enough—we integrate them into a **RAG (Retrieval-Augmented Generation)** pipeline.

---

## What is RAG?

RAG is an architecture where:

1. **Relevant information is retrieved from external sources**  
2. **AI generates answers based on this information**

PiriX uses two main functions to achieve this:

1. **Retrieve Function** — finds the most relevant documents for a user’s question  
2. **Generate Function** — produces a precise answer based on the retrieved documents

---

### Retrieve Function

The retrieve function searches through all university data, including information on:

- Erasmus programs  
- Scholarships  
- Academic calendar  
- Bachelor’s degree programs  
- Transportation and more

The goal is simple: **get the data most relevant to the user’s question.**

#### How it works

1. Convert all documents into **chunks** of manageable size.  
2. Compute **embeddings** for each chunk and store them in a **FAISS vector database**.  
3. Use a **Cross-Encoder** to rerank the top results for relevance.  
4. Return the **top-ranked chunks** as context for the generate function.

---

### Generate Function

Once the relevant documents are retrieved, the generate function produces the answer:

1. The user’s question is analyzed and clarified using **chat history**.  
2. Relevant documents are provided as context.  
3. GPT-4o processes the question + context to produce a concise, accurate answer.  

This ensures that the chatbot answers based on the **latest, most relevant data** without hallucinating information.

---

## Why Not Train Our Own Model?

Training a model from scratch would require:

1. Re-training every time new data arrives  
2. Large amounts of clean, structured data  
3. Expertise in model design, tuning, and maintenance  
4. Powerful GPUs and lots of time  

Using **RAG with pre-trained models** allows PiriX to **stay updated efficiently** and deliver reliable answers without the overhead of training a full LLM.

---

## Data Handling

### Why Markdown Instead of JSON?

Initially, data came as PDFs and images. Converting to JSON was cumbersome:

- Multiple JSON loaders needed for different formats  
- Large codebase just to handle loading  

Switching to **Markdown** simplified this:

- Single loader for all documents  
- Easier updates with new unstructured data  
- Maintains efficiency without affecting answer quality

---

### Chunking

**Chunking** splits long documents into smaller, manageable pieces (chunks) so the LLM can handle them efficiently.  

- Each chunk: ~1000 words with 350-word overlap  
- Prevents hitting token limits  
- Improves retrieval accuracy  
- Reduces response latency

---

### Hashing Chunks

Each chunk gets a **hash (digital fingerprint)**:

- Same data → same hash  
- Different data → different hash  

Duplicate chunks are skipped, keeping storage efficient and retrieval accurate.

---

### Embedding Chunks

**Embeddings** convert text into **vectors** (numerical representations):

- Similar text → similar vectors  
- Stored in **FAISS vector database**  
- Enables fast similarity search for relevant documents

---

### Cross-Encoder

The **Cross-Encoder** ranks retrieved chunks for relevance:

1. Takes user’s question + chat history  
2. Compares each retrieved chunk  
3. Scores and reranks chunks  
4. Returns top 12 most relevant for the generate function

This ensures the chatbot uses **only the most relevant context** when answering.

---

## Putting It All Together

1. User asks a question  
2. Question is enhanced with chat history  
3. Retrieve function finds relevant chunks using embeddings + Cross-Encoder  
4. Generate function uses GPT-4o with context to produce a precise answer  
5. Response is returned to the user

This pipeline ensures **accurate, fast, and context-aware answers** without training a new model from scratch.
