import streamlit as st

# ---------------------------------------------
# PAGE CONFIG
# ---------------------------------------------
st.set_page_config(
    page_title="Unit Converter",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 Simple Unit Converter (All-in-One Page) - Day 5 Challenge")
st.write("Real-time conversions for currency, temperature, length, and weight.")


# ---------------------------------------------
# Conversion Logic
# ---------------------------------------------
def convert_currency(amount, mode):
    INR_USD = 0.012
    INR_AED = 0.044
    USD_AED = 3.67

    if mode == "INR → USD": return amount * INR_USD
    if mode == "USD → INR": return amount / INR_USD
    if mode == "INR → AED": return amount * INR_AED
    if mode == "AED → INR": return amount / INR_AED
    if mode == "USD → AED": return amount * USD_AED
    if mode == "AED → USD": return amount / USD_AED
    return 0

def convert_temperature(v, mode):
    return (v * 9/5) + 32 if mode == "°C → °F" else (v - 32) * 5/9

def convert_length(v, mode):
    return v / 2.54 if mode == "cm → inch" else v * 2.54

def convert_weight(v, mode):
    return v * 2.20462 if mode == "kg → lb" else v * 0.453592

# ---------------------------------------------
# LAYOUT (4 Panels)
# ---------------------------------------------
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# ---------------------------------------------
# PANEL 1 — CURRENCY
# ---------------------------------------------
with col1:
    st.subheader("💰 Currency Converter (INR / USD / AED)")
    amount = st.number_input("Amount", key="cur_amt", step=0.1)

    mode = st.selectbox("Direction", [
        "INR → USD", "USD → INR",
        "INR → AED", "AED → INR",
        "USD → AED", "AED → USD"
    ], key="cur_mode")

    result = convert_currency(amount, mode)
    st.write("### Result:", f"**{result:,.2f}**")

# ---------------------------------------------
# PANEL 2 — TEMPERATURE
# ---------------------------------------------
with col2:
    st.subheader("🌡 Temperature Converter (°C ↔ °F)")
    t_val = st.number_input("Temperature", key="temp_val", step=0.1)
    t_mode = st.selectbox("Direction", ["°C → °F", "°F → °C"], key="temp_mode")

    res = convert_temperature(t_val, t_mode)
    st.write("### Result:", f"**{res:,.2f}**")

# ---------------------------------------------
# PANEL 3 — LENGTH
# ---------------------------------------------
with col3:
    st.subheader("📏 Length Converter (cm ↔ inch)")
    l_val = st.number_input("Length", key="len_val", step=0.1)
    l_mode = st.selectbox("Direction", ["cm → inch", "inch → cm"], key="len_mode")

    res = convert_length(l_val, l_mode)
    st.write("### Result:", f"**{res:,.2f}**")

# ---------------------------------------------
# PANEL 4 — WEIGHT
# ---------------------------------------------
with col4:
    st.subheader("⚖ Weight Converter (kg ↔ lb)")
    w_val = st.number_input("Weight", key="wt_val", step=0.1)
    w_mode = st.selectbox("Direction", ["kg → lb", "lb → kg"], key="wt_mode")

    res = convert_weight(w_val, w_mode)
    st.write("### Result:", f"**{res:,.2f}**")