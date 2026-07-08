import customtkinter as ctk
import pandas as pd
import components as cmt
import database as db
import random
from PIL import Image
import utilities as utl

class AffordabilityFrame(ctk.CTkFrame):
    def __init__(self, master, app_ref):
        super().__init__(master, fg_color="transparent")
        self.app = app_ref
        
    # 1. LOAD HOUSE THUMBNAILS (For the result cards)
        self.house_images = []
        for i in range(1, 11):
            try:
                img_path = utl.resource_path(f"h{i}.jpg")
                img = ctk.CTkImage(Image.open(img_path), size=(80, 80)) 
                self.house_images.append(img)
            except Exception as e:
                pass

    # 2. LOAD MAIN PLACEHOLDER IMAGE 
        try:
            placeholder_path = utl.resource_path("pune-city.png")
            self.placeholder_img = ctk.CTkImage(Image.open(placeholder_path), size=(1280, 720))
        except Exception as e:
            print(f"Could not load pune-city.png: {e}")
            self.placeholder_img = None
                
        self.setup_ui()

    def setup_ui(self):
        # Top Search Bar Area (Light/Dark mode background)
        search_bar = ctk.CTkFrame(self, fg_color=("#ffffff", "#2b2b2b"), corner_radius=15)
        search_bar.pack(fill="x", padx=20, pady=20)

        # Labels updated for Light/Dark mode text
        ctk.CTkLabel(search_bar, text="Target Location:", font=("Segoe UI", 14, "bold"), text_color=("black", "white")).pack(side="left", padx=(20, 10), pady=20)
        self.scan_loc = cmt.SearchableComboBox(search_bar, values=self.app.locations, width=250)
        self.scan_loc.pack(side="left", padx=10)

        ctk.CTkLabel(search_bar, text="Max Budget:", font=("Segoe UI", 14, "bold"), text_color=("black", "white")).pack(side="left", padx=(30, 10))
        self.scan_budget = ctk.CTkEntry(search_bar, placeholder_text="e.g. 80", width=120)
        self.scan_budget.pack(side="left", padx=(0, 5))

        self.scan_unit = ctk.CTkOptionMenu(search_bar, values=["Lakhs", "Crores"], width=90, fg_color="#444", button_color="#555")
        self.scan_unit.pack(side="left", padx=(0, 10))

        ctk.CTkButton(search_bar, text="🔍 Find Options", font=("Segoe UI", 14, "bold"), 
                      fg_color="#008CBA", hover_color="#005F80", command=self.scan_properties).pack(side="right", padx=20)

        self.scan_err = ctk.CTkLabel(self, text="", text_color="#FF4B4B")
        self.scan_err.pack()

        # Results Area
        self.scan_results = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scan_results.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
    # SHOW PUNE CITY IMAGE OR FALLBACK TEXT 
        if self.placeholder_img:
            ctk.CTkLabel(self.scan_results, image=self.placeholder_img, text="").pack(pady=40)
        else:
            ctk.CTkLabel(self.scan_results, text="Enter a location and budget to see real market options.", text_color="gray", font=("Segoe UI", 16)).pack(pady=50)

    def save_property(self, prop_dict, btn_ref):
        """Saves the property to the SQLite database"""
        if not db.is_saved(prop_dict):
            db.add_favorite(prop_dict)
            btn_ref.configure(text="✅ Saved", fg_color="#28a745", hover_color="#218838")

    def scan_properties(self):
        loc = self.scan_loc.get()
        try:
            input_budget = float(self.scan_budget.get())
            unit = self.scan_unit.get()
            self.scan_err.configure(text="")
            budget_in_lakhs = input_budget * 100 if unit == "Crores" else input_budget
        except ValueError:
            self.scan_err.configure(text="⚠️ Please enter a valid numeric budget.")
            return

        if not loc or loc not in self.app.locations:
            self.scan_err.configure(text="⚠️ Please select a valid location from the list.")
            return

    # THIS CLEARS THE BIG PUNE IMAGE!
        for widget in self.scan_results.winfo_children(): widget.destroy()

    # SHUFFLING SETUP FOR THIS SEARCH RESULT SET 
        shuffled_images_for_this_search = utl.get_shuffled_images(self.house_images)
        image_index_for_this_search = 0

        df = self.app.df.copy()
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        matches = df[(df['site_location'] == loc) & (df['price'] <= budget_in_lakhs)]
        matches = matches.sort_values(by='price', ascending=False).head(30)

        display_budget = f"₹{input_budget:g} {unit}"

        if matches.empty:
            ctk.CTkLabel(self.scan_results, text=f"No properties found in {loc} under {display_budget}.", text_color="#FF4B4B", font=("Segoe UI", 16)).pack(pady=50)
            return

        ctk.CTkLabel(self.scan_results, text=f"Found {len(matches)} options in {loc} under {display_budget}:", font=("Segoe UI", 18, "bold"), text_color="#00D2FF").pack(anchor="w", pady=(0, 10))

        for _, row in matches.iterrows():
            prop_dict = row.to_dict()
            
            card = ctk.CTkFrame(self.scan_results, fg_color=("#e0e0e0", "#1f1f1f"), corner_radius=10)
            card.pack(fill="x", pady=5, padx=5)
            
        # (NO REPEATS)
            if shuffled_images_for_this_search:
                safe_index = image_index_for_this_search % len(shuffled_images_for_this_search)
                house_img = shuffled_images_for_this_search[safe_index]
                ctk.CTkLabel(card, image=house_img, text="").pack(side="left", padx=(15, 0), pady=10)
                image_index_for_this_search += 1
            
            soc = str(row['society']).strip()
            society_name = soc if soc and soc != 'nan' else "Independent Property"
            info_text = f"🏢 {society_name}   |   🛏️ {row['size']}   |   📐 {row['total_sqft']} Sqft"
            price_text = f"₹{row['price']/100:.2f} Cr" if row['price'] >= 100 else f"₹{row['price']} L"

            is_saved = db.is_saved(prop_dict)
            btn_text = "✅ Saved" if is_saved else "❤️"
            btn_color = "#28a745" if is_saved else "#444"
            btn_hover = "#218838" if is_saved else "#FF4B4B"

            btn_save = ctk.CTkButton(card, text=btn_text, width=70, fg_color=btn_color, hover_color=btn_hover)
            btn_save.configure(command=lambda p=prop_dict, b=btn_save: self.save_property(p, b))
            btn_save.pack(side="right", padx=(10, 20), pady=15)

            ctk.CTkLabel(card, text=price_text, font=("Segoe UI", 16, "bold"), text_color="#00D2FF").pack(side="right", padx=10, pady=15)
            ctk.CTkLabel(card, text=info_text, font=("Segoe UI", 14), text_color=("black", "white")).pack(side="left", padx=20, pady=15)