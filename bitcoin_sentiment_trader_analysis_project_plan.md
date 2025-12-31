
---
# **1. Project Objective**
Your objective is to **explore the relationship between trader performance and market sentiment**, uncover hidden patterns, and produce insights that can help build smarter trading strategies.

Since you only have two datasets (market data + sentiment index), the project analyzes:

- How **Fear & Greed sentiment** correlates with Bitcoin’s price movement.
- Whether certain sentiment phases lead to higher volatility.
- How sentiment cycles align with trend reversals.
- How price momentum interacts with sentiment momentum.

This project focuses purely on **data-driven insights**, **exploratory analytics**, and **predictive patterns**.

---
# **2. Datasets**
All datasets are stored inside the `dataset/` folder.

### **2.1 historical_data.csv**
Contains Bitcoin’s historical market data.
Columns typically include:
- `date`
- `open`
- `high`
- `low`
- `close`
- `volume`

### **2.2 fear_greed_index.csv**
Contains daily Bitcoin sentiment (0–100 scale).
Columns include:
- `date`
- `fear_greed_score`
- `classification` (Fear / Neutral / Greed)

---
# **3. Project Workflow (Step‑by‑Step Plan)**
Below is the complete pipeline an AI agent should follow.

## **3.1 Data Loading & Cleaning**
1. Load both datasets from `dataset/` folder.
2. Convert `date` columns to datetime.
3. Align both datasets by date.
4. Handle missing values (forward/backfill or remove).
5. Normalize column names.
6. Add engineered features from both datasets.

---
# **4. Feature Engineering**
### **4.1 From Historical Price Data**
Generate:
- Daily returns
- 7‑day & 30‑day moving averages
- Price volatility
- RSI, MACD, EMA indicators
- Price momentum

### **4.2 From Fear & Greed Index**
Generate:
- Sentiment momentum (difference between days)
- 7‑day SMA of sentiment
- Sentiment volatility
- Binary labels like:
  - *High Fear* (score < 20)
  - *Extreme Greed* (score > 80)

### **4.3 Merge Data**
Final merged table structure:
```
 date | open | high | low | close | volume | return | volatility | RSI | sentiment_score | sentiment_class | sentiment_momentum | …
```

---
# **5. Exploratory Data Analysis (EDA)**
The AI should generate:

### **5.1 Visualizations**
- Price vs sentiment line graph
- Correlation heatmap
- Volatility vs sentiment scatterplot
- Boxplots: returns grouped by Fear / Greed levels
- Lag analysis: how sentiment leads/lag price

### **5.2 Statistical Tests**
- Correlation tests (Pearson/Spearman)
- Granger causality (does sentiment predict price?)
- Regime analysis (fear periods vs greed periods)

---
# **6. Modeling (Optional but Recommended)**
Since the objective is **insights**, models are lightweight:

### **6.1 Predictive Models**
- Logistic regression for next‑day up/down movement
- Random Forest feature importance
- Simple LSTM/Multi‑layer Perceptron using:
  - historical price features
  - sentiment features

### **6.2 Evaluate**
- Accuracy
- Precision/recall (up/down movements)
- MAPE for price prediction
- Sentiment contribution analysis

---
# **7. Insights to Deliver**
The AI must produce:

### **7.1 Key Relationships**
- How sentiment phases correlate with returns
- Which sentiment levels predict strong trends
- How volatility behaves during fear vs greed
- Lag effects: Does sentiment shift before price?

### **7.2 Trading Insights**
Examples:
- *Extreme fear often precedes reversals*
- *Momentum is strongest during neutral → greed transitions*
- *Volatility clusters during fear periods*

### **7.3 Actionable Strategy Ideas**
The AI should propose rule‑based strategies like:

- Buy when sentiment < 20 AND price momentum flips positive.
- Reduce exposure during extreme greed + declining sentiment momentum.

---
# **8. Folder Structure**
```
project/
│
├── dataset/
│   ├── historical_data.csv
│   └── fear_greed_index.csv
│
├── notebooks/
│   └── analysis.ipynb
│
├── src/
│   ├── data_loader.py
│   ├── feature_engineering.py
│   ├── eda.py
│   ├── modeling.py
│   └── insights.py
│
└── README.md
```

---
# **9. Deliverables**
The AI system must produce:

- Fully cleaned and merged dataset
- Visual analytics report
- Sentiment–market relationship insights
- Optional prediction model
- Strategy suggestions
- Final PDF/Notebook summary

