# Crypto Dashboard

**Crypto Dashboard** is a real-time cryptocurrency market analysis and tracking application developed in Python. It features a modern, professional user interface designed for a seamless user experience.

The project fetches live data from the **Binance Public API** to display interactive Candlestick Charts, Order Books, and Recent Trades in real-time.


---

## Key Features

* **Real-time Data:** Fetches live price, percentage change, and volume data from Binance.
* **Interactive Charting:** Beautiful Candlestick charts generated using `mplfinance` with customizable styles.
* **Multi-Timeframe Support:** Users can switch between various timeframes: 1m, 15m, 1h, 4h, 1d.
* **Order Book Visualization:** Visual representation of Bids and Asks with depth bars.
* **Live Trades Feed:** Displays real-time executed trades (Running Trades) with color-coded buy/sell indicators.
* **Modular Architecture:** The codebase is organized into modular components for maintainability and scalability.
* **Modern UI/UX:** Built with `customtkinter` featuring a sleek Dark Mode and a professional Deep Green color scheme.
* **Responsive Performance:** Utilizes Python `threading` to handle API requests asynchronously, ensuring the GUI never freezes.

---

## Project Structure

This project follows a modular design pattern to separate logic, configuration, and UI components:

```text
crypto_dashboard/
│
├── main.py                  # Main application loop and layout
├── config.py                # Configuration: Constants, Colors, and Coin lists
├── utils.py                 # Utilities: API handling (Binance) and Image processing
│
├── components/              # UI Components Package
│   ├── __init__.py          # Package initializer
│   ├── sidebar.py           # Sidebar: Coin list and Toggle buttons
│   ├── chart_panel.py       # Chart Panel: Header, Stats, Timeframe selector, and Graph
│   ├── orderbook_panel.py   # Order Book Panel: Bids/Asks visualization
│   ├── trades_panel.py      # Recent Trades Panel: Live trade feed
│   └── stat_card.py         # Stat Card: Reusable widget for header statistics
│
├── README.md                # Project documentation
└── *.png                    # Coin icons (e.g., BTC.png, ETH.png)
```

## Installation & Usage

**1. Prerequisites**
Python 3.8 or higher  
Git (Optional)

**2. Install Dependencies**
Open your terminal or command prompt in the project directory and run:

```Bash
pip install customtkinter requests pandas mplfinance matplotlib pillow
```

**3. Setup Icons (Optional)**
For the best visual experience, place coin icon images (e.g., BTC.png, ETH.png) in the same directory as main.py. (If icons are missing, the app will automatically display a default placeholder.)

**4. Run the Application**
```Bash
python main.py
```

## Configuration
You can customize the application by editing config.py:

* **Change Theme Colors:** Modify COLOR_BG, COLOR_CARD, etc.
* **Add/Remove Coins:** Update the COINS_INFO dictionary.

```Bash
COINS_INFO = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "DOGE": "Dogecoin",
    # Add new coins here
    "ADA": "Cardano"
}
```

## Tech Stack

* **CustomTkinter:** A modern, customizable GUI library based on Tkinter.
* **Binance API:** Provides public market data (Spot).
* **Pandas:** Data manipulation and analysis for OHLCV data.
* **mplfinance:** Financial market data visualization.
* **Matplotlib:** The backend used for plotting charts within the GUI.
* **Threading:** Ensures the application remains responsive while fetching network data.

## Notes
This application uses the Binance Public API which has rate limits. The code is optimized to respect these limits, but excessive modifications to refresh rates might cause temporary IP bans from Binance.

Initial chart loading might take a brief moment depending on your internet connection speed.