## Overview
This project explores the relationship between trader performance and market sentiment (Fear & Greed Index) to uncover hidden patterns and deliver actionable trading insights.

## Approach
We analyze how a trader's behavior correlates with Bitcoin market sentiment by examining:
- Win rates across different sentiment phases
- Position sizing patterns
- Long/Short ratios
- Entry and exit timing
- Risk behavior during extreme sentiment

## Project Structure
```
project/
├── datasets/
│   ├── historical_data.csv       # BTC transaction data
│   └── fear_greed_index.csv      # Daily sentiment scores
├── src/
│   ├── data_loader.py            # Data loading and preprocessing
│   ├── trader_analysis.py        # Performance metrics calculation
│   ├── eda.py                    # Visualizations and statistical tests
│   └── insights.py               # Insights generation
├── notebooks/
│   └── trader_sentiment_analysis.ipynb
└── README.md
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Install required packages
pip install pandas numpy matplotlib seaborn scipy statsmodels scikit-learn jupyter
```

## Usage

### 1. Data Processing
```bash
python src/data_loader.py
```

### 2. Run Analysis
```bash
python src/trader_analysis.py
python src/eda.py
python src/insights.py
```

### 3. Interactive Analysis
```bash
jupyter notebook notebooks/trader_sentiment_analysis.ipynb
```

## Key Insights
*(Will be populated after analysis)*

- Optimal sentiment conditions for trading
- Risk patterns during extreme sentiment
- Behavioral biases identified
- Recommended trading rules

## Dependencies
- pandas: Data manipulation
- numpy: Numerical computations
- matplotlib/seaborn: Visualizations
- scipy: Statistical tests
- statsmodels: Advanced statistical analysis
- scikit-learn: Machine learning utilities

## Output
<div>
<img width="2382" height="1181" alt="cumulative_pnl_sentiment" src="https://github.com/user-attachments/assets/1bac43c0-13e6-4260-9384-238f2c6b53f3" />
<img width="4764" height="1763" alt="pnl_by_sentiment" src="https://github.com/user-attachments/assets/579894d0-d73b-41ff-8826-b3829b0844aa" />
<img width="4766" height="1763" alt="position_size_sentiment" src="https://github.com/user-attachments/assets/2a69bc4d-4770-43df-a883-4712e4f34c53" />
<img width="4764" height="3561" alt="trade_timeline" src="https://github.com/user-attachments/assets/811410c6-b91e-4331-8520-83dceae8a92b" />
<img width="2775" height="1762" alt="win_rate_heatmap" src="https://github.com/user-attachments/assets/d69275af-e9d2-4e3c-b08a-1a4b024bce4c" />

</div>


