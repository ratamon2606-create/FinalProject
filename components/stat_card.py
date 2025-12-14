import customtkinter as ctk
import config

class StatCard(ctk.CTkFrame):
    def __init__(self, master, title, value_text, value_color, **kwargs):
        super().__init__(master, corner_radius=12, fg_color=config.COLOR_CARD_DARK, **kwargs)
        self.grid_propagate(False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.lbl_value = ctk.CTkLabel(self, text=value_text, font=("Roboto", 16, "bold"), text_color=value_color)
        self.lbl_value.grid(row=0, column=0, pady=(5, 0), sticky="s")
        
        self.lbl_title = ctk.CTkLabel(self, text=title, font=("Roboto", 11), text_color=config.COLOR_TEXT_SUB)
        self.lbl_title.grid(row=1, column=0, pady=(0, 5), sticky="n")

    def update_value(self, text, color=None):
        self.lbl_value.configure(text=text)
        if color:
            self.lbl_value.configure(text_color=color)