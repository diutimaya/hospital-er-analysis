import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hospital ER Analytics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Mono', monospace;
        background-color: #080d16;
        color: #e2e8f0;
    }

    .stApp { background-color: #080d16; }

    .block-container {
        padding: 2rem 2.5rem 3rem;
        max-width: 1400px;
    }

    h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: #fff !important; }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 28px;
    }

    .kpi-card {
        background: #0f172a;
        border: 1px solid #1e2d45;
        border-radius: 8px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
    }

    .kpi-card.blue::before  { background: #38bdf8; }
    .kpi-card.green::before { background: #34d399; }
    .kpi-card.pink::before  { background: #f472b6; }
    .kpi-card.orange::before{ background: #fb923c; }

    .kpi-label { font-size: 10px; color: #64748b; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 6px; }
    .kpi-value { font-family: 'Syne', sans-serif; font-size: 34px; font-weight: 800; color: #fff; line-height: 1; }
    .kpi-sub   { font-size: 10px; color: #64748b; margin-top: 5px; }

    .section-title {
        font-size: 10px;
        color: #64748b;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        border-bottom: 1px solid #1e2d45;
        padding-bottom: 8px;
        margin-bottom: 14px;
    }

    .insight-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 8px;
    }

    .pill {
        background: #162032;
        border: 1px solid #1e2d45;
        border-radius: 4px;
        padding: 7px 14px;
        font-size: 11px;
        color: #94a3b8;
    }

    .pill strong { color: #fff; }

    footer { color: #64748b; font-size: 10px; margin-top: 40px; }

    div[data-testid="stMetric"] {
        background: #0f172a;
        border: 1px solid #1e2d45;
        border-radius: 8px;
        padding: 16px 20px;
    }
</style>
""", unsafe_allow_html=True)

# ── DATA LOADER ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Drop name columns if they exist
    drop_cols = [c for c in ["Patient First Inital", "Patient Last Name"] if c in df.columns]
    if drop_cols:
        df.drop(columns=drop_cols, inplace=True)

    # Fill missing values
    if "Department Referral" in df.columns:
        df["Department Referral"] = df["Department Referral"].fillna("Unknown")

    if "Patient Satisfaction Score" in df.columns:
        df["Patient Satisfaction Score"] = df["Patient Satisfaction Score"].fillna(
            df["Patient Satisfaction Score"].mean()
        )

    # Parse dates
    if "Patient Admission Date" in df.columns:
        df["Patient Admission Date"] = pd.to_datetime(
            df["Patient Admission Date"], errors="coerce"
        )
        df["Hour"] = df["Patient Admission Date"].dt.hour

    # Age groups
    if "Patient Age" in df.columns:
        df["Age Group"] = pd.cut(
            df["Patient Age"],
            bins=[0, 18, 35, 50, 65, 100],
            labels=["Child", "Young Adult", "Adult", "Middle Age", "Senior"],
        )

    return df


# ── CHART STYLE ────────────────────────────────────────────────────────────────
BG   = "#080d16"
SURF = "#0f172a"
BORDER = "#1e2d45"
TEXT = "#94a3b8"
ACCENT = "#3b82f6"

def apply_style(ax, fig):
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    ax.tick_params(colors=TEXT, labelsize=8)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.xaxis.label.set_size(8)
    ax.yaxis.label.set_size(8)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)
    ax.grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.7)
    ax.grid(axis="x", visible=False)
    return fig, ax


# ── MAIN ───────────────────────────────────────────────────────────────────────
def main():
    # ── HEADER ──
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("""
        <h1 style="font-size:clamp(24px,3vw,42px);font-weight:400;line-height:1.1;margin-bottom:4px">
            Hospital <em style="font-style:italic;color:#38bdf8">Emergency Room</em> Analytics
        </h1>
        <p style="font-size:10px;color:#64748b;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:24px">
            Diutimaya Mohanty &nbsp;·&nbsp; B.Tech — Data Science &nbsp;·&nbsp; 2024
        </p>
        """, unsafe_allow_html=True)

    with col_h2:
        st.markdown("""
        <div style="text-align:right;padding-top:6px">
            <span style="background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.3);
                border-radius:4px;padding:5px 12px;font-size:10px;color:#34d399;
                letter-spacing:0.12em;text-transform:uppercase">
                ● Dashboard Live
            </span>
        </div>
        """, unsafe_allow_html=True)

    # ── CSV UPLOAD ──
    uploaded = st.file_uploader(
        "Upload Hospital ER Data CSV",
        type=["csv"],
        help="Upload your Hospital ER_Data.csv to load real data"
    )

    data_path = None
    if uploaded:
        tmp_path = "/tmp/er_data_upload.csv"
        with open(tmp_path, "wb") as f:
            f.write(uploaded.read())
        data_path = tmp_path
        st.success(f"✔ Loaded: {uploaded.name}")

    # Try local path as fallback
    local_paths = [
        "data/Hospital ER_Data.csv",
        "data/Hospital ER Data.csv",
        "data/hospital_er_cleaned.csv",
    ]
    if not data_path:
        for p in local_paths:
            if os.path.exists(p):
                data_path = p
                break

    if not data_path:
        st.info("Upload your CSV above, or place it at `data/Hospital ER_Data.csv`.\n\nShowing demo stats from dashboard in the meantime.")
        show_static_dashboard()
        return

    df = load_data(data_path)

    # ── KPI CARDS ──
    total     = len(df)
    avg_wait  = df["Patient Waittime"].mean() if "Patient Waittime" in df.columns else 35
    avg_sat   = df["Patient Satisfaction Score"].mean() if "Patient Satisfaction Score" in df.columns else 5.4
    top_dept  = df["Department Referral"].value_counts().idxmax() if "Department Referral" in df.columns else "General Practice"

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="kpi-label">Total Patients</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-sub">ER records analyzed</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">Avg Wait Time</div>
            <div class="kpi-value">{avg_wait:.0f}<span style="font-size:14px;color:#64748b"> min</span></div>
            <div class="kpi-sub">before treatment begins</div>
        </div>
        <div class="kpi-card pink">
            <div class="kpi-label">Avg Satisfaction</div>
            <div class="kpi-value">{avg_sat:.1f}<span style="font-size:14px;color:#64748b">/10</span></div>
            <div class="kpi-sub">patient satisfaction score</div>
        </div>
        <div class="kpi-card orange">
            <div class="kpi-label">Top Department</div>
            <div class="kpi-value" style="font-size:18px;line-height:1.3;padding-top:4px">{top_dept}</div>
            <div class="kpi-sub">{df["Department Referral"].value_counts().iloc[0]:,} referrals</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ROW 1 ──
    c1, c2 = st.columns([5, 7])

    with c1:
        st.markdown('<div class="section-title">Patients per Department</div>', unsafe_allow_html=True)
        dept_counts = df["Department Referral"].value_counts().head(8)
        fig, ax = plt.subplots(figsize=(5, 3.6))
        colors = [ACCENT if i == 0 else "#1e3a5f" for i in range(len(dept_counts))]
        bars = ax.barh(dept_counts.index[::-1], dept_counts.values[::-1], color=colors[::-1], height=0.6)
        for bar, val in zip(bars, dept_counts.values[::-1]):
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                    f"{val:,}", va="center", ha="left", color="#fff", fontsize=8)
        ax.set_xlabel("Count of Patients")
        ax.set_xlim(0, dept_counts.max() * 1.18)
        apply_style(ax, fig)
        ax.grid(axis="x", color=BORDER, linewidth=0.5, alpha=0.7)
        ax.grid(axis="y", visible=False)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    with c2:
        st.markdown('<div class="section-title">Wait Time Distribution</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(7, 3.6))
        ax.hist(df["Patient Waittime"].dropna(), bins=20,
                color=ACCENT, edgecolor="#080d16", linewidth=0.5, alpha=0.9)
        ax.set_xlabel("Patient Wait Time (min)")
        ax.set_ylabel("Count")
        apply_style(ax, fig)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    # ── ROW 2 ──
    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="section-title">Wait Time vs Satisfaction Score</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 3.4))
        ax.scatter(
            df["Patient Waittime"], df["Patient Satisfaction Score"],
            alpha=0.25, s=10, color="#38bdf8", edgecolors="none"
        )
        ax.set_xlabel("Avg Patient Waittime")
        ax.set_ylabel("Avg Patient Satisfaction Score")
        apply_style(ax, fig)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    with c4:
        st.markdown('<div class="section-title">Patient Arrival by Hour</div>', unsafe_allow_html=True)
        hour_counts = df["Hour"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(6, 3.4))
        bar_colors = ["#f87171" if h == hour_counts.idxmax() else ACCENT for h in hour_counts.index]
        ax.bar(hour_counts.index, hour_counts.values, color=bar_colors, width=0.7)
        ax.set_xlabel("Arrival Hour")
        ax.set_ylabel("Count")
        apply_style(ax, fig)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    # ── ROW 3 ──
    c5, c6 = st.columns([7, 5])

    with c5:
        st.markdown('<div class="section-title">Patient Age Distribution</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(7, 3.2))
        ax.hist(df["Patient Age"].dropna(), bins=20,
                color="#f472b6", edgecolor="#080d16", linewidth=0.5, alpha=0.85)
        ax.set_xlabel("Patient Age (bin)")
        ax.set_ylabel("Number of Patients")
        apply_style(ax, fig)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    with c6:
        st.markdown('<div class="section-title">Patients by Age Group</div>', unsafe_allow_html=True)
        age_order = ["Child", "Young Adult", "Adult", "Middle Age", "Senior"]
        age_counts = df["Age Group"].value_counts().reindex(age_order).dropna()
        fig, ax = plt.subplots(figsize=(5, 3.2))
        bar_colors = ["#7c3aed","#a855f7","#c084fc","#e879f9","#f0abfc"]
        bars = ax.barh(age_counts.index[::-1], age_counts.values[::-1],
                       color=bar_colors, height=0.55)
        for bar, val in zip(bars, age_counts.values[::-1]):
            ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                    f"{val:,}", va="center", ha="left", color="#fff", fontsize=8)
        ax.set_xlabel("Count of Patients")
        ax.set_xlim(0, age_counts.max() * 1.18)
        apply_style(ax, fig)
        ax.grid(axis="x", color=BORDER, linewidth=0.5, alpha=0.7)
        ax.grid(axis="y", visible=False)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    # ── KEY INSIGHTS ──
    st.markdown('<div class="section-title" style="margin-top:20px">Key Insights</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="insight-grid">
        <div class="pill"><strong>{top_dept}</strong> leads referrals at <strong>{df["Department Referral"].value_counts().iloc[0]:,}</strong> patients</div>
        <div class="pill">Average wait time is <strong>{avg_wait:.0f} minutes</strong> across all patients</div>
        <div class="pill"><strong>Middle Age &amp; Senior</strong> groups form the majority of ER visits</div>
        <div class="pill">Satisfaction <strong>decreases slightly</strong> as wait time increases</div>
        <div class="pill">Peak arrivals observed at <strong>hour {hour_counts.idxmax() if "Hour" in df.columns else 23}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <footer style="margin-top:40px;padding-top:20px;border-top:1px solid #1e2d45;
        display:flex;justify-content:space-between;font-size:10px;color:#64748b">
        <span>Hospital ER Analytics · Python · Pandas · Streamlit · Matplotlib</span>
        <span>github.com/diutimaya/hospital-er-analysis</span>
    </footer>
    """, unsafe_allow_html=True)


def show_static_dashboard():
    """Fallback view using hardcoded values from the dashboard screenshot."""
    st.markdown("""
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="kpi-label">Total Patients</div>
            <div class="kpi-value">9,216</div>
            <div class="kpi-sub">ER records analyzed</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">Avg Wait Time</div>
            <div class="kpi-value">35<span style="font-size:14px;color:#64748b"> min</span></div>
            <div class="kpi-sub">before treatment begins</div>
        </div>
        <div class="kpi-card pink">
            <div class="kpi-label">Avg Satisfaction</div>
            <div class="kpi-value">5.4<span style="font-size:14px;color:#64748b">/10</span></div>
            <div class="kpi-sub">patient satisfaction score</div>
        </div>
        <div class="kpi-card orange">
            <div class="kpi-label">Top Department</div>
            <div class="kpi-value" style="font-size:18px;line-height:1.3;padding-top:4px">General Practice</div>
            <div class="kpi-sub">1,840 referrals</div>
        </div>
    </div>

    <div class="insight-grid" style="margin-top:16px">
        <div class="pill"><strong>General Practice</strong> leads referrals at <strong>1,840</strong> patients</div>
        <div class="pill">Average wait time is <strong>~35 minutes</strong> across all patients</div>
        <div class="pill"><strong>Middle Age &amp; Senior</strong> groups form the majority of ER visits</div>
        <div class="pill">Satisfaction <strong>decreases slightly</strong> as wait time increases</div>
        <div class="pill">Peak arrivals at <strong>hour 23</strong> (late evening)</div>
        <div class="pill"><strong>Orthopedics</strong> 2nd busiest at <strong>995</strong> referrals</div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
