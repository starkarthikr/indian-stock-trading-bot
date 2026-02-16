import os
import json
import requests
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import pytz

class IndianStockAnalyzer:
    """Automated trading analysis system for Indian stocks."""
    
    # Top NSE stocks to monitor (Nifty 50 + high-liquidity mid-caps)
    WATCHLIST = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
        'HINDUNILVR.NS', 'BHARTIARTL.NS', 'SBIN.NS', 'BAJFINANCE.NS', 'LT.NS',
        'KOTAKBANK.NS', 'ITC.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS',
        'TITAN.NS', 'SUNPHARMA.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS', 'WIPRO.NS',
        'TATAMOTORS.NS', 'ADANIENT.NS', 'ONGC.NS', 'NTPC.NS', 'POWERGRID.NS',
        'M&M.NS', 'JSWSTEEL.NS', 'BAJAJFINSV.NS', 'HCLTECH.NS', 'DIVISLAB.NS'
    ]
    
    # NSE API base (free alternative)
    NSE_API_BASE = "http://nse-api-khaki.vercel.app:5000"
    
    def __init__(self):
        self.ist = pytz.timezone('Asia/Kolkata')
        self.results_dir = os.getenv('ANALYSIS_OUTPUT_DIR', 'analysis_results')
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Configurable thresholds
        self.min_rsi_oversold = float(os.getenv('MIN_RSI_OVERSOLD', '30'))
        self.max_rsi_overbought = 70
        self.min_volume_ratio = float(os.getenv('MIN_VOLUME_RATIO', '1.5'))
        
    def fetch_nse_data(self) -> Dict:
        """Fetch top gainers and losers from NSE."""
        try:
            gainers = requests.get(f"{self.NSE_API_BASE}/nse/get_gainers", timeout=10).json()
            losers = requests.get(f"{self.NSE_API_BASE}/nse/get_losers", timeout=10).json()
            return {'gainers': gainers, 'losers': losers}
        except Exception as e:
            print(f"Error fetching NSE data: {e}")
            return {'gainers': [], 'losers': []}
    
    def fetch_stock_data(self, symbol: str, period: str = '3mo') -> pd.DataFrame:
        """Fetch historical stock data using yfinance."""
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)
            if df.empty:
                return None
            return df
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate RSI, MACD, Moving Averages, and Bollinger Bands."""
        # RSI (14-period)
        df['RSI'] = ta.rsi(df['Close'], length=14)
        
        # MACD (12, 26, 9)
        macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
        df = pd.concat([df, macd], axis=1)
        
        # Moving Averages
        df['SMA_20'] = ta.sma(df['Close'], length=20)
        df['SMA_50'] = ta.sma(df['Close'], length=50)
        df['EMA_9'] = ta.ema(df['Close'], length=9)
        df['EMA_21'] = ta.ema(df['Close'], length=21)
        
        # Bollinger Bands
        bbands = ta.bbands(df['Close'], length=20, std=2)
        df = pd.concat([df, bbands], axis=1)
        
        # Volume indicators
        df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA']
        
        return df
    
    def generate_buy_signal(self, df: pd.DataFrame, symbol: str) -> Dict:
        """Generate buy signals based on technical analysis."""
        if df is None or len(df) < 50:
            return None
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        signal_strength = 0
        reasons = []
        
        # RSI oversold bounce
        if latest['RSI'] < 35 and latest['RSI'] > prev['RSI']:
            signal_strength += 3
            reasons.append(f"RSI bouncing from oversold ({latest['RSI']:.1f})")
        
        # MACD bullish crossover
        if (latest['MACD_12_26_9'] > latest['MACDs_12_26_9'] and 
            prev['MACD_12_26_9'] <= prev['MACDs_12_26_9']):
            signal_strength += 3
            reasons.append("MACD bullish crossover")
        
        # Price above key moving averages
        if latest['Close'] > latest['EMA_21'] > latest['SMA_50']:
            signal_strength += 2
            reasons.append("Price above key EMAs (uptrend)")
        
        # Golden cross forming
        if latest['SMA_20'] > latest['SMA_50'] and prev['SMA_20'] <= prev['SMA_50']:
            signal_strength += 2
            reasons.append("Golden Cross (SMA 20 crossing above SMA 50)")
        
        # Volume surge
        if latest['Volume_Ratio'] > self.min_volume_ratio:
            signal_strength += 1
            reasons.append(f"Volume surge ({latest['Volume_Ratio']:.1f}x average)")
        
        # Bollinger Band bounce
        if latest['Close'] < latest['BBL_20_2.0'] and latest['Close'] > prev['Close']:
            signal_strength += 1
            reasons.append("Bounce from lower Bollinger Band")
        
        # Calculate price targets and stop loss
        current_price = latest['Close']
        atr = df['High'].tail(14).max() - df['Low'].tail(14).min()
        
        entry_point = current_price
        target_price = current_price + (atr * 2)  # 2x ATR target
        stop_loss = current_price - (atr * 1)     # 1x ATR stop
        profit_potential = ((target_price - current_price) / current_price) * 100
        
        if signal_strength >= 5:
            return {
                'symbol': symbol.replace('.NS', ''),
                'company_name': self._get_company_name(symbol),
                'current_price': round(current_price, 2),
                'entry_point': round(entry_point, 2),
                'target_price': round(target_price, 2),
                'stop_loss': round(stop_loss, 2),
                'profit_potential': round(profit_potential, 2),
                'signal_strength': signal_strength,
                'rsi': round(latest['RSI'], 2),
                'macd_signal': 'Bullish' if latest['MACD_12_26_9'] > latest['MACDs_12_26_9'] else 'Bearish',
                'volume_ratio': round(latest['Volume_Ratio'], 2),
                'reasoning': ' | '.join(reasons),
                'timestamp': datetime.now(self.ist).strftime('%Y-%m-%d %H:%M:%S IST')
            }
        
        return None
    
    def _get_company_name(self, symbol: str) -> str:
        """Get company name from symbol."""
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info.get('longName', symbol.replace('.NS', ''))
        except:
            return symbol.replace('.NS', '')
    
    def analyze_all_stocks(self) -> Tuple[List[Dict], List[Dict]]:
        """Analyze all stocks in watchlist."""
        high_priority = []
        medium_priority = []
        
        print(f"\n{'='*60}")
        print(f"Starting analysis at {datetime.now(self.ist).strftime('%Y-%m-%d %H:%M:%S IST')}")
        print(f"{'='*60}\n")
        
        for symbol in self.WATCHLIST:
            print(f"Analyzing {symbol}...", end=' ')
            
            df = self.fetch_stock_data(symbol)
            if df is None:
                print("❌ No data")
                continue
            
            df = self.calculate_technical_indicators(df)
            signal = self.generate_buy_signal(df, symbol)
            
            if signal:
                if signal['signal_strength'] >= 7:
                    high_priority.append(signal)
                    print(f"✅ HIGH PRIORITY (Strength: {signal['signal_strength']}/10)")
                else:
                    medium_priority.append(signal)
                    print(f"⚠️  Medium Priority (Strength: {signal['signal_strength']}/10)")
            else:
                print("⏭️  No signal")
        
        # Sort by signal strength
        high_priority.sort(key=lambda x: x['signal_strength'], reverse=True)
        medium_priority.sort(key=lambda x: x['signal_strength'], reverse=True)
        
        return high_priority, medium_priority
    
    def save_results(self, high_priority: List[Dict], medium_priority: List[Dict]):
        """Save analysis results to JSON files."""
        timestamp = datetime.now(self.ist).strftime('%Y%m%d_%H%M%S')
        
        # Save latest signals
        results = {
            'timestamp': datetime.now(self.ist).isoformat(),
            'high_priority': high_priority,
            'medium_priority': medium_priority,
            'total_signals': len(high_priority) + len(medium_priority)
        }
        
        with open(f"{self.results_dir}/latest_signals.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save timestamped copy for history
        with open(f"{self.results_dir}/signals_{timestamp}.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✅ Results saved to {self.results_dir}/")
    
    def run(self):
        """Main execution method."""
        high_priority, medium_priority = self.analyze_all_stocks()
        self.save_results(high_priority, medium_priority)
        
        print(f"\n{'='*60}")
        print(f"Analysis Complete")
        print(f"{'='*60}")
        print(f"High Priority Signals: {len(high_priority)}")
        print(f"Medium Priority Signals: {len(medium_priority)}")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    analyzer = IndianStockAnalyzer()
    analyzer.run()
