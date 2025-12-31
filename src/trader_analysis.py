"""
Trader Analysis Module
Analyzes trader performance across different sentiment conditions
"""

import pandas as pd
import numpy as np
from pathlib import Path

class TraderAnalyzer:
    def __init__(self, data_path='datasets/merged_btc_sentiment.csv'):
        self.data_path = Path(data_path)
        self.df = None
        
    def load_data(self):
        """Load merged dataset"""
        print("Loading merged dataset...")
        self.df = pd.read_csv(self.data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        print(f"Loaded {len(self.df):,} transactions")
        return self.df
    
    def win_rate_by_sentiment(self):
        """Calculate win rate for each sentiment category"""
        print("\n" + "=" * 60)
        print("WIN RATE BY SENTIMENT")
        print("=" * 60)
        
        # Group by sentiment class
        sentiment_groups = self.df.groupby('sentiment_class').agg({
            'is_win': ['sum', 'count', 'mean'],
            'net_pnl': ['sum', 'mean', 'median']
        }).round(4)
        
        sentiment_groups.columns = ['Wins', 'Total_Trades', 'Win_Rate', 
                                    'Total_PnL', 'Avg_PnL', 'Median_PnL']
        
        print(sentiment_groups)
        
        # Detailed breakdown by sentiment score ranges
        print("\n" + "-" * 60)
        print("WIN RATE BY SENTIMENT SCORE RANGES")
        print("-" * 60)
        
        bins = [0, 20, 40, 60, 80, 100]
        labels = ['Extreme Fear (0-20)', 'Fear (20-40)', 'Neutral (40-60)', 
                  'Greed (60-80)', 'Extreme Greed (80-100)']
        
        self.df['sentiment_range'] = pd.cut(self.df['sentiment_score'], 
                                             bins=bins, labels=labels, include_lowest=True)
        
        range_analysis = self.df.groupby('sentiment_range').agg({
            'is_win': ['sum', 'count', 'mean'],
            'net_pnl': ['sum', 'mean']
        }).round(4)
        
        range_analysis.columns = ['Wins', 'Total', 'Win_Rate', 'Total_PnL', 'Avg_PnL']
        print(range_analysis)
        
        return sentiment_groups
    
    def position_sizing_analysis(self):
        """Analyze position sizing patterns across sentiment"""
        print("\n" + "=" * 60)
        print("POSITION SIZING BY SENTIMENT")
        print("=" * 60)
        
        sizing = self.df.groupby('sentiment_class').agg({
            'Size USD': ['mean', 'median', 'std', 'min', 'max']
        }).round(2)
        
        sizing.columns = ['Avg_Size', 'Median_Size', 'Std_Size', 'Min_Size', 'Max_Size']
        print(sizing)
        
        return sizing
    
    def trade_direction_analysis(self):
        """Analyze long vs short ratios by sentiment"""
        print("\n" + "=" * 60)
        print("TRADE DIRECTION BY SENTIMENT")
        print("=" * 60)
        
        direction = self.df.groupby('sentiment_class').agg({
            'is_long': 'sum',
            'is_short': 'sum'
        })
        
        direction['Total'] = direction['is_long'] + direction['is_short']
        direction['Long_Ratio'] = (direction['is_long'] / direction['Total'] * 100).round(2)
        direction['Short_Ratio'] = (direction['is_short'] / direction['Total'] * 100).round(2)
        
        print(direction)
        
        return direction
    
    def trade_frequency_analysis(self):
        """Analyze trading frequency across sentiment phases"""
        print("\n" + "=" * 60)
        print("TRADE FREQUENCY BY SENTIMENT")
        print("=" * 60)
        
        # Trades per day by sentiment
        daily_trades = self.df.groupby(['date', 'sentiment_class']).size().reset_index(name='trade_count')
        
        freq_stats = daily_trades.groupby('sentiment_class')['trade_count'].agg([
            'mean', 'median', 'std', 'min', 'max'
        ]).round(2)
        
        freq_stats.columns = ['Avg_Daily_Trades', 'Median', 'Std', 'Min', 'Max']
        print(freq_stats)
        
        return freq_stats
    
    def pnl_distribution_analysis(self):
        """Analyze PnL distribution across sentiment"""
        print("\n" + "=" * 60)
        print("P&L DISTRIBUTION BY SENTIMENT")
        print("=" * 60)
        
        pnl_stats = self.df.groupby('sentiment_class')['net_pnl'].describe().round(2)
        print(pnl_stats)
        
        # Calculate percentiles
        print("\n" + "-" * 60)
        print("P&L PERCENTILES BY SENTIMENT")
        print("-" * 60)
        
        percentiles = self.df.groupby('sentiment_class')['net_pnl'].quantile([0.25, 0.5, 0.75, 0.9, 0.95]).unstack()
        percentiles.columns = ['25th', '50th', '75th', '90th', '95th']
        print(percentiles.round(2))
        
        return pnl_stats
    
    def best_worst_conditions(self):
        """Identify best and worst sentiment conditions for trading"""
        print("\n" + "=" * 60)
        print("OPTIMAL VS WORST TRADING CONDITIONS")
        print("=" * 60)
        
        # Group by sentiment range
        perf = self.df.groupby('sentiment_range').agg({
            'net_pnl': ['sum', 'mean', 'count'],
            'is_win': 'mean'
        }).round(4)
        
        perf.columns = ['Total_PnL', 'Avg_PnL', 'Trade_Count', 'Win_Rate']
        perf = perf.sort_values('Win_Rate', ascending=False)
        
        print("\n📈 BEST CONDITIONS (Ranked by Win Rate):")
        print(perf.head(3))
        
        print("\n📉 WORST CONDITIONS (Ranked by Win Rate):")
        print(perf.tail(3))
        
        return perf
    
    def run_complete_analysis(self):
        """Run all analysis modules"""
        print("=" * 60)
        print("BITCOIN SENTIMENT TRADER ANALYSIS")
        print("=" * 60)
        
        self.load_data()
        
        self.win_rate_by_sentiment()
        self.position_sizing_analysis()
        self.trade_direction_analysis()
        self.trade_frequency_analysis()
        self.pnl_distribution_analysis()
        self.best_worst_conditions()
        
        print("\n" + "=" * 60)
        print("✓ ANALYSIS COMPLETE")
        print("=" * 60)


if __name__ == '__main__':
    analyzer = TraderAnalyzer()
    analyzer.run_complete_analysis()
