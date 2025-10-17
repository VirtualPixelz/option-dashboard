import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Options Trading Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .positive {
        color: #00ff00;
        font-weight: bold;
    }
    .negative {
        color: #ff0000;
        font-weight: bold;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('/home/claude/trades_with_delta.csv')
    df['openDate'] = pd.to_datetime(df['openDate'])
    df['closeDate'] = pd.to_datetime(df['closeDate'])
    df['winning_trade'] = df['pnl'] > 0
    df['month'] = df['openDate'].dt.to_period('M').astype(str)
    return df

df = load_data()

# Title
st.markdown('<p class="main-header">📊 Options Trading Performance Dashboard</p>', unsafe_allow_html=True)
st.markdown(f"**Analysis Period:** {df['openDate'].min().strftime('%B %d, %Y')} - {df['openDate'].max().strftime('%B %d, %Y')} | **Total Trades:** {len(df)}")

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Strategy filter
strategies = ['All'] + sorted(df['type'].unique().tolist())
selected_strategy = st.sidebar.selectbox("Strategy", strategies)

# Status filter
statuses = ['All'] + sorted(df['status'].unique().tolist())
selected_status = st.sidebar.selectbox("Status", statuses)

# Symbol filter
symbols = ['All'] + sorted(df['symbol'].unique().tolist())
selected_symbol = st.sidebar.selectbox("Symbol", symbols)

# Date range filter
date_range = st.sidebar.date_input(
    "Date Range",
    value=(df['openDate'].min(), df['openDate'].max()),
    min_value=df['openDate'].min(),
    max_value=df['openDate'].max()
)

# Apply filters
filtered_df = df.copy()
if selected_strategy != 'All':
    filtered_df = filtered_df[filtered_df['type'] == selected_strategy]
if selected_status != 'All':
    filtered_df = filtered_df[filtered_df['status'] == selected_status]
if selected_symbol != 'All':
    filtered_df = filtered_df[filtered_df['symbol'] == selected_symbol]
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['openDate'].dt.date >= date_range[0]) &
        (filtered_df['openDate'].dt.date <= date_range[1])
    ]

# Calculate metrics
total_pnl = filtered_df['pnl'].sum()
avg_pnl = filtered_df['pnl'].mean()
median_pnl = filtered_df['pnl'].median()
win_rate = (filtered_df['pnl'] > 0).sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
total_trades = len(filtered_df)

gross_profit = filtered_df[filtered_df['pnl'] > 0]['pnl'].sum()
gross_loss = abs(filtered_df[filtered_df['pnl'] < 0]['pnl'].sum())
profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Overview", 
    "🎯 Strategy Analysis", 
    "⚡ Status Analysis", 
    "📊 Best/Worst Trades",
    "🔢 Delta Analysis",
    "📋 Trade Log"
])

