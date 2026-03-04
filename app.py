import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Smart Agriculture Dashboard", layout="wide")

# Load data
data = pd.read_csv("Final_Output.csv")

st.title("🌾 Smart Agriculture Dashboard")
st.markdown("Real-time Monitoring of Field Conditions & Irrigation Decisions")

# -------------------------------
# 🔍 Search Field ID
# -------------------------------
col1, col2 = st.columns([2,1])

with col1:
    field_id = st.number_input("🔍 Enter Field ID", min_value=0, max_value=len(data)-1, step=1)

with col2:
    st.write("")
    st.write("")
    if st.button("Search Field"):
        st.success(f"Showing data for Field {field_id}")

# Get selected field
field = data.iloc[int(field_id)]

st.markdown("---")

# -------------------------------
# 🌱 Crop Info
# -------------------------------
st.subheader("🌱 Crop Information")
st.info(f"Crop: **{field['label']}**")

# -------------------------------
# 📊 Sensor Data (Cards)
# -------------------------------
st.subheader("📊 Sensor Readings")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Nitrogen (N)", field['N'])
c2.metric("Phosphorus (P)", field['P'])
c3.metric("Potassium (K)", field['K'])
c4.metric("pH", field['ph'])

c5, c6, c7 = st.columns(3)

c5.metric("Temperature 🌡", field['temperature'])
c6.metric("Humidity 💧", field['humidity'])
c7.metric("Rainfall 🌧", field['rainfall'])

# -------------------------------
# 💧 Decision Section
# -------------------------------
st.subheader("💧 Irrigation Decision")

if field['Decision'] == "Irrigation needed":
    st.error("🚨 Irrigation Needed")
else:
    st.success("✅ Normal Condition")

# =========================================================
# 🌾 Crop Name Search Section (NEW)
# =========================================================

st.markdown("---")
st.subheader("🔍 Search by Crop Name")

col3, col4 = st.columns([2,1])

with col3:
    crop_name = st.selectbox("Select Crop", data['label'].unique())

with col4:
    st.write("")
    st.write("")
    if st.button("Search Crop"):
        st.success(f"Showing data for crop: {crop_name}")

# Filter dataset
crop_data = data[data['label'] == crop_name]

st.markdown("---")

# -------------------------------
# 📊 Crop Summary
# -------------------------------
st.subheader(f"🌾 Crop Analysis: {crop_name}")

total = len(crop_data)
normal = len(crop_data[crop_data['Decision'] == "Normal"])
irrigation = len(crop_data[crop_data['Decision'] == "Irrigation needed"])

c1, c2, c3 = st.columns(3)
c1.metric("Total Fields", total)
c2.metric("Normal", normal)
c3.metric("Irrigation Needed", irrigation)

# -------------------------------
# 📊 Bar Graph (Decision)
# -------------------------------
st.subheader("📊 Irrigation Decision Distribution")

decision_counts = crop_data['Decision'].value_counts()
st.bar_chart(decision_counts)

# -------------------------------
# 📋 View Dataset (Filtered)
# -------------------------------
with st.expander("📋 View Crop Dataset"):
    st.dataframe(crop_data)