# GrowledgePilot: Your AI-Powered Personalized Learning Companion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

---

## 🚀 Introduction

GrowledgePilot is an AI-powered personalized learning assistant designed to help you learn efficiently and enjoyably
across multiple domains. It combines the power of programming and AI to provide intelligent learning workflows,
personalized content, and interactive experiences, enabling you to overcome learning challenges and achieve continuous
knowledge growth.

## ✨ Features

- 🎯 **Personalized Learning Plans**: AI dynamically adjusts your learning path based on your interests, goals, and
  current proficiency.
- 🤖 **Interactive AI Tutoring**: Engage with AI for customized study guidance through text or voice.
- 🔍 **Real-Time Knowledge Updates**: Fetches latest news, stock prices, and data insights through integrated APIs.
- 📊 **Progress Tracking**: Stores and visualizes your learning progress using SQLite.

## 📚 How It Works

GrowledgePilot employs several key strategies to enhance your learning experience:

1. **Active Recall:** The AI assistant regularly asks you questions about what you've learned, forcing you to actively
   retrieve information from memory. This strengthens neural pathways and improves long-term retention.
2. **Spaced Repetition:**  (Future Feature) The system will track when you last interacted with specific concepts and
   strategically schedule reviews to optimize retention.
3. **Interleaving:** GrowledgePilot encourages you to switch between different subjects or topics within a learning
   session. This helps you build stronger connections between concepts and improves your ability to transfer knowledge
   to new situations.
4. **Elaboration:** The AI prompts you to explain concepts in your own words, connect them to your prior knowledge, and
   generate examples. This deepens your understanding and promotes critical thinking.

## 🛠 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourname/GrowledgePilot.git
cd GrowledgePilot
pip install -r requirements.txt
```

## 🚀 Quick Start

Run the main script:

```bash
python main.py
```

Or launch the Gradio-based UI:

```bash
python -m ui_pages.run
```

## 📂 Project Structure

```
GrowledgePilot/
│── models/          # Data models
│── ai_agents/       # AI-driven learning agents
│── controllers/     # API interaction and logic control
│── data/            # SQLite database
│── ui_pages/        # Gradio-based UI
│── utils/           # Utility functions
│── settings.py      # Configuration settings
│── logger_conf.py   # Logging setup (Loguru)
│── main.py          # Entry point
```

## 🤝 Contributing

We welcome contributions! Feel free to fork the repo, submit PRs, and join the discussion.

## 📜 License

Licensed under the MIT License. See `LICENSE` for details.

