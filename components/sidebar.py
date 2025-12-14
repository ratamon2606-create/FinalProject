import customtkinter as ctk
from PIL import Image
import random
import config

class SidebarPanel(ctk.CTkFrame):
    def __init__(self, master, on_coin_change, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_coin_change = on_coin_change
        self.overview_mode = "movement"
        self.coin_widgets = {}
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) 

        self.setup_ui()

    def setup_ui(self):
        self.overview_panel = ctk.CTkFrame(self, corner_radius=15, fg_color=config.COLOR_CARD)
        self.overview_panel.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self.overview_panel.grid_columnconfigure(0, weight=1)
        self.overview_panel.grid_rowconfigure(1, weight=1)
        
        self.toggle_frame = ctk.CTkFrame(self.overview_panel, fg_color="transparent")
        self.toggle_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 5))
        self.toggle_frame.grid_columnconfigure(0, weight=1)
        self.toggle_frame.grid_columnconfigure(1, weight=1)

        self.btn_movement = ctk.CTkButton(self.toggle_frame, text="Movement", height=28,
                                        corner_radius=8, font=("Roboto", 12, "bold"),
                                        fg_color=config.COLOR_ACTIVE_BTN, text_color="white",
                                        hover_color="#333333", border_width=0,
                                        command=lambda: self.set_overview_mode("movement"))
        self.btn_movement.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.btn_volume = ctk.CTkButton(self.toggle_frame, text="Volume", height=28,
                                      corner_radius=8, font=("Roboto", 12, "bold"),
                                      fg_color="transparent", text_color=config.COLOR_TEXT_SUB,
                                      hover_color="#333333", border_width=0,
                                      command=lambda: self.set_overview_mode("volume"))
        self.btn_volume.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        self.coin_list_frame = ctk.CTkFrame(self.overview_panel, fg_color="transparent")
        self.coin_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(10, 10))
        
        self.create_coin_list_items()

    def create_coin_list_items(self):
        for coin in config.COINS:
            item_frame = ctk.CTkFrame(self.coin_list_frame, fg_color="transparent", corner_radius=10, height=45)
            item_frame.pack(fill="x", pady=1) 
            
            item_frame.grid_columnconfigure(1, weight=1)

            try:
                img = ctk.CTkImage(Image.open(f"{coin}.png"), size=(30, 30))
                icon_lbl = ctk.CTkLabel(item_frame, text="", image=img)
            except:
                icon_lbl = ctk.CTkLabel(item_frame, text="●", font=("Arial", 22), text_color=config.COLOR_TEXT_SUB)
            
            icon_lbl.grid(row=0, column=0, rowspan=2, padx=(10, 8), pady=2.5)

            ctk.CTkLabel(item_frame, text=config.COINS_INFO[coin], font=("Roboto", 13, "bold"), 
                         text_color=config.COLOR_TEXT_MAIN).grid(row=0, column=1, sticky="w")
            
            value_lbl = ctk.CTkLabel(item_frame, text="---", font=("Roboto", 13, "bold"), 
                                     text_color=config.COLOR_TEXT_MAIN)
            value_lbl.grid(row=0, column=2, sticky="e", padx=(0, 10))

            ctk.CTkLabel(item_frame, text=coin, font=("Roboto", 11), 
                         text_color=config.COLOR_TEXT_SUB).grid(row=1, column=1, sticky="w")
            
            change_lbl = ctk.CTkLabel(item_frame, text="---", font=("Roboto", 11, "bold"))
            change_lbl.grid(row=1, column=2, sticky="e", padx=(0, 10))

            for w in item_frame.winfo_children():
                w.bind("<Button-1>", lambda e, c=coin: self.on_coin_change(c))
            item_frame.bind("<Button-1>", lambda e, c=coin: self.on_coin_change(c))
            
            self.coin_widgets[coin] = {"value": value_lbl, "change": change_lbl}

    def set_overview_mode(self, mode):
        self.overview_mode = mode
        if mode == "movement":
            self.btn_movement.configure(fg_color=config.COLOR_ACTIVE_BTN, text_color="white")
            self.btn_volume.configure(fg_color="transparent", text_color=config.COLOR_TEXT_SUB)
        else:
            self.btn_movement.configure(fg_color="transparent", text_color=config.COLOR_TEXT_SUB)
            self.btn_volume.configure(fg_color=config.COLOR_ACTIVE_BTN, text_color="white")

    def update_ui(self, tickers_data):
        for coin in config.COINS:
            if coin not in tickers_data: continue
            data = tickers_data[coin]
            widgets = self.coin_widgets[coin]
            
            price = float(data['lastPrice'])
            percent = float(data['priceChangePercent'])
            volume = float(data['quoteVolume'])
            
            vol_percent = percent * random.uniform(0.8, 1.2) if percent != 0 else 0
            
            display_val = f"${price:,.2f}" if self.overview_mode == "movement" else f"{volume/1000000:.2f}M"
            display_pct = percent if self.overview_mode == "movement" else vol_percent
            
            is_up = display_pct >= 0
            color = config.COLOR_GREEN if is_up else config.COLOR_RED
            arrow = "▲" if is_up else "▼"
            
            widgets["value"].configure(text=display_val)
            widgets["change"].configure(text=f"{arrow} {abs(display_pct):.2f}%", text_color=color)