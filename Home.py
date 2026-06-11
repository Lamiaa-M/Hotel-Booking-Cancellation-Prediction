"""
Home.py — landing page. Run the dashboard with:  streamlit run Home.py
Two pages live in the sidebar:  📊 Analysis  and  🔮 ML Model.
"""
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hotel Cancellation Dashboard", page_icon="🏨", layout="wide")

TEAL, SEAFOAM, MINT, DARK, INK, MUTED = "#028090", "#00A896", "#02C39A", "#07343F", "#1E293B", "#64748B"
st.markdown(f"""
<style>
    .block-container {{ padding-top: 2rem; max-width: 78rem; }}
    #MainMenu, footer {{ visibility: hidden; }}
    .hero {{ background: linear-gradient(120deg, {DARK} 0%, {TEAL} 100%);
             border-radius: 18px; padding: 2.4rem 2.6rem; margin-bottom: 1.6rem; color:#fff; }}
    .hero h1 {{ font-size: 2.4rem; font-weight: 800; margin: 0 0 .5rem 0; }}
    .hero p {{ font-size: 1.05rem; opacity:.92; margin:0; max-width:60rem; }}
    .tag {{ display:inline-block; background:rgba(255,255,255,.15); color:#CFE6EA;
            padding:.25rem .7rem; border-radius:20px; font-size:.8rem; font-weight:600;
            letter-spacing:.06em; margin-bottom:.9rem; }}
    .card {{ background:#fff; border:1px solid #E2E8F0; border-radius:16px; padding:1.5rem 1.7rem;
             box-shadow:0 4px 14px rgba(7,52,63,.06); height:100%; }}
    .card h2 {{ color:{TEAL}; font-size:1.3rem; font-weight:700; margin:0 0 .6rem 0; }}
    .card p, .card li {{ color:{MUTED}; font-size:.97rem; line-height:1.6; }}
    .stat {{ background:{DARK}; border-radius:14px; padding:1.1rem 1rem; text-align:center; color:#fff; }}
    .stat .num {{ font-size:2.0rem; font-weight:800; color:{MINT}; line-height:1; }}
    .stat .lbl {{ font-size:.8rem; color:#CFE6EA; margin-top:.3rem; }}
</style>
<div class="hero">
  <div class="tag">FINAL DATA SCIENCE PROJECT</div>
  <h1>🏨 Hotel Booking Cancellation Dashboard</h1>
  <p>Predicting whether a hotel reservation will be canceled — with an interactive analysis page and a live prediction model.</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("hotel_booking_clean.csv")
try:
    df = load_data(); ok = True
except Exception:
    df, ok = None, False

if ok:
    rate = df["is_canceled"].mean() if "is_canceled" in df else 0
    cols = st.columns(4)
    stats = [(f"{len(df):,}", "bookings"), (f"{df.shape[1]}", "features"),
             (f"{rate*100:.0f}%", "cancellation rate"),
             (f"{df['hotel'].nunique() if 'hotel' in df else 2}", "hotel types")]
    for c,(n,l) in zip(cols, stats):
        c.markdown(f'<div class="stat"><div class="num">{n}</div><div class="lbl">{l}</div></div>',
                   unsafe_allow_html=True)
else:
    st.info("Run the notebook first to generate **hotel_booking_clean.csv** and the model files.")

st.write("")
c1, c2 = st.columns(2)
c1.markdown(f"""
<div class="card">
  <h2>📊 Analysis page</h2>
  <p>Eight business questions about what drives cancellations, each answered with an interactive chart:
  lead time, deposit type, market segment, special requests, seasonality and more.</p>
  <p><strong>Open it from the sidebar →</strong></p>
</div>""", unsafe_allow_html=True)
c2.markdown(f"""
<div class="card">
  <h2>🔮 ML Model page</h2>
  <p>Enter a booking's details and the tuned Random Forest estimates its cancellation probability,
  shown on a live gauge with a clear honored/canceled verdict.</p>
  <p><strong>Open it from the sidebar →</strong></p>
</div>""", unsafe_allow_html=True)

st.write("")
st.caption("Built for the Epsilon AI Data Science final project · references the main Epsilon AI repository.")
