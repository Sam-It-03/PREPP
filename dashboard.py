import customtkinter as ctk
import numpy as np
import components as cmt
import utilities as utl
import affordability
import favorites
from PIL import Image

class MainAppFrame(ctk.CTkFrame):
    def __init__(self, master, app_ref):
        super().__init__(master, fg_color="transparent")
        self.app = app_ref

 # ==========================================
# 🏢 HEADER SECTION
 # ==========================================
        header = ctk.CTkFrame(self, height=80, fg_color=("#e0e0e0", "#1f1f1f"), corner_radius=0)
        header.pack(fill="x", side="top")

        # 1. Logo
        try:
            icon_path = utl.resource_path("logo.png") 
            img_icon = ctk.CTkImage(Image.open(icon_path), size=(40, 40))
            lbl_icon = ctk.CTkLabel(header, image=img_icon, text="")
            lbl_icon.pack(side="left", padx=(30, 10), pady=10)
        except Exception as e:
            ctk.CTkLabel(header, text="🏠", font=("Segoe UI", 30)).pack(side="left", padx=(30, 10))

        # 2. Title
        ctk.CTkLabel(header, text="PREPP", font=("Segoe UI", 24, "bold"), text_color="#00D2FF").pack(side="left", padx=5, pady=10)

        # 3. RIGHT CONTROLS (Buttons & Welcome Text)
        right_container = ctk.CTkFrame(header, fg_color="transparent")
        right_container.pack(side="right", padx=20, pady=10)

    # Top row of right container (Buttons)
        btn_row = ctk.CTkFrame(right_container, fg_color="transparent")
        btn_row.pack(anchor="e")

        # 1. The Sun Icon (Left)
        ctk.CTkLabel(btn_row, text="☀️", font=("Segoe UI", 18)).pack(side="left", padx=(0, 5))

        # 2. The Switch (Middle)
        self.mode_switch = ctk.CTkSwitch(btn_row, text="", width=40, command=self.toggle_mode)
        self.mode_switch.select()  # Selects it by default so it matches Dark Mode
        self.mode_switch.pack(side="left", padx=0)

        # 3. The Moon Icon (Right)
        ctk.CTkLabel(btn_row, text="🌙", font=("Segoe UI", 18)).pack(side="left", padx=(5, 15))

        # 4. Logout Button
        ctk.CTkButton(btn_row, text="Logout", width=90, height=35, command=self.app.show_login_screen, 
                      fg_color="#444", hover_color="#FF4B4B", font=("Segoe UI", 13, "bold")).pack(side="left")

    # Bottom row of right container (Welcome Text)
        # grab the username 
        user_name = getattr(self.app, 'current_user', 'Member')
        
        ctk.CTkLabel(right_container, text=f"Welcome, {user_name}", font=("Segoe UI", 18, "italic"), 
                     text_color=("black", "#00D2FF")).pack(anchor="e", pady=(2, 0))

 # ==========================================
# 📑 TABS SECTION
 # ==========================================
        self.tabs = ctk.CTkTabview(
            self, 
            segmented_button_selected_color="#008CBA",
            segmented_button_selected_hover_color="#008CBA",
            segmented_button_unselected_color="#2b2b2b",
            segmented_button_unselected_hover_color="#2b2b2b",
            command=self.on_tab_change  
        )
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tab_dashboard = self.tabs.add("Dashboard")
        self.tab_affordability = self.tabs.add("Affordability")
        self.tab_history = self.tabs.add("Favorites")
        
        self.setup_dashboard_tab()
        self.setup_affordability_tab()
        self.setup_favorites_tab() 

 # =========================
