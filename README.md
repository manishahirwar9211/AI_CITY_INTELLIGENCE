# 🌍 AI City Intelligence

An AI-powered **City Intelligence and Travel Assistant** built with **Python, LangChain, Mistral AI, Streamlit, and multiple real-world APIs**.

The application uses an AI agent that automatically selects and calls the appropriate tools based on the user's request. It can provide information about **weather, air quality, news, tourist places, restaurants, directions, hotels, and currency conversion**.

---

## 🚀 Features

* 🌤️ **Weather Information**

  * Get current temperature and weather conditions for a city.

* 🌫️ **Air Quality**

  * Get AQI, PM2.5, PM10, CO, NO₂ and O₃ information.

* 📰 **Latest City News**

  * Search for the latest news about a city.

* 📍 **Tourist Places**

  * Find interesting places and attractions to visit.

* 🍴 **Restaurants**

  * Find restaurants in a selected city.

* 🗺️ **Directions**

  * Calculate driving distance, estimated travel time and toll information.

* 🏨 **Hotels**

  * Search for available hotels and display hotel information such as ratings and prices.

* 💱 **Currency Conversion**

  * Convert currencies using current exchange-rate data.

* 🤖 **AI Agent**

  * Automatically selects the appropriate tool based on the user's question.
  * Can use multiple tools for complex travel-related requests.

* 💬 **Chat Interface**

  * Interactive Streamlit chat interface for asking multiple questions.

---

## 🧠 How It Works

The project uses a **LangChain AI Agent** as the central decision-maker.

```text
                    🌍 USER
                       |
                       v
              🤖 LANGCHAIN AGENT
                       |
        --------------------------------
        |       |       |       |       |
        v       v       v       v       v
     Weather  Places  Hotels  News  Restaurants
        |       |       |       |       |
   OpenWeather Geoapify StayingAPI Tavily Geoapify

        --------------------------------
        |       |       |
        v       v       v
   Directions  AQI  Currency
        |       |       |
     Geoapify OpenWeather Frankfurter
```

The user does not need to manually select a tool.

For example:

> "What is the weather in Jaipur?"

The agent identifies that the **weather tool** is required and calls it automatically.

For a more complex query:

> "I'm visiting Jaipur for two days. Check the weather and suggest places and restaurants."

The agent can select multiple tools to gather the required information.

---

## 🛠️ Technologies Used

### Programming

* Python

### AI / LLM

* LangChain
* Mistral AI
* LangChain Agents
* Tool Calling

### Web Application

* Streamlit

### APIs

* OpenWeather API
* Geoapify API
* Tavily API
* StayingAPI
* Frankfurter API

### Other Libraries

* Requests
* python-dotenv

---

## 🔧 Tools

The project currently contains the following tools:

| Tool                | Purpose             | API         |
| ------------------- | ------------------- | ----------- |
| `get_weather()`     | Current weather     | OpenWeather |
| `get_news()`        | Latest city news    | Tavily      |
| `get_places()`      | Tourist attractions | Geoapify    |
| `get_restaurants()` | Restaurants         | Geoapify    |
| `get_directions()`  | Driving directions  | Geoapify    |
| `get_air_quality()` | Air pollution data  | OpenWeather |
| `get_hotels()`      | Hotel search        | StayingAPI  |
| `get_currency()`    | Currency conversion | Frankfurter |

---

## 📁 Project Structure

```text
AI-City-Intelligence/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
└── assets/
    └── screenshots/
```

> `.env` should never be uploaded to GitHub.

---

## 🔑 Environment Variables

Create a `.env` file for local development:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
GEOAPIFY_API_KEY=your_geoapify_api_key
STAYING_API_KEY=your_stayingapi_api_key
```

The Frankfurter API does not require an API key.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AI-City-Intelligence.git
```

### 2. Open the project

```bash
cd AI-City-Intelligence
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

#### macOS / Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Add API keys

Create a `.env` file and add your API keys.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 💡 Example Queries

You can ask questions such as:

```text
What is the weather in Bhopal?
```

```text
What is the air quality in Delhi?
```

```text
What are the best places to visit in Jaipur?
```

```text
Find restaurants in Mumbai.
```

```text
Give me directions from Bhopal to Delhi.
```

```text
Find hotels in Jaipur.
```

```text
Convert 5000 INR to USD.
```

### Multi-tool Example

```text
I'm planning a trip to Jaipur. Check the weather,
suggest tourist places, and find restaurants.
```

The AI agent automatically decides which tools are required.

---

## 🤖 Agent Workflow

The basic workflow is:

```text
User Query
    ↓
LangChain Agent
    ↓
Understand User Intent
    ↓
Select Tool(s)
    ↓
Call External API
    ↓
Receive Tool Results
    ↓
LLM Processes Results
    ↓
Final Response
```

---

## 🔐 API Security

API keys are stored using environment variables and should **never be hardcoded** in the source code.

The `.gitignore` file should contain:

```gitignore
.env
__pycache__/
*.pyc
```

For Streamlit deployment, API keys can be added through **Streamlit Secrets** instead of committing them to GitHub.

---

## ☁️ Deployment

The application can be deployed using **Streamlit Community Cloud**.

Basic deployment steps:

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Select the GitHub repository.
4. Select `app.py`.
5. Add the required API keys under **Secrets**.
6. Deploy the application.

Required secrets:

```toml
OPENWEATHER_API_KEY = "your_key"
TAVILY_API_KEY = "your_key"
GEOAPIFY_API_KEY = "your_key"
STAYING_API_KEY = "your_key"
```

---

## 🎯 Project Objective

The main objective of this project is to demonstrate how **LLM-powered agents can interact with external APIs and tools to solve real-world problems**.

Instead of building separate applications for weather, restaurants, hotels, directions, news and currency conversion, this project combines them into a single **AI-powered travel assistant**.

---

## 📚 Concepts Demonstrated

This project demonstrates practical implementation of:

* Large Language Models (LLMs)
* LangChain
* AI Agents
* Tool Calling
* Function Calling
* API Integration
* Multiple Tool Orchestration
* Prompt Engineering
* Environment Variables
* Streamlit
* Error Handling
* Real-time Data Retrieval
* Multi-step AI Workflows

---

## 🔮 Future Improvements

* 📅 Dynamic check-in and check-out dates for hotel searches
* 🗓️ AI-generated day-wise travel itineraries
* 🧠 Conversation memory for follow-up questions
* 💰 Travel budget estimation
* 🚆 Flight and train information
* 🌦️ Weather forecasting
* 📊 Travel cost analysis
* 🗺️ Interactive maps
* ⚡ API response caching
* 📈 LangSmith monitoring and tracing
* 🎯 Personalized travel recommendations

---

## 👨‍💻 Author

**Manish Ahirwar**

B.Tech – Electrical & Electronics Engineering

Interested in **Data Analytics, Artificial Intelligence, Machine Learning and Generative AI**.

---

## ⭐ If You Like This Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.
