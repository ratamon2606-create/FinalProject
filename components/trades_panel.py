import customtkinter as ctk
from datetime import datetime
import config

class TradesPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=config.COLOR_CARD, corner_radius=15, **kwargs)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        ctk.CTkLabel(self, text="Running Trades", font=("Roboto", 15, "bold"), text_color=config.COLOR_TEXT_MAIN).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        
        header = ctk.CTkFrame(self, fg_color="transparent", height=25)
        header.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 5))
        header.grid_columnconfigure(0, weight=1); header.grid_columnconfigure(1, weight=1); header.grid_columnconfigure(2, weight=1)
        
        for i, t in enumerate(["Price", "Amount", "Time"]):
            ctk.CTkLabel(header, text=t, font=("Consolas", 12, "bold"), text_color=config.COLOR_TEXT_SUB).grid(row=0, column=i, sticky="nsew")

        self.list_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 10))
        self.list_frame.grid_columnconfigure(0, weight=1)

    def update_data(self, trades_data):
        for w in self.list_frame.winfo_children(): w.destroy()
        
        if not trades_data: return
        
        for trade in trades_data[:12]:
            price = float(trade['price'])
            qty = float(trade['qty'])
            time_obj = datetime.fromtimestamp(trade['time'] / 1000)
            time_str = time_obj.strftime("%H:%M:%S")
            is_buyer_maker = trade['isBuyerMaker'] 
            
            color = config.COLOR_RED if is_buyer_maker else config.COLOR_GREEN
            
            row = ctk.CTkFrame(self.list_frame, fg_color="transparent", height=22)
            row.pack(fill="x")
            row.grid_columnconfigure(0, weight=1); row.grid_columnconfigure(1, weight=1); row.grid_columnconfigure(2, weight=1)
            
            ctk.CTkLabel(row, text=f"{price:,.2f}", font=("Consolas", 11), text_color=color).grid(row=0, column=0)
            ctk.CTkLabel(row, text=f"{qty:.4f}", font=("Consolas", 11), text_color=config.COLOR_TEXT_MAIN).grid(row=0, column=1)
            ctk.CTkLabel(row, text=time_str, font=("Consolas", 11), text_color=config.COLOR_TEXT_SUB).grid(row=0, column=2)