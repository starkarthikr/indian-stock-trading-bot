"""Example configuration file for customizing the trading bot.

Copy this file to config.py and modify according to your preferences.
Note: config.py is gitignored to keep your settings private.
"""

# ============================================================================
# WATCHLIST CONFIGURATION
# ============================================================================

# Default watchlist (Nifty 50 + high-liquidity stocks)
WATCHLIST_DEFAULT = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
    'HINDUNILVR.NS', 'BHARTIARTL.NS', 'SBIN.NS', 'BAJFINANCE.NS', 'LT.NS',
    'KOTAKBANK.NS', 'ITC.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS',
    'TITAN.NS', 'SUNPHARMA.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS', 'WIPRO.NS',
    'TATAMOTORS.NS', 'ADANIENT.NS', 'ONGC.NS', 'NTPC.NS', 'POWERGRID.NS',
    'M&M.NS', 'JSWSTEEL.NS', 'BAJAJFINSV.NS', 'HCLTECH.NS', 'DIVISLAB.NS'
]

# Sector-specific watchlists
WATCHLIST_BANKING = [
    'HDFCBANK.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'AXISBANK.NS',
    'SBIN.NS', 'INDUSINDBK.NS', 'BANDHANBNK.NS', 'FEDERALBNK.NS'
]

WATCHLIST_IT = [
    'TCS.NS', 'INFY.NS', 'WIPRO.NS', 'HCLTECH.NS',
    'TECHM.NS', 'LTIM.NS', 'PERSISTENT.NS', 'COFORGE.NS'
]

WATCHLIST_AUTO = [
    'MARUTI.NS', 'TATAMOTORS.NS', 'M&M.NS', 'BAJAJ-AUTO.NS',
    'EICHERMOT.NS', 'HEROMOTOCO.NS', 'MOTHERSON.NS'
]

WATCHLIST_PHARMA = [
    'SUNPHARMA.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'CIPLA.NS',
    'AUROPHARMA.NS', 'LUPIN.NS', 'BIOCON.NS'
]

# Choose your active watchlist
ACTIVE_WATCHLIST = WATCHLIST_DEFAULT
# Or combine multiple:
# ACTIVE_WATCHLIST = WATCHLIST_BANKING + WATCHLIST_IT

# ============================================================================
# TECHNICAL INDICATOR PARAMETERS
# ============================================================================

# RSI Settings
RSI_PERIOD = 14          # Standard: 14, Faster: 9, Slower: 21
RSI_OVERSOLD = 30        # Buy signal threshold (standard: 30)
RSI_OVERBOUGHT = 70      # Sell signal threshold (standard: 70)

# MACD Settings
MACD_FAST = 12           # Fast EMA period
MACD_SLOW = 26           # Slow EMA period
MACD_SIGNAL = 9          # Signal line period

# Moving Average Settings
SMA_SHORT = 20           # Short-term SMA
SMA_LONG = 50            # Long-term SMA
EMA_SHORT = 9            # Short-term EMA
EMA_LONG = 21            # Long-term EMA

# Bollinger Bands
BB_PERIOD = 20           # Lookback period
BB_STD = 2.0             # Standard deviation multiplier

# Volume Analysis
VOLUME_MA_PERIOD = 20    # Moving average period for volume
VOLUME_SURGE_RATIO = 1.5 # Minimum ratio for volume surge (1.5x = 50% above avg)

# ============================================================================
# SIGNAL SCORING WEIGHTS
# ============================================================================

# Adjust these to prioritize different indicators
WEIGHT_RSI_BOUNCE = 3         # RSI bouncing from oversold
WEIGHT_MACD_CROSSOVER = 3     # MACD bullish crossover
WEIGHT_PRICE_ABOVE_EMA = 2    # Price above key moving averages
WEIGHT_GOLDEN_CROSS = 2       # SMA 20 crossing above SMA 50
WEIGHT_VOLUME_SURGE = 1       # Unusual volume increase
WEIGHT_BB_BOUNCE = 1          # Bounce from lower Bollinger Band

# Signal classification thresholds
HIGH_PRIORITY_THRESHOLD = 7   # Minimum score for high-priority signals
MEDIUM_PRIORITY_THRESHOLD = 5 # Minimum score for medium-priority signals

