# ✨ AI-Powered E-commerce Product Recommender

This project is a complete, full-stack application that provides personalized product recommendations to users. It combines a collaborative filtering algorithm with the Google Gemini Large Language Model to generate human-like explanations for why each product is recommended.

The application features a stunning, animated "Aurora" user interface and automatically identifies users via browser cookies to track their behavior, creating a dynamic and engaging user experience without requiring a login.



---

## Core Features

-   **🤖 Collaborative Filtering:** Recommends products by finding "taste twins"—other users who have viewed similar items from a large, dynamically generated dataset.
-   **✍️ AI-Powered Explanations:** Utilizes the Google Gemini API to generate a unique, context-aware reason for each recommendation ("*Because you liked X, you might love Y!*").
-   **🍪 Automatic User Tracking:** Seamlessly identifies new and returning users with browser cookies, requiring no login or manual user selection.
-   **🚀 Advanced Aurora UI:** A beautiful, animated UI built with vanilla technologies. It features a soft, drifting aurora gradient background and minimalist cards with subtle glow effects.
-   ** scalable Data Generation:** Includes a Python script to generate a large, realistic dataset of 200 products and over 1000 user interactions.

---

## 🛠️ Tech Stack

| Category      | Technology                                    |
| ------------- | --------------------------------------------- |
| **Backend** | Python, Flask, Pandas, Google Generative AI   |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript               |
| **Database** | CSV Files (for demonstration purposes)        |
| **DevOps** | Virtual Environments (venv)                   |

---

## 📂 Project Structure

```

product-recommender/
├── backend/
│   ├── data/
│   │   ├── products.csv         \# Generated product catalog
│   │   └── user\_behavior.csv    \# Generated user interactions
│   ├── venv/                    \# Virtual environment
│   ├── .env                     \# API keys and secrets
│   ├── app.py                   \# Main Flask API server
│   ├── generate\_huge\_data.py    \# Script to create the dataset
│   └── README.md                \# Backend-specific documentation
├── frontend/
│   ├── index.html               \# Main HTML page
│   ├── style.css                \# All styles and animations
│   ├── script.js                \# Frontend logic and API calls
│   └── README.md                \# Frontend-specific documentation
└── README.md                    \# This file

````

---

## 🚀 Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

-   Python 3.8+
-   An active Google Gemini API Key.

### Installation & Setup

**1. Clone the Repository**
```bash
git clone <your-repository-url>
cd product-recommender
````

**2. Set Up the Backend**

This is the core of the application.

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv

# On Windows
.\venv\Scripts\Activate.ps1

# On macOS/Linux
source venv/bin/activate

# Install the required Python packages
pip install Flask pandas python-dotenv Flask-Cors google-generativeai

# Create the environment file
# Create a new file named .env in the backend/ folder and add your API key
echo "GOOGLE_API_KEY=YOUR_GEMINI_API_KEY_HERE" > .env

# Generate the large dataset (run this only once)
python generate_huge_data.py
```

**3. Running the Application**

1.  **Start the Backend Server:** In your terminal (with the virtual environment active in the `backend` folder), run:

    ```bash
    python app.py
    ```

    The server will start on `http://127.0.0.1:5000`. Keep this terminal running.

2.  **Launch the Frontend:** In your file explorer, navigate to the `frontend` folder and open the `index.html` file directly in your web browser (like Chrome, Firefox, or Edge).

You can now click the **"Generate My Recommendations"** button to see the application in action\!

-----

## 👤 Author Information

  - **Name:** `Shashwat Vikram Singh`
  - **University Registration Number:** `22BCE11619`

<!-- end list -->

