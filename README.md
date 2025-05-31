# 🤖 AI Research Chatbot

A powerful, Streamlit-based AI chatbot that leverages **CrewAI** agents and tools to deliver **detailed answers with real-time web sources and contact information**. Ideal for tasks like professional lookup (e.g., doctors, lawyers), tutorial recommendations, news updates, and much more.

---

## 🚀 Features

- 🔍 Web search and scraping using Serper and ScrapeWebsiteTool  
- 🧠 LLM-powered responses with **Groq's DeepSeek LLaMA 70B**  
- 📄 Includes **citations and source links**  
- 📞 Provides **contact information** for professionals when available  
- 💬 Keeps **chat history** in memory during the session  
- 🎛️ Simple and elegant Streamlit UI  
- 🧰 Agent-based architecture using **CrewAI**

---

## 📦 Project Structure

ai-research-chatbot/
├── app.py # Main Streamlit application
├── .env # for groq api and serp api key environment variables
├── requirements.txt # Python dependencies
└── README.md # This file

## 🛠️ Tech Stack

- Streamlit

- CrewAI

- Groq LLM

- Serper.dev

- Python

##  📌 Notes

- Chat history is stored in st.session_state and is not persistent across refreshes.

- Requires internet access for Serper and ScrapeWebsiteTool to work.

- Ensure your API keys are valid, else the agent won’t initialize.

- Made with crew AI need some seconds for research

##  🧑‍💻 Author
Aarish Quazi
Python & AI Developer —Jaipur, India
