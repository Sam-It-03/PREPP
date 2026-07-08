import customtkinter as ctk
import database as db
from PIL import Image
import utilities as utl

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_success):
        super().__init__(master, fg_color="transparent")
        self.on_success = on_success
        
    # Main Card
        self.main_card = ctk.CTkFrame(self, fg_color=("#ffffff", "#2b2b2b"), corner_radius=20, width=400, height=500)
        self.main_card.pack(expand=True)
        self.main_card.pack_propagate(False) 
        
  # ==========================================
# 🖼️ LOGO
  # ==========================================
        try:
            icon_path = utl.resource_path("logo.png") 
            img_icon = ctk.CTkImage(Image.open(icon_path), size=(60, 60))
            ctk.CTkLabel(self.main_card, image=img_icon, text="").pack(pady=(40, 10))
        except Exception as e:
    # Fallback emoji if logo.png is missing
            ctk.CTkLabel(self.main_card, text="🏠", font=("Segoe UI", 50)).pack(pady=(40, 10))
        
    # Updated Text
        ctk.CTkLabel(self.main_card, text="Login to PREPP", font=("Segoe UI", 24, "bold"), text_color=("black", "white")).pack(pady=(0, 20))
        
        self.u_ent = ctk.CTkEntry(self.main_card, placeholder_text="Username", width=250, height=40)
        self.u_ent.pack(pady=(0, 10))
        
        self.p_ent = ctk.CTkEntry(self.main_card, placeholder_text="Password", show="*", width=250, height=40)
        self.p_ent.pack(pady=(10, 10))
        
    # REMEMBER ME CHECKBOX
        self.remember_var = ctk.StringVar(value="off")
        self.chk_remember = ctk.CTkCheckBox(self.main_card, text="Remember Me", variable=self.remember_var, 
                                            onvalue="on", offvalue="off", font=("Segoe UI", 12), text_color=("black", "white"))
        self.chk_remember.pack(pady=(5, 15), padx=75, anchor="w")
        
        self.lbl_msg = ctk.CTkLabel(self.main_card, text="", text_color="#FF4B4B")
        self.lbl_msg.pack()
        
    # BUTTONS
        btn_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        btn_frame.pack(pady=(10, 0))

        ctk.CTkButton(btn_frame, text="Login", command=self.attempt_login, width=105, height=40, 
                      font=("Segoe UI", 14, "bold"), 
                      fg_color="#008CBA", hover_color="#005F80").pack(side="left", padx=5)
                      
        ctk.CTkButton(btn_frame, text="Register", command=self.attempt_register, width=105, height=40, 
                      font=("Segoe UI", 14, "bold"), 
                      fg_color="#444", hover_color="#555").pack(side="right", padx=5)
                      
    # Auto-fill if remembered in the database
        self.load_credentials()

 # =================================
# 💾 DATABASE CREDENTIAL LOGIC
 # =================================
    def load_credentials(self):
        saved_user = db.get_remembered_user()
        if saved_user:
            # saved_user[0] is username, saved_user[1] is password
            self.u_ent.insert(0, saved_user[0])
            self.p_ent.insert(0, saved_user[1])
            self.chk_remember.select()

 # =================================
# 🔐 LOGIN & REGISTER LOGIC
 # =================================
    def attempt_login(self):
        username = self.u_ent.get().strip()
        password = self.p_ent.get().strip()
        
        if db.verify_user(username, password):
            self.lbl_msg.configure(text="")
            
        # Tell the DB to remember or forget the user based on the checkbox
            db.set_remembered_user(username, password, self.remember_var.get()) 
            
            self.on_success(username)  
        else:
            self.lbl_msg.configure(text="⚠️ Invalid username or password", text_color="#FF4B4B")
            
    def attempt_register(self):
        username = self.u_ent.get().strip()
        password = self.p_ent.get().strip()
        
        if len(username) < 3 or len(password) < 3:
            self.lbl_msg.configure(text="⚠️ Must be at least 3 characters", text_color="#FF4B4B")
            return
            
        if db.add_user(username, password):
            self.lbl_msg.configure(text="✅ Registered! You can now login.", text_color="#28a745")
            self.u_ent.delete(0, 'end')
            self.p_ent.delete(0, 'end')
        else:
            self.lbl_msg.configure(text="⚠️ Username already exists", text_color="#FF4B4B")