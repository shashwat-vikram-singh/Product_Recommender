import os
import pandas as pd
import time
import uuid
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

# -- Configuration Constants ---
NUM_USERS = 50 # This must match the number of users in generate_huge_data.py
USER_ID_START = 101 # This must also match

print(f"--- Using google-generativeai version: {genai.__version__} ---")
load_dotenv()
app = Flask(__name__)
# Allow cookies to be sent from the frontend
CORS(app, supports_credentials=True)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

try:
    products_df = pd.read_csv('data/products.csv')
    behavior_df = pd.read_csv('data/user_behavior.csv')
except FileNotFoundError as e:
    print(f"FATAL ERROR: {e}. Please run 'python generate_huge_data.py' first.")
    exit()

def get_recommendations(user_id):
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

def get_llm_explanation(user_history, recommended_product):
    prompt = f"A user has previously viewed: {', '.join(user_history['product_name'].tolist())}. We are recommending '{recommended_product['product_name']}'. In one short, exciting sentence, explain why, starting with 'Because you liked...'"
    try:
        model = genai.GenerativeModel('models/gemini-pro-latest')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Google Gemini: {e}")
        return "This would be a great addition to your collection!"

@app.route('/recommendations', methods=['GET'])
def recommendations_endpoint():
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        print(f"New user detected. Assigning ID: {user_id}")
    
    # --- CRUCIAL UPDATE ---
    # This calculation now maps the unique cookie ID to one of our 50 user profiles.
    pseudo_int_id = int(uuid.UUID(user_id).int % NUM_USERS) + USER_ID_START
    
    recommended_products = get_recommendations(pseudo_int_id)
    user_history_ids = behavior_df[behavior_df['user_id'] == pseudo_int_id]['viewed_product_id']
    user_history_df = products_df[products_df['product_id'].isin(user_history_ids)]
    
    response_data = []
    for product in recommended_products.to_dict('records'):
        explanation = get_llm_explanation(user_history_df, product)
        response_data.append({
            "product_name": product['product_name'],
            "category": product['category'],
            "image_url": product['image_url'],
            "platforms": product['platforms'],
            "explanation": explanation
        })
        print("Waiting 31 seconds to avoid rate limit...")
        time.sleep(31)
        
    response = make_response(jsonify(response_data))
    response.set_cookie('user_id', user_id, max_age=60*60*24*365)
    
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)