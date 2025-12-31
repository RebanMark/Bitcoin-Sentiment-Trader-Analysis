# Bitcoin Sentiment Trader Analysis - Complete Guide

This guide explains everything from start to finish: what the code does, how it works, and how to interpret the visualizations.

---

## Table of Contents
1. [What This Project Does](#what-this-project-does)
2. [How to Run the Analysis](#how-to-run-the-analysis)
3. [Understanding Each Module](#understanding-each-module)
4. [Understanding the Visualizations](#understanding-the-visualizations)
5. [Interpreting the Results](#interpreting-the-results)

---

## What This Project Does

### The Big Picture

This project answers one main question: **"Does market sentiment affect my trading performance?"**

It analyzes your Bitcoin trading history and compares it with the Bitcoin Fear & Greed Index to find:
- When you trade best (Fear vs Greed)
- How sentiment affects your position sizing
- Whether you have behavioral biases
- What trading rules could improve performance

### The Data

**Input #1: Your Bitcoin Trades** (`datasets/historical_data.csv`)
- 26,064 BTC transactions
- Details: price, size, direction (long/short), profit/loss, timestamps

**Input #2: Fear & Greed Index** (`datasets/fear_greed_index.csv`)
- Daily sentiment scores (0-100)
- 0-20 = Extreme Fear
- 20-40 = Fear
- 40-60 = Neutral
- 60-80 = Greed
- 80-100 = Extreme Greed

**Output: Insights about how your trading performance changes with market sentiment**

---

## How to Run the Analysis

### Step 1: Activate Virtual Environment
```bash
# On Windows
.venv\Scripts\activate
```
You'll see `(.venv)` at the start of your command prompt.

### Step 2: Run the Analysis Pipeline

**Option A: Run All Modules (Recommended First Time)**
```bash
# 1. Load and merge data
.\.venv\Scripts\python.exe src\data_loader.py

# 2. Analyze trading performance
.\.venv\Scripts\python.exe src\trader_analysis.py

# 3. Create visualizations
.\.venv\Scripts\python.exe src\eda.py

# 4. Generate insights and recommendations
.\.venv\Scripts\python.exe src\insights.py
```

**Option B: Interactive Jupyter Notebook**
```bash
.\.venv\Scripts\jupyter notebook notebooks/trader_sentiment_analysis.ipynb
```

### What Happens When You Run It?

1. **Data Loader** merges your trades with sentiment data → Creates `merged_btc_sentiment.csv`
2. **Trader Analysis** calculates win rates, P&L by sentiment → Prints statistics
3. **EDA** generates 5 visualizations → Saves PNG files in `notebooks/`
4. **Insights** creates trading recommendations → Saves `insights_report.txt`

---

## Understanding Each Module

### Module 1: data_loader.py

**What it does:**
1. Loads your 211,224 total transactions
2. Filters only BTC trades (26,064 transactions)
3. Loads the Fear & Greed Index (2,644 daily records)
4. Matches each trade to the sentiment on that day
5. Calculates: win/loss, net P&L (after fees), trade direction

**Output:**
- `datasets/merged_btc_sentiment.csv` - One file with everything combined

**Key Metrics Added:**
- `net_pnl` = Closed P&L - Fees (your actual profit/loss)
- `is_win` = True if profitable
- `is_long` / `is_short` = Trade direction
- `sentiment_score` = 0-100 fear/greed score
- `sentiment_class` = Extreme Fear, Fear, Neutral, Greed, Extreme Greed

---

### Module 2: trader_analysis.py

**What it does:**
Calculates your performance statistics grouped by sentiment.

**Analysis Performed:**

1. **Win Rate by Sentiment**
   - For each sentiment level, calculates: wins ÷ total trades
   - Example: "During Fear, you won 40.1% of trades"

2. **Position Sizing**
   - Average, median, min, max position sizes per sentiment
   - Reveals if you trade larger during fear or greed

3. **Trade Direction**
   - Long vs Short ratio for each sentiment
   - Example: "83% long trades during Extreme Fear"

4. **Trade Frequency**
   - How many trades per day in each sentiment phase
   - Identifies overtrading periods

5. **P&L Distribution**
   - Total profit, average profit per trade
   - Percentiles to show extreme outcomes

**Output:** Prints detailed tables to console

---

### Module 3: eda.py

**What it does:**
Creates 5 visualization files and runs 3 statistical tests.

**Visualizations Created:**

1. **pnl_by_sentiment.png** - Box plots of your profit/loss
2. **win_rate_heatmap.png** - Color grid showing best conditions
3. **position_size_sentiment.png** - How big you trade in each phase
4. **trade_timeline.png** - Your trading history over time
5. **cumulative_pnl_sentiment.png** - Your profit curve colored by sentiment

**Statistical Tests:**

1. **ANOVA** - Tests if P&L is truly different across sentiments
2. **Chi-Square** - Tests if your long/short choice depends on sentiment
3. **Correlation** - Tests if position size correlates with sentiment

**Output:** 5 PNG files in `notebooks/` folder

---

### Module 4: insights.py

**What it does:**
Analyzes everything and creates actionable recommendations.

**Insights Generated:**

1. **Optimal Conditions** - When you perform best
2. **Risk Patterns** - When to be careful
3. **Behavioral Biases** - Your psychological patterns
4. **Trading Rules** - Specific recommendations

**Output:** 
- `notebooks/insights_report.txt` - Text file with all insights
- Console output with colored emojis

---

## Understanding the Visualizations

### 1. P&L by Sentiment (pnl_by_sentiment.png)

**What you see:**
- Two box plots showing profit/loss distribution
- Left: grouped by sentiment class (Fear, Greed, etc.)
- Right: grouped by sentiment ranges (0-20, 20-40, etc.)

**How to read it:**
- **Box**: Middle 50% of your trades
- **Line in box**: Median (middle value)
- **Whiskers**: Full range (excluding outliers)
- **Dots**: Outlier trades (very big wins/losses)
- **Red dashed line**: Break-even point (0)

**What to look for:**
- Which sentiment has boxes ABOVE zero? (profitable)
- Which sentiment has taller boxes? (more consistent)
- Are there more outliers above or below? (big wins vs big losses)

**Example interpretation:**
"During Fear, my median trade is slightly profitable, but I have some big losses. During Greed, I'm consistently losing money."

---

### 2. Win Rate Heatmap (win_rate_heatmap.png)

**What you see:**
- Color grid: rows = sentiment levels, columns = Long/Short/Unknown
- Colors: Green = high win rate, Red = low win rate
- Numbers: exact win rate percentage

**How to read it:**
- **Green cells** (>50%) = Good conditions for that trade type
- **Red cells** (<30%) = Bad conditions
- **Yellow** (~50%) = Neutral/random

**What to look for:**
- Which sentiment + direction combination is greenest?
- Are Longs better during certain sentiments?
- Are there any red cells you should avoid?

**Example interpretation:**
"Long trades during Extreme Fear have 45% win rate (yellow), but Short trades during Greed have only 25% (red). I should avoid shorting during greed."

---

### 3. Position Size Distribution (position_size_sentiment.png)

**What you see:**
- Left: Violin plots (sideways distributions)
- Right: Horizontal bar chart of average sizes

**How to read it:**
- **Violin width**: How common that position size is
- **Wider = more trades at that size**
- **Taller violin**: Wider range of position sizes

**What to look for:**
- Do you trade larger during fear or greed?
- Is your position sizing consistent (narrow) or variable (wide)?
- Are there different "clusters" of sizes?

**Example interpretation:**
"I trade 2x larger positions during Fear ($31,609 avg) vs Extreme Greed ($16,000 avg). This might be increasing risk at the wrong time."

---

### 4. Trade Timeline (trade_timeline.png)

**What you see:**
Three stacked charts over time:
- **Top**: Number of trades per day (blue bars)
- **Middle**: Fear & Greed score (purple line)
- **Bottom**: Your cumulative profit (green/red line)

**How to read it:**
- **Top chart**: Tall bars = active trading days
- **Middle chart**: Purple line movements show sentiment changes
  - Above 80 = Extreme Greed zone (green shading)
  - Below 20 = Extreme Fear zone (red shading)
- **Bottom chart**: Line going up = making money, down = losing money
  - Green area = profitable periods
  - Red area = loss periods

**What to look for:**
- Do you trade more when sentiment is extreme?
- Does your profit curve drop during specific sentiment periods?
- Are there long periods where you're inactive?

**Example interpretation:**
"I see my profit curve drops sharply whenever sentiment hits Extreme Greed (green zone in middle chart). Maybe I should reduce trading during those times."

---

### 5. Cumulative P&L with Sentiment (cumulative_pnl_sentiment.png)

**What you see:**
- Black line: Your total profit over time
- Colored dots: Each day colored by sentiment
  - Red = Extreme Fear
  - Orange = Fear
  - Yellow = Neutral
  - Light green = Greed
  - Dark green = Extreme Greed

**How to read it:**
- **Line slope up**: Making money
- **Line slope down**: Losing money
- **Flat line**: Breaking even
- **Dot color**: What sentiment was that day

**What to look for:**
- What color dots appear when line goes up?
- What color dots appear when line goes down?
- Are steep drops clustered with certain colors?

**Example interpretation:**
"My biggest profit gains (steep upward slopes) happen on orange dots (Fear). My losses (downward slopes) happen on dark green dots (Extreme Greed)."

---

## Interpreting the Results

### Your Actual Results Summary

Based on the analysis run, here's what was found:

#### Overall Performance
- **Total Trades**: 26,064
- **Total Net P&L**: $728,820.51 ✅
- **Overall Win Rate**: 34.6%
- **Trading Period**: Dec 2023 - May 2025 (286 days)

#### Best Performance: FEAR 🎯

| Metric | Value |
|--------|-------|
| Win Rate | 40.1% (highest) |
| Total Profit | $370,071.31 |
| Avg per Trade | $45.65 |
| Number of Trades | 8,106 |

**Interpretation:** You perform BEST during Fear. This is counterintuitive but valuable!

#### Worst Performance

| Sentiment | Win Rate | Total P&L |
|-----------|----------|-----------|
| Neutral | 31.6% | $306,366 (high volume, low efficiency) |
| Greed | 32.6% | $76,721 |
| Extreme Fear | 33.9% | -$48,243 (losing money) |

**Interpretation:** Avoid extreme fear, and be cautious during neutral markets.

---

### Statistical Significance

All three tests were **statistically significant** (p < 0.001), meaning:

1. ✅ **Sentiment DOES affect your P&L** (not random)
2. ✅ **Your trade direction choice DEPENDS on sentiment** (you have biases)
3. ✅ **Your position sizing correlates with sentiment** (you size differently)

---

### Behavioral Biases Detected

1. **Long Bias During Fear**
   - 72% of trades during Fear are LONG
   - 83% during Extreme Fear are LONG
   - This might be "buying the dip" or confirmation bias

2. **Position Sizing Bias**
   - You trade 1.9x larger during Fear vs Extreme Greed
   - Largest average position: $31,609 during Fear

3. **Overtrading During Neutral**
   - 9,823 trades during Neutral sentiment
   - Only 731 trades during Extreme Greed
   - You might be forcing trades when there's no clear sentiment

---

### Recommended Trading Rules

Based on your data:

1. ✅ **INCREASE trading during Fear** (40.1% win rate, highest profit)
2. ❌ **REDUCE trading during Neutral** (31.6% win rate, overtrading)
3. ❌ **AVOID Extreme Fear** (losing money: -$48,243)
4. ⚠️ **VERIFY position sizing** - Largest positions during Fear might be increasing risk
5. 📊 **FAVOR LONG positions** during Extreme Fear (better performance than shorts)

---

## Next Steps

### 1. Review Your Visualizations
Open each PNG file in `notebooks/` and compare to this guide.

### 2. Read the Insights Report
```bash
# Read the full report
type notebooks\insights_report.txt
```

### 3. Run the Jupyter Notebook
```bash
.\.venv\Scripts\jupyter notebook notebooks/trader_sentiment_analysis.ipynb
```
This gives you an interactive environment to explore the data further.

### 4. Implement Changes
Based on your results:
- Set alerts for Fear periods (good trading opportunities)
- Reduce position sizes during high-volatility periods
- Avoid overtrading during Neutral sentiment
- Track if following these rules improves future performance

### 5. Monitor Forward Performance
Run this analysis again after 1-2 months to see if:
- Your win rate improved
- Behavioral biases reduced
- Overall P&L increased

---

## Common Questions

**Q: Why is my win rate only 34.6%?**
A: Win rate alone doesn't determine profitability. You can be profitable with a 35% win rate if your average win is larger than your average loss. Your total P&L is positive ($728K), which is what matters.

**Q: Should I only trade during Fear?**
A: Not necessarily. Fear is your BEST condition, but you also made money during Neutral and Greed. Focus on INCREASING trading during Fear and REDUCING during your worst conditions.

**Q: What's a "good" win rate?**
A: Depends on your strategy. Day traders: 50-60%. Swing traders: 40-50%. Your 40.1% during Fear is solid for active trading.

**Q: How do I use this going forward?**
A: Before entering a trade, check the Fear & Greed Index. If it's in Fear, you historically perform better. If it's Extreme Fear or Neutral, be more cautious.

**Q: Can I run this on other coins?**
A: Yes! Just filter for different coins in `data_loader.py`. Change line 21 from `df['Coin'] == 'BTC'` to `df['Coin'] == 'ETH'` etc.

---

## Troubleshooting

**"Module not found" error:**
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

**"File not found" error:**
```bash
# Make sure you're in the project directory
cd e:\Projects\primetrade.ai

# Check datasets exist
dir datasets
```

**Visualizations not appearing:**
```bash
# Check if PNG files were created
dir notebooks\*.png

# If missing, run EDA again
.\.venv\Scripts\python.exe src\eda.py
```

---

## Summary

This project proves that **market sentiment significantly affects your trading performance**. Your best results come during Fear periods, with a 40.1% win rate and $370K in profits. By focusing your trading activity on sentiment phases where you historically perform well, you can potentially improve your overall returns.

The key insight: **Trade MORE during Fear, LESS during Neutral, and AVOID Extreme Fear.**
