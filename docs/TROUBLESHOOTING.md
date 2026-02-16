# 🐛 Troubleshooting Guide

Common issues and their solutions for the Indian Stock Trading Bot.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Workflow Failures](#workflow-failures)
3. [Data Fetching Errors](#data-fetching-errors)
4. [No Signals Generated](#no-signals-generated)
5. [API Rate Limiting](#api-rate-limiting)

---

## Installation Issues

### Issue: `pandas-ta` Installation Fails

**Error Message:**
```
ERROR: Could not find a version that satisfies the requirement pandas-ta>=0.3.14b0
ERROR: No matching distribution found for pandas-ta>=0.3.14b0
```

**Solution:**

The version `0.3.14b0` doesn't exist. Use `0.3.14b` instead[web:35][web:37].

Your `requirements.txt` should have:
```
pandas-ta==0.3.14b
```

**Status:** ✅ **FIXED** - This has been corrected in the latest commit[cite:42].

---

### Issue: NumPy Version Conflict

**Error Message:**
```
ERROR: pandas-ta requires numpy<2, but you have numpy 2.x
```

**Solution:**

Constrain NumPy to version 1.x:

```txt
numpy>=1.24.0,<2.0.0
```

**Status:** ✅ **FIXED** - Already included in requirements.txt[cite:42].

---

### Issue: Python Version Incompatibility

**Error Message:**
```
ERROR: pandas-ta requires Python >=3.12
```

**Solution:**

This happens if you try to install `pandas-ta>=0.4.x`, which requires Python 3.12+[web:37].

**Options:**
1. **Use pandas-ta 0.3.14b** (supports Python 3.8-3.11) - Recommended
2. **Upgrade to Python 3.12+** - Update `.github/workflows/stock-analysis.yml`:
   ```yaml
   - name: Set up Python
     uses: actions/setup-python@v5
     with:
       python-version: '3.12'
   ```
3. **Use pandas-ta-classic** (supports Python 3.9-3.13)[web:33]:
   ```
   pip install pandas-ta-classic
   ```

---

## Workflow Failures

### Issue: Workflow Doesn't Run on Schedule

**Symptoms:**
- Scheduled workflows not executing at expected times
- No automatic runs visible in Actions tab

**Solutions:**

1. **Enable GitHub Actions**
   - Go to Actions tab
   - Click "I understand my workflows, go ahead and enable them"

2. **Repository Activity**
   - GitHub disables scheduled workflows for inactive repos
   - Make a commit to reactivate
   - Occurs if no commits for 60 days

3. **Check Cron Syntax**
   - Verify timing in `.github/workflows/stock-analysis.yml`
   - Use [crontab.guru](https://crontab.guru/) to validate
   - Remember: GitHub uses UTC, IST = UTC + 5:30

4. **Manual Trigger**
   - Use "Run workflow" button to test
   - Helps identify if issue is schedule-specific

---

### Issue: Workflow Fails at "Install Dependencies" Step

**Error Message:**
```
ERROR: Failed building wheel for pandas-ta
```

**Solution:**

1. **Check requirements.txt versions**
   - Ensure using `pandas-ta==0.3.14b`
   - Verify NumPy constraint `<2.0.0`

2. **Clear pip cache** (add to workflow):
   ```yaml
   - name: Install Dependencies
     run: |
       pip cache purge
       pip install --upgrade pip
       pip install -r requirements.txt
   ```

3. **Install from wheel** (alternative):
   ```bash
   pip install --only-binary :all: pandas-ta==0.3.14b
   ```

---

### Issue: Commit Step Fails

**Error Message:**
```
fatal: detected dubious ownership in repository
```

**Solution:**

Add safe directory configuration in workflow:

```yaml
- name: Configure Git Safe Directory
  run: |
    git config --global --add safe.directory "$GITHUB_WORKSPACE"

- name: Commit Analysis Results
  run: |
    git config --local user.email "github-actions[bot]@users.noreply.github.com"
    git config --local user.name "github-actions[bot]"
    # ... rest of commit commands
```

---

## Data Fetching Errors

### Issue: "Error fetching SYMBOL" for Multiple Stocks

**Symptoms:**
```
Analyzing RELIANCE.NS... ❌ No data
Analyzing TCS.NS... ❌ No data
```

**Solutions:**

1. **Yahoo Finance Rate Limiting**
   - Add delay between requests in `analyze_stocks.py`:
   ```python
   import time
   
   for symbol in self.WATCHLIST:
       df = self.fetch_stock_data(symbol)
       time.sleep(0.5)  # 500ms delay
   ```

2. **Network Timeout Issues**
   - Increase timeout in `fetch_stock_data()`:
   ```python
   stock = yf.Ticker(symbol)
   df = stock.history(period=period, timeout=30)  # Increase from 10
   ```

3. **Invalid Symbols**
   - Verify NSE symbols end with `.NS`
   - BSE symbols end with `.BO`
   - Check symbol is still listed/active

4. **API Keys Not Set**
   - Add Alpha Vantage or Finnhub keys to GitHub Secrets
   - Workflow will fallback to these APIs

---

### Issue: Data Fetch Succeeds but No Technical Indicators

**Error Message:**
```
KeyError: 'RSI' or 'MACD_12_26_9'
```

**Solution:**

Ensure sufficient historical data:

```python
# Need at least 50 bars for all indicators
if df is None or len(df) < 50:
    print(f"Insufficient data for {symbol}: {len(df) if df is not None else 0} bars")
    return None
```

Change fetch period if needed:
```python
df = self.fetch_stock_data(symbol, period='6mo')  # Increase from 3mo
```

---

## No Signals Generated

### Issue: Analysis Completes but No Stocks Recommended

**Symptoms:**
```
High Priority Signals: 0
Medium Priority Signals: 0
```

**This is often NORMAL** - it means no stocks meet the technical criteria at the moment.

**To Generate More Signals:**

1. **Lower RSI Threshold** (more aggressive):
   ```python
   # In analyze_stocks.py
   self.min_rsi_oversold = 25  # Default: 30
   ```

2. **Reduce Volume Requirement**:
   ```python
   self.min_volume_ratio = 1.2  # Default: 1.5
   ```

3. **Lower Signal Strength Threshold**:
   ```python
   # In generate_buy_signal()
   if signal_strength >= 4:  # Changed from 5
       return {...}
   ```

4. **Expand Watchlist**:
   ```python
   WATCHLIST = [
       # Add more stocks
       'ZOMATO.NS', 'PAYTM.NS', 'NYKAA.NS',
       'POLICYBZR.NS', 'DELHIVERY.NS'
   ]
   ```

5. **Check Market Conditions**:
   - During strong bull markets, few stocks are "oversold"
   - During bear markets, waiting for confirmation reduces signals
   - This is by design for quality over quantity

---

### Issue: Only Low-Strength Signals (4-6 points)

**Symptoms:**
- Signals generated but all below high-priority threshold
- Many stocks with 4-6 point scores

**Solutions:**

1. **Adjust Priority Thresholds**:
   ```python
   # In analyze_all_stocks()
   if signal['signal_strength'] >= 6:  # Changed from 7
       high_priority.append(signal)
   ```

2. **Review Scoring Weights**:
   - Check if indicators are conflicting
   - Adjust weights in `generate_buy_signal()`

3. **Add More Indicators**:
   - Include Stochastic, ADX for additional confirmation
   - More indicators = more potential points

---

## API Rate Limiting

### Issue: Yahoo Finance Rate Limit Errors

**Error Message:**
```
HTTPError: 429 Too Many Requests
```

**Solutions:**

1. **Add Request Delays**:
   ```python
   import time
   
   for symbol in self.WATCHLIST:
       df = self.fetch_stock_data(symbol)
       time.sleep(1)  # 1 second between requests
   ```

2. **Implement Retry Logic**:
   ```python
   from requests.adapters import HTTPAdapter
   from requests.packages.urllib3.util.retry import Retry
   
   def fetch_stock_data(self, symbol, period='3mo', retries=3):
       for attempt in range(retries):
           try:
               stock = yf.Ticker(symbol)
               df = stock.history(period=period)
               if not df.empty:
                   return df
           except Exception as e:
               if attempt < retries - 1:
                   time.sleep(2 ** attempt)  # Exponential backoff
               else:
                   print(f"Failed after {retries} attempts: {e}")
       return None
   ```

3. **Use Alpha Vantage Fallback**:
   - Add API key to secrets
   - Implement fallback in code:
   ```python
   df = self.fetch_yahoo_data(symbol)
   if df is None:
       df = self.fetch_alphavantage_data(symbol)
   ```

---

### Issue: Alpha Vantage Daily Limit Reached

**Error Message:**
```
{"Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 500 calls/day"}
```

**Solutions:**

1. **Reduce Watchlist Size**
   - Monitor fewer stocks per run
   - Rotate watchlist daily

2. **Cache Data Locally**
   - Save fetched data in artifacts
   - Only fetch updates for changed dates

3. **Use Free Finnhub API**
   - Add as secondary fallback
   - 60 calls/minute limit

4. **Upgrade API Plan**
   - Premium Alpha Vantage: $50/month for unlimited calls

---

## Debugging Tips

### Enable Debug Logging

Add to `analyze_stocks.py`:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Then use throughout code:
logger.debug(f"Fetching data for {symbol}")
logger.info(f"Signal strength: {signal_strength}")
logger.error(f"Failed to fetch {symbol}: {e}")
```

### Test Locally

```bash
# Clone and test
git clone https://github.com/starkarthikr/indian-stock-trading-bot.git
cd indian-stock-trading-bot

# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run with debug
python scripts/analyze_stocks.py

# Check output
cat analysis_results/latest_signals.json
```

### Check Workflow Logs

1. Go to Actions tab
2. Click on failed workflow run
3. Expand failed step
4. Look for specific error messages
5. Download logs for detailed analysis

---

## Getting Help

If issues persist:

1. **Search Existing Issues**: [GitHub Issues](https://github.com/starkarthikr/indian-stock-trading-bot/issues)
2. **Create New Issue**: Include:
   - Error message (full traceback)
   - Workflow run link
   - Python version
   - What you've tried
3. **Check Dependencies**: 
   - pandas-ta documentation: [GitHub](https://github.com/twopirllc/pandas-ta)
   - yfinance docs: [GitHub](https://github.com/ranaroussi/yfinance)

---

**Last Updated:** February 16, 2026
