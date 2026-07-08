# ✅ Git Commands to Push Pune House Price Predictor to GitHub

```bash
# Step 1: Navigate to your project folder
cd C:\Users\HP\Desktop\Punehouseproject

# Step 2: Set your Git identity (only needed once per system)
git config --global user.name "Samit Wadappi"
git config --global user.email "samitwadappi3031@gmail.com"

# Step 3: Remove any existing remote (if already set)
git remote remove origin

# Step 4: Add the correct GitHub repository URL
git remote add origin https://github.com/SamitWadappi/pune-house-price-predictor.git

# Step 5: Stage and commit all your files
git add .
git commit -m "Initial commit: Pune House Price Predictor with XGBoost

# Step 6: Set the main branch and push to GitHub
git branch -M main
git push -u origin main
```

# 🏘️ PREPP: Pune Real Estate Price Predictor

PREPP is a modern, full-stack Python desktop application that leverages Machine Learning to predict house prices in Pune, analyze market trends, and help users discover affordable homes. 

Built with a sleek, hardware-accelerated user interface, it bridges the gap between raw real estate data and a user-friendly software experience.

---

## ✨ Key Features

* **🧠 Machine Learning Price Predictor:** Input property details (BHK, Sqft, Location, Bathrooms) to get instant, accurate price estimates powered by a custom-trained Random Forest Regressor.
* **📊 Interactive Market Insights:** Dual-state Matplotlib charts embedded directly into the UI. View scatter plots of price distributions or bar charts comparing average prices across top neighborhoods.
* **🔍 Affordability Scanner:** Set a target location and a maximum budget to instantly filter historical market data and find real properties that match your criteria.
* **💾 Secure Local Accounts & Favorites:** A self-contained SQLite database handles user registration, secure login sessions ("Remember Me"), and allows users to save/remove favorite properties.
* **🌗 Modern UI/UX:** Built with CustomTkinter, featuring a fluid Dark/Light mode toggle, dynamic placeholder imagery, randomized property thumbnails, and a responsive maximized dashboard.

---

## 🛠️ Technology Stack

* **Language:** Python 3.x
* **Frontend/GUI:** `customtkinter`, `Pillow` (Image Processing)
* **Data Science & ML:** `scikit-learn`, `pandas`, `numpy`
* **Data Visualization:** `matplotlib`
* **Database:** `sqlite3` (Built-in)
* **Serialization:** `pickle`

---

## 📂 Project Architecture

The application is built using a modular, Separation-of-Concerns architecture:

* `pune_desktop_app.py`: **Main Entry Point** - Manages the root window and tab transitions.
* `login.py`: **Auth View** - Handles user registration, login, and secure database sessions.
* `dashboard.py`: **Predictor View** - Collects ML inputs and renders interactive Matplotlib charts.
* `affordability.py`: **Scanner View** - The search engine for filtering properties within a budget.
* `favorites.py`: **Saved View** - Reads and displays user-saved properties from the database.
* `database.py`: **Backend** - Auto-generates and manages SQLite tables (`users`, `session`, `favorites`).
* `utilities.py`: **Helper Module** - Handles PyInstaller asset paths, chart generation, and image shuffling.
* `components.py`: **Custom Widgets** - Stores reusable complex UI elements (like Searchable ComboBoxes).
* `train_model_with_6_features.py`: **Data Science Script** - Cleans raw CSV data and trains the `.pkl` model.

---

## 🚀 Installation & Setup

**1. Clone the repository or download the project files.**
Ensure all files, including `Pune_house_data.csv`, `pune_price_model.pkl`, and image assets (`logo.png`, `pune-city.jpg`, `h1.jpg`...`h10.jpg`) are in the root directory.

**2. Install dependencies:**
Open your terminal in the project folder and run:
```bash
pip install -r requirements.txt