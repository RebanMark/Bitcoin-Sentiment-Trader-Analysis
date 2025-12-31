"""
Exploratory Data Analysis Module
Creates visualizations and performs statistical tests
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

class EDAAnalyzer:
    def __init__(self, data_path='datasets/merged_btc_sentiment.csv', output_dir='notebooks'):
        self.data_path = Path(data_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.df = None
        
    def load_data(self):
        """Load merged dataset"""
        print("Loading data for EDA...")
        self.df = pd.read_csv(self.data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        # Add sentiment range
        bins = [0, 20, 40, 60, 80, 100]
        labels = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
        self.df['sentiment_range'] = pd.cut(self.df['sentiment_score'], 
                                             bins=bins, labels=labels, include_lowest=True)
        return self.df
    
    def plot_pnl_by_sentiment(self):
        """Box plot of P&L grouped by sentiment"""
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # By sentiment class
        sns.boxplot(data=self.df, x='sentiment_class', y='net_pnl', ax=axes[0])
        axes[0].set_title('Net P&L Distribution by Sentiment Class', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Sentiment Class')
        axes[0].set_ylabel('Net P&L ($)')
        axes[0].axhline(y=0, color='red', linestyle='--', alpha=0.5)
        axes[0].tick_params(axis='x', rotation=45)
        
        # By sentiment range
        sns.boxplot(data=self.df, x='sentiment_range', y='net_pnl', ax=axes[1])
        axes[1].set_title('Net P&L Distribution by Sentiment Range', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Sentiment Range')
        axes[1].set_ylabel('Net P&L ($)')
        axes[1].axhline(y=0, color='red', linestyle='--', alpha=0.5)
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'pnl_by_sentiment.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: pnl_by_sentiment.png")
        plt.close()
    
    def plot_win_rate_heatmap(self):
        """Heatmap of win rate by sentiment and trade direction"""
        # Create pivot table
        self.df['trade_type'] = self.df.apply(
            lambda x: 'Long' if x['is_long'] else ('Short' if x['is_short'] else 'Unknown'), axis=1
        )
        
        pivot = self.df.groupby(['sentiment_range', 'trade_type'])['is_win'].mean().unstack() * 100
        
        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', center=50, 
                    vmin=0, vmax=100, cbar_kws={'label': 'Win Rate (%)'})
        plt.title('Win Rate Heatmap: Sentiment vs Trade Type', fontsize=14, fontweight='bold')
        plt.xlabel('Trade Type')
        plt.ylabel('Sentiment Range')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'win_rate_heatmap.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: win_rate_heatmap.png")
        plt.close()
    
    def plot_position_size_distribution(self):
        """Position size distribution across sentiment"""
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Violin plot
        sns.violinplot(data=self.df, x='sentiment_range', y='Size USD', ax=axes[0])
        axes[0].set_title('Position Size Distribution by Sentiment', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Sentiment Range')
        axes[0].set_ylabel('Position Size (USD)')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Average position size
        avg_size = self.df.groupby('sentiment_range')['Size USD'].mean().sort_values()
        avg_size.plot(kind='barh', ax=axes[1], color='steelblue')
        axes[1].set_title('Average Position Size by Sentiment', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Average Size (USD)')
        axes[1].set_ylabel('Sentiment Range')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'position_size_sentiment.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: position_size_sentiment.png")
        plt.close()
    
    def plot_trade_timeline(self):
        """Trade count timeline with sentiment overlay"""
        daily_summary = self.df.groupby('date').agg({
            'net_pnl': 'sum',
            'sentiment_score': 'first',
            'sentiment_class': 'first'
        }).reset_index()
        
        daily_summary['trade_count'] = self.df.groupby('date').size().values
        
        fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
        
        # Trade count
        axes[0].bar(daily_summary['date'], daily_summary['trade_count'], 
                    alpha=0.6, color='steelblue', label='Trade Count')
        axes[0].set_ylabel('Number of Trades')
        axes[0].set_title('Daily Trading Activity Timeline', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Sentiment score
        axes[1].plot(daily_summary['date'], daily_summary['sentiment_score'], 
                     color='purple', linewidth=2, label='Sentiment Score')
        axes[1].axhline(y=20, color='red', linestyle='--', alpha=0.5, label='Fear Threshold')
        axes[1].axhline(y=80, color='green', linestyle='--', alpha=0.5, label='Greed Threshold')
        axes[1].fill_between(daily_summary['date'], 0, 20, alpha=0.1, color='red')
        axes[1].fill_between(daily_summary['date'], 80, 100, alpha=0.1, color='green')
        axes[1].set_ylabel('Sentiment Score')
        axes[1].set_title('Fear & Greed Index Over Time', fontsize=14, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        #Cumulative PnL
        daily_summary['cumulative_pnl'] = daily_summary['net_pnl'].cumsum()
        axes[2].plot(daily_summary['date'], daily_summary['cumulative_pnl'], 
                     color='darkgreen', linewidth=2, label='Cumulative P&L')
        axes[2].axhline(y=0, color='red', linestyle='--', alpha=0.5)
        axes[2].fill_between(daily_summary['date'], 0, daily_summary['cumulative_pnl'], 
                            where=daily_summary['cumulative_pnl']>=0, alpha=0.3, color='green')
        axes[2].fill_between(daily_summary['date'], 0, daily_summary['cumulative_pnl'], 
                            where=daily_summary['cumulative_pnl']<0, alpha=0.3, color='red')
        axes[2].set_ylabel('Cumulative P&L ($)')
        axes[2].set_xlabel('Date')
        axes[2].set_title('Cumulative P&L Performance', fontsize=14, fontweight='bold')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'trade_timeline.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: trade_timeline.png")
        plt.close()
    
    def plot_cumulative_pnl_sentiment(self):
        """Cumulative PnL with sentiment phases highlighted"""
        daily_summary = self.df.groupby('date').agg({
            'net_pnl': 'sum',
            'sentiment_score': 'first',
            'sentiment_class': 'first'
        }).reset_index().sort_values('date')
        
        daily_summary['cumulative_pnl'] = daily_summary['net_pnl'].cumsum()
        
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # Color by sentiment
        sentiment_colors = {
            'Extreme Fear': '#d32f2f',
            'Fear': '#f57c00', 
            'Neutral': '#ffd54f',
            'Greed': '#7cb342',
            'Extreme Greed': '#388e3c'
        }
        
        for sentiment, color in sentiment_colors.items():
            mask = daily_summary['sentiment_class'] == sentiment
            ax.scatter(daily_summary[mask]['date'], 
                      daily_summary[mask]['cumulative_pnl'],
                      c=color, label=sentiment, s=50, alpha=0.6)
        
        ax.plot(daily_summary['date'], daily_summary['cumulative_pnl'], 
                color='black', linewidth=1.5, alpha=0.5, zorder=0)
        ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative P&L ($)')
        ax.set_title('Cumulative P&L with Sentiment Phases Highlighted', fontsize=14, fontweight='bold')
        ax.legend(title='Sentiment', loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'cumulative_pnl_sentiment.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: cumulative_pnl_sentiment.png")
        plt.close()
    
    def statistical_tests(self):
        """Perform statistical tests"""
        print("\n" + "=" * 60)
        print("STATISTICAL TESTS")
        print("=" * 60)
        
        # ANOVA: PnL across sentiment groups
        print("\n1. ANOVA: Net P&L differences across sentiment classes")
        sentiment_groups = [group['net_pnl'].values for name, group in self.df.groupby('sentiment_class')]
        f_stat, p_value = stats.f_oneway(*sentiment_groups)
        print(f"   F-statistic: {f_stat:.4f}")
        print(f"   P-value: {p_value:.6f}")
        print(f"   Result: {'Significant' if p_value < 0.05 else 'Not significant'} difference in P&L across sentiments")
        
        # Chi-square: Trade direction independence from sentiment
        print("\n2. Chi-Square: Trade direction independence from sentiment")
        contingency = pd.crosstab(self.df['sentiment_class'], self.df['trade_type'])
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
        print(f"   Chi-square: {chi2:.4f}")
        print(f"   P-value: {p_value:.6f}")
        print(f"   Result: Trade direction {'is dependent on' if p_value < 0.05 else 'is independent of'} sentiment")
        
        # Correlation: Position size vs sentiment score
        print("\n3. Correlation: Position size vs sentiment score")
        corr, p_value = stats.pearsonr(self.df['Size USD'], self.df['sentiment_score'])
        print(f"   Pearson correlation: {corr:.4f}")
        print(f"   P-value: {p_value:.6f}")
        print(f"   Result: {'Significant' if p_value < 0.05 else 'No significant'} correlation")
        
    def run_complete_eda(self):
        """Run all EDA analyses"""
        print("=" * 60)
        print("EXPLORATORY DATA ANALYSIS")
        print("=" * 60)
        
        self.load_data()
        
        print("\nGenerating visualizations...")
        self.plot_pnl_by_sentiment()
        self.plot_win_rate_heatmap()
        self.plot_position_size_distribution()
        self.plot_trade_timeline()
        self.plot_cumulative_pnl_sentiment()
        
        self.statistical_tests()
        
        print("\n" + "=" * 60)
        print(f"✓ EDA COMPLETE - All visualizations saved to {self.output_dir}")
        print("=" * 60)


if __name__ == '__main__':
    eda = EDAAnalyzer()
    eda.run_complete_eda()
