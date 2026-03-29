import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="ER Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&family=DM+Mono:wght@400;500&display=swap');

*, html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 2rem !important; max-width: 100% !important; }
.stApp { background: #0c0e16; color: #dde0ee; }

/* ── NAVBAR ── */
.navbar {
    position: sticky; top: 0; z-index: 999;
    background: #10131e;
    border-bottom: 1px solid #1c1f32;
    height: 52px;
    display: flex; align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    margin: 0 -4rem 24px -4rem;
}
.nb-left { display: flex; align-items: center; gap: 10px; }
.nb-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #4f7fe8; box-shadow: 0 0 10px #4f7fe866;
}
.nb-title { font-size: 0.88rem; font-weight: 600; color: #dde0ee; letter-spacing: -0.01em; }
.nb-slash { color: #252840; margin: 0 2px; }
.nb-sub { font-size: 0.78rem; color: #3b4060; font-weight: 400; }
.nb-right { display: flex; align-items: center; gap: 10px; }
.badge {
    font-size: 0.67rem; font-weight: 500; letter-spacing: 0.07em;
    text-transform: uppercase; padding: 4px 10px;
    border-radius: 20px; border: 1px solid #1c1f32; color: #3b4060;
}
.badge-live { color: #34d399; border-color: #34d39928; background: #34d39906; }
.badge-demo { color: #f59e0b; border-color: #f59e0b28; background: #f59e0b06; }
.badge-count { color: #3b4060; font-family: 'DM Mono', monospace; font-size: 0.7rem; }

/* Float upload button into navbar */
[data-testid="stFileUploader"] {
    position: fixed; top: 10px; right: 32px; z-index: 1000;
    width: 120px !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important; border: none !important;
    padding: 0 !important; min-height: unset !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] { display: none !important; }
[data-testid="stFileUploadedFile"] {
    background: #181b2c !important; border-radius: 6px !important;
    font-size: 0.7rem !important; color: #9ca3af !important;
    margin-top: 2px !important;
}
[data-testid="stBaseButton-secondary"] {
    background: #181b2c !important; border: 1px solid #262a40 !important;
    color: #9ca3af !important; font-size: 0.72rem !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important;
    letter-spacing: 0.03em !important; border-radius: 6px !important;
    height: 30px !important; min-height: 30px !important;
    padding: 0 14px !important; line-height: 30px !important;
    transition: border-color 0.15s, color 0.15s !important;
}
[data-testid="stBaseButton-secondary"]:hover {
    border-color: #4f7fe8 !important; color: #dde0ee !important;
}

/* ── KPI GRID ── */
.kpi-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 14px; margin-bottom: 4px;
}
.kpi {
    background: #10131e; border: 1px solid #1c1f32;
    border-radius: 10px; padding: 20px 22px;
    position: relative; overflow: hidden;
    transition: border-color 0.2s, transform 0.15s;
    cursor: default;
}
.kpi:hover { border-color: #2a2d4a; transform: translateY(-1px); }
.kpi::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: var(--c, #4f7fe8);
}
.kpi-lbl {
    font-size: 0.67rem; font-weight: 500; letter-spacing: 0.09em;
    text-transform: uppercase; color: #3b4060; margin-bottom: 10px;
}
.kpi-val {
    font-size: 2.1rem; font-weight: 600; color: #dde0ee;
    letter-spacing: -0.04em; line-height: 1;
    font-family: 'DM Mono', monospace;
}
.kpi-unit { font-size: 0.9rem; color: #3b4060; font-weight: 400; margin-left: 3px; }
.kpi-sub { font-size: 0.7rem; color: #252840; margin-top: 8px; }

/* ── SECTION LABELS ── */
.sec {
    font-size: 0.67rem; font-weight: 500; letter-spacing: 0.1em;
    text-transform: uppercase; color: #3b4060;
    margin: 28px 0 14px 0; padding-bottom: 10px;
    border-bottom: 1px solid #13162a;
    display: flex; align-items: center; gap: 8px;
}
.sec::before {
    content: ''; display: inline-block; width: 14px; height: 1px;
    background: #4f7fe8; flex-shrink: 0;
}

/* ── CHART CARDS ── */
.chart-card {
    background: #10131e; border: 1px solid #1c1f32;
    border-radius: 10px; padding: 4px; overflow: hidden;
}

/* ── INSIGHT CARDS ── */
.ins-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 12px; margin-top: 4px;
}
.ins {
    background: #10131e; border: 1px solid #1c1f32;
    border-radius: 8px; padding: 18px 20px;
}
.ins-lbl {
    font-size: 0.67rem; letter-spacing: 0.08em; text-transform: uppercase;
    color: #3b4060; margin-bottom: 8px;
}
.ins-val { font-size: 1rem; font-weight: 500; color: #dde0ee; }
.ins-val em { font-style: normal; font-size: 0.8rem; color: #3b4060; }
</style>
""", unsafe_allow_html=True)

# ── CHART THEME ──
BG   = "#10131e"
TEXT = "#c0c4d6"
GRID = "#1c1f32"
C1, C2, C3, C4 = "#4f7fe8", "#34d399", "#f59e0b", "#f472b6"
PAL  = [C1, C2, C3, C4, "#a78bfa", "#fb923c"]

def style(fig, ax):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.tick_params(colors=TEXT, labelsize=8.5)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    for sp in ax.spines.values(): sp.set_edgecolor(GRID)
    ax.yaxis.grid(True, color=GRID, linewidth=0.5, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)
    ax.xaxis.grid(False)

# ── DATA ──
def demo(n=1000):
    np.random.seed(42)
    return pd.DataFrame({
        "Patient Age":                np.random.randint(1, 90, n),
        "Patient Waittime":           np.random.randint(5, 120, n),
        "Patient Satisfaction Score": np.random.uniform(3, 9, n),
        "Department Referral":        np.random.choice(
            ["General Practice", "Orthopedics", "Cardiology", "Neurology", "Radiology"], n),
        "Hour": np.random.randint(0, 24, n),
    })

@st.cache_data
def load(file):
    try:
        df = pd.read_csv(file)
        for c in ["Patient Age","Patient Waittime","Patient Satisfaction Score","Department Referral"]:
            if c not in df.columns: df[c] = np.nan
        df["Patient Satisfaction Score"] = df["Patient Satisfaction Score"].fillna(
            df["Patient Satisfaction Score"].mean())
        df["Department Referral"] = df["Department Referral"].fillna("Unknown")
        if "Patient Admission Date" in df.columns:
            df["Patient Admission Date"] = pd.to_datetime(df["Patient Admission Date"], errors="coerce")
            df["Hour"] = df["Patient Admission Date"].dt.hour
        else:
            df["Hour"] = np.random.randint(0, 24, len(df))
        return df
    except Exception:
        return demo()

# ── APP ──
def main():
    # File uploader (floated into navbar via CSS)
    uploaded = st.file_uploader("csv", type=["csv"], label_visibility="collapsed")

    if uploaded:
        df = load(uploaded)
        mode_badge = '<span class="badge badge-live">Live</span>'
    else:
        df = demo()
        mode_badge = '<span class="badge badge-demo">Demo</span>'

    total = len(df)

    # Navbar
    st.markdown(f"""
    <div class="navbar">
        <div class="nb-left">
            <div class="nb-dot"></div>
            <span class="nb-title">ER Analytics</span>
            <span class="nb-slash">/</span>
            <span class="nb-sub">Emergency Room Performance</span>
        </div>
        <div class="nb-right">
            {mode_badge}
            <span class="badge badge-count">{total:,} records</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──
    avg_wait = df["Patient Waittime"].mean()
    avg_sat  = df["Patient Satisfaction Score"].mean()
    top_dept = df["Department Referral"].mode()[0]
    crit_pct = (df["Patient Waittime"] > 90).mean() * 100

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi" style="--c:{C1};">
            <div class="kpi-lbl">Total Patients</div>
            <div class="kpi-val">{total:,}</div>
            <div class="kpi-sub">All records</div>
        </div>
        <div class="kpi" style="--c:{C2};">
            <div class="kpi-lbl">Avg Wait Time</div>
            <div class="kpi-val">{avg_wait:.0f}<span class="kpi-unit">min</span></div>
            <div class="kpi-sub">Per patient</div>
        </div>
        <div class="kpi" style="--c:{C3};">
            <div class="kpi-lbl">Satisfaction Score</div>
            <div class="kpi-val">{avg_sat:.1f}<span class="kpi-unit">/ 10</span></div>
            <div class="kpi-sub">Average rating</div>
        </div>
        <div class="kpi" style="--c:{C4};">
            <div class="kpi-lbl">Critical Wait &gt;90 min</div>
            <div class="kpi-val">{crit_pct:.1f}<span class="kpi-unit">%</span></div>
            <div class="kpi-sub">Of all patients</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ROW 1 ──
    st.markdown('<div class="sec">Department &amp; Wait Distribution</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="medium")

    with c1:
        dept = df["Department Referral"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 3.5))
        bars = ax.barh(dept.index, dept.values, color=PAL[:len(dept)], height=0.5, edgecolor="none")
        for b, v in zip(bars, dept.values):
            ax.text(v + dept.values.max()*0.015, b.get_y() + b.get_height()/2,
                    str(v), va="center", color=TEXT, fontsize=8, fontfamily="monospace")
        ax.invert_yaxis()
        ax.set_xlabel("Patient Count", fontsize=8)
        style(fig, ax); fig.tight_layout(pad=1.4)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        plt.close(fig)

    with c2:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.hist(df["Patient Waittime"], bins=26, color=C1, edgecolor=BG, linewidth=0.3, alpha=0.88)
        ax.axvline(avg_wait, color=C2, linewidth=1.3, linestyle="--", label=f"Avg {avg_wait:.0f} min")
        ax.legend(fontsize=8, framealpha=0, labelcolor=TEXT)
        ax.set_xlabel("Wait Time (minutes)", fontsize=8)
        ax.set_ylabel("Patients", fontsize=8)
        style(fig, ax); fig.tight_layout(pad=1.4)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        plt.close(fig)

    # ── ROW 2 ──
    st.markdown('<div class="sec">Patient Patterns</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2, gap="medium")

    with c3:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.scatter(df["Patient Waittime"], df["Patient Satisfaction Score"],
                   alpha=0.22, s=11, c=df["Patient Waittime"], cmap="coolwarm", edgecolors="none")
        z = np.polyfit(df["Patient Waittime"].dropna(), df["Patient Satisfaction Score"].dropna(), 1)
        xln = np.linspace(df["Patient Waittime"].min(), df["Patient Waittime"].max(), 100)
        ax.plot(xln, np.poly1d(z)(xln), color=C2, linewidth=1.4, alpha=0.85)
        ax.set_xlabel("Wait Time (minutes)", fontsize=8)
        ax.set_ylabel("Satisfaction Score", fontsize=8)
        style(fig, ax); fig.tight_layout(pad=1.4)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        plt.close(fig)

    with c4:
        hour = df["Hour"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(6, 3.5))
        colors = [C1 if h in range(8, 20) else "#1e2235" for h in hour.index]
        ax.bar(hour.index, hour.values, color=colors, edgecolor="none", width=0.75)
        ax.set_xlabel("Hour of Day", fontsize=8)
        ax.set_ylabel("Arrivals", fontsize=8)
        ax.set_xticks([0, 6, 12, 18, 23])
        ax.set_xticklabels(["12 AM", "6 AM", "Noon", "6 PM", "11 PM"], fontsize=7.5)
        style(fig, ax); fig.tight_layout(pad=1.4)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        plt.close(fig)

    # ── AGE ──
    st.markdown('<div class="sec">Age Distribution</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12, 2.6))
    ax.hist(df["Patient Age"], bins=36, color=C3, edgecolor=BG, linewidth=0.3, alpha=0.85)
    ax.axvline(df["Patient Age"].mean(), color=C4, linewidth=1.3, linestyle="--",
               label=f"Avg {df['Patient Age'].mean():.0f} yrs")
    ax.legend(fontsize=8, framealpha=0, labelcolor=TEXT)
    ax.set_xlabel("Patient Age", fontsize=8)
    ax.set_ylabel("Count", fontsize=8)
    style(fig, ax); fig.tight_layout(pad=1.4)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    plt.close(fig)

    # ── INSIGHTS ──
    st.markdown('<div class="sec">Key Insights</div>', unsafe_allow_html=True)
    corr = df[["Patient Waittime","Patient Satisfaction Score"]].corr().iloc[0,1]
    peak = int(df["Hour"].value_counts().idxmax())

    st.markdown(f"""
    <div class="ins-grid">
        <div class="ins">
            <div class="ins-lbl">Busiest Arrival Window</div>
            <div class="ins-val">{peak:02d}:00 <em>to {peak+1:02d}:00</em></div>
        </div>
        <div class="ins">
            <div class="ins-lbl">Wait vs Satisfaction Correlation</div>
            <div class="ins-val">{corr:.2f} <em>({'negative' if corr < 0 else 'positive'} trend)</em></div>
        </div>
        <div class="ins">
            <div class="ins-lbl">Highest Volume Department</div>
            <div class="ins-val">{top_dept}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()