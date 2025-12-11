# 🔬 Autonomous Socionics Research Lab

A multi-agent AI system that researches fictional characters and determines their Socionics personality type through web search and parallel analysis.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge)

## ✨ Features

- **Multi-Agent Analysis**: Three specialist AI agents analyze characters from different Socionics perspectives:
  - **Agent Reinin** - Analyzes Reinin Dichotomies
  - **Agent Quadra** - Analyzes Quadra Values
  - **Agent Functions** - Analyzes Model A Functions

- **The Scout**: Automated web research to gather character information and build a comprehensive dossier

- **The Council**: Parallel analysis by specialist agents with live discussion and debate

- **The Validator**: Fact-checks theoretical claims for accuracy

- **The Manager**: Synthesizes all analyses into a final type determination

- **PDF Reports**: Generate downloadable PDF reports of your analysis

- **Analysis History**: Save and review past character analyses

- **Auto-Proceed Mode**: Automatically progress through all analysis phases

## 📋 Prerequisites

- Python 3.8 or higher
- An [OpenRouter API Key](https://openrouter.ai/) for AI model access

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/spaceynyc/socionics-panel.git
cd socionics-panel
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note for macOS/Linux:** If `pip` doesn't work, try `pip3 install -r requirements.txt`

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### 4. Configure Your API Key

1. In the sidebar, enter your **OpenRouter API Key**
2. Select your preferred AI model
3. Your settings will be saved automatically for future sessions

## 📁 Project Structure

```
socionics-panel/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── agents/                # AI Agent implementations
│   ├── scout.py          # Research agent (web search)
│   ├── council.py        # Analysis specialists (Reinin, Quadra, Functions)
│   └── manager.py        # Synthesis agent
├── config/                # Configuration files
│   ├── models.py         # OpenRouter model definitions
│   ├── prompts.py        # Agent prompts and instructions
│   └── socionics_kb.py   # Socionics knowledge base
├── utils/                 # Utility functions
│   ├── pdf_generator.py  # PDF report generation
│   └── search.py         # Web search utilities
├── styles/                # Custom CSS styling
│   └── main.css
└── .analysis_history/     # Saved analysis history (auto-created)
```

## 🎮 How to Use

### Starting a New Analysis

1. Enter the **Character Name** (e.g., "Walter White")
2. Enter the **Media Source** (e.g., "Breaking Bad")
3. Click **🚀 Begin Analysis**

### Analysis Phases

| Phase | Description |
|-------|-------------|
| **Phase 1: Research** | The Scout agent searches the web and builds a character dossier |
| **Phase 2: Analysis** | The Council (3 specialist agents) analyzes the dossier in parallel |
| **Phase 3: Discussion** | Agents review each other's work and debate their findings |
| **Phase 4: Synthesis** | The Manager produces a final type determination |

### Sidebar Options

- **Auto-proceed**: Enable to automatically progress through all phases
- **Reset Analysis**: Start over with a new character
- **History**: View and reload past analyses

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web application framework |
| `langchain` | LLM orchestration |
| `langchain-openai` | OpenAI/OpenRouter integration |
| `duckduckgo-search` | Web search for character research |
| `python-dotenv` | Environment variable management |
| `reportlab` | PDF report generation |

## ⚙️ Configuration

### AI Model

This application runs on **Google Gemini 3 Pro Preview** via OpenRouter. All agents use the same model for best results:

```
All Agents → google/gemini-3-pro-preview
```

### Changing Models

If you want to use a different model, edit `config/models.py`:

```python
# All agents use the same model - change this to use a different one
PRO_MODEL = "google/gemini-3-pro-preview"
MID_MODEL = "google/gemini-3-pro-preview"
FLASH_MODEL = "google/gemini-3-pro-preview"
```

You can replace these with any model available on [OpenRouter](https://openrouter.ai/models).

### Persistent Settings

Your preferences are automatically saved to `.user_config.json`:
- API Key
- Auto-proceed preference

## 🔧 Troubleshooting

### Common Issues

**"Please enter your OpenRouter API key"**
- Ensure you have a valid API key from [openrouter.ai](https://openrouter.ai/)
- Check that the key is correctly entered in the sidebar

**Research phase takes too long**
- Web search depends on DuckDuckGo availability
- Some characters may have limited online information

**PDF download fails**
- Ensure `reportlab` is properly installed
- Check console for specific error messages

### Running in Headless Mode

For server deployments:

```bash
streamlit run app.py --server.headless true
```

## 📄 License

This project is for educational and research purposes.

---

**Made with ❤️ for the Socionics community**
