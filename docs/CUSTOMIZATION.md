# ⚙️ Customization Guide

## Table of Contents

1. [Watchlist Customization](#watchlist-customization)
2. [Technical Indicator Parameters](#technical-indicator-parameters)
3. [Signal Scoring Logic](#signal-scoring-logic)
4. [Schedule Configuration](#schedule-configuration)
5. [Risk Management Settings](#risk-management-settings)
6. [Output Formatting](#output-formatting)

## Watchlist Customization

### Add Individual Stocks

Edit `scripts/analyze_stocks.py`:

```python
WATCHLIST = [
    'RELIANCE.NS',
    'TCS.NS',
    'HDFCBANK.NS',
    # Add your stocks here
    'ZOMATO.NS',
    'PAYTM.NS'
]
```

### Sector-Specific Watchlists

```python
# Banking sector
BANKING_STOCKS = [
    'HDFCBANK.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS',
    'AXISBANK.NS', 'SBIN.NS', 'INDUSINDBK.NS'
]

# IT sector
IT_STOCKS = [
    'TCS.NS', 'INFY.NS', 'WIPRO.NS', 'HCLTECH.NS',
    'TECHM.NS', 'LTIM.NS'
]

# Combine
WATCHLIST = BANKING_STOCKS + IT_STOCKS
```

### Dynamic Watchlist from Nifty Indices

```python
import yfinance as yf

def get_nifty50_stocks():
    """Fetch current Nifty 50 constituents."""
    nifty50 = yf.Ticker("^NSEI")
    # This requires additional scraping logic
    # Placeholder for demonstration
    return ['RELIANCE.NS', 'TCS.NS', ...]  # All 50 stocks

WATCHLIST = get_nifty50_stocks()
```

## Technical Indicator Parameters

### RSI Customization

```python
# Faster RSI (more signals, more noise)
df['RSI'] = ta.rsi(df['Close'], length=9)

# Slower RSI (fewer signals, more reliable)
df['RSI'] = ta.rsi(df['Close'], length=21)

# Multiple RSI periods
df['RSI_9'] = ta.rsi(df['Close'], length=9)
df['RSI_14'] = ta.rsi(df['Close'], length=14)
df['RSI_21'] = ta.rsi(df['Close'], length=21)
```

### MACD Settings

```python
# Aggressive MACD (faster signals)
macd = ta.macd(df['Close'], fast=8, slow=17, signal=9)

# Conservative MACD (slower signals)
macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)

# Weekly MACD (for swing trading)
macd = ta.macd(df['Close'], fast=5, slow=13, signal=5)
```

### Moving Average Strategies

```python
# Day trading (shorter periods)
df['EMA_5'] = ta.ema(df['Close'], length=5)
df['EMA_13'] = ta.ema(df['Close'], length=13)

# Swing trading (medium periods)
df['EMA_21'] = ta.ema(df['Close'], length=21)
df['SMA_50'] = ta.sma(df['Close'], length=50)

# Position trading (longer periods)
df['SMA_100'] = ta.sma(df['Close'], length=100)
df['SMA_200'] = ta.sma(df['Close'], length=200)
```

### Bollinger Band Customization

```python
# Tighter bands (more signals)
bbands = ta.bbands(df['Close'], length=20, std=1.5)

# Wider bands (fewer signals)
bbands = ta.bbands(df['Close'], length=20, std=2.5)

# Longer period
bbands = ta.bbands(df['Close'], length=30, std=2)
```

## Signal Scoring Logic

### Adjust Point Weights

```python
def generate_buy_signal(self, df, symbol):
    # ... existing code ...
    
    # Prioritize RSI more heavily
    if latest['RSI'] < 35 and latest['RSI'] > prev['RSI']:
        signal_strength += 4  # Increased from 3
        reasons.append(f"RSI bouncing from oversold ({latest['RSI']:.1f})")
    
    # Add volume requirement as mandatory (not just bonus)
    if latest['Volume_Ratio'] < self.min_volume_ratio:
        return None  # No signal without volume confirmation
```

### Add New Signal Conditions

```python
# Morning star candlestick pattern
if self._is_morning_star(df):
    signal_strength += 2
    reasons.append("Morning star pattern detected")

# Support level bounce
if self._near_support(df, latest['Close']):
    signal_strength += 1
    reasons.append("Price near support level")

# Relative strength vs Nifty
if self._outperforming_index(symbol):
    signal_strength += 1
    reasons.append("Outperforming Nifty index")
```

### Change Priority Thresholds

```python
# More strict classification
if signal_strength >= 8:  # Changed from 7
    high_priority.append(signal)
else:
    medium_priority.append(signal)

# Or use percentage-based
total_possible_points = 10
if signal_strength / total_possible_points >= 0.8:
    high_priority.append(signal)
```

## Schedule Configuration

### Different Time Intervals

```yaml
# Every 30 minutes during market hours
schedule:
  - cron: '0,30 3-9 * * 1-5'

# Every hour from 9 AM to 3 PM IST
schedule:
  - cron: '30 3,4,5,6,7,8,9 * * 1-5'

# Only at market open and close
schedule:
  - cron: '0 4 * * 1-5'   # 9:30 AM IST
  - cron: '30 9 * * 1-5'  # 3:00 PM IST

# Once daily after market close
schedule:
  - cron: '0 10 * * 1-5'  # 3:30 PM IST
```

### Weekend Analysis

```yaml
# Run on Sunday for weekly analysis
schedule:
  - cron: '0 4 * * 0'  # Sunday 9:30 AM IST

# Include Saturdays
schedule:
  - cron: '0 4 * * 6'  # Saturday 9:30 AM IST
```

## Risk Management Settings

### ATR-Based Targets

```python
# More aggressive targets
target_price = current_price + (atr * 3)  # 3x ATR
stop_loss = current_price - (atr * 0.5)   # 0.5x ATR

# More conservative
target_price = current_price + (atr * 1.5)
stop_loss = current_price - (atr * 1.5)

# Fixed risk-reward ratio
risk = atr * 1
target_price = current_price + (risk * 3)  # 1:3 risk-reward
stop_loss = current_price - risk
```

### Percentage-Based Targets

```python
# Fixed percentage targets
target_price = current_price * 1.05  # 5% target
stop_loss = current_price * 0.97     # 3% stop loss

# Volatility-adjusted
volatility = df['Close'].pct_change().std() * 100
target_price = current_price * (1 + volatility * 2)
stop_loss = current_price * (1 - volatility)
```

### Position Sizing

```python
def calculate_position_size(self, signal, account_size=100000, risk_per_trade=0.02):
    """Calculate shares to buy based on risk."""
    risk_amount = account_size * risk_per_trade
    risk_per_share = signal['entry_point'] - signal['stop_loss']
    shares = int(risk_amount / risk_per_share)
    
    signal['recommended_shares'] = shares
    signal['total_investment'] = shares * signal['entry_point']
    return signal
```

## Output Formatting

### Change Report Style

Edit `scripts/generate_report.py`:

```python
# Minimal report (just high priority)
if data['high_priority']:
    for stock in data['high_priority']:
        report += f"**{stock['symbol']}** - Entry: ₹{stock['entry_point']}, "
        report += f"Target: ₹{stock['target_price']} ({stock['profit_potential']}%)\n"

# Detailed report with charts (requires matplotlib)
import matplotlib.pyplot as plt

def add_chart_to_report(symbol, df):
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Close'], label='Price')
    plt.plot(df.index, df['SMA_20'], label='SMA 20')
    plt.plot(df.index, df['SMA_50'], label='SMA 50')
    plt.legend()
    plt.savefig(f"analysis_results/charts/{symbol}.png")
    plt.close()
```

### Export Multiple Formats

```python
# Excel export
import pandas as pd

df = pd.DataFrame(data['high_priority'])
df.to_excel(f"{results_dir}/signals.xlsx", index=False)

# HTML report
html = df.to_html(index=False, classes='table table-striped')
with open(f"{results_dir}/report.html", 'w') as f:
    f.write(f"<html><body>{html}</body></html>")
```

### Custom Notifications

```python
# Add to workflow after analysis
- name: Send Telegram Message
  if: success()
  run: |
    python scripts/send_telegram.py
```

Create `scripts/send_telegram.py`:

```python
import requests
import json
import os

def send_telegram_alert():
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    with open('analysis_results/latest_signals.json') as f:
        data = json.load(f)
    
    if data['high_priority']:
        message = f"🚨 {len(data['high_priority'])} High-Priority Signals\n\n"
        
        for signal in data['high_priority'][:3]:  # Top 3
            message += f"*{signal['symbol']}* - ₹{signal['current_price']}\n"
            message += f"Target: ₹{signal['target_price']} (+{signal['profit_potential']}%)\n\n"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        requests.post(url, json={'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    send_telegram_alert()
```

## Testing Changes

### Local Testing

```bash
# Test analysis script
python scripts/analyze_stocks.py

# Check output
cat analysis_results/latest_signals.json

# Test report generation
python scripts/generate_report.py
cat analysis_results/README.md
```

### Debug Mode

Add verbose logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def analyze_all_stocks(self):
    for symbol in self.WATCHLIST:
        logger.debug(f"Fetching data for {symbol}")
        df = self.fetch_stock_data(symbol)
        logger.debug(f"Got {len(df)} rows of data")
        # ... rest of code
```

---

**Experiment and find what works for your trading style!** 🛠️
