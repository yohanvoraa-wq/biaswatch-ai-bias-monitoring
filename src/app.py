import streamlit as st
import pandas as pd

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Loan Bias Drift Monitor",
    layout="centered"
)

st.title("📊 Loan Approval Bias Drift Monitoring")
st.markdown("Monitoring fairness degradation due to population shift")

# -----------------------------
# Helper functions
# -----------------------------
@st.cache_data
def load_data(path_or_file):
    df = pd.read_csv(path_or_file)
    df.columns = df.columns.str.strip().str.lower()
    df["govt_employed"] = df["govt_employed"].astype(str).str.strip().str.lower()
    df["loan_status"] = df["loan_status"].astype(str).str.strip()
    return df

def compute_metrics(df):
    results = {}
    for group in ["yes", "no"]:
        gdf = df[df["govt_employed"] == group]
        total = len(gdf)
        approved = (gdf["loan_status"] == "Approved").sum()
        rate = approved / total if total > 0 else 0
        results[group] = round(rate, 3)
    return results

# -----------------------------
# File uploader
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload decision log CSV",
    type=["csv"]
)

# -----------------------------
# Data source selection
# -----------------------------
if uploaded_file is not None:
    df = load_data(uploaded_file)
    source = "Uploaded dataset"
    st.success("✅ Uploaded file processed")
else:
    df = load_data("after_shift_biased.csv")
    source = "Example dataset (simulated post-deployment)"

st.caption(f"📂 Data source: **{source}**")

# -----------------------------
# Compute metrics
# -----------------------------
metrics = compute_metrics(df)

# -----------------------------
# Display metrics
# -----------------------------
st.header("📌 Approval Rates")

col1, col2 = st.columns(2)

with col1:
    st.metric("Govt Employed", metrics["yes"])

with col2:
    st.metric("Non-Govt Employed", metrics["no"])

# -----------------------------
# Bias drift detection
# -----------------------------
st.header("🚨 Bias Drift Detection")

diff = abs(metrics["yes"] - metrics["no"])
threshold = 0.15

st.write(f"Approval rate difference: **{round(diff,3)}**")
st.write(f"Alert threshold: **{threshold}**")

if diff > threshold:
    st.error("🚨 BIAS DRIFT DETECTED")
else:
    st.success("✅ No significant bias drift detected")

# -----------------------------
# Explanation
# -----------------------------
st.markdown("---")
st.subheader("ℹ️ Explanation")

st.markdown("""
- The system compares **group-wise approval rates**  
- A significant divergence after population shift indicates **bias drift**  
- Thresholds are **policy-defined and configurable**  
""")
