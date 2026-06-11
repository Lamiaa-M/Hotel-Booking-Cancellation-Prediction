"""pages/1_Analysis.py — the analysis page: the same Q1–Q8 charts as the notebook."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Analysis", page_icon="📊", layout="wide")

TEAL, SEAFOAM, MINT, DARK, MUTED = "#028090", "#00A896", "#02C39A", "#07343F", "#64748B"
st.markdown(f"""
<style>
    .block-container {{ padding-top: 2rem; max-width: 80rem; }}
    #MainMenu, footer {{ visibility: hidden; }}
    .phero {{ background: linear-gradient(120deg, {DARK} 0%, {TEAL} 100%);
              border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.4rem; color:#fff; }}
    .phero h1 {{ font-size: 1.8rem; font-weight: 800; margin: 0; }}
    .phero p {{ opacity:.9; margin:.3rem 0 0 0; }}
</style>
<div class="phero"><h1>📊 Cancellation Analysis</h1>
<p>Eight business questions about what drives hotel-booking cancellations.</p></div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("hotel_booking_clean.csv")
try:
    df = load_data()
except Exception:
    st.error("`hotel_booking_clean.csv` not found. Run the notebook to generate it.")
    st.stop()

def cancel_rate(col):
    return (df.groupby(col)["is_canceled"].mean()
              .reset_index().rename(columns={"is_canceled": "cancel_rate"})
              .sort_values("cancel_rate", ascending=False))

def style(fig, pct_axis=None):
    fig.update_layout(plot_bgcolor="white", height=340, margin=dict(t=50, b=10, l=10, r=10))
    if pct_axis == "y": fig.update_layout(yaxis_tickformat=".0%")
    if pct_axis == "x": fig.update_layout(xaxis_tickformat=".0%")
    return fig

# Q1 + Q2
a, b = st.columns(2)
with a:
    st.markdown("**Q1 — What share of bookings get canceled?**")
    bal = df["is_canceled"].map({0: "Honored", 1: "Canceled"}).value_counts().reset_index()
    bal.columns = ["status", "count"]
    fig = px.pie(bal, names="status", values="count", hole=0.45,
                 color_discrete_sequence=[TEAL, MINT])
    fig.update_traces(textinfo="label+percent")
    st.plotly_chart(style(fig), use_container_width=True)
with b:
    st.markdown("**Q2 — How far in advance do guests book?**")
    fig = px.histogram(df, x="lead_time", nbins=50, color_discrete_sequence=[TEAL])
    fig.update_layout(xaxis_title="lead time (days)", yaxis_title="bookings")
    st.plotly_chart(style(fig), use_container_width=True)

# Q3 + Q4
a, b = st.columns(2)
with a:
    st.markdown("**Q3 — Do bookings made far in advance cancel more?**")
    tmp = df.copy(); tmp["status"] = tmp["is_canceled"].map({0: "Honored", 1: "Canceled"})
    fig = px.box(tmp, x="status", y="lead_time", color="status",
                 color_discrete_sequence=[TEAL, MINT])
    fig.update_layout(showlegend=False, xaxis_title="")
    st.plotly_chart(style(fig), use_container_width=True)
with b:
    st.markdown("**Q4 — Which hotel type cancels more?**")
    d = cancel_rate("hotel")
    fig = px.bar(d, x="hotel", y="cancel_rate", color="hotel", text_auto=".0%",
                 color_discrete_sequence=[TEAL, SEAFOAM])
    fig.update_layout(showlegend=False, xaxis_title="")
    st.plotly_chart(style(fig, "y"), use_container_width=True)

# Q5 + Q6
a, b = st.columns(2)
with a:
    st.markdown("**Q5 — How does deposit type affect cancellation?**")
    d = cancel_rate("deposit_type")
    fig = px.bar(d, x="deposit_type", y="cancel_rate", text_auto=".0%",
                 color_discrete_sequence=[TEAL])
    fig.update_layout(xaxis_title="")
    st.plotly_chart(style(fig, "y"), use_container_width=True)
with b:
    st.markdown("**Q6 — Which market segments cancel the most?**")
    d = cancel_rate("market_segment")
    fig = px.bar(d, x="cancel_rate", y="market_segment", orientation="h", text_auto=".0%",
                 color_discrete_sequence=[SEAFOAM])
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, yaxis_title="")
    st.plotly_chart(style(fig, "x"), use_container_width=True)

# Q7 + Q8
a, b = st.columns(2)
with a:
    st.markdown("**Q7 — Do more special requests reduce cancellation?**")
    d = cancel_rate("total_of_special_requests").sort_values("total_of_special_requests")
    fig = px.bar(d, x="total_of_special_requests", y="cancel_rate", text_auto=".0%",
                 color_discrete_sequence=[TEAL])
    fig.update_layout(xaxis_title="special requests")
    st.plotly_chart(style(fig, "y"), use_container_width=True)
with b:
    st.markdown("**Q8 — Does cancellation vary by arrival month?**")
    order = ["January","February","March","April","May","June",
             "July","August","September","October","November","December"]
    d = df.groupby("arrival_date_month")["is_canceled"].mean().reindex(order).reset_index()
    d.columns = ["month", "cancel_rate"]
    fig = px.line(d, x="month", y="cancel_rate", markers=True, color_discrete_sequence=[TEAL])
    fig.update_layout(xaxis_title="")
    st.plotly_chart(style(fig, "y"), use_container_width=True)

# Correlation heatmap
st.markdown("**Correlation between numeric features**")
num_df = df.select_dtypes(include=[np.number])
fig = px.imshow(num_df.corr(), color_continuous_scale="Teal", zmin=-1, zmax=1, aspect="auto")
fig.update_layout(height=600, margin=dict(t=20, b=10))
st.plotly_chart(fig, use_container_width=True)
