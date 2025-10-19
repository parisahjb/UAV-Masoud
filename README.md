# 🚁 UAV Distribution Generator

AI-powered UAV trajectory generator with custom spatial distributions using LLMs.

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run app.py
```

## 📋 Features
- AI-powered distribution generation using Groq LLM
- Real-time trajectory visualization
- 6 comprehensive plots
- Interactive web interface

## 🔑 Setup
1. Get your API key from [console.groq.com](https://console.groq.com)
2. Enter it in the app sidebar
3. Generate distributions!

## 📁 Structure
- `app.py` - Streamlit web application
- `src/` - Core modules
  - `llm_generator.py` - LLM integration
  - `uav_system.py` - UAV trajectory system
  - `visualizations.py` - Plotting functions
