# option-dashboard

# 📊 Options Trading Performance Dashboard

A comprehensive Streamlit dashboard for analyzing options trading performance with focus on strategy comparison, status analysis (closed vs expired), and actionable insights.

## 🚀 Features

- **Interactive Filtering**: Filter by strategy, status, symbol, and date range
- **6 Analysis Tabs**: 
  - 📈 Overview - Core KPIs and cumulative P&L
  - 🎯 Strategy Analysis - Performance by strategy type
  - ⚡ Status Analysis - Critical closed vs expired comparison
  - 📊 Best/Worst Trades - Top performers and underperformers
  - 🔢 Delta Analysis - Portfolio delta exposure analysis
  - 📋 Trade Log - Complete searchable trade history
- **Visual Analytics**: Interactive charts with Plotly
- **Real-time Metrics**: Live calculations based on filters
- **Export Functionality**: Download filtered data as CSV

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/trading-dashboard.git
cd trading-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Prepare your data**
   - Place your CSV files in the root directory, OR
   - Update the data loading path in `trading_dashboard.py` to point to your data

## 🎮 Usage

### Running the Dashboard

```bash
streamlit run trading_dashboard.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

### Data Format

The dashboard expects CSV files with the following columns:
- `botName`: Trading bot or system name
- `type`: Strategy type (ironcondor, ironbutterfly, shortputspread, etc.)
- `symbol`: Underlying symbol (SPX, SPY, etc.)
- `status`: Trade status (closed, expired)
- `quantity`: Number of contracts
- `pnl`: Profit/Loss in dollars
- `returnPct`: Return percentage
- `daysInTrade`: Number of days trade was held
- `openDate`: Trade open date
- `closeDate`: Trade close date
- `estimated_delta`: Calculated delta exposure
- `delta_category`: Delta direction (Neutral, Bullish, Bearish)

## 📊 Key Metrics Tracked

- **Total P&L**: Overall profit/loss across all trades
- **Win Rate**: Percentage of winning trades
- **Profit Factor**: Gross profit / Gross loss ratio
- **Average P&L**: Mean profit/loss per trade
- **Status Performance**: Closed vs Expired comparison
- **Strategy Rankings**: Performance by strategy type
- **Delta Exposure**: Portfolio directional bias

## 🎯 Critical Insights

The dashboard highlights the most important finding from options trading analysis:

> **Closing trades early vs holding to expiration can produce dramatically different results.**

The Status Analysis tab provides detailed breakdown of:
- Performance multiplier (closed vs expired avg P&L)
- Win rate comparison
- Strategy-specific status performance

## 📁 Project Structure

```
trading-dashboard/
├── trading_dashboard.py       # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── trades_with_delta.csv     # Enhanced trade data (example)
└── data/                     # Optional: Directory for data files
```

## 🛠️ Customization

### Adding New Metrics

Edit `trading_dashboard.py` and add calculations in the `metrics` useMemo hook:

```python
const customMetric = useMemo(() => {
    // Your calculation here
    return calculatedValue;
}, [filteredData]);
```

### Modifying Charts

The dashboard uses Plotly for visualizations. Customize charts in the respective tab sections:

```python
fig = px.bar(
    data,
    x='category',
    y='value',
    title='Your Custom Chart',
    color='value',
    color_continuous_scale=['red', 'yellow', 'green']
)
```

### Changing Color Schemes

Update the color variables at the top of each chart section:

```python
colors = ['green' if x > 0 else 'red' for x in values]
```

## 📈 Performance Optimization

For large datasets (>1000 trades):
1. Enable caching: Use `@st.cache_data` decorator
2. Optimize filters: Reduce re-computation with `useMemo`
3. Paginate trade log: Limit initial display to 100 rows

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Charts powered by [Plotly](https://plotly.com/)
- Data analysis with [Pandas](https://pandas.pydata.org/)

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This dashboard is for educational and analysis purposes only. Not financial advice. Trade at your own risk.
