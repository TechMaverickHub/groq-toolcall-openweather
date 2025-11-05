import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- Function Definition ---
def get_current_weather(location):
    """Get the current weather using OpenWeatherMap API"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}"
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return json.dumps({
            "location": location,
            "temperature": data['main']['temp'],
            "feels_like": data['main']['feels_like'],
            "humidity": data['main']['humidity'],
            "pressure": data['main']['pressure'],
            "wind_speed": data['wind']['speed'],
            "description": data['weather'][0]['description'],
            "icon": data['weather'][0]['icon']
        })
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"API Error: {str(e)}"})

# --- Define Tools ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        },   
    }
]

# --- Streamlit UI ---
st.set_page_config(page_title="Weather with Groq Function Calling", page_icon="☁️", layout="centered")

st.title("☁️ Groq Function Calling Weather Assistant")
st.caption("Powered by Groq LLM + OpenWeatherMap")

# Input box
city = st.text_input("Enter a city name", placeholder="e.g., Bengaluru, London, Tokyo")

# On button click
if st.button("Get Weather"):
    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        with st.spinner("Thinking..."):
            try:
                # Step 1: Ask model about weather
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": "user", "content": f"What is the weather like in {city}?"}],
                    tools=tools,
                    tool_choice="auto",
                )

                groq_response = response.choices[0].message
            
                # Step 2: Extract args and call function
                args = json.loads(groq_response.tool_calls[0].function.arguments)
                
                weather_result = get_current_weather(**args)
                
                # Step 3: Feed back to model for natural answer
                final_response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a weather assistant that summarizes JSON weather data into a clear, "
                            "structured, and consistent format. Always respond in the following text format:\n\n"
                            "🌍 Location: <city, country>\n"
                            "🌡️ Temperature: <temp>°C\n"
                            "💧 Humidity: <humidity>%\n"
                            "💨 Wind Speed: <wind_speed> m/s\n"
                            "🌤️ Description: <description>\n"
                            "Feels Like: <feels_like>°C | Pressure: <pressure> hPa\n\n"
                            "Do not add any commentary, extra text, or variation. "
                            "Only output this formatted summary using values from the provided JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"What is the weather like in {city}?",
                    },
                    {
                        "role": "assistant",
                        "content": f"Here is the JSON weather data: {weather_result}",
                    },
                ],
            )


                st.success("✅ Weather data retrieved successfully!")
                st.write(final_response.choices[0].message.content)

                # Optional: Show structured weather info
                weather_json = json.loads(weather_result)
                if "error" not in weather_json:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.image(f"http://openweathermap.org/img/wn/{weather_json['icon']}@2x.png")
                    st.markdown(f"### 🌍 {weather_json['location']}")
                    st.metric("🌡️ Temperature (°C)", weather_json["temperature"])
                    st.metric("💨 Wind Speed (m/s)", weather_json["wind_speed"])
                    st.metric("💧 Humidity (%)", weather_json["humidity"])
                    st.metric("🔽 Pressure (hPa)", weather_json["pressure"])
                    st.caption(f"Feels like {weather_json['feels_like']}°C — {weather_json['description'].capitalize()}")

                else:
                    st.error(weather_json["error"])


            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
