# 🚁 UAV Distribution Generator

AI-powered UAV trajectory generator with custom spatial distributions using LLMs.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fkfynx7rdlkie7b5beisxz.streamlit.app/)

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run app.py
```

## 🔑 Setup

1. Get your API key from [console.groq.com](https://console.groq.com)
2. Enter it in the app sidebar when running
3. Generate distributions!

## ✨ Features

- 🤖 AI-powered distribution generation using Groq LLM
- 📊 6 comprehensive visualization plots
- 🎯 Custom distributions from text descriptions
- ⚡ Real-time trajectory generation
- 📈 Interactive Plotly and static Matplotlib options

## 📁 Project Structure
```
UAV-Masoud/
├── app.py                  # Streamlit web application
├── src/
│   ├── __init__.py        # Package initialization
│   ├── llm_generator.py   # LLM integration
│   ├── uav_system.py      # Core UAV system
│   └── visualizations.py  # Plotting functions
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

## 📋 Usage

1. **Enter API Key**: Add your Groq API key in the sidebar
2. **Select Distribution**: Choose preset or write custom description
3. **Adjust Parameters**:
   - Delta (δ): Minimum radius
   - Rho (ρ): Maximum radius  
   - Tau (τ): Time scale
   - Intervals: Number of trajectory points
4. **Generate**: Click the generate button
5. **View Results**: Explore the 6 generated plots

## 🎯 Example Distributions

- **Eastern 4x Denser**: Higher density in the right half
- **Center Hotspot**: Concentrated activity in center
- **Ring Pattern**: Dense ring at specific radius
- **Custom**: Any description you can imagine!

## 👤 Author

- GitHub: [@parisahjb](https://github.com/parisahjb)

## 📝 License

MIT License - feel free to use this project!
```

## ✅ **Quick Summary - Files You Need:**

After these steps, your repository should have:
```
UAV-Masoud/
├── app.py                  ✅ (you have it)
├── src/                    📁 (create by renaming)
│   ├── __init__.py        ➕ (create new)
│   ├── llm_generator.py   ♻️ (rename to src/...)
│   ├── uav_system.py      ♻️ (rename to src/...)
│   └── visualizations.py  ♻️ (rename to src/...)
├── requirements.txt       ✅ (you have it, verify content)
├── README.md             ✅ (update with more content)
├── .gitignore           ➕ (create new)
└── ❌ Delete __init__.py from root
