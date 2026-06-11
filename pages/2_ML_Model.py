"""pages/2_ML_Model.py — the ML model page: scores a single booking."""
import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from category_encoders import BinaryEncoder  # needed to unpickle the preprocessor

st.set_page_config(page_title="ML Model", page_icon="", layout="wide")

TEAL, MINT, DARK = "#028090", "#02C39A", "#07343F"
st.markdown(f"""
<style>
    .block-container {{ padding-top: 2rem; max-width: 80rem; }}
    #MainMenu, footer {{ visibility: hidden; }}
    .phero {{ background: linear-gradient(120deg, {DARK} 0%, {TEAL} 100%);
              border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.4rem; color:#fff; }}
    .phero h1 {{ font-size: 1.8rem; font-weight: 800; margin: 0; }}
    .phero p {{ opacity:.9; margin:.3rem 0 0 0; }}
</style>
<div class="phero"><h1> Cancellation Prediction Model</h1>
<p>Enter the booking details; the tuned Random Forest estimates the cancellation probability.</p></div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_artifacts():
    # model.pkl is the FULL pipeline (preprocessing + feature selection + model)
    return (joblib.load("hotel_cancellation_model.pkl"),
            joblib.load("feature_columns.pkl"))
try:
    model, feature_columns = load_artifacts()
except Exception:
    st.error("Model files not found. Run the notebook to generate "
             "`hotel_cancellation_model.pkl` and `feature_columns.pkl`.")
    st.stop()

st.subheader("Booking details")
c1, c2, c3 = st.columns(3)
with c1:
    hotel = st.selectbox("Hotel type", ["City Hotel", "Resort Hotel"])
    lead_time = st.number_input("Lead time (days)", 0, 800, 100)
    adults = st.number_input("Adults", 1, 6, 2)
    children = st.number_input("Children", 0, 5, 0)
    babies = st.number_input("Babies", 0, 5, 0)
with c2:
    stays_week = st.number_input("Week nights", 0, 30, 2)
    stays_weekend = st.number_input("Weekend nights", 0, 15, 1)
    special_requests = st.number_input("Special requests", 0, 5, 0)
    booking_changes = st.number_input("Booking changes", 0, 20, 0)
    previous_cancellations = st.number_input("Previous cancellations", 0, 30, 0)
with c3:
    deposit_type = st.selectbox("Deposit type", ["No Deposit", "Non Refund", "Refundable"])
    customer_type = st.selectbox("Customer type", ["Transient", "Transient-Party", "Contract", "Group"])
    market_segment = st.selectbox("Market segment",
                                  ["Online TA", "Offline TA/TO", "Direct", "Groups", "Corporate", "Aviation"])
    distribution_channel = st.selectbox("Distribution channel", ["TA/TO", "Direct", "Corporate", "GDS"])
    is_repeated_guest = st.selectbox("Repeated guest?", [0, 1])

row = {
    "hotel": hotel, "lead_time": lead_time, "arrival_date_year": 2017,
    "arrival_date_month": "August", "arrival_date_week_number": 27, "arrival_date_day_of_month": 15,
    "stays_in_weekend_nights": stays_weekend, "stays_in_week_nights": stays_week,
    "adults": adults, "children": children, "babies": babies, "meal": "BB", "country": "PRT",
    "market_segment": market_segment, "distribution_channel": distribution_channel,
    "is_repeated_guest": is_repeated_guest, "previous_cancellations": previous_cancellations,
    "previous_bookings_not_canceled": 0, "reserved_room_type": "A", "assigned_room_type": "A",
    "booking_changes": booking_changes, "deposit_type": deposit_type, "agent": 9,
    "days_in_waiting_list": 0, "customer_type": customer_type, "adr": 100.0,
    "required_car_parking_spaces": 0, "total_of_special_requests": special_requests,
    "total_nights": stays_week + stays_weekend, "total_guests": adults + children + babies,
    "is_family": int(adults > 0 and (children > 0 or babies > 0)), "room_changed": 0,
}
input_df = pd.DataFrame([row]).reindex(columns=feature_columns, fill_value=0)

st.write("")
if st.button("Predict cancellation risk", type="primary", use_container_width=True):
    prob = float(model.predict_proba(input_df)[0][1])
    r1, r2 = st.columns([1, 1])
    with r1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=prob * 100, number={"suffix": "%", "font": {"size": 46}},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": TEAL},
                   "steps": [{"range": [0, 50], "color": "#E6F4F1"},
                             {"range": [50, 100], "color": "#D6ECEA"}],
                   "threshold": {"line": {"color": DARK, "width": 3}, "value": 50}}))
        fig.update_layout(height=300, margin=dict(t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with r2:
        st.write(""); st.write("")
        if prob >= 0.5:
            st.error("### ⚠️ Likely to be CANCELED")
            st.write("Consider a deposit requirement or an overbooking buffer for this reservation.")
        else:
            st.success("### ✅ Likely to be HONORED")
            st.write("This booking shows a low cancellation risk.")
        st.caption("Decision threshold = 50%.")
