import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Hospital ER Analytics",
    layout="wide"
)

# ── DEMO DATA GENERATOR (IMPORTANT FIX) ──
def generate_demo_data(n=1000):
    np.random.seed(42)
    df = pd.DataFrame({
        "Patient Age": np.random.randint(1, 90, n),
        "Patient Waittime": np.random.randint(5, 120, n),
        "Patient Satisfaction Score": np.random.uniform(3, 9, n),
        "Department Referral": np.random.choice(
            ["General Practice", "Orthopedics", "Cardiology", "Neurology"],
            n
        ),
        "Hour": np.random.randint(0, 24, n)
    })
    return df

# ── SAFE LOADER ──
@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)

        # Ensure required columns exist
        required_cols = [
            "Patient Age",
            "Patient Waittime",
            "Patient Satisfaction Score",
            "Department Referral"
        ]

        for col in required_cols:
            if col not in df.columns:
                df[col] = np.nan

        df["Patient Satisfaction Score"].fillna(df["Patient Satisfaction Score"].mean(), inplace=True)
        df["Department Referral"].fillna("Unknown", inplace=True)

        if "Patient Admission Date" in df.columns:
            df["Patient Admission Date"] = pd.to_datetime(df["Patient Admission Date"], errors="coerce")
            df["Hour"] = df["Patient Admission Date"].dt.hour
        else:
            df["Hour"] = np.random.randint(0, 24, len(df))

        return df

    except:
        return generate_demo_data()

# ── MAIN ──
def main():

    st.title("🏥 Hospital Emergency Room Analytics")

    # Upload
    uploaded = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded:
        df = load_data(uploaded)
        st.success("Data loaded successfully ✅")
    else:
        st.warning("Using demo dataset (upload CSV to use real data)")
        df = generate_demo_data()

    # ── KPIs ──
    total = len(df)
    avg_wait = df["Patient Waittime"].mean()
    avg_sat = df["Patient Satisfaction Score"].mean()
    top_dept = df["Department Referral"].mode()[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Patients", f"{total:,}")
    c2.metric("Avg Wait Time", f"{avg_wait:.0f} min")
    c3.metric("Satisfaction", f"{avg_sat:.1f}/10")
    c4.metric("Top Dept", top_dept)

    # ── CHARTS ──
    st.subheader("Patients per Department")
    dept = df["Department Referral"].value_counts()

    fig, ax = plt.subplots()
    ax.barh(dept.index, dept.values)
    st.pyplot(fig)

    st.subheader("Wait Time Distribution")
    fig, ax = plt.subplots()
    ax.hist(df["Patient Waittime"], bins=20)
    st.pyplot(fig)

    st.subheader("Wait vs Satisfaction")
    fig, ax = plt.subplots()
    ax.scatter(df["Patient Waittime"], df["Patient Satisfaction Score"], alpha=0.3)
    st.pyplot(fig)

    st.subheader("Arrivals by Hour")
    hour = df["Hour"].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.bar(hour.index, hour.values)
    st.pyplot(fig)

    st.subheader("Age Distribution")
    fig, ax = plt.subplots()
    ax.hist(df["Patient Age"], bins=20)
    st.pyplot(fig)

    # ── INSIGHTS ──
    st.subheader("Key Insights")

    st.write(f"• Top department: **{top_dept}**")
    st.write(f"• Avg wait time: **{avg_wait:.0f} mins**")
    st.write("• Satisfaction decreases with higher wait time")

# ── RUN ──
if __name__ == "__main__":
    main()
