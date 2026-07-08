import customtkinter as ctk
import database as db
import random
from PIL import Image
import utilities as utl

class FavoritesFrame(ctk.CTkFrame):
    def __init__(self, master, app_ref):
        super().__init__(master, fg_color="transparent")
        self.app = app_ref
        
    # LOAD PROPERTY IMAGES 
        self.house_images = []
        for i in range(1, 11):
            try:
                img_path = utl.resource_path(f"h{i}.jpg")
                img = ctk.CTkImage(Image.open(img_path), size=(80, 80)) 
                self.house_images.append(img)
            except Exception as e:
                pass
        
    # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header_frame, text="  Saved Properties", font=("Segoe UI", 24, "bold"), text_color="#00D2FF").pack(side="left")
        
    # Scrollable Area
        self.results_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.load_favorites()

    def remove_property(self, prop_id):
        """Removes from the database via ID and redraws"""
        db.remove_favorite(prop_id)
        self.load_favorites()

    def load_favorites(self):
        """Fetches all properties from SQLite and displays them"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        saved = db.get_all_favorites()
        
        if not saved:
            ctk.CTkLabel(self.results_frame, text="No favorite properties yet. Go to the Affordability tab to save some!", 
                         text_color="gray", font=("Segoe UI", 16)).pack(pady=50)
            return
            
    # SHUFFLING SETUP FOR THIS REFRESH 
        # Generate a new shuffled list of images for this specific refresh of the favorites screen
        shuffled_images_for_this_refresh = utl.get_shuffled_images(self.house_images)
        # local counter to keep track of our position in the shuffled list
        image_index_for_this_refresh = 0
            
        for prop in saved:
        # Card background updated
            card = ctk.CTkFrame(self.results_frame, fg_color=("#e0e0e0", "#1f1f1f"), corner_radius=10)
            card.pack(fill="x", pady=5, padx=5)
            
        # (NO REPEATS)
            if shuffled_images_for_this_refresh:
            # We use the modulo operator (%) to ensure the index always cycles from 0-9
                safe_index = image_index_for_this_refresh % len(shuffled_images_for_this_refresh)
                house_img = shuffled_images_for_this_refresh[safe_index]
                
                ctk.CTkLabel(card, image=house_img, text="").pack(side="left", padx=(15, 0), pady=10)
                
            # Increment the counter for the next card on this screen refresh
                image_index_for_this_refresh += 1
            
            soc = str(prop.get('society', '')).strip()
            society_name = soc if soc and soc != 'nan' else "Independent Property"
            loc = prop.get('site_location', 'Unknown')
            
            info_text = f"📍 {loc}   |   🏢 {society_name}   |   🛏️ {prop.get('size')}   |   📐 {prop.get('total_sqft')} Sqft"
            price = prop.get('price', 0)
            price_text = f"₹{price/100:.2f} Cr" if price >= 100 else f"₹{price} L"

            btn_remove = ctk.CTkButton(card, text="❌ Remove", width=70, fg_color="#444", hover_color="#FF4B4B",
                                       command=lambda pid=prop['id']: self.remove_property(pid))
            btn_remove.pack(side="right", padx=(10, 20), pady=15)
            
            ctk.CTkLabel(card, text=price_text, font=("Segoe UI", 16, "bold"), text_color="#00D2FF").pack(side="right", padx=10, pady=15)
            
        # Card text updated
            ctk.CTkLabel(card, text=info_text, font=("Segoe UI", 14), text_color=("black", "white")).pack(side="left", padx=20, pady=15)