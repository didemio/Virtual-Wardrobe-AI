# Virtual Wardrobe AI

## 1. Project Description and Goal
The objective of this project is to develop an intelligent agent that serves as a personal stylist. The system analyzes the user's local clothing inventory data against real-time weather information to provide optimized outfit recommendations. 

**Goal:** To eliminate decision fatigue in daily planning by ensuring the user is appropriately dressed based on current environmental conditions.

## 2. AI and Agent-Based Approach
The system utilizes a **ReAct (Reasoning and Acting)** architecture:
- **Reasoning:** The agent analyzes the user's request, determines the necessary information (weather and inventory), and formulates a plan.
- **Acting:** The agent executes specific tool calls to retrieve data from external APIs and local storage.
- **Result:** The system synthesizes the gathered data into a human-readable recommendation report.

## 3. List of Tools
1. **WeatherAPI_Tool:** Connects to an external weather service (e.g., OpenWeatherMap) to fetch real-time temperature and precipitation data.
2. **Closet_Manager_Tool:** Manages the local `data/wardrobe.json` file to filter and retrieve available clothing items based on category and weather suitability tags.
3. **Outfit_Matcher_Tool:** Processes the weather data and inventory list to generate an optimized outfit combination recommendation.

## 4. Preliminary Programming Concepts
- **Object-Oriented Programming (OOP):** Implementing Agent and Tool structures as modular classes.
- **Data Serialization (JSON):** Managing clothing inventory using structured JSON files.
- **API Integration (requests/httpx):** Fetching real-time weather data.
- **Environment Management (.env):** Securing API keys using environment variables.
- **Error Handling:** Implementing `try-except` blocks to handle API failures, network issues, or data inconsistencies.

## 5. Deployment Preparation
- **Requirements:** The project requires Python 3.10+ and the libraries listed in `requirements.txt`.
- **Usage:**
  1. Clone the repository.
  2. Install dependencies: `pip install -r requirements.txt`
  3. Configure environment variables in a `.env` file.
  4. Execute the system using: `python src/main.py`
