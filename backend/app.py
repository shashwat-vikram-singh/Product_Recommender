import os
import pandas as pd
import uuid
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

# -- Configuration Constants ---
NUM_USERS = 50
USER_ID_START = 101

# --- Get the absolute path for data files to work correctly on Render ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_CSV_PATH = os.path.join(BASE_DIR, 'data', 'products.csv')
BEHAVIOR_CSV_PATH = os.path.join(BASE_DIR, 'data', 'user_behavior.csv')

# --- App and API Configuration ---
load_dotenv()
app = Flask(__name__)
# Allows your Vercel frontend to talk to your Render backend
CORS(app, supports_credentials=True)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Data Loading ---
try:
    print(f"Attempting to load products from: {PRODUCTS_CSV_PATH}")
    products_df = pd.read_csv(PRODUCTS_CSV_PATH)
    print(f"Attempting to load behavior from: {BEHAVIOR_CSV_PATH}")
    behavior_df = pd.read_csv(BEHAVIOR_CSV_PATH)
    print("--- Data files loaded successfully! ---")
except FileNotFoundError as e:
    print(f"FATAL ERROR: Could not find data files. The server will not work. Error: {e}")
    products_df = pd.DataFrame()
    behavior_df = pd.DataFrame()


# --- Recommendation Logic (Unchanged) ---
def get_recommendations(user_id):
    if behavior_df.empty or products_df.empty:
        return pd.DataFrame()
        
    user_viewed_products = behavior_df[behavior_df['user_id'] == user_id]['viewed_product_id'].unique()
    if len(user_viewed_products) == 0:
        return products_df.sample(n=3, replace=True)
    similar_users = behavior_df[behavior_df['viewed_product_id'].isin(user_viewed_products)]
    similar_users = similar_users[similar_users['user_id'] != user_id]
    if similar_users.empty:
        viewed_categories = products_df[products_df['product_id'].isin(user_viewed_products)]['category'].unique()
        recommendations = products_df[products_df['category'].isin(viewed_categories)]
        return recommendations[~recommendations['product_id'].isin(user_viewed_products)].head(3)
    recommendation_pool = behavior_df[behavior_df['user_id'].isin(similar_users['user_id'])]['viewed_product_id']
    recommendations = recommendation_pool[~recommendation_pool.isin(user_viewed_products)]
    if recommendations.empty:
        return products_df[~products_df['product_id'].isin(user_viewed_products)].sample(n=3, replace=True)
    top_recs_ids = recommendations.value_counts().nlargest(3).index.tolist()
    return products_df[products_df['product_id'].isin(top_recs_ids)]


# --- API Endpoint with Debugging ---
@app.route('/recommendations', methods=['GET'])
def recommendations_endpoint():
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        print(f"New user detected. Assigning ID: {user_id}")
    
    pseudo_int_id = int(uuid.UUID(user_id).int % NUM_USERS) + USER_ID_START
    
    recommended_products = get_recommendations(pseudo_int_id)
    user_history_ids = behavior_df[behavior_df['user_id'] == pseudo_int_id]['viewed_product_id']
    user_history_df = products_df[products_df['product_id'].isin(user_history_ids)]
    
    if recommended_products.empty:
        return jsonify([])

    user_history_str = ', '.join(user_history_df['product_name'].tolist()) if not user_history_df.empty else "a variety of items"
    recs_list_str = '\n'.join([f"- {row['product_name']}" for _, row in recommended_products.iterrows()])
    
    prompt = f"""
A user has previously viewed: {user_history_str}.

Based on this history, we are recommending the following products:
{recs_list_str}

For each recommended product, provide a short, exciting, one-sentence explanation for why the user might like it. Start each explanation with the exact product name followed by a colon.

Example format:
Product Name 1: Because you liked [related item], you'll love this one's features.
Product Name 2: Since you're interested in [category], this is a perfect match.
"""

    # --- DEBUGGING STEP 1: Log the prompt being sent ---
    print("-----------------------------------------")
    print("--- PROMPT SENT TO GEMINI ---")
    print(prompt)
    print("-----------------------------------------")

    explanation_map = {}
    try:
        model = genai.GenerativeModel('models/gemini-pro-latest')
        response = model.generate_content(prompt)
        explanations_text = response.text.strip()
        
        # --- DEBUGGING STEP 2: Log the raw response from Gemini ---
        print("--- RESPONSE RECEIVED FROM GEMINI ---")
        print(explanations_text)
        print("-----------------------------------------")

        for line in explanations_text.split('\n'):
            if ':' in line:
                parts = line.split(':', 1)
                product_name = parts[0].strip().lstrip('- ').strip()
                explanation = parts[1].strip()
                explanation_map[product_name] = explanation

    except Exception as e:
        # --- DEBUGGING STEP 3: Log any error that occurs ---
        print("!!!!!! ERROR CALLING GEMINI API !!!!!!")
        print(e)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    response_data = []
    for _, product in recommended_products.iterrows():
        product_dict = product.to_dict()
        product_name = product_dict['product_name']
        product_dict['explanation'] = explanation_map.get(product_name, "This would be a great addition to your collection!")
        response_data.append(product_dict)
            
    response = make_response(jsonify(response_data))
    response.set_cookie('user_id', user_id, max_age=60*60*24*365, samesite='None', secure=True)
    
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