# ============================================================================
# RISK MANAGEMENT
# ============================================================================

# ATR-based targets (Average True Range)
ATR_PERIOD = 14              # Period for ATR calculation
ATR_TARGET_MULTIPLIER = 2.0  # Target = Entry + (ATR × multiplier)
ATR_STOP_MULTIPLIER = 1.0    # Stop Loss = Entry - (ATR × multiplier)

# Alternative: Fixed percentage targets (uncomment to use)
# FIXED_TARGET_PERCENT = 5.0    # 5% profit target
# FIXED_STOP_PERCENT = 3.0      # 3% stop loss

# Position sizing (if implemented)
DEFAULT_RISK_PER_TRADE = 0.02  # 2% of account per trade
DEFAULT_ACCOUNT_SIZE = 100000  # Default account size in INR

# ============================================================================
# DATA SOURCES
# ============================================================================

# Primary data source
PRIMARY_DATA_SOURCE = 'yfinance'  # Options: 'yfinance', 'alphavantage', 'finnhub'

# Data fetch parameters
HISTORICAL_PERIOD = '3mo'     # Amount of historical data to fetch
# Options: '1mo', '3mo', '6mo', '1y', '2y', '5y'

DATA_FETCH_TIMEOUT = 10        # Seconds to wait for data fetch
RETRY_ATTEMPTS = 3             # Number of retry attempts on failure

# ============================================================================
# ANALYSIS OUTPUT
# ============================================================================

# Report settings
MAX_MEDIUM_PRIORITY_DISPLAY = 10  # Number of medium-priority stocks in report
INCLUDE_REASONING = True          # Include detailed reasoning in reports
INCLUDE_CHARTS = False            # Generate price charts (requires matplotlib)

# Notification settings
CREATE_GITHUB_ISSUES = True       # Create issues for high-priority signals
ISSUE_LABELS = ['trading-signal', 'high-priority']

# Export formats
EXPORT_JSON = True               # Export signals as JSON
EXPORT_CSV = False               # Export signals as CSV
EXPORT_HTML = False              # Export signals as HTML

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Backtesting
BACKTEST_ENABLED = False
BACKTEST_PERIOD = '1y'
BACKTEST_FORWARD_DAYS = 30      # Days to check if target was hit

# Filtering
MIN_STOCK_PRICE = 10             # Minimum stock price (avoid penny stocks)
MAX_STOCK_PRICE = 50000          # Maximum stock price
MIN_DAILY_VOLUME = 100000        # Minimum daily volume

# Market hours (IST)
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 15
MARKET_CLOSE_HOUR = 15
MARKET_CLOSE_MINUTE = 30

# Debug mode
DEBUG_MODE = False               # Enable verbose logging
SAVE_INTERMEDIATE_DATA = False   # Save data at each processing step

# ============================================================================
# EXAMPLE PROFILES
# ============================================================================

# Aggressive day trader profile
PROFILE_AGGRESSIVE = {
    'RSI_PERIOD': 9,
    'RSI_OVERSOLD': 25,
    'MACD_FAST': 8,
    'MACD_SLOW': 17,
    'VOLUME_SURGE_RATIO': 2.0,
    'ATR_TARGET_MULTIPLIER': 3.0,
    'ATR_STOP_MULTIPLIER': 0.5,
    'HIGH_PRIORITY_THRESHOLD': 8
}

# Conservative swing trader profile
PROFILE_CONSERVATIVE = {
    'RSI_PERIOD': 21,
    'RSI_OVERSOLD': 35,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'VOLUME_SURGE_RATIO': 1.2,
    'ATR_TARGET_MULTIPLIER': 1.5,
    'ATR_STOP_MULTIPLIER': 1.5,
    'HIGH_PRIORITY_THRESHOLD': 6
}

# To use a profile, uncomment and apply:
# ACTIVE_PROFILE = PROFILE_CONSERVATIVE
# RSI_PERIOD = ACTIVE_PROFILE['RSI_PERIOD']
# RSI_OVERSOLD = ACTIVE_PROFILE['RSI_OVERSOLD']
# ... (apply other settings)
