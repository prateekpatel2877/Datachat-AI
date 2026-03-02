# 🤖 DataChat AI

> An AI-powered multi-modal file analyzer built with Groq + Llama 3.3 70B

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-API-orange?style=flat)
![LLaMA](https://img.shields.io/badge/Llama_3.3-70B-purple?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 🌐 Live Demo
👉 [Click here to try DataChat AI](https://datachat-ai-pro.streamlit.app/)

---

## 📌 About the Project

**DataChat AI** is a Generative AI powered application that allows users to upload any file — CSV, Excel, PDF, or Image — and ask questions about it in plain English. The app uses **Meta's Llama 3.3 70B** model for text analysis and **Llama 4 Scout** for vision/image analysis, both powered by the **Groq API** for ultra-fast inference.

---

## ✨ Features

- 📊 **CSV & Excel Analyzer** — Upload tabular data and ask AI questions about it
- 📄 **PDF Analyzer** — Extract and analyze text from any PDF file
- 🖼️ **Image Analyzer** — Upload images and ask AI to describe or analyze them
- 💬 **Chat History** — Multi-turn conversation memory within a session
- 📈 **Data Visualization** — Interactive Line, Bar, and Area charts with custom range slider
- 📥 **Download Answers** — Save AI responses as text files
- 🎨 **Professional Dark UI** — Clean, recruiter-friendly interface

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Core programming language |
| Streamlit | Web UI framework |
| Groq API | LLM inference engine |
| Llama 3.3 70B | Text & data analysis model |
| Llama 4 Scout | Vision & image analysis model |
| Pandas | Data processing |
| PDFPlumber | PDF text extraction |
| Python-dotenv | Secure API key management |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/prateekpatel2877/Datachat-AI.git
cd Datachat-AI
```

### 2. Create conda environment
```bash
conda create -n csv-ai-analyzer python=3.11
conda activate csv-ai-analyzer
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
Create a `.env` file in the project folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at 👉 [https://console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📸 Screenshots

![DataChat AI Screenshot](https://datachat-ai-pro.streamlit.app/)

---

## 🔑 API Key

This project uses the **Groq API** which is completely free. Get your API key at:
👉 [https://console.groq.com](https://console.groq.com)

---

## 👨‍💻 Author

**Prateek Patel**
- 📧 prateekpatel2877@gmail.com
- 💼 [LinkedIn](https://www.linkedin.com/in/prateek728/)
- 🐙 [GitHub](https://github.com/prateekpatel2877)

---

## 📄 License

This project is licensed under the MIT License.

---

⭐ **If you found this project helpful, please give it a star!** ⭐