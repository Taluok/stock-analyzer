# 📈 Stock Analyzer

A Python-based financial analysis tool that downloads historical stock data, calculates technical indicators, and generates interactive charts.

Built as part of my **AI FinTech Engineer** portfolio.

---

## 🚀 Demo

![Stock Analyzer Demo](graphs/demo.png)

---

## ✨ Features

- 📊 **Interactive candlestick charts** with zoom and hover
- 📉 **Moving averages** — MA20 and MA50
- 📈 **Daily returns** bar chart (green/red)
- 🧮 **Key statistics** — total return, volatility, best/worst day
- 🔍 **Any ticker** — stocks, ETFs, crypto (BTC-USD, ETH-USD)
- ⏱️ **Flexible periods** — 1 month to 2 years

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core language |
| pandas | Data manipulation |
| yfinance | Market data (Yahoo Finance) |
| Plotly | Interactive charts |

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/Taluok/stock-analyzer.git
cd stock-analyzer
```

**2. Install dependencies**
```bash
pip install pandas yfinance plotly
```

**3. Run**
```bash
python main.py
```

---

## 📖 Usage

```
===============================================
   ANALIZADOR DE ACCIONES - AI FinTech
===============================================

Ingresá el ticker (ej: AAPL, TSLA, BTC-USD): AAPL

PERÍODOS DISPONIBLES:
  1 → 1 mes
  2 → 3 meses
  3 → 6 meses
  4 → 1 año
  5 → 2 años

Elegí una opción (1-5): 4
```

**Supported tickers:**
- Stocks: `AAPL`, `TSLA`, `MSFT`, `GOOGL`, `MELI`
- ETFs: `VOO`, `SPY`, `QQQ`
- Crypto: `BTC-USD`, `ETH-USD`, `SOL-USD`
- Argentine stocks: `GGAL`, `YPF`, `BBAR`

---

## 📊 Output Example

```
=============================================
  RESUMEN: AAPL 📈
=============================================
  Precio actual:       $211.45
  Precio inicial:      $189.30
  Retorno total:       11.70%
  Retorno diario prom: 0.047%
  Volatilidad prom:    1.23%
  Mejor día:           +7.22%
  Peor día:            -6.18%
=============================================
```

---

## 📁 Project Structure

```
stock-analyzer/
├── main.py          # Main script
├── data/            # Downloaded data (optional export)
├── graphs/          # Saved chart screenshots
└── README.md        # This file
```

---

## 🧠 Concepts Applied

- **Moving Averages (MA20/MA50)** — trend detection
- **Daily Returns** — percentage change day over day
- **Volatility** — rolling standard deviation as risk measure
- **Candlestick Charts** — OHLC price visualization

---

## 🗺️ Roadmap

- [ ] Export data to CSV
- [ ] Add RSI and MACD indicators
- [ ] Multi-ticker comparison
- [ ] Email/Telegram alerts

---

## 👩‍💻 Author

**Tania** — AI FinTech - Programadora 
📍 Córdoba, Argentina  
🔗 [GitHub](https://github.com/Taluok) · [LinkedIn](https://linkedin.com/in/Taluok)

---

## 📄 License

MIT License — free to use and modify.