# 🚀 Complete Setup Guide

## Prerequisites

- GitHub account
- Basic understanding of Git
- (Optional) Python 3.11+ for local testing

## Step-by-Step Setup

### 1. Get Your Own Copy

#### Option A: Fork the Repository
1. Click the **Fork** button at the top-right of the repository page
2. This creates a copy under your GitHub account
3. You'll receive all updates from the original repository

#### Option B: Use as Template
1. Click **Use this template** button
2. Create a new repository with a custom name
3. This creates an independent copy (no connection to original)

### 2. Enable GitHub Actions

1. Go to your repository
2. Click the **Actions** tab
3. Click **"I understand my workflows, go ahead and enable them"**
4. Workflows are now active and will run on schedule

### 3. Configure API Keys (Optional but Recommended)

API keys enhance data quality and reliability.

#### Alpha Vantage (Free Tier: 500 calls/day)

1. Visit [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)
2. Enter your email and click **GET FREE API KEY**
3. Copy the API key
4. In your GitHub repo: **Settings** → **Secrets and variables** → **Actions**
5. Click **New repository secret**
6. Name: `ALPHA_VANTAGE_API_KEY`
7. Value: Paste your API key
8. Click **Add secret**

#### Finnhub (Free Tier: 60 calls/minute)

1. Visit [finnhub.io/register](https://finnhub.io/register)
2. Sign up with email
3. Go to Dashboard and copy your API key
4. Add to GitHub secrets as `FINNHUB_API_KEY`

### 4. Run Your First Analysis

#### Manual Trigger

1. Go to **Actions** tab
2. Click **Indian Stock Market Analysis** workflow
3. Click **Run workflow** dropdown (right side)
4. (Optional) Adjust parameters:
   - `min_rsi_oversold`: Default 30 (lower = more aggressive)
   - `min_volume_ratio`: Default 1.5 (higher = stricter)
5. Click **Run workflow** button
6. Wait 5-10 minutes for completion

#### Check Results

**Option 1: View in Repository**
- Navigate to `analysis_results/README.md`
- See formatted report with all signals

**Option 2: GitHub Issues**
- Go to **Issues** tab
- High-priority signals automatically create issues
- Look for 🚨 labels

**Option 3: Download Artifacts**
- Go to **Actions** tab
- Click on the completed workflow run
- Scroll to **Artifacts** section
- Download `stock-analysis-X` ZIP file
- Contains JSON data for programmatic use

### 5. Customize for Your Needs

#### Change Watchlist

Edit `scripts/analyze_stocks.py`:

```python
WATCHLIST = [
    # Large-cap focus
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS',
    
    # Mid-cap momentum
    'ZOMATO.NS', 'PAYTM.NS', 'POLICYBZR.NS',
    
    # Your custom picks
    'TATASTEEL.NS', 'ADANIPORTS.NS'
]
```

Commit and push changes:
```bash
git add scripts/analyze_stocks.py
git commit -m "Update watchlist with my preferred stocks"
git push
```

#### Adjust Schedule

Edit `.github/workflows/stock-analysis.yml`:

```yaml
schedule:
  # Every hour during market hours (9 AM - 3 PM IST)
  - cron: '30 3-9 * * 1-5'  # UTC times
  
  # Or just once daily at market close
  - cron: '30 9 * * 1-5'    # 3:00 PM IST
```

**Cron Time Converter**: IST = UTC + 5:30
- 9:30 AM IST = 4:00 AM UTC
- 3:00 PM IST = 9:30 AM UTC

Use [crontab.guru](https://crontab.guru/) to design custom schedules.

#### Modify Signal Thresholds

Edit `scripts/analyze_stocks.py`:

```python
def __init__(self):
    # More aggressive oversold detection
    self.min_rsi_oversold = 25  # Default: 30
    
    # Stricter volume requirements
    self.min_volume_ratio = 2.0  # Default: 1.5
    
    # Overbought threshold
    self.max_rsi_overbought = 75  # Default: 70
```

### 6. Set Up Notifications

#### Email Notifications

1. Go to your GitHub profile (top-right corner)
2. **Settings** → **Notifications**
3. Under **Actions**:
   - Check "Email" for workflow run notifications
   - Optionally enable for failed runs only

#### Mobile Notifications

1. Install [GitHub Mobile App](https://github.com/mobile)
2. Sign in with your account
3. Enable push notifications for:
   - Workflow runs
   - Issues (for high-priority signals)

#### Webhook/Discord/Slack

Add to workflow file after "Create Issue" step:

```yaml
- name: Send Discord Notification
  if: success()
  run: |
    curl -H "Content-Type: application/json" \
      -d '{"content": "New trading signals generated! Check repository."}' \
      ${{ secrets.DISCORD_WEBHOOK_URL }}
```

Add `DISCORD_WEBHOOK_URL` to repository secrets.

## Troubleshooting

### Workflow Not Running

**Issue**: Scheduled workflow doesn't execute

**Solutions**:
1. Ensure Actions are enabled (Settings → Actions)
2. Check if repository has recent activity (GitHub may disable Actions for inactive repos)
3. Make a commit to "wake up" the repository
4. Verify cron syntax is correct

### No Signals Generated

**Issue**: Analysis completes but no stocks recommended

**Reasons**:
1. Market conditions don't meet criteria (normal)
2. Thresholds too strict
3. Watchlist stocks not showing technical setups

**Solutions**:
- Lower `min_rsi_oversold` to 25
- Reduce `min_volume_ratio` to 1.2
- Expand watchlist to more stocks
- Check `analysis_results/signals_*.json` for near-misses

### Data Fetch Errors

**Issue**: "Error fetching SYMBOL" messages

**Solutions**:
1. Check internet connectivity (unlikely in GitHub Actions)
2. Verify symbol format (must end with `.NS` for NSE)
3. Yahoo Finance API may be rate-limiting (add delays)
4. Add API keys for alternative data sources

### Python Dependency Errors

**Issue**: `pip install` fails or import errors

**Solutions**:
1. Update `requirements.txt` versions
2. Pin specific versions: `pandas==2.1.0`
3. Check Python version compatibility
4. Clear pip cache: Add `pip cache purge` before install

## Advanced Configuration

### Add More Technical Indicators

Edit `calculate_technical_indicators()` in `scripts/analyze_stocks.py`:

```python
# Stochastic Oscillator
stoch = ta.stoch(df['High'], df['Low'], df['Close'])
df = pd.concat([df, stoch], axis=1)

# Average Directional Index (ADX)
df['ADX'] = ta.adx(df['High'], df['Low'], df['Close'])['ADX_14']

# Commodity Channel Index (CCI)
df['CCI'] = ta.cci(df['High'], df['Low'], df['Close'], length=20)
```

Then update `generate_buy_signal()` to use these indicators:

```python
# Strong trend confirmation
if latest['ADX'] > 25:
    signal_strength += 1
    reasons.append(f"Strong trend (ADX: {latest['ADX']:.1f})")
```

### Backtesting

Create `scripts/backtest.py`:

```python
import pandas as pd
from analyze_stocks import IndianStockAnalyzer

analyzer = IndianStockAnalyzer()

for symbol in analyzer.WATCHLIST:
    df = analyzer.fetch_stock_data(symbol, period='1y')
    if df is None:
        continue
    
    df = analyzer.calculate_technical_indicators(df)
    
    # Check each historical date
    for i in range(50, len(df)):
        historical_df = df.iloc[:i]
        signal = analyzer.generate_buy_signal(historical_df, symbol)
        
        if signal:
            # Check if target was hit in next 30 days
            future_df = df.iloc[i:i+30]
            max_price = future_df['High'].max()
            
            target_hit = max_price >= signal['target_price']
            print(f"{symbol}: Target {'HIT' if target_hit else 'MISSED'}")
```

### Export to CSV

Add to `generate_report.py`:

```python
import pandas as pd

def export_to_csv():
    with open(f"{results_dir}/latest_signals.json", 'r') as f:
        data = json.load(f)
    
    # Combine high and medium priority
    all_signals = data['high_priority'] + data['medium_priority']
    
    # Convert to DataFrame
    df = pd.DataFrame(all_signals)
    
    # Export
    df.to_csv(f"{results_dir}/signals.csv", index=False)
    print("✅ CSV exported")
```

## Next Steps

1. **Monitor Performance**: Track signal accuracy over 2-4 weeks
2. **Refine Parameters**: Adjust thresholds based on hit rate
3. **Paper Trade**: Test signals without real money first
4. **Expand Watchlist**: Add promising mid-cap and small-cap stocks
5. **Combine with Fundamentals**: Use technical signals as entry timing for fundamentally strong stocks

## Support

For issues or questions:
1. Check [GitHub Issues](https://github.com/starkarthikr/indian-stock-trading-bot/issues)
2. Review [pandas-ta documentation](https://github.com/twopirllc/pandas-ta)
3. Consult [yfinance documentation](https://github.com/ranaroussi/yfinance)

---

**Happy Trading! 🚀📊**
