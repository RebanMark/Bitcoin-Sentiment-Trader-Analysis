"""
Insights Generation Module
Generates actionable trading insights from sentiment analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path

class InsightsGenerator:
    def __init__(self, data_path='datasets/merged_btc_sentiment.csv'):
        self.data_path = Path(data_path)
        self.df = None
        self.insights = []
        
    def load_data(self):
        """Load merged dataset"""
        self.df = pd.read_csv(self.data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        # Add sentiment range
        bins = [0, 20, 40, 60, 80, 100]
        labels = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
        self.df['sentiment_range'] = pd.cut(self.df['sentiment_score'], 
                                             bins=bins, labels=labels, include_lowest=True)
        return self.df
    
    def identify_optimal_conditions(self):
        """Identify optimal sentiment conditions for trading"""
        print("\n" + "=" * 60)
        print("💡 OPTIMAL TRADING CONDITIONS")
        print("=" * 60)
        
        # Performance by sentiment range
        perf = self.df.groupby('sentiment_range').agg({
            'net_pnl': ['sum', 'mean', 'count'],
            'is_win': 'mean',
            'Size USD': 'mean'
        }).round(4)
        
        perf.columns = ['Total_PnL', 'Avg_PnL', 'Trades', 'Win_Rate', 'Avg_Size']
        
        best_sentiment = perf['Win_Rate'].idxmax()
        best_win_rate = perf.loc[best_sentiment, 'Win_Rate'] * 100
        
        insight = f"✓ HIGHEST WIN RATE: {best_win_rate:.1f}% during {best_sentiment} conditions"
        print(insight)
        self.insights.append(insight)
        
        # Most profitable
        most_profitable = perf['Total_PnL'].idxmax()
        total_profit = perf.loc[most_profitable, 'Total_PnL']
        
        insight = f"✓ MOST PROFITABLE: ${total_profit:,.2f} total profit during {most_profitable} conditions"
        print(insight)
        self.insights.append(insight)
        
        # Best average PnL
        best_avg = perf['Avg_PnL'].idxmax()
        avg_pnl = perf.loc[best_avg, 'Avg_PnL']
        
        insight = f"✓ BEST AVERAGE: ${avg_pnl:,.2f} per trade during {best_avg} conditions"
        print(insight)
        self.insights.append(insight)
    
    def identify_risk_patterns(self):
        """Identify risk patterns during extreme sentiment"""
        print("\n" + "=" * 60)
        print("⚠️ RISK PATTERNS")
        print("=" * 60)
        
        # Extreme sentiment analysis
        extreme_fear = self.df[self.df['sentiment_range'] == 'Extreme Fear']
        extreme_greed = self.df[self.df['sentiment_range'] == 'Extreme Greed']
        
        if len(extreme_fear) > 0:
            fear_win_rate = extreme_fear['is_win'].mean() * 100
            fear_avg_loss = extreme_fear[extreme_fear['net_pnl'] < 0]['net_pnl'].mean()
            
            insight = f"✗ Extreme Fear: {fear_win_rate:.1f}% win rate, average loss ${fear_avg_loss:,.2f}"
            print(insight)
            self.insights.append(insight)
        
        if len(extreme_greed) > 0:
            greed_win_rate = extreme_greed['is_win'].mean() * 100
            greed_avg_loss = extreme_greed[extreme_greed['net_pnl'] < 0]['net_pnl'].mean()
            
            insight = f"✗ Extreme Greed: {greed_win_rate:.1f}% win rate, average loss ${greed_avg_loss:,.2f}"
            print(insight)
            self.insights.append(insight)
        
        # Volatility in position sizing
        size_volatility = self.df.groupby('sentiment_range')['Size USD'].std()
        highest_volatility = size_volatility.idxmax()
        
        insight = f"✗ Highest position size volatility during {highest_volatility} (${ size_volatility.max():,.2f} std)"
        print(insight)
        self.insights.append(insight)
    
    def identify_behavioral_biases(self):
        """Identify behavioral biases"""
        print("\n" + "=" * 60)
        print("🧠 BEHAVIORAL BIASES DETECTED")
        print("=" * 60)
        
        # Position sizing bias
        avg_size_by_sentiment = self.df.groupby('sentiment_range')['Size USD'].mean()
        max_size_sentiment = avg_size_by_sentiment.idxmax()
        min_size_sentiment = avg_size_by_sentiment.idxmin()
        size_ratio = avg_size_by_sentiment.max() / avg_size_by_sentiment.min()
        
        insight = f"📊 Position Sizing Bias: {size_ratio:.1f}x larger positions during {max_size_sentiment} vs {min_size_sentiment}"
        print(insight)
        self.insights.append(insight)
        
        # Trade direction bias
        self.df['trade_type'] = self.df.apply(
            lambda x: 'Long' if x['is_long'] else ('Short' if x['is_short'] else 'Unknown'), axis=1
        )
        
        long_ratio = self.df.groupby('sentiment_range')['is_long'].mean() * 100
        
        for sentiment, ratio in long_ratio.items():
            if ratio > 70:
                insight = f"📈 Long Bias: {ratio:.0f}% long trades during {sentiment} (potential confirmation bias)"
                print(insight)
                self.insights.append(insight)
            elif ratio < 30:
                insight = f"📉 Short Bias: {100-ratio:.0f}% short trades during {sentiment} (potential pessimism bias)"
                print(insight)
                self.insights.append(insight)
        
        # Overtrading detection
        trade_freq = self.df.groupby('sentiment_range').size()
        if trade_freq.max() / trade_freq.min() > 2:
            max_freq_sentiment = trade_freq.idxmax()
            insight = f"⚡ Overtrading Alert: {trade_freq.max()} trades during {max_freq_sentiment} vs {trade_freq.min()} in quietest period"
            print(insight)
            self.insights.append(insight)
    
    def generate_trading_rules(self):
        """Generate sentiment-based trading rules"""
        print("\n" + "=" * 60)
        print("📋 RECOMMENDED TRADING RULES")
        print("=" * 60)
        
        # Analyze performance to create rules
        perf = self.df.groupby('sentiment_range').agg({
            'is_win': 'mean',
            'net_pnl': ['mean', 'sum'],
            'Size USD': 'mean'
        })
        
        perf.columns = ['Win_Rate', 'Avg_PnL', 'Total_PnL', 'Avg_Size']
        
        # Rule 1: High win rate conditions
        high_wr = perf[perf['Win_Rate'] > 0.55].index.tolist()
        if high_wr:
            rule = f"✓ RULE 1: Increase position size during {', '.join(high_wr)} (win rate > 55%)"
            print(rule)
            self.insights.append(rule)
        
        # Rule 2: Low win rate conditions
        low_wr = perf[perf['Win_Rate'] < 0.45].index.tolist()
        if low_wr:
            rule = f"✗ RULE 2: Reduce or avoid trading during {', '.join(low_wr)} (win rate < 45%)"
            print(rule)
            self.insights.append(rule)
        
        # Rule 3: Position sizing
        max_size_sentiment = perf['Avg_Size'].idxmax()
        current_avg = perf.loc[max_size_sentiment, 'Avg_Size']
        
        rule = f"💰 RULE 3: Current largest positions during {max_size_sentiment} (${current_avg:,.0f}) - verify this aligns with win rate"
        print(rule)
        self.insights.append(rule)
        
        # Rule 4: Trade direction
        long_performance = self.df[self.df['is_long']].groupby('sentiment_range')['is_win'].mean()
        short_performance = self.df[self.df['is_short']].groupby('sentiment_range')['is_win'].mean()
        
        for sentiment in long_performance.index:
            if sentiment in short_performance.index:
                if long_performance[sentiment] > short_performance[sentiment] + 0.1:
                    rule = f"📈 RULE 4: Favor LONG positions during {sentiment} (better performance)"
                    print(rule)
                    self.insights.append(rule)
                elif short_performance[sentiment] > long_performance[sentiment] + 0.1:
                    rule = f"📉 RULE 4: Favor SHORT positions during {sentiment} (better performance)"
                    print(rule)
                    self.insights.append(rule)
    
    def generate_summary_report(self):
        """Generate final summary report"""
        print("\n" + "=" * 60)
        print("📊 SUMMARY REPORT")
        print("=" * 60)
        
        total_trades = len(self.df)
        total_pnl = self.df['net_pnl'].sum()
        overall_wr = self.df['is_win'].mean() * 100
        
        print(f"\nOVERALL PERFORMANCE:")
        print(f"  Total Trades: {total_trades:,}")
        print(f"  Total Net P&L: ${total_pnl:,.2f}")
        print(f"  Overall Win Rate: {overall_wr:.1f}%")
        
        print(f"\nKEY INSIGHTS ({len(self.insights)} total):")
        for i, insight in enumerate(self.insights[:10], 1):  # Top 10
            print(f"  {i}. {insight}")
        
        # Save to file with UTF-8 encoding for special characters
        report_path = Path('notebooks/insights_report.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("BITCOIN SENTIMENT TRADER ANALYSIS - INSIGHTS REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total Trades: {total_trades:,}\n")
            f.write(f"Total Net P&L: ${total_pnl:,.2f}\n")
            f.write(f"Overall Win Rate: {overall_wr:.1f}%\n\n")
            f.write("KEY INSIGHTS:\n")
            f.write("-" * 60 + "\n")
            for i, insight in enumerate(self.insights, 1):
                f.write(f"{i}. {insight}\n")
        
        print(f"\n✓ Report saved to: {report_path}")
    
    def generate_all_insights(self):
        """Run complete insights generation"""
        print("=" * 60)
        print("INSIGHTS GENERATION")
        print("=" * 60)
        
        self.load_data()
        self.identify_optimal_conditions()
        self.identify_risk_patterns()
        self.identify_behavioral_biases()
        self.generate_trading_rules()
        self.generate_summary_report()
        
        print("\n" + "=" * 60)
        print("✓ INSIGHTS GENERATION COMPLETE")
        print("=" * 60)


if __name__ == '__main__':
    generator = InsightsGenerator()
    generator.generate_all_insights()
