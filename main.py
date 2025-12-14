import customtkinter as ctk
import threading
import matplotlib.pyplot as plt
from PIL import Image 
import config
import utils
from components.sidebar import SidebarPanel
from components.chart_panel import ChartPanel
from components.orderbook_panel import OrderBookPanel
from components.trades_panel import TradesPanel

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class CryptoDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Dashboard - Final")
        self.geometry("1400x900")
        
        self.configure(fg_color=config.COLOR_BG_TOP)
        
        self.bg_image = None
        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self.resize_background)
        
        self.tickers_data = {}
        self.current_coin = "BTC"
        self.is_running = True 
        self.loop_id = None
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_ui()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.update_overview_data() 
        self.update_detail_data()   
        self.update_chart_task()    
        self.start_live_updates()   

    def resize_background(self, event):
        if event.widget == self:
            w, h = self.winfo_width(), self.winfo_height()
            pil_img = utils.create_gradient_image(w, h, config.COLOR_BG_TOP, config.COLOR_BG_BOTTOM)
            self.bg_image = ctk.CTkImage(pil_img, size=(w, h))
            self.bg_label.configure(image=self.bg_image)
            self.bg_label.lower()

    def setup_ui(self):
        self.sidebar_container = ctk.CTkFrame(self, width=320, fg_color="transparent")
        self.sidebar_container.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.sidebar_container.grid_rowconfigure(0, weight=1)
        
        self.sidebar = SidebarPanel(self.sidebar_container, on_coin_change=self.change_coin)
        self.sidebar.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        self.trades_panel = TradesPanel(self.sidebar_container, height=350)
        self.trades_panel.grid(row=1, column=0, sticky="ew")

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.chart_panel = ChartPanel(self.main_frame, 
                                      on_toggle_trades=lambda: self.toggle_panel(self.trades_panel),
                                      on_toggle_book=lambda: self.toggle_panel(self.order_panel),
                                      on_interval_change=self.update_chart_task)
        self.chart_panel.grid(row=0, column=0, sticky="nsew", pady=(0, 15))

        self.order_panel = OrderBookPanel(self.main_frame, height=350)
        self.order_panel.grid(row=1, column=0, sticky="ew")

    def change_coin(self, coin):
        if not self.is_running: return
        self.current_coin = coin
        self.chart_panel.current_symbol = coin 
        self.update_chart_task()
        self.update_detail_data()

    def update_chart_task(self):
        if not self.is_running: return
        threading.Thread(target=self.update_chart_task_thread, daemon=True).start()

    def update_chart_task_thread(self):
        if not self.is_running: return
        try:
            df = self.chart_panel.fetch_data()
            if self.is_running and df is not None:
                self.after(0, lambda: self.safe_draw_chart(df))
        except Exception:
            pass

    def safe_draw_chart(self, df):
        if not self.is_running or not self.winfo_exists(): return
        try:
            self.chart_panel.draw_chart(df)
        except Exception:
            pass

    def update_overview_data(self):
        def task():
            if not self.is_running: return
            try:
                data = utils.fetch_ticker_24hr()
                if data and self.is_running:
                    for t in data:
                        sym = t['symbol']
                        if sym.endswith("USDT"):
                            coin = sym.replace("USDT", "")
                            if coin in config.COINS:
                                self.tickers_data[coin] = t
                    if self.is_running:
                        self.after(0, lambda: self.safe_update_sidebar())
            except Exception:
                pass
        threading.Thread(target=task, daemon=True).start()

    def safe_update_sidebar(self):
        if not self.is_running or not self.winfo_exists(): return
        self.sidebar.update_ui(self.tickers_data)
        if self.current_coin in self.tickers_data:
            self.chart_panel.update_info(self.current_coin, self.tickers_data[self.current_coin])

    def update_detail_data(self):
        def task():
            if not self.is_running: return
            try:
                depth = utils.fetch_depth(self.current_coin, limit=15)
                trades = utils.fetch_recent_trades(self.current_coin)
                if self.is_running:
                    self.after(0, lambda: self.safe_update_details(depth, trades))
            except Exception:
                pass
        threading.Thread(target=task, daemon=True).start()

    def safe_update_details(self, depth, trades):
        if not self.is_running or not self.winfo_exists(): return
        self.order_panel.update_data(depth)
        self.trades_panel.update_data(trades)

    def start_live_updates(self):
        if not self.is_running: return
        self.update_overview_data()
        self.update_detail_data()
        self.loop_id = self.after(5000, self.start_live_updates)

    def toggle_panel(self, panel):
        if panel.winfo_viewable():
            panel.grid_remove()
        else:
            panel.grid()

    def on_closing(self):
        self.is_running = False
        if self.loop_id:
            try:
                self.after_cancel(self.loop_id)
            except ValueError:
                pass
        try:
            plt.close('all')
        except:
            pass
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = CryptoDashboard()
    app.mainloop()