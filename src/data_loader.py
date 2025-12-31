"""
Data Loader Module
Loads BTC transactions and Fear & Greed Index, merges them by date
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

class DataLoader:
    def __init__(self, data_dir='datasets'):
        self.data_dir = Path(data_dir)
        self.historical_path = self.data_dir / 'historical_data.csv'
        self.sentiment_path = self.data_dir / 'fear_greed_index.csv'
        
    def load_btc_transactions(self):
        """Load and filter BTC transactions"""
        print("Loading transaction data...")
        df = pd.read_csv(self.historical_path)
        
        # Filter for BTC transactions only
        btc_df = df[df['Coin'] == 'BTC'].copy()
        print(f"Found {len(btc_df):,} BTC transactions out of {len(df):,} total")
        
        # Parse timestamp
        btc_df['Timestamp IST'] = pd.to_datetime(btc_df['Timestamp IST'], format='%d-%m-%Y %H:%M')
        btc_df['date'] = btc_df['Timestamp IST'].dt.date
        
        # Convert to appropriate types
        btc_df['Execution Price'] = pd.to_numeric(btc_df['Execution Price'], errors='coerce')
        btc_df['Size Tokens'] = pd.to_numeric(btc_df['Size Tokens'], errors='coerce')
        btc_df['Size USD'] = pd.to_numeric(btc_df['Size USD'], errors='coerce')
        btc_df['Closed PnL'] = pd.to_numeric(btc_df['Closed PnL'], errors='coerce')
        btc_df['Fee'] = pd.to_numeric(btc_df['Fee'], errors='coerce')
        
        return btc_df
    
    def load_sentiment_data(self):
        """Load Fear & Greed Index"""
        print("Loading sentiment data...")
        df = pd.read_csv(self.sentiment_path)
        
        # Parse date
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        print(f"Loaded {len(df):,} sentiment records from {df['date'].min()} to {df['date'].max()}")
        
        return df
    
    def calculate_derived_metrics(self, btc_df):
        """Calculate trade-level metrics"""
        print("Calculating derived metrics...")
        
        # Net PnL after fees
        btc_df['net_pnl'] = btc_df['Closed PnL'] - btc_df['Fee']
        
        # Win/Loss classification
        btc_df['is_win'] = btc_df['net_pnl'] > 0
        btc_df['is_loss'] = btc_df['net_pnl'] < 0
        
        # Trade direction
        btc_df['is_long'] = btc_df['Direction'].str.contains('Long', case=False, na=False)
        btc_df['is_short'] = btc_df['Direction'].str.contains('Short', case=False, na=False)
        
        # Position type
        btc_df['action_type'] = btc_df['Side'].str.upper()
        
        return btc_df
    
    def merge_with_sentiment(self, btc_df, sentiment_df):
        """Merge transactions with sentiment data"""
        print("Merging with sentiment data...")
        
        # Merge on date
        merged_df = btc_df.merge(
            sentiment_df[['date', 'value', 'classification']], 
            on='date', 
            how='left'
        )
        
        # Rename sentiment columns for clarity
        merged_df.rename(columns={
            'value': 'sentiment_score',
            'classification': 'sentiment_class'
        }, inplace=True)
        
        # Fill missing sentiment with forward fill then backward fill
        merged_df['sentiment_score'] = merged_df.groupby('date')['sentiment_score'].ffill().bfill()
        merged_df['sentiment_class'] = merged_df.groupby('date')['sentiment_class'].ffill().bfill()
        
        print(f"Merged dataset: {len(merged_df):,} transactions")
        print(f"Date range: {merged_df['date'].min()} to {merged_df['date'].max()}")
        print(f"Missing sentiment: {merged_df['sentiment_score'].isna().sum()} rows")
        
        return merged_df
    
    def load_and_merge(self, save_output=True):
        """Complete data loading pipeline"""
        print("=" * 60)
        print("BITCOIN SENTIMENT TRADER ANALYSIS - DATA LOADING")
        print("=" * 60)
        
        # Load data
        btc_df = self.load_btc_transactions()
        sentiment_df = self.load_sentiment_data()
        
        # Calculate metrics
        btc_df = self.calculate_derived_metrics(btc_df)
        
        # Merge
        merged_df = self.merge_with_sentiment(btc_df, sentiment_df)
        
        # Save if requested
        if save_output:
            output_path = self.data_dir / 'merged_btc_sentiment.csv'
            merged_df.to_csv(output_path, index=False)
            print(f"\n✓ Saved merged dataset to: {output_path}")
        
        print("\n" + "=" * 60)
        print("DATA SUMMARY")
        print("=" * 60)
        print(f"Total BTC transactions: {len(merged_df):,}")
        print(f"Unique trading days: {merged_df['date'].nunique()}")
        print(f"Date range: {merged_df['date'].min()} to {merged_df['date'].max()}")
        print(f"\nSentiment Distribution:")
        print(merged_df['sentiment_class'].value_counts())
        print(f"\nTrade Direction:")
        print(f"  Long trades: {merged_df['is_long'].sum():,}")
        print(f"  Short trades: {merged_df['is_short'].sum():,}")
        print(f"\nP&L Overview:")
        print(f"  Winning trades: {merged_df['is_win'].sum():,}")
        print(f"  Losing trades: {merged_df['is_loss'].sum():,}")
        print(f"  Total Net PnL: ${merged_df['net_pnl'].sum():,.2f}")
        
        return merged_df


if __name__ == '__main__':
    # Run data loading
    loader = DataLoader()
    df = loader.load_and_merge(save_output=True)
    
    # Display sample
    print("\n" + "=" * 60)
    print("SAMPLE DATA (First 5 rows)")
    print("=" * 60)
    print(df[['date', 'Execution Price', 'Size USD', 'net_pnl', 'sentiment_score', 'sentiment_class', 'Direction']].head())
