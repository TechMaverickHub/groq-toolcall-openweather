# ☁️ Groq Function Calling Weather Demo

This repository demonstrates how to use **Groq’s LLM** with **function calling (tool use)** to fetch live weather data from the **OpenWeatherMap API**, and display it in a **Streamlit UI**.

---

## 🚀 Features

- Function calling integration with Groq LLM  
- Real-time weather data retrieval via OpenWeatherMap  
- Streamlit web app interface  
- JSON tool call parsing and structured response  

---

## 🧰 Tech Stack

- **Groq LLM API**
- **OpenWeatherMap API**
- **Streamlit**
- **Python 3.10+**
- **dotenv** for environment configuration

---

## ⚙️ Setup

```bash
git clone https://github.com/<your-username>/groq-function-calling-weather-demo.git
cd groq-function-calling-weather-demo
pip install -r requirements.txt
```

### Environment Variables Setup

1. Create a `.env` file in the root directory of the project:

   - **Windows**: Create a new file named `.env` in the project root
   - **Linux/Mac**: Run `touch .env` in the terminal

2. Add your API keys to the `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

**Where to get your API keys:**

- **Groq API Key**:
  - Visit [console.groq.com](https://console.groq.com)
  - Sign up or log in
  - Navigate to API Keys section
  - Create a new API key and copy it

- **OpenWeatherMap API Key**:
  - Visit [openweathermap.org/api](https://openweathermap.org/api)
  - Sign up for a free account
  - Go to your API keys section
  - Create a new API key (free tier includes 60 calls/minute)
  - Copy your API key

**Note**: The `.env` file is already included in `.gitignore` to keep your keys secure. Never commit your `.env` file to version control.
