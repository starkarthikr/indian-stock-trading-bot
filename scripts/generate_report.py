import json
import os
from datetime import datetime
import pytz

def generate_markdown_report():
    """Generate a readable markdown report from analysis results."""
    
    results_dir = os.getenv('ANALYSIS_OUTPUT_DIR', 'analysis_results')
    
    with open(f"{results_dir}/latest_signals.json", 'r') as f:
        data = json.load(f)
    
    ist = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.fromisoformat(data['timestamp']).astimezone(ist)
    
    report = f"""# 📊 Indian Stock Market Analysis Report

**Generated:** {timestamp.strftime('%Y-%m-%d %H:%M:%S IST')}  
**Total Signals:** {data['total_signals']}  
**High Priority:** {len(data['high_priority'])}  
**Medium Priority:** {len(data['medium_priority'])}

---

## 🚨 High Priority Signals

"""
    
    if data['high_priority']:
        for stock in data['high_priority']:
            report += f"""### {stock['symbol']} - {stock['company_name']}

| Metric | Value |
|--------|-------|
| **Signal Strength** | {stock['signal_strength']}/10 ⭐ |
| **Current Price** | ₹{stock['current_price']} |
| **Entry Point** | ₹{stock['entry_point']} |
| **Target Price** | ₹{stock['target_price']} |
| **Profit Potential** | {stock['profit_potential']}% 📈 |
| **Stop Loss** | ₹{stock['stop_loss']} |
| **RSI** | {stock['rsi']} |
| **MACD Signal** | {stock['macd_signal']} |
| **Volume Ratio** | {stock['volume_ratio']}x |

**Analysis:** {stock['reasoning']}

---

"""
    else:
        report += "_No high priority signals at this time._\n\n"
    
    report += "\n## ⚠️ Medium Priority Signals\n\n"
    
    if data['medium_priority']:
        report += "| Symbol | Price | Target | Potential | Strength | RSI | Reasoning |\n"
        report += "|--------|-------|--------|-----------|----------|-----|----------|\n"
        
        for stock in data['medium_priority'][:10]:  # Top 10
            report += f"| {stock['symbol']} | ₹{stock['current_price']} | ₹{stock['target_price']} | {stock['profit_potential']}% | {stock['signal_strength']}/10 | {stock['rsi']} | {stock['reasoning'][:50]}... |\n"
    else:
        report += "_No medium priority signals at this time._\n"
    
    report += f"""

---

## 📖 How to Use This Report

1. **High Priority Signals**: Strong technical setups with multiple confirmations
2. **Entry Point**: Recommended price to enter the trade
3. **Target Price**: Expected profit-taking level (2x ATR)
4. **Stop Loss**: Risk management level (1x ATR)
5. **Signal Strength**: Combined score from multiple indicators (max 10)

**Disclaimer:** This is an automated analysis tool. Always do your own research and consult with a financial advisor before making investment decisions.

---

_Automated by GitHub Actions | Next update in 3 hours_
"""
    
    with open(f"{results_dir}/README.md", 'w') as f:
        f.write(report)
    
    print("✅ Markdown report generated")

if __name__ == "__main__":
    generate_markdown_report()
