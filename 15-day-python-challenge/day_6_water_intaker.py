import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Water Intake Tracker", page_icon="💧", layout="centered")
st.title("💧 Water Intake Tracker – Day 6 Challenge")
st.write("Track your daily hydration and view your weekly progress!")

DAILY_GOAL = 3000  # 3 Liters = 3000 ml

# -----------------------------
# Initialize Storage
# -----------------------------
if "water_log" not in st.session_state:
    st.session_state.water_log = []   # store {"date":..., "amount":...}

# -----------------------------
# Input: Add water intake
# -----------------------------
st.subheader("📥 Log Water Intake")

amount = st.number_input("Enter amount (ml):", step=100, min_value=0)

# NEW — optional date input
input_date = st.date_input("Choose date (optional)", value=None)

# If no date chosen → use today's date
selected_date = input_date if input_date is not None else datetime.now().date()

if st.button("Add Entry"):
    st.session_state.water_log.append({
        "date": selected_date,
        "amount": amount
    })
    st.success(f"Added {amount} ml on {selected_date}")

# -----------------------------
# Daily Progress
# -----------------------------
st.subheader("📊 Today's Progress")

today = datetime.now().date()
today_total = sum(entry["amount"] for entry in st.session_state.water_log if entry["date"] == today)

progress = min(today_total / DAILY_GOAL, 1.0)

st.write(f"**Total Today:** {today_total} ml / {DAILY_GOAL} ml")
st.progress(progress)

# -----------------------------
# Weekly Chart
# -----------------------------
st.subheader("📅 Weekly Hydration Chart")

# Prepare Data
last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

chart_data = {
    "Date": [],
    "Water (ml)": []
}

for d in last_7_days:
    total = sum(e["amount"] for e in st.session_state.water_log if e["date"] == d)
    chart_data["Date"].append(d.strftime("%b %d"))
    chart_data["Water (ml)"].append(total)

df = pd.DataFrame(chart_data)

# Bar chart
st.bar_chart(df.set_index("Date"))