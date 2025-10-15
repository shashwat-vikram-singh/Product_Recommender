import pandas as pd
import random
import itertools

print("Starting data generation process...")

# --- Configuration ---
NUM_PRODUCTS = 200
NUM_USERS = 50
NUM_INTERACTIONS = 1200
USER_ID_START = 101

# --- Expanded Product Details ---
categories_config = {
    "Electronics": {
        "adjectives": ["Wireless", "Smart", "4K", "Portable", "Gaming", "Ultra-Slim"],
        "nouns": ["Headphones", "Speaker", "Monitor", "Charger", "Mouse", "Keyboard"],
        "platforms": ["Amazon", "Best Buy", "Newegg"]
    },
    "Home Goods": {
        "adjectives": ["Ergonomic", "Handmade", "Minimalist", "Electric", "Non-Stick"],
        "nouns": ["Coffee Maker", "Blender", "Desk Chair", "Air Fryer", "Cookware Set"],
        "platforms": ["Amazon", "Target", "Wayfair"]
    },
    "Apparel": {
        "adjectives": ["Vintage", "Athletic", "Denim", "Waterproof", "Organic Cotton"],
        "nouns": ["Jacket", "T-Shirt", "Running Shoes", "Jeans", "Backpack"],
        "platforms": ["Nike", "ASOS", "Amazon"]
    },
    "Books": {
        "adjectives": ["Bestselling", "Classic", "Sci-Fi", "Fantasy", "Historical"],
        "nouns": ["Novel", "Biography", "Cookbook", "Anthology", "Graphic Novel"],
        "platforms": ["Amazon", "Barnes & Noble", "Audible"]
    },
    "Sports & Outdoors": {
        "adjectives": ["Durable", "Lightweight", "Insulated", "All-Weather", "Professional"],
        "nouns": ["Yoga Mat", "Dumbbell Set", "Tent", "Water Bottle", "Basketball"],
        "platforms": ["Amazon", "REI", "Dick's Sporting Goods"]
    }
}

# --- Generate Products ---
products = []
product_names = set()
product_id_counter = 1

for category, details in categories_config.items():
    # Create all unique combinations of adjectives and nouns for the category
    combinations = list(itertools.product(details["adjectives"], details["nouns"]))
    random.shuffle(combinations)
    
    for adj, noun in combinations:
        if product_id_counter > NUM_PRODUCTS:
            break
        
        name = f"{adj} {noun}"
        if name not in product_names:
            products.append({
                "product_id": product_id_counter,
                "product_name": name,
                "category": category,
                # Simple placeholder image URL logic
                "image_url": f"https://placehold.co/600x400/0c1021/e0e0e0?text={name.replace(' ', '+')}",
                "platforms": "|".join(details["platforms"])
            })
            product_names.add(name)
            product_id_counter += 1

products_df = pd.DataFrame(products)
products_df.to_csv('data/products.csv', index=False)
print(f"✅ Generated {len(products_df)} unique products in 'data/products.csv'")

# --- Generate User Behavior ---
user_preferences = {
    user_id: random.choice(list(categories_config.keys()))
    for user_id in range(USER_ID_START, USER_ID_START + NUM_USERS)
}

interactions = []
for _ in range(NUM_INTERACTIONS):
    user_id = random.choice(list(user_preferences.keys()))
    
    # 80% chance the user views something from their preferred category
    if random.random() < 0.8:
        preferred_cat = user_preferences[user_id]
        possible_products = products_df[products_df['category'] == preferred_cat]
    else:
        possible_products = products_df

    if not possible_products.empty:
        viewed_product_id = random.choice(possible_products['product_id'].tolist())
        interactions.append({
            "user_id": user_id,
            "viewed_product_id": viewed_product_id
        })

behavior_df = pd.DataFrame(interactions).drop_duplicates()
behavior_df.to_csv('data/user_behavior.csv', index=False)
print(f"✅ Generated {len(behavior_df)} unique user interactions in 'data/user_behavior.csv'")
print("\nData generation complete!")