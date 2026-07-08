
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("Pune_house_data.csv")

# Convert total_sqft to float safely
def convert_sqft_to_num(x):
    try:
        if '-' in str(x):
            parts = x.split('-')
            return (float(parts[0]) + float(parts[1])) / 2
        return float(x)
    except:
        return None

df['total_sqft'] = df['total_sqft'].apply(convert_sqft_to_num)

# Drop rows with missing or invalid data
df = df.dropna(subset=['total_sqft', 'size', 'bath', 'balcony', 'area_type', 'site_location', 'price'])

# Feature engineering
df['bhk'] = df['size'].apply(lambda x: int(str(x).split(' ')[0]) if isinstance(x, str) else 0)

# Encode categorical variables
area_type_map = {val: idx for idx, val in enumerate(sorted(df['area_type'].unique()))}
site_location_map = {val: idx for idx, val in enumerate(sorted(df['site_location'].unique()))}
df['area_type_encoded'] = df['area_type'].map(area_type_map)
df['site_location_encoded'] = df['site_location'].map(site_location_map)

# Final features and label
features = df[['total_sqft', 'bhk', 'bath', 'balcony', 'area_type_encoded', 'site_location_encoded']]
labels = df['price']



# Split data
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train model
model = XGBRegressor()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred) ** 0.5

r2 = r2_score(y_test, y_pred)

print(f"✅ Model trained successfully!")
print(f"📈 RMSE: {rmse}")
print(f"📊 R² Score: {r2}")

# Save model
with open("pune_price_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("💾 Model saved as pune_price_model.pkl")