import customtkinter as ctk

class SearchableComboBox(ctk.CTkFrame):
    def __init__(self, master, values, placeholder="Type to search...", width=320, **kwargs):
        # Lock the initial size to exactly 320x35
        super().__init__(master, fg_color="transparent", width=width, height=35)
        self.pack_propagate(False) # Prevent the frame from shrinking/resizing automatically
        
        self.values = values
        
        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=width, height=35)
        self.entry.pack(fill="x")
        self.entry.bind("<KeyRelease>", self.on_key_release)
        
        # Give the scrollable frame the exact same width
        self.results_frame = ctk.CTkScrollableFrame(self, width=width, height=120)
        self.result_buttons = []

    def get(self):
        return self.entry.get().strip()

    def on_key_release(self, event):
        query = self.entry.get().lower()
        if not query:
            self.hide_results()
            return
        self.update_results(query)

    def update_results(self, query):
        for btn in self.result_buttons:
            btn.destroy()
        self.result_buttons = []

        matches = sorted([v for v in self.values if v.lower().startswith(query)])[:8]
        if not matches:
            matches = sorted([v for v in self.values if query in v.lower()])[:8]

        if matches:
            self.show_results()
            for match in matches:
                btn = ctk.CTkButton(
                    self.results_frame, text=match, fg_color="transparent", 
                    hover_color="#00D2FF", anchor="w", 
                    command=lambda m=match: self.select_result(m)
                )
                btn.pack(fill="x")
                self.result_buttons.append(btn)
        else:
            self.hide_results()

    def show_results(self):
        # Dynamically EXPAND the frame's height to show the dropdown list
        self.configure(height=160) 
        self.results_frame.pack(fill="both", expand=True, pady=(2, 0))

    def hide_results(self):
        # SHRINK the frame back down to just the text box
        self.configure(height=35)
        self.results_frame.pack_forget()

    def select_result(self, match):
        self.entry.delete(0, 'end')
        self.entry.insert(0, match)
        self.hide_results()