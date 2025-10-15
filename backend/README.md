# Backend Service for AI Recommender

This directory contains the Python Flask server that powers the AI Product Recommender. It handles the core recommendation logic, integrates with the Google Gemini API, and manages user identification via cookies.

---

## 核心功能 (Core Functionality)

-   **🤖 Recommendation Engine:** Implements a collaborative filtering algorithm using the Pandas library to analyze a large, generated dataset of user behavior.
-   **✍️ LLM Integration:** Connects to the Google Gemini API to generate dynamic, natural language explanations for each recommendation.
-   **🍪 Automatic User Management:** Assigns a unique ID via a browser cookie to new visitors and recognizes them on subsequent visits, creating a seamless, login-free experience.
-   **REST API:** Exposes a single endpoint to serve personalized recommendations to the frontend.
-   **Rate Limiting:** Includes a delay mechanism to work within the free tier limitations of the Gemini API.

---

## 🔗 API Endpoints

### Get Recommendations

-   **URL:** `/recommendations`
-   **Method:** `GET`
-   **Description:** Fetches 3 personalized product recommendations for the user. It automatically identifies the user via their `user_id` cookie. If no cookie is present, a new one is generated and sent back with the response.
-   **Success Response (200 OK):**
    ```json
    [
      {
        "category": "Electronics",
        "explanation": "Because you liked the Smart Keyboard, you'll love how these Wireless Headphones complete your tech setup!",
        "image_url": "[https://placehold.co/600x400/](https://placehold.co/600x400/)...",
        "platforms": "Amazon|Best Buy|Newegg",
        "product_name": "Wireless Headphones"
      },
      // ... 2 more products
    ]
    ```

---

## 🛠️ Technology Stack

-   **Flask:** Micro web framework for building the API.
-   **Pandas:** For efficient data manipulation and analysis of the CSV files.
-   **google-generativeai:** The official Python client for the Google Gemini API.
-   **python-dotenv:** For managing environment variables (like API keys).
-   **Flask-Cors:** To handle Cross-Origin Resource Sharing with the frontend, specifically with cookie support.

---

## 🚀 Setup and Running

1.  **Navigate to this Directory:**
    ```bash
    cd backend
    ```
2.  **Create & Activate Virtual Environment:**
    ```bash
    python -m venv venv
    
    # On Windows
    .\venv\Scripts\Activate.ps1
    
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install Flask pandas python-dotenv Flask-Cors google-generativeai
    ```
    *(**Pro-tip:** After installing, you can create a `requirements.txt` file for easier setup by running `pip freeze > requirements.txt`)*

4.  **Create `.env` File:** Create a file named `.env` in this directory and add your Google Gemini API key:
    ```
    GOOGLE_API_KEY=YOUR_API_KEY_HERE
    ```
5.  **Generate Data (Run Once):**
    ```bash
    python generate_huge_data.py
    ```
6.  **Run the Server:**
    ```bash
    python app.py
    ```
    The server will be running on `http://127.0.0.1:5000`.