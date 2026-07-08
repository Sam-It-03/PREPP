import customtkinter as ctk
import login as log
import dashboard 
import utilities as utl
import database as db  

# Initialize database right before the app starts
db.init_db()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PuneHousePriceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pune Real Estate Price Predictor")
        
        utl.center_window(self, 700, 450)
        utl.load_data(self)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.container.winfo_children(): widget.destroy()
        login_view = log.LoginFrame(self.container, on_success=self.show_main_app) #this line chnages to main app if login is success
        login_view.pack(fill="both", expand=True)

    def show_main_app(self, username="Member"):  
        for widget in self.container.winfo_children(): widget.destroy()
        
        # FULL SCREEN LOGIC 
        # "zoomed" is the Windows command to maximize a window natively
        self.after(0, lambda: self.state("zoomed")) 
        
        self.current_user = username 
        
        main_view = dashboard.MainAppFrame(self.container, self)
        main_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = PuneHousePriceApp()
    app.mainloop()