# TAB 1: OVERVIEW
with tab1:
    # Key Metrics Row
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric(
            "Total P&L",
            f"${total_pnl:,.0f}",
            delta=f"{total_pnl/total_trades:.0f} per trade" if total_trades > 0 else "N/A"
        )
    
    with col2:
        st.metric(
            "Win Rate",
            f"{win_rate:.1f}%",
            delta="Above Target" if win_rate >= 75 else "Below Target",
            delta_color="normal" if win_rate >= 75 else "inverse"
        )
    
    with col3:
        st.metric(
            "Total Trades",
            f"{total_trades}",
            delta=f"{total_trades//2} per month"
        )
    
    with col4:
        st.metric(
            "Avg P&L",
            f"${avg_pnl:.0f}",
            delta=f"Median: ${median_pnl:.0f}"
        )
    
    with col5:
        st.metric(
            "Profit Factor",
            f"{profit_factor:.2f}",
            delta="Excellent" if profit_factor >= 2.0 else "Good" if profit_factor >= 1.5 else "Poor",
            delta_color="normal" if profit_factor >= 2.0 else "off"
        )
    
    with col6:
        best_trade = filtered_df['pnl'].max()
        st.metric(
            "Best Trade",
            f"${best_trade:,.0f}",
            delta=f"Worst: ${filtered_df['pnl'].min():,.0f}"
        )
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Cumulative P&L
        df_sorted = filtered_df.sort_values('closeDate')
        df_sorted['cumulative_pnl'] = df_sorted['pnl'].cumsum()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_sorted['closeDate'],
            y=df_sorted['cumulative_pnl'],
            mode='lines',
            name='Cumulative P&L',
            line=dict(color='#1f77b4', width=3),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
        fig.update_layout(
            title="Cumulative P&L Over Time",
            xaxis_title="Date",
            yaxis_title="Cumulative P&L ($)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # P&L Distribution
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=filtered_df['pnl'],
            nbinsx=30,
            marker_color='steelblue',
            name='P&L Distribution'
        ))
        fig.add_vline(x=avg_pnl, line_dash="dash", line_color="red", 
                      annotation_text=f"Mean: ${avg_pnl:.0f}")
        fig.add_vline(x=median_pnl, line_dash="dash", line_color="green",
                      annotation_text=f"Median: ${median_pnl:.0f}")
        fig.update_layout(
            title="P&L Distribution",
            xaxis_title="P&L ($)",
            yaxis_title="Frequency",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly Performance
        monthly_pnl = filtered_df.groupby('month')['pnl'].sum().reset_index()
        fig = px.bar(
            monthly_pnl,
            x='month',
            y='pnl',
            title="Monthly P&L",
            labels={'pnl': 'P&L ($)', 'month': 'Month'},
            color='pnl',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Win/Loss Breakdown
        win_loss = pd.DataFrame({
            'Result': ['Wins', 'Losses'],
            'Count': [
                (filtered_df['pnl'] > 0).sum(),
                (filtered_df['pnl'] <= 0).sum()
            ],
            'Total P&L': [
                filtered_df[filtered_df['pnl'] > 0]['pnl'].sum(),
                filtered_df[filtered_df['pnl'] <= 0]['pnl'].sum()
            ]
        })
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Trade Count', 'Total P&L'),
            specs=[[{'type':'pie'}, {'type':'pie'}]]
        )
        
        fig.add_trace(go.Pie(
            labels=win_loss['Result'],
            values=win_loss['Count'],
            marker_colors=['green', 'red'],
            name='Count'
        ), row=1, col=1)
        
        fig.add_trace(go.Pie(
            labels=win_loss['Result'],
            values=win_loss['Total P&L'],
            marker_colors=['green', 'red'],
            name='P&L'
        ), row=1, col=2)
        
        fig.update_layout(title_text="Win/Loss Analysis", height=400)
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: STRATEGY ANALYSIS
with tab2:
    st.header("🎯 Strategy Performance Analysis")
    
    # Strategy metrics
    strategy_stats = filtered_df.groupby('type').agg({
        'pnl': ['sum', 'mean', 'median', 'count'],
        'winning_trade': 'mean',
        'returnPct': 'mean',
        'daysInTrade': 'mean'
    }).round(2)
    
    strategy_stats.columns = ['Total_PnL', 'Avg_PnL', 'Median_PnL', 'Trades', 'Win_Rate', 'Avg_Return_%', 'Avg_Days']
    strategy_stats['Win_Rate'] = (strategy_stats['Win_Rate'] * 100).round(1)
    strategy_stats = strategy_stats.sort_values('Total_PnL', ascending=False)
    
    # Calculate profit factor by strategy
    profit_factors = []
    for strategy in strategy_stats.index:
        strategy_trades = filtered_df[filtered_df['type'] == strategy]
        gp = strategy_trades[strategy_trades['pnl'] > 0]['pnl'].sum()
        gl = abs(strategy_trades[strategy_trades['pnl'] < 0]['pnl'].sum())
        pf = gp / gl if gl > 0 else float('inf')
        profit_factors.append(pf)
    
    strategy_stats['Profit_Factor'] = profit_factors
    
    # Display strategy table
    st.subheader("Strategy Performance Summary")
    st.dataframe(
        strategy_stats.style.background_gradient(subset=['Total_PnL'], cmap='RdYlGn')
                           .background_gradient(subset=['Win_Rate'], cmap='RdYlGn')
                           .format({
                               'Total_PnL': '${:,.0f}',
                               'Avg_PnL': '${:,.0f}',
                               'Median_PnL': '${:,.0f}',
                               'Win_Rate': '{:.1f}%',
                               'Avg_Return_%': '{:.2%}',
                               'Avg_Days': '{:.2f}',
                               'Profit_Factor': '{:.2f}'
                           }),
        use_container_width=True
    )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Total P&L by Strategy
        fig = px.bar(
            strategy_stats.reset_index(),
            x='type',
            y='Total_PnL',
            title="Total P&L by Strategy",
            labels={'type': 'Strategy', 'Total_PnL': 'Total P&L ($)'},
            color='Total_PnL',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Win Rate by Strategy
        fig = px.bar(
            strategy_stats.reset_index(),
            x='type',
            y='Win_Rate',
            title="Win Rate by Strategy",
            labels={'type': 'Strategy', 'Win_Rate': 'Win Rate (%)'},
            color='Win_Rate',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig.add_hline(y=75, line_dash="dash", line_color="blue", 
                      annotation_text="Target: 75%")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Trade count by strategy
        trade_counts = filtered_df['type'].value_counts().reset_index()
        trade_counts.columns = ['Strategy', 'Count']
        
        fig = px.pie(
            trade_counts,
            values='Count',
            names='Strategy',
            title="Trade Distribution by Strategy"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit Factor by Strategy
        pf_data = strategy_stats.reset_index()[['type', 'Profit_Factor']]
        pf_data = pf_data[pf_data['Profit_Factor'] != float('inf')]
        
        fig = px.bar(
            pf_data,
            x='type',
            y='Profit_Factor',
            title="Profit Factor by Strategy",
            labels={'type': 'Strategy', 'Profit_Factor': 'Profit Factor'},
            color='Profit_Factor',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig.add_hline(y=2.0, line_dash="dash", line_color="green",
                      annotation_text="Excellent: 2.0")
        fig.add_hline(y=1.5, line_dash="dash", line_color="orange",
                      annotation_text="Good: 1.5")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: STATUS ANALYSIS (CRITICAL)
with tab3:
    st.header("⚡ Critical Status Analysis: Closed vs Expired")
    
    st.markdown("""
    <div style='background-color: #ffebcc; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ff9900;'>
        <strong>⚠️ CRITICAL INSIGHT:</strong> This analysis shows whether closing trades early or holding to expiration produces better results.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Status metrics
    status_stats = filtered_df.groupby('status').agg({
        'pnl': ['sum', 'mean', 'median', 'count'],
        'winning_trade': 'mean',
        'daysInTrade': 'mean'
    }).round(2)
    
    status_stats.columns = ['Total_PnL', 'Avg_PnL', 'Median_PnL', 'Trades', 'Win_Rate', 'Avg_Days']
    status_stats['Win_Rate'] = (status_stats['Win_Rate'] * 100).round(1)
    
    # Display status comparison
    col1, col2, col3, col4 = st.columns(4)
    
    if 'closed' in status_stats.index:
        with col1:
            st.metric("Closed - Total P&L", f"${status_stats.loc['closed', 'Total_PnL']:,.0f}")
        with col2:
            st.metric("Closed - Avg P&L", f"${status_stats.loc['closed', 'Avg_PnL']:,.0f}")
        with col3:
            st.metric("Closed - Win Rate", f"{status_stats.loc['closed', 'Win_Rate']:.1f}%")
        with col4:
            st.metric("Closed - Trades", f"{int(status_stats.loc['closed', 'Trades'])}")
    
    if 'expired' in status_stats.index:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Expired - Total P&L", f"${status_stats.loc['expired', 'Total_PnL']:,.0f}")
        with col2:
            st.metric("Expired - Avg P&L", f"${status_stats.loc['expired', 'Avg_PnL']:,.0f}")
        with col3:
            st.metric("Expired - Win Rate", f"{status_stats.loc['expired', 'Win_Rate']:.1f}%")
        with col4:
            st.metric("Expired - Trades", f"{int(status_stats.loc['expired', 'Trades'])}")
    
    # Performance multiplier
    if 'closed' in status_stats.index and 'expired' in status_stats.index:
        multiplier = status_stats.loc['closed', 'Avg_PnL'] / status_stats.loc['expired', 'Avg_PnL'] if status_stats.loc['expired', 'Avg_PnL'] != 0 else 0
        st.markdown(f"""
        <div style='background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #28a745; margin-top: 1rem;'>
            <strong>📈 PERFORMANCE MULTIPLIER:</strong> Closing early produces <strong>{multiplier:.1f}x</strong> better average P&L than holding to expiration!
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Total P&L comparison
        fig = px.bar(
            status_stats.reset_index(),
            x='status',
            y='Total_PnL',
            title="Total P&L: Closed vs Expired",
            labels={'status': 'Status', 'Total_PnL': 'Total P&L ($)'},
            color='Total_PnL',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average P&L comparison
        fig = px.bar(
            status_stats.reset_index(),
            x='status',
            y='Avg_PnL',
            title="Average P&L: Closed vs Expired",
            labels={'status': 'Status', 'Avg_PnL': 'Avg P&L ($)'},
            color='Avg_PnL',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Status by Strategy breakdown
    st.subheader("Status Performance by Strategy")
    
    status_strategy = filtered_df.groupby(['type', 'status']).agg({
        'pnl': ['sum', 'mean', 'count'],
        'winning_trade': 'mean'
    }).round(2)
    
    status_strategy.columns = ['Total_PnL', 'Avg_PnL', 'Trades', 'Win_Rate']
    status_strategy['Win_Rate'] = (status_strategy['Win_Rate'] * 100).round(1)
    status_strategy = status_strategy.reset_index()
    
    # Pivot for heatmap
    pivot_total = status_strategy.pivot(index='type', columns='status', values='Total_PnL')
    pivot_avg = status_strategy.pivot(index='type', columns='status', values='Avg_PnL')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Total P&L by Strategy & Status**")
        st.dataframe(
            pivot_total.style.background_gradient(cmap='RdYlGn', axis=None)
                             .format('${:,.0f}'),
            use_container_width=True
        )
    
    with col2:
        st.write("**Average P&L by Strategy & Status**")
        st.dataframe(
            pivot_avg.style.background_gradient(cmap='RdYlGn', axis=None)
                           .format('${:,.0f}'),
            use_container_width=True
        )
    
    # Stacked bar chart
    fig = px.bar(
        status_strategy,
        x='type',
        y='Total_PnL',
        color='status',
        title="P&L by Strategy & Status (Stacked)",
        labels={'type': 'Strategy', 'Total_PnL': 'Total P&L ($)', 'status': 'Status'},
        barmode='group'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# TAB 4: BEST/WORST TRADES
with tab4:
    st.header("📊 Best & Worst Trades Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 10 Best Trades")
        best_trades = filtered_df.nlargest(10, 'pnl')[
            ['openDate', 'type', 'symbol', 'status', 'pnl', 'returnPct', 'daysInTrade']
        ].copy()
        best_trades['openDate'] = best_trades['openDate'].dt.strftime('%Y-%m-%d')
        best_trades['returnPct'] = (best_trades['returnPct'] * 100).round(2)
        
        st.dataframe(
            best_trades.style.background_gradient(subset=['pnl'], cmap='Greens')
                             .format({
                                 'pnl': '${:,.0f}',
                                 'returnPct': '{:.2f}%'
                             }),
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.subheader("❌ Top 10 Worst Trades")
        worst_trades = filtered_df.nsmallest(10, 'pnl')[
            ['openDate', 'type', 'symbol', 'status', 'pnl', 'returnPct', 'daysInTrade']
        ].copy()
        worst_trades['openDate'] = worst_trades['openDate'].dt.strftime('%Y-%m-%d')
        worst_trades['returnPct'] = (worst_trades['returnPct'] * 100).round(2)
        
        st.dataframe(
            worst_trades.style.background_gradient(subset=['pnl'], cmap='Reds_r')
                              .format({
                                  'pnl': '${:,.0f}',
                                  'returnPct': '{:.2f}%'
                              }),
            use_container_width=True,
            hide_index=True
        )
    
    # Key observations
    st.markdown("---")
    st.subheader("📌 Key Observations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        best_closed = (best_trades['status'] == 'closed').sum()
        st.metric("Best Trades Closed Early", f"{best_closed}/10", 
                 delta=f"{best_closed*10}% of top trades")
    
    with col2:
        worst_expired = (worst_trades['status'] == 'expired').sum()
        st.metric("Worst Trades Expired", f"{worst_expired}/10",
                 delta=f"{worst_expired*10}% of worst trades")
    
    with col3:
        best_avg = best_trades['pnl'].mean()
        worst_avg = worst_trades['pnl'].mean()
        st.metric("Avg Best Trade", f"${best_avg:,.0f}",
                 delta=f"Worst: ${worst_avg:,.0f}")
    
    # Symbol breakdown
    st.markdown("---")
    st.subheader("Performance by Symbol")
    
    symbol_stats = filtered_df.groupby('symbol').agg({
        'pnl': ['sum', 'mean', 'count'],
        'winning_trade': 'mean'
    }).round(2)
    
    symbol_stats.columns = ['Total_PnL', 'Avg_PnL', 'Trades', 'Win_Rate']
    symbol_stats['Win_Rate'] = (symbol_stats['Win_Rate'] * 100).round(1)
    symbol_stats = symbol_stats.sort_values('Total_PnL', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(
            symbol_stats.style.background_gradient(subset=['Total_PnL'], cmap='RdYlGn')
                              .format({
                                  'Total_PnL': '${:,.0f}',
                                  'Avg_PnL': '${:,.0f}',
                                  'Win_Rate': '{:.1f}%'
                              }),
            use_container_width=True
        )
    
    with col2:
        fig = px.bar(
            symbol_stats.reset_index(),
            x='symbol',
            y='Total_PnL',
            title="Total P&L by Symbol",
            color='Total_PnL',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# TAB 5: DELTA ANALYSIS
with tab5:
    st.header("🔢 Delta Exposure Analysis")
    
    st.info("""
    **Delta estimates:** These are approximations based on strategy type. 
    - Neutral strategies (Iron Condor, Iron Butterfly): 0 delta
    - Bullish strategies (Short Put Spreads, Long Calls): Positive delta
    - Bearish strategies (Short Call Spreads, Long Puts): Negative delta
    """)
    
    # Delta metrics
    total_delta = filtered_df['estimated_delta'].sum()
    avg_delta = filtered_df['estimated_delta'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Delta Exposure", f"{total_delta:,.0f}")
    
    with col2:
        st.metric("Avg Delta per Trade", f"{avg_delta:.1f}")
    
    with col3:
        bias = "Bullish" if total_delta > 50 else "Bearish" if total_delta < -50 else "Neutral"
        st.metric("Portfolio Bias", bias)
    
    with col4:
        neutral_pct = (filtered_df['delta_category'] == 'Neutral').sum() / len(filtered_df) * 100
        st.metric("Neutral Trades", f"{neutral_pct:.1f}%")
    
    # Delta by strategy
    st.subheader("Delta Exposure by Strategy")
    
    delta_strategy = filtered_df.groupby('type').agg({
        'estimated_delta': ['mean', 'sum'],
        'pnl': 'sum',
        'type': 'count'
    }).round(2)
    
    delta_strategy.columns = ['Avg_Delta', 'Total_Delta', 'Total_PnL', 'Trades']
    delta_strategy = delta_strategy.sort_values('Total_PnL', ascending=False)
    
    st.dataframe(
        delta_strategy.style.background_gradient(subset=['Total_PnL'], cmap='RdYlGn')
                            .format({
                                'Total_PnL': '${:,.0f}',
                                'Avg_Delta': '{:.1f}',
                                'Total_Delta': '{:.0f}'
                            }),
        use_container_width=True
    )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Delta distribution
        fig = px.histogram(
            filtered_df,
            x='estimated_delta',
            nbins=20,
            title="Delta Distribution",
            labels={'estimated_delta': 'Estimated Delta'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Delta vs P&L scatter
        fig = px.scatter(
            filtered_df,
            x='estimated_delta',
            y='pnl',
            color='type',
            title="Delta vs P&L",
            labels={'estimated_delta': 'Estimated Delta', 'pnl': 'P&L ($)'},
            hover_data=['symbol', 'status']
        )
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
        fig.add_vline(x=0, line_dash="dash", line_color="blue", opacity=0.5)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance by delta category
    st.subheader("Performance by Delta Direction")
    
    delta_perf = filtered_df.groupby('delta_category').agg({
        'pnl': ['sum', 'mean', 'count'],
        'winning_trade': 'mean'
    }).round(2)
    
    delta_perf.columns = ['Total_PnL', 'Avg_PnL', 'Trades', 'Win_Rate']
    delta_perf['Win_Rate'] = (delta_perf['Win_Rate'] * 100).round(1)
    
    st.dataframe(
        delta_perf.style.background_gradient(subset=['Total_PnL'], cmap='RdYlGn')
                        .format({
                            'Total_PnL': '${:,.0f}',
                            'Avg_PnL': '${:,.0f}',
                            'Win_Rate': '{:.1f}%'
                        }),
        use_container_width=True
    )

# TAB 6: TRADE LOG
with tab6:
    st.header("📋 Complete Trade Log")
    
    # Add search
    search_term = st.text_input("🔍 Search trades (symbol, description, etc.)")
    
    # Prepare display dataframe
    display_df = filtered_df[[
        'openDate', 'closeDate', 'type', 'symbol', 'status', 
        'quantity', 'pnl', 'returnPct', 'daysInTrade', 
        'estimated_delta', 'delta_category'
    ]].copy()
    
    display_df['openDate'] = display_df['openDate'].dt.strftime('%Y-%m-%d')
    display_df['closeDate'] = display_df['closeDate'].dt.strftime('%Y-%m-%d')
    display_df['returnPct'] = (display_df['returnPct'] * 100).round(2)
    
    # Apply search
    if search_term:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
        display_df = display_df[mask]
    
    # Sort options
    sort_col = st.selectbox("Sort by", display_df.columns.tolist(), index=display_df.columns.get_loc('openDate'))
    sort_order = st.radio("Order", ["Descending", "Ascending"], horizontal=True)
    
    display_df = display_df.sort_values(sort_col, ascending=(sort_order == "Ascending"))
    
    # Display
    st.dataframe(
        display_df.style.applymap(
            lambda x: 'background-color: #d4edda' if isinstance(x, (int, float)) and x > 0 else 
                     ('background-color: #f8d7da' if isinstance(x, (int, float)) and x < 0 else ''),
            subset=['pnl']
        ).format({
            'pnl': '${:,.0f}',
            'returnPct': '{:.2f}%'
        }),
        use_container_width=True,
        height=600
    )
    
    # Export button
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=display_df.to_csv(index=False),
        file_name=f"trading_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <strong>Options Trading Performance Dashboard</strong> | 
    Data-driven insights for optimal performance | 
    Generated: {0}
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)
