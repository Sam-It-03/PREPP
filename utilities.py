import os, sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import pickle
import login as log
import random  #  ADDED for the non-repeating image logic

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load Data & Model
def load_data(self):
    try:
        self.df = pd.read_csv(resource_path("Pune_house_data.csv"))
        self.locations = sorted(self.df['site_location'].dropna().unique())
        self.area_types = sorted(self.df['area_type'].unique())
        self.site_map = {val: idx for idx, val in enumerate(self.locations)}
        self.area_map = {val: idx for idx, val in enumerate(self.area_types)}
        self.model = pickle.load(open(resource_path("pune_price_model.pkl"), "rb"))
    except Exception as e:
        print(f"Startup Error: {e}")

def center_window(window, width, height):
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def get_scatter_plot(master_frame, df, location):
    """Creates the Scatter Plot and returns the canvas"""
    for widget in master_frame.winfo_children(): widget.destroy()
    
    loc_data = df[df['site_location'] == location].copy()
    loc_data['total_sqft'] = pd.to_numeric(loc_data['total_sqft'], errors='coerce')
    loc_data['price'] = pd.to_numeric(loc_data['price'], errors='coerce')
    loc_data = loc_data.dropna(subset=['total_sqft', 'price'])

    fig, ax = plt.subplots(figsize=(5, 4), facecolor='#2b2b2b')
    ax.set_facecolor('#2b2b2b')
    ax.scatter(loc_data['total_sqft'], loc_data['price'], color='#00D2FF', alpha=0.6)
    ax.set_title(f"Price Distribution: {location}", color='white', pad=10)
    ax.set_xlabel("Sqft", color='white')
    ax.set_ylabel("Price (Lakhs)", color='white')
    ax.tick_params(colors='white', labelsize=8)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=master_frame)
    return canvas

def get_bar_chart(master_frame, df):
    """Creates the Comparison Bar Chart and returns the canvas"""
    for widget in master_frame.winfo_children(): widget.destroy()

    avg_prices = df.groupby('site_location')['price'].mean().sort_values()
    comparison_data = pd.concat([avg_prices.head(5), avg_prices.tail(5)])

    fig, ax = plt.subplots(figsize=(5, 4), facecolor='#2b2b2b')
    ax.set_facecolor('#2b2b2b')
    colors = ['#FF4B4B']*5 + ['#008CBA']*5
    comparison_data.plot(kind='barh', ax=ax, color=colors)
    ax.set_title("Pune Price Benchmarks (Avg Lakhs)", color='white', pad=10)
    ax.tick_params(colors='white', labelsize=8)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=master_frame)
    return canvas

# Property Image Shuffling Logic 
def get_shuffled_images(image_list):
    """Returns a shuffled copy of the input image list"""
    shuffled_copy = image_list[:] # Make a copy
    random.shuffle(shuffled_copy)  # Shuffle it
    return shuffled_copy

def show_login_screen(self):
    for widget in self.container.winfo_children(): widget.destroy()
    login_view = log.LoginFrame(self.container, on_success=self.show_main_app)
    login_view.pack(fill="both", expand=True)