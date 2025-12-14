import customtkinter as ctk
from PIL import Image
import pandas as pd
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from components.stat_card import StatCard
import config
import utils

class ChartPanel(ctk.CTkFrame):
    def __init__(self, master, on_toggle_trades, on_toggle_book, on_interval_change=None, **kwargs):
        super().__init__(master, fg_color=config.COLOR_CARD, corner_radius=15, **kwargs)
        self.on_toggle_trades = on_toggle_trades
        self.on_toggle_book = on_toggle_book
        self.on_interval_change = on_interval_change
        
        self.current_symbol = "BTC"
        self.current_interval = "1h"
        
        self.is_trades_active = True
        self.is_book_active = True
        
        self.chart_canvas = None
        self.timeframe_buttons = {}
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.setup_header()
        self.setup_chart_area()
        self.set_timeframe(self.current_interval)

    def setup_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=130)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=20)
        self.header_frame.grid_propagate(False)

        left = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        left.pack(side="left", fill="y")
        
        self.lbl_logo = ctk.CTkLabel(left, text="●", font=("Arial", 36), text_color="#f2a900")
        self.lbl_logo.pack(side="left", padx=(0, 20), anchor="n", pady=(5,0))
        
        info_stack = ctk.CTkFrame(left, fg_color="transparent")
        info_stack.pack(side="left", fill="y")
        
        row1 = ctk.CTkFrame(info_stack, fg_color="transparent")
        row1.pack(anchor="w")
        self.lbl_name = ctk.CTkLabel(row1, text="Bitcoin", font=("Roboto", 24, "bold"), text_color=config.COLOR_TEXT_MAIN)
        self.lbl_name.pack(side="left", padx=(0, 10))
        self.pct_badge = ctk.CTkLabel(row1, text="+0.00%", font=("Roboto", 13, "bold"), width=80, height=24, corner_radius=6)
        self.pct_badge.pack(side="left")
        
        self.lbl_price = ctk.CTkLabel(info_stack, text="$0.00", font=("Roboto", 28, "bold"), text_color=config.COLOR_TEXT_MAIN)
        self.lbl_price.pack(anchor="w")
        
        tf_frame = ctk.CTkFrame(info_stack, fg_color="transparent")
        tf_frame.pack(anchor="w", pady=(20, 0))
        for tf in ["1m", "15m", "1h", "4h", "1d"]:
            btn = ctk.CTkButton(tf_frame, text=tf, width=40, height=22, corner_radius=12, 
                                fg_color="transparent", border_width=1, border_color=config.COLOR_TEXT_SUB,
                                text_color="white", font=("Roboto", 11, "bold"),
                                command=lambda t=tf: self.set_timeframe(t))
            btn.pack(side="left", padx=(0, 6))
            self.timeframe_buttons[tf] = btn

        right = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        right.pack(side="right", fill="y")
        
        top_right = ctk.CTkFrame(right, fg_color="transparent")
        top_right.pack(side="top", anchor="e")
        self.card_movement = StatCard(top_right, title="24 Hours Movement", value_text="---", value_color=config.COLOR_GREEN, width=220, height=60)
        self.card_movement.pack(side="left", padx=(0, 15))
        self.card_volume = StatCard(top_right, title="24 Hours Volume", value_text="---", value_color="white", width=220, height=60)
        self.card_volume.pack(side="left")
        
        btm_right = ctk.CTkFrame(right, fg_color="transparent")
        btm_right.pack(side="bottom", anchor="e", pady=(0, 5))
        
        self.btn_trades = ctk.CTkButton(btm_right, text="Trades", width=60, height=22, 
                                      corner_radius=12, border_width=0, font=("Roboto", 11, "bold"),
                                      fg_color=config.COLOR_ACTIVE_BTN, text_color="white", hover_color="#333333",
                                      command=self.handle_toggle_trades)
        self.btn_trades.pack(side="left", padx=(0, 10))
        
        self.btn_book = ctk.CTkButton(btm_right, text="Book", width=60, height=22, 
                                    corner_radius=12, border_width=0, font=("Roboto", 11, "bold"),
                                    fg_color=config.COLOR_ACTIVE_BTN, text_color="white", hover_color="#333333",
                                    command=self.handle_toggle_book)
        self.btn_book.pack(side="left")

    def setup_chart_area(self):
        self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_container.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 10))

    def handle_toggle_trades(self):
        self.is_trades_active = not self.is_trades_active
        if self.is_trades_active:
            self.btn_trades.configure(fg_color=config.COLOR_ACTIVE_BTN, text_color="white")
        else:
            self.btn_trades.configure(fg_color="transparent", text_color=config.COLOR_TEXT_SUB)
        
        if self.on_toggle_trades: self.on_toggle_trades()

    def handle_toggle_book(self):
        self.is_book_active = not self.is_book_active
        if self.is_book_active:
            self.btn_book.configure(fg_color=config.COLOR_ACTIVE_BTN, text_color="white")
        else:
            self.btn_book.configure(fg_color="transparent", text_color=config.COLOR_TEXT_SUB)
            
        if self.on_toggle_book: self.on_toggle_book()

    def set_timeframe(self, tf):
        self.current_interval = tf
        for t, btn in self.timeframe_buttons.items():
            if t == tf:
                btn.configure(fg_color=config.COLOR_GREEN, border_color=config.COLOR_GREEN)
            else:
                btn.configure(fg_color="transparent", border_color=config.COLOR_TEXT_SUB)
        
        if self.on_interval_change:
            self.on_interval_change()

    def update_info(self, coin, data):
        self.current_symbol = coin
        try:
            img = ctk.CTkImage(Image.open(f"{coin}.png"), size=(48, 48))
            self.lbl_logo.configure(image=img, text="")
        except:
            self.lbl_logo.configure(image=None, text="●")

        if not data: return
        
        price = float(data['lastPrice'])
        percent = float(data['priceChangePercent'])
        volume = float(data['quoteVolume'])
        price_change_val = float(data['priceChange'])
        
        self.lbl_name.configure(text=config.COINS_INFO.get(coin, coin))
        self.lbl_price.configure(text=f"${price:,.2f}")
        
        is_up = percent >= 0
        self.pct_badge.configure(text=f"{'+' if is_up else ''}{percent:.2f}%", 
                               fg_color=config.COLOR_GREEN_BG if is_up else config.COLOR_RED_BG,
                               text_color=config.COLOR_GREEN if is_up else config.COLOR_RED)
        
        self.card_movement.update_value(f"{'+' if price_change_val >= 0 else ''}${price_change_val:,.2f}",
                                      color=config.COLOR_GREEN if price_change_val >= 0 else config.COLOR_RED)
        
        vol_str = f"${volume/1_000_000_000:.2f}B" if volume > 1e9 else f"${volume/1_000_000:.2f}M"
        self.card_volume.update_value(vol_str)

    def fetch_data(self):
        data = utils.fetch_klines(self.current_symbol, self.current_interval)
        if not data: return None
        try:
            df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'vol', 'x', 'y', 'z', 'a', 'b', 'c'])
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            df.set_index('time', inplace=True)
            df = df[['open', 'high', 'low', 'close', 'vol']].astype(float)
            return df
        except Exception as e:
            print(f"Data process error: {e}")
            return None

    def draw_chart(self, df):
        if df is None: return

        try:
            if self.chart_canvas:
                self.chart_canvas.get_tk_widget().destroy()
                self.chart_canvas = None

            mc = mpf.make_marketcolors(up=config.COLOR_GREEN, down=config.COLOR_RED, edge='inherit', wick='inherit', volume='in')
            s = mpf.make_mpf_style(marketcolors=mc, facecolor=config.COLOR_CARD, edgecolor=config.COLOR_CARD, 
                                 figcolor=config.COLOR_CARD, gridcolor="#595959", gridstyle="--")
            
            fig, ax = mpf.plot(df, type='candle', style=s, volume=False, returnfig=True, figsize=(12, 6))
            
            fig.subplots_adjust(left=0.06, right=1.00, top=0.95, bottom=0.15)
            
            for spine in ax[0].spines.values():
                spine.set_visible(False)
            
            ax[0].yaxis.tick_left()
            ax[0].yaxis.set_label_position("left")
            ax[0].set_ylabel("")
            
            ax[0].tick_params(axis='x', rotation=0, colors='#848e9c', labelsize=9)
            ax[0].tick_params(axis='y', colors='#848e9c', labelsize=9)
            
            last_price = df['close'].iloc[-1]
            last_open = df['open'].iloc[-1]
            color = config.COLOR_GREEN if last_price >= last_open else config.COLOR_RED
            
            ax[0].axhline(y=last_price, color=color, linestyle='--', linewidth=1, alpha=0.5)
            
            ax[0].text(x=1.00, y=last_price, 
                       s=f" {last_price:,.2f} ",
                       color='white', verticalalignment='center', horizontalalignment='right',
                       transform=ax[0].get_yaxis_transform(),
                       fontdict={'size': 9, 'weight': 'bold'},
                       bbox=dict(boxstyle="round,pad=0.2", facecolor=color, edgecolor=color, alpha=1.0))
            
            self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
            self.chart_canvas.draw()
            self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            print(f"Draw Chart Error: {e}")