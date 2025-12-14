import customtkinter as ctk
import tkinter as tk
import config

class OrderBookPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=config.COLOR_CARD, corner_radius=15, **kwargs)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        ctk.CTkLabel(self, text="Order Book", font=("Roboto", 15, "bold"), text_color=config.COLOR_TEXT_MAIN).grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(15, 5))
        
        header = ctk.CTkFrame(self, fg_color="transparent", height=25)
        header.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=(0, 5))
        header.grid_columnconfigure(0, weight=1); header.grid_columnconfigure(2, weight=1)
        
        ask_h = ctk.CTkFrame(header, fg_color="transparent")
        ask_h.grid(row=0, column=0, sticky="nsew")
        for t in ["Price", "Size", "Sum"]:
            ctk.CTkLabel(ask_h, text=t, font=("Consolas", 11, "bold"), text_color=config.COLOR_TEXT_SUB).pack(side="left", expand=True)
            
        bid_h = ctk.CTkFrame(header, fg_color="transparent")
        bid_h.grid(row=0, column=2, sticky="nsew")
        for t in ["Price", "Size", "Sum"]:
            ctk.CTkLabel(bid_h, text=t, font=("Consolas", 11, "bold"), text_color=config.COLOR_TEXT_SUB).pack(side="left", expand=True)

        self.ask_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.ask_frame.grid(row=2, column=0, sticky="nsew", padx=(20, 5), pady=(0, 10))
        
        ctk.CTkFrame(self, width=2, fg_color="#2b2b2b").grid(row=2, column=1, sticky="ns", pady=(5, 10))
        
        self.bid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bid_frame.grid(row=2, column=2, sticky="nsew", padx=(5, 20), pady=(0, 10))

    def create_row(self, parent, price, size, total, max_vol, is_ask):
        h = 22
        canvas = tk.Canvas(parent, height=h, bg=config.COLOR_CARD, highlightthickness=0)
        canvas.pack(fill="x", pady=0)
        
        percent = min(1.0, size / max_vol) if max_vol > 0 else 0
        bar_color = config.COLOR_RED_BAR if is_ask else config.COLOR_GREEN_BAR
        text_color = config.COLOR_RED if is_ask else config.COLOR_GREEN
        
        def draw(event=None):
            w = canvas.winfo_width()
            canvas.delete("all")
            bar_w = w * percent
            
            if is_ask:
                canvas.create_rectangle(0, 0, bar_w, h, fill=bar_color, outline="")
            else:
                canvas.create_rectangle(w - bar_w, 0, w, h, fill=bar_color, outline="")
            
            c1, c2, c3 = w*(1/6), w*(3/6), w*(5/6)
            canvas.create_text(c1, h/2, text=f"{price:,.2f}", fill=text_color, font=("Consolas", 10))
            canvas.create_text(c2, h/2, text=f"{size:.4f}", fill=config.COLOR_TEXT_MAIN, font=("Consolas", 10))
            canvas.create_text(c3, h/2, text=f"{total:,.2f}", fill=config.COLOR_TEXT_SUB, font=("Consolas", 10))
            
        canvas.bind("<Configure>", draw)

    def update_data(self, depth_data):
        for w in self.ask_frame.winfo_children(): w.destroy()
        for w in self.bid_frame.winfo_children(): w.destroy()
        
        if not depth_data: return

        bids = depth_data.get('bids', [])
        asks = depth_data.get('asks', [])
        
        max_vol = 0
        parsed_asks = []
        parsed_bids = []
        
        rows_limit = 11
        
        total_ask = 0
        for p, q in asks[:rows_limit]:
            p, q = float(p), float(q)
            total_ask += p * q
            max_vol = max(max_vol, q)
            parsed_asks.append((p, q, total_ask))
            
        total_bid = 0
        for p, q in bids[:rows_limit]:
            p, q = float(p), float(q)
            total_bid += p * q
            max_vol = max(max_vol, q)
            parsed_bids.append((p, q, total_bid))

        for p, s, t in reversed(parsed_asks):
            self.create_row(self.ask_frame, p, s, t, max_vol, True)
            
        for p, s, t in parsed_bids:
            self.create_row(self.bid_frame, p, s, t, max_vol, False)