# 🌓 THEME TOGGLE LOGIC
 # =========================
    def toggle_mode(self):
        """Switches between Dark and Light mode based on switch position"""
        if self.mode_switch.get() == 1:
            # Switch is on the right side (Moon)
            ctk.set_appearance_mode("dark")
        else:
            # Switch is on the left side (Sun)
            ctk.set_appearance_mode("light")


  # 1. DASHBOARD TAB LOGIC
    def setup_dashboard_tab(self):
        split_container = ctk.CTkFrame(self.tab_dashboard, fg_color="transparent")
        split_container.pack(fill="both", expand=True, pady=10)

    # Left Pane (Inputs)
        self.card = ctk.CTkFrame(split_container, fg_color=("#ffffff", "#2b2b2b"), corner_radius=15)
        self.card.pack(side="left", fill="y", padx=(10, 10), pady=10) 

        ctk.CTkLabel(self.card, text="Enter Property Details", font=("Segoe UI", 22, "bold"), text_color=("black", "white")).pack(pady=(20, 10))

        ctk.CTkLabel(self.card, text="Location:", font=("Segoe UI", 13, "bold"), text_color=("black", "white")).pack(anchor="w", padx=40, pady=(10, 2))
        self.opt_loc = cmt.SearchableComboBox(self.card, values=self.app.locations)
        self.opt_loc.pack(anchor="w", padx=40, pady=(0, 10))

        ctk.CTkLabel(self.card, text="Area Type:", font=("Segoe UI", 13, "bold"), text_color=("black", "white")).pack(anchor="w", padx=40, pady=(10, 2))
        self.opt_area = ctk.CTkOptionMenu(self.card, values=self.app.area_types, width=320)
        self.opt_area.pack(anchor="w", padx=40, pady=(0, 10))

        self.lbl_bhk = ctk.CTkLabel(self.card, text="Bedrooms: 1 BHK", font=("Segoe UI", 13, "bold"), text_color="#00D2FF")
        self.lbl_bhk.pack(anchor="w", padx=40, pady=(10, 2))
        self.sld_bhk = ctk.CTkSlider(self.card, from_=1, to=10, number_of_steps=9, width=320, 
                                     command=lambda v: self.lbl_bhk.configure(text=f"Bedrooms: {int(v)} BHK"))
        self.sld_bhk.set(1)
        self.sld_bhk.pack(anchor="w", padx=40, pady=(0, 10))

        ctk.CTkLabel(self.card, text="Square Feet:", font=("Segoe UI", 13, "bold"), text_color=("black", "white")).pack(anchor="w", padx=40, pady=(10, 2))
        self.ent_sqft = ctk.CTkEntry(self.card, placeholder_text="e.g. 1200", width=320)
        self.ent_sqft.pack(anchor="w", padx=40, pady=(0, 10))

        ctk.CTkLabel(self.card, text="Bathrooms:", font=("Segoe UI", 13, "bold"), text_color=("black", "white")).pack(anchor="w", padx=40, pady=(10, 2))
        self.ent_bath = ctk.CTkEntry(self.card, placeholder_text="e.g. 2", width=320)
        self.ent_bath.pack(anchor="w", padx=40, pady=(0, 20))

        self.lbl_err = ctk.CTkLabel(self.card, text="", text_color="#FF4B4B")
        self.lbl_err.pack()

        ctk.CTkButton(self.card, text="Predict Price", font=("Segoe UI", 15, "bold"),
                      command=self.predict, height=45, width=320, 
                      fg_color="#008CBA", text_color="white", hover_color="#005F80").pack(pady=10)
        
        self.lbl_res = ctk.CTkLabel(self.card, text="", font=("Segoe UI", 36, "bold"), text_color="#00D2FF")
        self.lbl_res.pack(pady=(5, 20))

    # Right Pane (Charts)
        self.trends_card = ctk.CTkFrame(split_container, fg_color=("#ffffff", "#2b2b2b"), corner_radius=15)
        self.trends_card.pack(side="right", fill="both", expand=True, padx=(10, 10), pady=10)
        
        self.chart_header_frame = ctk.CTkFrame(self.trends_card, fg_color="transparent")
        self.chart_header_frame.pack(fill="x", pady=(20, 0))

        ctk.CTkButton(self.chart_header_frame, text="<", width=30, fg_color="#444", command=self.prev_chart).pack(side="left", padx=20)
        self.chart_title = ctk.CTkLabel(self.chart_header_frame, text="📊 Market Insights", font=("Segoe UI", 22, "bold"), text_color="#008CBA")
        self.chart_title.pack(side="left", expand=True)
        ctk.CTkButton(self.chart_header_frame, text=">", width=30, fg_color="#444", command=self.next_chart).pack(side="right", padx=20)
        
        self.chart_frame = ctk.CTkFrame(self.trends_card, fg_color="transparent")
        self.chart_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        self.chart_placeholder = ctk.CTkLabel(self.chart_frame, text="Click Predict to view trends.", font=("Segoe UI", 16), text_color="gray")
        self.chart_placeholder.pack(expand=True)

        self.current_chart_index = 0
        self.last_predicted_loc = None

    def next_chart(self):
        self.current_chart_index = (self.current_chart_index + 1) % 2
        if self.last_predicted_loc: self.update_display()

    def prev_chart(self):
        self.current_chart_index = (self.current_chart_index - 1) % 2
        if self.last_predicted_loc: self.update_display()

    def update_display(self):
        if self.current_chart_index == 0:
            canvas = utl.get_scatter_plot(self.chart_frame, self.app.df, self.last_predicted_loc)
        else:
            canvas = utl.get_bar_chart(self.chart_frame, self.app.df)
        
        if canvas:
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

   # Prediction Logic
    def predict(self):
        try:
            loc = self.opt_loc.get()
            if not loc or loc not in self.app.site_map:
                self.lbl_err.configure(text="⚠️ Select a valid location!")
                return
                
            sqft = float(self.ent_sqft.get())
            bhk = int(self.sld_bhk.get())
            bath = int(self.ent_bath.get())
            
            feat = np.array([[sqft, bhk, bath, 1, self.app.area_map[self.opt_area.get()], self.app.site_map[loc]]])
            price = self.app.model.predict(feat)[0]
            
            self.lbl_err.configure(text="")
            res_text = f"₹{price/100:.2f} Cr" if price >= 100 else f"₹{price:.2f} Lakhs"
            self.lbl_res.configure(text=res_text)
            
            self.last_predicted_loc = loc
            self.update_display()
            
        except ValueError:
            self.lbl_err.configure(text="⚠️ Check numeric inputs!")
        except Exception as e:
            self.lbl_err.configure(text=f"⚠️ Error: {str(e)[:30]}")


   # 2. AFFORDABILITY SCANNER TAB LOGIC
    def setup_affordability_tab(self):
        self.affordability_view = affordability.AffordabilityFrame(self.tab_affordability, self.app)
        self.affordability_view.pack(fill="both", expand=True)


   # 3. FAVORITES TAB LOGIC
    def setup_favorites_tab(self):
        self.favorites_view = favorites.FavoritesFrame(self.tab_history, self.app)
        self.favorites_view.pack(fill="both", expand=True)

    def on_tab_change(self):
        if self.tabs.get() == "Favorites":
            self.favorites_view.load_favorites()