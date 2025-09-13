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