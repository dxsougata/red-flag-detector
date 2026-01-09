# 🚩 Red Flag Detector

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://red-flag-detector-rwdrrznezgx22u5isqd5pk.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Groq](https://img.shields.io/badge/AI-Groq_Llama_3-orange)

An AI-powered application that analyzes chat screenshots and dating profiles to detect "red flags," toxic traits, and "cringe" behavior using computer vision.

**🔗 [Live Demo](https://red-flag-detector-rwdrrznezgx22u5isqd5pk.streamlit.app/)**

---


## ✨ Features

- **🚩 Red Flag Scanner**: Detects manipulation, gaslighting, and toxic phrases in text/images.
- **⚡ Rizz Rater**: Rates flirting skills on a scale of 1-10.
- **📝 Drama Summary**: Summarizes long, messy arguments instantly.
- **👁️ Computer Vision**: Powered by **Llama 3.2 Vision** (via Groq) to read text directly from images.
- **⚡ Blazing Fast**: Uses Groq LPUs for near-instant analysis.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Model**: Llama 3.2 Vision (11B/90B)
- **Inference Engine**: [GroqCloud](https://groq.com/)
- **Language**: Python

## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/dxsougata/red-flag-detector.git
   cd red-flag-detector

2. **Install dependencies**
```bash
    pip install -r requirements.txt
```

3. Set up API Keys
```bash
    Get a free API key from GroqCloud Console.
    Create a file named .streamlit/secrets.toml in your project folder:

    Ini, TOML

    # .streamlit/secrets.toml
    GROQ_API_KEY = "gsk_..."
```

4.Run the app

```Bash

    python -m streamlit run app.py
```

☁️ Deployment
This app is deployed on Streamlit Community Cloud.

To deploy your own version:

Fork this repo.

Go to Streamlit Cloud.

Connect your GitHub and deploy.

Add your GROQ_API_KEY in the Advanced Settings -> Secrets area.

🤝 Contributing
Got a funny idea for a new "flag"? Open an issue or submit a pull request!

Fork it.

Create your feature branch (git checkout -b feature/CoolNewMode).

Commit your changes.

Push to the branch.

Open a Pull Request.

Built with 🚩 and ☕ by Sougata
