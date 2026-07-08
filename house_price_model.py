import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle

print("✅ Script started!")

# 1. Load Data
try:
    df = pd.read_csv("Pune_house_data.csv")
    print("📊 Data loaded successfully:", df.shape)
except Exception as e:
    print("❌ Failed to load data:", e)
    exit()

# 2. Clean Data
df.dropna(inplace=True)
df.columns = df.columns.str.strip().str.lower()
print("🧹 Data cleaned:", df.shape)

# 3. Choose features and target:

# Extract BHK from 'size' column
df['bhk'] = df['size'].apply(lambda x: int(str(x).split(' ')[0]) if pd.notnull(x) else None)

# Clean again after adding bhk
df.dropna(subset=['total_sqft', 'bhk', 'bath', 'price'], inplace=True)

# Convert total_sqft to numeric (some values may be ranges like "2100 - 2850")
def convert_sqft(x):
    try:
        if '-' in str(x):
            a, b = x.split('-')
            return (float(a) + float(b)) / 2
        return float(x)
    except:
        return None

df['total_sqft'] = df['total_sqft'].apply(convert_sqft)
df.dropna(subset=['total_sqft'], inplace=True)

# Final feature selection
features = ['total_sqft', 'bhk', 'bath']
target = 'price'

X = df[features]
y = df[target]

# 4. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("📦 Split data:", X_train.shape, X_test.shape)

# 5. Train Model
from xgboost import XGBRegressor

model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)


# 6. Evaluate
y_pred = model.predict(X_test)
print("📈 RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("📊 R² Score:", r2_score(y_test, y_pred))

# 7. Save Model
with open("pune_price_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved as pune_price_model.pkl")

def get_prediction(model, sqft, bhk, bath, area_idx, loc_idx):
    """Handles the numeric processing and returns the raw price."""
    # Order must match exactly: [sqft, bhk, bath, balcony, area_type, location]
    features = np.array([[sqft, bhk, bath, 1, area_idx, loc_idx]])
    prediction = model.predict(features)[0]
    return prediction