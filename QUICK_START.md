# 🚀 Quick Start Guide

## ✅ Status: Ready to Use!

Your automated Indian stock trading bot is **fully configured** and ready to run.

---

## 🎯 3 Steps to Get Started

### Step 1: Enable GitHub Actions

1. Go to your repository: https://github.com/starkarthikr/indian-stock-trading-bot
2. Click the **Actions** tab
3. Click **"I understand my workflows, go ahead and enable them"**

### Step 2: Add API Key (Optional but Recommended)

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `ALPHA_VANTAGE_API_KEY`
4. Value: `GXX7A3VY8D3TP6MJ`
5. Click **Add secret**

### Step 3: Run Your First Analysis

1. Go to **Actions** tab
2. Click **"Indian Stock Market Analysis"** (left sidebar)
3. Click **"Run workflow"** dropdown (green button, right side)
4. Select branch: **main**
5. Click **"Run workflow"** button
6. Wait 5-10 minutes ⏱️

---

## 📊 What Happens Next

The workflow will:

1. ✅ Install all dependencies (pandas-ta-classic for Python 3.11)
2. 📈 Fetch data for 30 NSE stocks
3. 🔍 Calculate technical indicators (RSI, MACD, Moving Averages, Bollinger Bands)
4. 🎯 Identify buy signals with 0-10 scoring
5. 📝 Generate reports in `analysis_results/README.md`
6. 🚨 Create GitHub Issues for high-priority signals (7+ points)
7. 💾 Save JSON data for historical tracking

---

## 📖 View Results

### Option 1: Repository Files
- Navigate to `analysis_results/README.md` for formatted report
- Check `analysis_results/latest_signals.json` for raw data

### Option 2: GitHub Issues
- Go to **Issues** tab
- Look for 🚨 "High-Priority Trading Signals" issues
- Contains detailed stock recommendations

### Option 3: Download Artifacts
- Actions tab → Click completed workflow run
- Scroll to **Artifacts** section
- Download ZIP file with JSON data (90-day retention)

---

## ⚙️ Configuration

### Change Schedule

Edit `.github/workflows/stock-analysis.yml`:

```yaml
schedule:
  - cron: '0 4 * * 1-5'   # 9:30 AM IST (Market Open)
  - cron: '30 6 * * 1-5'  # 12:00 PM IST (Mid-day)
  - cron: '30 9 * * 1-5'  # 3:00 PM IST (Market Close)
```

### Modify Watchlist

Edit `scripts/analyze_stocks.py`:

```python
WATCHLIST = [
    'RELIANCE.NS',
    'TCS.NS',
    'TATASTEEL.NS',  # Add your stocks here
    'ZOMATO.NS',
]
```

### Adjust Thresholds

Use workflow inputs when running manually:
- `min_rsi_oversold`: Default 30 (lower = more signals)
- `min_volume_ratio`: Default 1.5 (lower = more signals)

---

## ❓ Troubleshooting

### No Signals Generated

**This is normal!** It means no stocks meet the technical criteria at this time.

To get more signals:
- Lower RSI threshold to 25
- Reduce volume ratio to 1.2
- Expand watchlist to more stocks

### Workflow Fails

Check:
1. GitHub Actions are enabled
2. No recent commits broke the code
3. Review [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

### Dependencies Error

✅ **FIXED:** Now using `pandas-ta-classic>=1.0.0` which is Python 3.11 compatible.

If issues persist, check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md).

---

## 📚 Documentation

- **[README.md](README.md)** - Complete overview and features
- **[SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Detailed setup instructions
- **[CUSTOMIZATION.md](docs/CUSTOMIZATION.md)** - Modify indicators, schedules, watchlists
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Solutions for common issues

---

## 🔧 Technical Details

### Current Configuration

- **Python Version:** 3.11
- **Dependencies:** pandas-ta-classic (Python 3.11 compatible)
- **Schedule:** 3x daily (9:30 AM, 12 PM, 3 PM IST)
- **Watchlist:** 30 NSE stocks (Nifty 50 + high-liquidity)
- **Indicators:** RSI, MACD, SMA, EMA, Bollinger Bands, Volume

### Signal Scoring (0-10 points)

| Indicator | Points |
|-----------|--------|
| RSI Oversold Bounce | +3 |
| MACD Bullish Crossover | +3 |
| Price Above EMAs | +2 |
| Golden Cross | +2 |
| Volume Surge | +1 |
| Bollinger Band Bounce | +1 |

**High Priority:** 7+ points  
**Medium Priority:** 5-6 points

---

## ⚠️ Important Disclaimer

This tool is for **educational purposes only**:

- ❌ NOT financial advice
- ❌ NOT guaranteed profits
- ✅ Do your own research
- ✅ Consult financial advisor
- ✅ Use paper trading first

---

## 🎉 You're All Set!

Your trading bot is ready to run. Follow the 3 steps above to start automated analysis!

**Questions?** Check the [documentation](docs/) or create an [issue](https://github.com/starkarthikr/indian-stock-trading-bot/issues).

---

**Last Updated:** February 16, 2026  
**Fix Status:** ✅ pandas-ta-classic installed (Python 3.11 compatible)  
**Latest Commit:** [d8b3324](https://github.com/starkarthikr/indian-stock-trading-bot/commit/d8b3324fcac379f05f45017f64f4aa00358b9654)
