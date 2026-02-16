# 📊 Indian Stock Trading Bot

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

An automated trading analysis system that monitors Indian stock markets (NSE/BSE) using GitHub Actions. Analyzes stocks with technical indicators (RSI, MACD, Moving Averages, Bollinger Bands) and generates prioritized buy signals with profit potential analysis.

## ✨ Features

- **🔄 Automated Analysis**: Runs 3x daily during market hours (9:30 AM, 12 PM, 3 PM IST)
- **📈 Technical Indicators**: RSI, MACD, Moving Averages (SMA/EMA), Bollinger Bands, Volume Analysis
- **🎯 Signal Scoring**: Weighted scoring system (0-10) to prioritize highest-probability trades
- **🔔 Smart Alerts**: Automatic GitHub Issues for high-priority signals
- **📊 Risk Management**: Automated entry points, target prices (2x ATR), and stop losses (1x ATR)
- **💾 Historical Tracking**: 90-day artifact retention for performance analysis
- **🎓 NSE/BSE Coverage**: Monitors Nifty 50 and high-liquidity mid-cap stocks

## 🛠️ How It Works

### Analysis Pipeline

1. **Data Collection**: Fetches real-time stock data from Yahoo Finance for NSE-listed stocks
2. **Technical Analysis**: Calculates multiple indicators and identifies confluence patterns
3. **Signal Generation**: Scores opportunities based on indicator alignment
4. **Risk Calculation**: Determines entry points, targets, and stop losses using ATR
5. **Report Generation**: Creates formatted reports and GitHub Issues for actionable signals

### Signal Strength Scoring

The system uses a weighted scoring algorithm:

| Indicator | Points | Criteria |
|-----------|--------|----------|
| RSI Oversold Bounce | +3 | RSI < 35 and increasing |
| MACD Bullish Crossover | +3 | MACD crosses above signal line |
| Price Above EMAs | +2 | Close > EMA21 > SMA50 (uptrend) |
| Golden Cross | +2 | SMA20 crosses above SMA50 |
| Volume Surge | +1 | Volume > 1.5x average |
| Bollinger Band Bounce | +1 | Price bounces from lower band |

**High Priority**: 7+ points  
**Medium Priority**: 5-6 points

## 🚀 Quick Start

### 1. Fork or Clone Repository

```bash
git clone https://github.com/starkarthikr/indian-stock-trading-bot.git
cd indian-stock-trading-bot
```

### 2. Enable GitHub Actions

- Go to **Actions** tab in your repository
- Click **"I understand my workflows, go ahead and enable them"**

### 3. (Optional) Add API Keys

For enhanced data sources, add these secrets in **Settings → Secrets and variables → Actions**:

- `ALPHA_VANTAGE_API_KEY` - Free at [alphavantage.co](https://www.alphavantage.co/support/#api-key)
- `FINNHUB_API_KEY` - Free at [finnhub.io](https://finnhub.io/register)

### 4. Run First Analysis

- Go to **Actions** tab
- Select **"Indian Stock Market Analysis"** workflow
- Click **"Run workflow"** → **"Run workflow"** (green button)
- Wait 5-10 minutes for completion

### 5. View Results

- **Reports**: Check `analysis_results/README.md` in your repository
- **Issues**: High-priority signals appear as GitHub Issues with 🚨 labels
- **Artifacts**: Download detailed JSON data from Actions runs (90-day retention)

## 💻 Local Development

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run analysis
python scripts/analyze_stocks.py

# Generate report
python scripts/generate_report.py
```

### Customize Watchlist

Edit `scripts/analyze_stocks.py`:

```python
WATCHLIST = [
    'TATASTEEL.NS',  # Add your preferred stocks
    'ZOMATO.NS',
    'PAYTM.NS'
]
```

### Adjust Thresholds

Modify in workflow file or use manual trigger:

```yaml
workflow_dispatch:
  inputs:
    min_rsi_oversold: '25'      # More aggressive (default: 30)
    min_volume_ratio: '2.0'     # Stricter filter (default: 1.5)
```

## 📊 Sample Output

### High Priority Signal Example

```markdown
### RELIANCE - Reliance Industries Limited

| Metric | Value |
|--------|-------|
| Signal Strength | 8/10 ⭐ |
| Current Price | ₹2,456.75 |
| Entry Point | ₹2,456.75 |
| Target Price | ₹2,612.50 (6.34% upside) |
| Stop Loss | ₹2,378.50 |
| RSI | 32.5 |
| MACD Signal | Bullish |
| Volume Ratio | 2.3x |

Analysis: RSI bouncing from oversold (32.5) | MACD bullish crossover | Volume surge (2.3x average)
```

## 📅 Scheduled Runs

The workflow automatically runs:

- **9:30 AM IST** (4:00 AM UTC) - Market open analysis
- **12:00 PM IST** (6:30 AM UTC) - Mid-day momentum check
- **3:00 PM IST** (9:30 AM UTC) - Market close evaluation

Runs **Monday-Friday** only (Indian trading days).

## 🔧 Configuration

### Change Schedule

Edit `.github/workflows/stock-analysis.yml`:

```yaml
schedule:
  - cron: '*/30 9-10 * * 1-5'  # Every 30 min during market hours
```

[Cron syntax reference](https://crontab.guru/)

### Modify Technical Parameters

In `scripts/analyze_stocks.py`:

```python
# RSI period
df['RSI'] = ta.rsi(df['Close'], length=14)  # Change to 9 for faster signals

# MACD parameters
macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)

# Moving averages
df['SMA_20'] = ta.sma(df['Close'], length=20)
df['EMA_21'] = ta.ema(df['Close'], length=21)
```

## 📂 Repository Structure

```
indian-stock-trading-bot/
├── .github/
│   └── workflows/
│       └── stock-analysis.yml      # Main GitHub Actions workflow
├── scripts/
│   ├── analyze_stocks.py        # Core analysis engine
│   └── generate_report.py       # Report formatter
├── analysis_results/
│   ├── latest_signals.json      # Most recent analysis
│   ├── signals_YYYYMMDD_HHMMSS.json  # Historical snapshots
│   └── README.md                # Formatted report
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## ⚠️ Disclaimer

This tool is for **educational and informational purposes only**. It does not constitute financial advice.

- **Do your own research** before making any investment decisions
- **Consult a financial advisor** for personalized advice
- **Past performance does not guarantee future results**
- **Technical analysis has limitations** and should be combined with fundamental analysis
- The developers are **not responsible for any trading losses**

## 📚 Resources

- [Technical Analysis Basics](https://www.investopedia.com/terms/t/technicalanalysis.asp)
- [RSI Indicator Guide](https://www.investopedia.com/terms/r/rsi.asp)
- [MACD Strategy](https://www.investopedia.com/terms/m/macd.asp)
- [Moving Averages Explained](https://www.investopedia.com/terms/m/movingaverage.asp)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional technical indicators (Stochastic, ADX, Ichimoku)
- Sentiment analysis from news sources
- Backtesting framework
- Telegram/Discord notifications
- Machine learning signal optimization

## 📝 License

MIT License - see LICENSE file for details

## 👤 Author

Created by [starkarthikr](https://github.com/starkarthikr)

---

**⭐ If this project helps you, consider giving it a star!**
