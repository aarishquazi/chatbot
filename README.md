
# 🤖 AI Chatbot Assistant with Sources

This is a **Streamlit-based intelligent chatbot** built using [CrewAI](https://github.com/joaomdmoura/crewAI) and powered by Groq LLM. It performs intelligent search, web scraping, and provides responses with sources and contact details when available. Designed as a research assistant, it can answer user queries with detailed, verified information from the web.

---

## 🧠 Features

- 🔍 Real-time web search with [Serper.dev](https://serper.dev)
- 🕸️ Website scraping using `ScrapeWebsiteTool`
- 📚 Source citation in every response
- 🧑‍💼 Contact info (names, phones, emails, addresses) for professionals or businesses
- 💬 Chat history and context-aware conversations
- 🛠️ Uses the CrewAI framework and Groq LLM
- 🌐 Easily deployable via Streamlit

---

## 📦 Requirements

- Python 3.9+
- Streamlit
- CrewAI
- crewai-tools
- python-dotenv

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Setup

Create a `.env` file in the root directory with your API keys:

```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
```

---

## 🚀 Running the App

```bash
streamlit run main.py
```

Once it runs, open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 💡 Example Queries

- “Find dermatologists in Mumbai with their contact information”
- “Top 3 restaurants in Paris with address and phone”
- “Latest news on artificial intelligence”
- “Python courses for beginners”

---

## 📸 UI Overview

The interface includes:
- A sidebar with configuration and example queries
- Chat history with timestamped interactions
- Input form to ask any question
- Responses with properly cited sources

---

## 🛡️ Disclaimer

> This chatbot provides publicly available information with source links and contact details. Please verify critical information from the original sources before making decisions.

---

## 📁 Project Structure

```
chatbot/
├── main.py         # Main Streamlit app
├── .env            # API keys (not included in repo)
├── requirements.txt (optional)
└── README.md       # Project documentation
```

---

## 🙋‍♂️ Author

**Aarish Quazi**  
🔗 [LinkedIn](https://linkedin.com/in/aarishquazi) · [GitHub](https://github.com/aarishquazi)

---

## ⭐️ Give a Star

If you like this project, consider giving it a ⭐️ on GitHub!
