import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Hospital ER Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL STYLES ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* App background */
.stApp {
    background-color: #0f1117;
    color: #e8eaf0;
}

/* Top header bar */
.top-bar {
    background: linear-gradient(135deg, #1a1d2e 0%, #12151f 100%);
    border-bottom: 1px solid #2a2d3e;
    padding: 28px 40px 22px;
    margin: -1rem -1rem 2rem -1rem;
}

.top-bar h1 {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.65rem;
    font-weight: 600;
    color: #e8eaf0;
    letter-spacing: -0.02em;
    margin: 0 0 4px 0;
}

.top-bar p {
    font-size: 0.82rem;
    color: #6b7280;
    margin: 0;
    font-weight: 400;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 2rem;
}

.kpi-card {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 10px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent, #4f7fe8);
}

.kpi-card:hover { border-color: #3a3d5e; }

.kpi-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 600;
    color: #e8eaf0;
    letter-spacing: -0.03em;
    line-height: 1;
    font-family: 'DM Mono', monospace;
}

.kpi-sub {
    font-size: 0.75rem;
    color: #4b5563;
    margin-top: 6px;
}

/* Section headers */
.section-header {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b7280;
    margin: 2rem 0 1rem 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2130;
}

/* Upload area override */
.stFileUploader {
    background: #1a1d2e !important;
    border: 1px dashed #2a2d3e !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

/* Status banner */
.status-banner {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 8px;
    padding: 12px 18px;
    font-size: 0.82rem;
    color: #9ca3af;
    margin-bottom: 1.5rem;
}

.status-banner.live { border-left: 3px solid #34d399; }
.status-banner.demo { border-left: 3px solid #f59e0b; }

/* Insight cards */
.insight-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 0.5rem;
}

.insight-card {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 8px;
    padding: 16px 20px;
}

.insight-card .insight-label {
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 6px;
}

.insight-card .insight-val {
    font-size: 1.05rem;
    font-weight: 500;
    color: #e8eaf0;
}

/* Matplotlib chart container */
.chart-wrap {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 10px;
    padding: 4px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# ── MATPLOTLIB THEME ──
DARK_BG   = "#1a1d2e"
LIGHT_TEXT = "#c9cdd8"
GRID_COLOR = "#252840"
ACCENT    = "#4f7fe8"
ACCENT2   = "#34d399"
ACCENT3   = "#f59e0b"
ACCENT4   = "#f472b6"

PALETTE = [ACCENT, ACCENT2, ACCENT3, ACCENT4, "#a78bfa", "#fb923c"]

def apply_chart_style(fig, ax):
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.tick_params(colors=LIGHT_TEXT, labelsize=9)
    ax.xaxis.label.set_color(LIGHT_TEXT)
    ax.yaxis.label.set_color(LIGHT_TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.6, linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)
    ax.xaxis.grid(False)

# ── DEMO DATA ──
def generate_demo_data(n=1000):
    np.random.seed(42)
    return pd.DataFrame({
        "Patient Age":                np.random.randint(1, 90, n),
        "Patient Waittime":           np.random.randint(5, 120, n),
        "Patient Satisfaction Score": np.random.uniform(3, 9, n),
        "Department Referral":        np.random.choice(
            ["General Practice", "Orthopedics", "Cardiology", "Neurology", "Radiology"], n
        ),
        "Hour": np.random.randint(0, 24, n),
    })

# ── LOADER ──
@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
        for col in ["Patient Age", "Patient Waittime", "Patient Satisfaction Score", "Department Referral"]:
            if col not in df.columns:
                df[col] = np.nan
        df["Patient Satisfaction Score"] = df["Patient Satisfaction Score"].fillna(
            df["Patient Satisfaction Score"].mean()
        )
        df["Department Referral"] = df["Department Referral"].fillna("Unknown")
        if "Patient Admission Date" in df.columns:
            df["Patient Admission Date"] = pd.to_datetime(df["Patient Admission Date"], errors="coerce")
            df["Hour"] = df["Patient Admission Date"].dt.hour
        else:
            df["Hour"] = np.random.randint(0, 24, len(df))
        return df, True
    except Exception:
        return generate_demo_data(), False

# ── MAIN ──
def main():

    # Header
    st.markdown("""
    <div class="top-bar">
        <h1>Emergency Room Analytics</h1>
        <p>Patient Flow &amp; Performance Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    # Upload
    uploaded = st.file_uploader("Upload patient data CSV", type=["csv"], label_visibility="collapsed")

    if uploaded:
        df, success = load_data(uploaded)
        st.markdown('<div class="status-banner live">Live data loaded successfully.</div>', unsafe_allow_html=True)
    else:
        df = generate_demo_data()
        st.markdown('<div class="status-banner demo">Displaying demo dataset — upload a CSV to use real data.</div>', unsafe_allow_html=True)

    # ── KPIs ──
    total     = len(df)
    avg_wait  = df["Patient Waittime"].mean()
    avg_sat   = df["Patient Satisfaction Score"].mean()
    top_dept  = df["Department Referral"].mode()[0]
    crit_pct  = (df["Patient Waittime"] > 90).mean() * 100

    kpi_html = f"""
    <div class="kpi-grid">
        <div class="kpi-card" style="--accent:#4f7fe8;">
            <div class="kpi-label">Total Patients</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-sub">All records</div>
        </div>
        <div class="kpi-card" style="--accent:#34d399;">
            <div class="kpi-label">Avg Wait Time</div>
            <div class="kpi-value">{avg_wait:.0f}<span style="font-size:1rem;color:#6b7280;"> min</span></div>
            <div class="kpi-sub">Per patient</div>
        </div>
        <div class="kpi-card" style="--accent:#f59e0b;">
            <div class="kpi-label">Satisfaction Score</div>
            <div class="kpi-value">{avg_sat:.1f}<span style="font-size:1rem;color:#6b7280;">/10</span></div>
            <div class="kpi-sub">Average rating</div>
        </div>
        <div class="kpi-card" style="--accent:#f472b6;">
            <div class="kpi-label">Critical Wait (&gt;90 min)</div>
            <div class="kpi-value">{crit_pct:.1f}<span style="font-size:1rem;color:#6b7280;">%</span></div>
            <div class="kpi-sub">Of all patients</div>
        </div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)

    # ── CHARTS ROW 1 ──
    st.markdown('<div class="section-header">Department &amp; Wait Time</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        dept = df["Department Referral"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 3.6))
        bars = ax.barh(dept.index, dept.values,
                       color=PALETTE[:len(dept)], height=0.55, edgecolor="none")
        for bar, val in zip(bars, dept.values):
            ax.text(val + dept.values.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                    str(val), va="center", color=LIGHT_TEXT, fontsize=8.5,
                    fontfamily="monospace")
        apply_chart_style(fig, ax)
        ax.set_xlabel("Patient Count", fontsize=8.5)
        ax.invert_yaxis()
        fig.tight_layout(pad=1.5)
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        plt.close(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(6, 3.6))
        ax.hist(df["Patient Waittime"], bins=25, color=ACCENT, edgecolor=DARK_BG,
                linewidth=0.4, alpha=0.9)
        ax.axvline(avg_wait, color=ACCENT2, linewidth=1.4, linestyle="--", alpha=0.85,
                   label=f"Avg: {avg_wait:.0f} min")
        ax.legend(fontsize=8.5, framealpha=0, labelcolor=LIGHT_TEXT)
        apply_chart_style(fig, ax)
        ax.set_xlabel("Wait Time (minutes)", fontsize=8.5)
        ax.set_ylabel("Patients", fontsize=8.5)
        fig.tight_layout(pad=1.5)
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        plt.close(fig)

    # ── CHARTS ROW 2 ──
    st.markdown('<div class="section-header">Patient Patterns</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        fig, ax = plt.subplots(figsize=(6, 3.6))
        scatter = ax.scatter(
            df["Patient Waittime"],
            df["Patient Satisfaction Score"],
            alpha=0.25, s=12, c=df["Patient Waittime"],
            cmap="coolwarm", edgecolors="none"
        )
        # Trend line
        z = np.polyfit(df["Patient Waittime"].dropna(), df["Patient Satisfaction Score"].dropna(), 1)
        p = np.poly1d(z)
        xline = np.linspace(df["Patient Waittime"].min(), df["Patient Waittime"].max(), 100)
        ax.plot(xline, p(xline), color=ACCENT2, linewidth=1.4, alpha=0.8)
        apply_chart_style(fig, ax)
        ax.set_xlabel("Wait Time (minutes)", fontsize=8.5)
        ax.set_ylabel("Satisfaction Score", fontsize=8.5)
        fig.tight_layout(pad=1.5)
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        plt.close(fig)

    with col4:
        hour = df["Hour"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(6, 3.6))
        bar_colors = [ACCENT if h in range(8, 20) else "#2e3352" for h in hour.index]
        ax.bar(hour.index, hour.values, color=bar_colors, edgecolor="none", width=0.75)
        apply_chart_style(fig, ax)
        ax.set_xlabel("Hour of Day", fontsize=8.5)
        ax.set_ylabel("Arrivals", fontsize=8.5)
        ax.set_xticks([0, 6, 12, 18, 23])
        ax.set_xticklabels(["12 AM", "6 AM", "12 PM", "6 PM", "11 PM"], fontsize=8)
        fig.tight_layout(pad=1.5)
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        plt.close(fig)

    # ── AGE DISTRIBUTION ──
    st.markdown('<div class="section-header">Age Distribution</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12, 2.8))
    ax.hist(df["Patient Age"], bins=35, color=ACCENT3, edgecolor=DARK_BG,
            linewidth=0.4, alpha=0.85)
    ax.axvline(df["Patient Age"].mean(), color=ACCENT4, linewidth=1.4,
               linestyle="--", alpha=0.85,
               label=f"Avg: {df['Patient Age'].mean():.0f} yrs")
    ax.legend(fontsize=8.5, framealpha=0, labelcolor=LIGHT_TEXT)
    apply_chart_style(fig, ax)
    ax.set_xlabel("Patient Age", fontsize=8.5)
    ax.set_ylabel("Count", fontsize=8.5)
    fig.tight_layout(pad=1.5)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    plt.close(fig)

    # ── INSIGHTS ──
    st.markdown('<div class="section-header">Key Insights</div>', unsafe_allow_html=True)

    corr = df[["Patient Waittime", "Patient Satisfaction Score"]].corr().iloc[0, 1]
    peak_hour = int(df["Hour"].value_counts().idxmax())
    peak_label = f"{peak_hour:02d}:00 – {peak_hour+1:02d}:00"

    st.markdown(f"""
    <div class="insight-row">
        <div class="insight-card">
            <div class="insight-label">Busiest Arrival Window</div>
            <div class="insight-val">{peak_label}</div>
        </div>
        <div class="insight-card">
            <div class="insight-label">Wait vs Satisfaction Correlation</div>
            <div class="insight-val">{corr:.2f} <span style="font-size:0.8rem;color:#6b7280;">({'negative' if corr < 0 else 'positive'})</span></div>
        </div>
        <div class="insight-card">
            <div class="insight-label">Highest Volume Department</div>
            <div class="insight-val">{top_dept}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()