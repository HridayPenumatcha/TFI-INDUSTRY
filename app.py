"""
TFI Nepotism Analysis Dashboard
Telugu Film Industry – Nepo vs Self-Made Actor Analysis
Data Analytics Course Project | SP Jain GMBA
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, silhouette_score, r2_score
from sklearn.decomposition import PCA
import warnings
import os
import sys

warnings.filterwarnings("ignore")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TFI Nepotism Analyser",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Colour palette ────────────────────────────────────────────────────────────
NEPO_COLOR   = "#E63946"
SELF_COLOR   = "#457B9D"
BG_DARK      = "#0D1117"
CARD_BG      = "#161B22"
ACCENT       = "#F4A261"
TEXT_LIGHT   = "#E0E0E0"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #0D1117; color: #E0E0E0; }
  [data-testid="stSidebar"]          { background: #161B22; }
  h1,h2,h3,h4                        { color: #F4A261; }
  .metric-card {
      background:#161B22; border-radius:12px; padding:20px 16px;
      border-left:4px solid #F4A261; text-align:center; margin-bottom:8px;
  }
  .metric-val  { font-size:2rem; font-weight:700; color:#F4A261; }
  .metric-lbl  { font-size:.85rem; color:#aaa; margin-top:4px; }
  .nepo-badge  { background:#E63946; color:#fff; border-radius:6px; padding:2px 8px; font-size:.8rem; }
  .self-badge  { background:#457B9D; color:#fff; border-radius:6px; padding:2px 8px; font-size:.8rem; }
  .insight-box {
      background:#1C2333; border-left:4px solid #E63946;
      border-radius:8px; padding:14px 16px; margin:10px 0;
  }
  .section-divider { border-top:1px solid #30363D; margin:24px 0; }
</style>
""", unsafe_allow_html=True)


# ── Load / generate data ──────────────────────────────────────────────────────
@st.cache_data
def load_data():
    xlsx_path = "TFI_Nepotism_Analysis.xlsx"
    if not os.path.exists(xlsx_path):
        # auto-generate if running on Streamlit Cloud
        sys.path.insert(0, os.path.dirname(__file__))
        from generate_data import create_tfi_dataset
        df = create_tfi_dataset()
        df.to_excel(xlsx_path, index=False)
    else:
        df = pd.read_excel(xlsx_path)
    return df


df = load_data()
nepo_df = df[df["Background"] == "Nepo"]
self_df  = df[df["Background"] == "Self-Made"]


# ── Helpers ───────────────────────────────────────────────────────────────────
def metric_card(col, value, label):
    col.markdown(f"""
    <div class="metric-card">
      <div class="metric-val">{value}</div>
      <div class="metric-lbl">{label}</div>
    </div>""", unsafe_allow_html=True)


def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)


# ── Sidebar nav ───────────────────────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Telugu_film_icon.svg/120px-Telugu_film_icon.svg.png",
                 width=60, use_column_width=False)
st.sidebar.title("🎬 TFI Analyser")
st.sidebar.caption("Nepotism vs Self-Made | Telugu Film Industry")

pages = [
    "🏠  Home",
    "📊  Descriptive Stats",
    "⚔️  Nepo vs Self-Made",
    "🔵  K-Means Clustering",
    "📈  Regression Analysis",
    "🧩  Segmentation",
    "🗂️  Raw Data",
]
page = st.sidebar.radio("Navigate", pages)

# Sidebar filters
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")
gender_filter = st.sidebar.multiselect("Gender", ["Male", "Female"], default=["Male", "Female"])
bg_filter     = st.sidebar.multiselect("Background", ["Nepo", "Self-Made"], default=["Nepo", "Self-Made"])
min_movies    = st.sidebar.slider("Minimum Movies", 1, 30, 1)

fdf = df[
    df["Gender"].isin(gender_filter) &
    df["Background"].isin(bg_filter) &
    (df["Total_Movies"] >= min_movies)
]

st.sidebar.markdown("---")
st.sidebar.caption("SP Jain GMBA | Data Analytics Course\nBuilt with Streamlit + Scikit-learn")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 – HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Home":
    st.title("🎬 TFI Nepotism Analysis")
    st.markdown("### *Does your last name write your first script?*")
    st.caption("Analysing 45 active Telugu Film Industry actors & actresses through the lens of background, opportunity, and success.")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    metric_card(c1, len(df), "Total Actors Analysed")
    metric_card(c2, len(nepo_df), "Nepo Background")
    metric_card(c3, len(self_df), "Self-Made")
    metric_card(c4, f"{nepo_df['Success_Rate_Pct'].mean():.1f}%", "Avg Nepo Success Rate")
    metric_card(c5, f"{self_df['Success_Rate_Pct'].mean():.1f}%", "Avg Self-Made Success Rate")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        # Pie chart
        bg_counts = df["Background"].value_counts().reset_index()
        bg_counts.columns = ["Background", "Count"]
        fig_pie = px.pie(bg_counts, names="Background", values="Count",
                         color="Background",
                         color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                         title="Industry Composition",
                         hole=0.45)
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color=TEXT_LIGHT, title_font_color=ACCENT,
                              legend=dict(font=dict(color=TEXT_LIGHT)))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Success rate comparison bar
        tier_bg = df.groupby(["Career_Tier", "Background"]).size().reset_index(name="Count")
        tier_order = ["Superstar", "A-List", "Mid-Tier", "Struggling"]
        tier_bg["Career_Tier"] = pd.Categorical(tier_bg["Career_Tier"], categories=tier_order, ordered=True)
        tier_bg = tier_bg.sort_values("Career_Tier")
        fig_tier = px.bar(tier_bg, x="Career_Tier", y="Count", color="Background",
                          barmode="group", title="Career Tier Distribution: Nepo vs Self-Made",
                          color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR})
        fig_tier.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color=TEXT_LIGHT, title_font_color=ACCENT,
                               xaxis=dict(color=TEXT_LIGHT), yaxis=dict(color=TEXT_LIGHT),
                               legend=dict(font=dict(color=TEXT_LIGHT)))
        st.plotly_chart(fig_tier, use_container_width=True)

    # Opportunity gap snapshot
    st.subheader("⚡ The Opportunity Gap – At a Glance")
    col3, col4, col5 = st.columns(3)

    with col3:
        avg_opp_nepo = nepo_df["Opportunities_First_3Yrs"].mean()
        avg_opp_self = self_df["Opportunities_First_3Yrs"].mean()
        fig_opp = go.Figure(go.Bar(
            x=["Nepo", "Self-Made"],
            y=[avg_opp_nepo, avg_opp_self],
            marker_color=[NEPO_COLOR, SELF_COLOR],
            text=[f"{avg_opp_nepo:.1f}", f"{avg_opp_self:.1f}"],
            textposition="outside",
        ))
        fig_opp.update_layout(title="Avg Opportunities\nFirst 3 Years",
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color=TEXT_LIGHT, title_font_color=ACCENT,
                               yaxis=dict(color=TEXT_LIGHT), xaxis=dict(color=TEXT_LIGHT),
                               height=280)
        st.plotly_chart(fig_opp, use_container_width=True)

    with col4:
        avg_rec_nepo = nepo_df["Recovery_Chances_After_Flops"].mean()
        avg_rec_self = self_df["Recovery_Chances_After_Flops"].mean()
        fig_rec = go.Figure(go.Bar(
            x=["Nepo", "Self-Made"],
            y=[avg_rec_nepo, avg_rec_self],
            marker_color=[NEPO_COLOR, SELF_COLOR],
            text=[f"{avg_rec_nepo:.1f}", f"{avg_rec_self:.1f}"],
            textposition="outside",
        ))
        fig_rec.update_layout(title="Recovery Chances\nAfter Flops",
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color=TEXT_LIGHT, title_font_color=ACCENT,
                               yaxis=dict(color=TEXT_LIGHT), xaxis=dict(color=TEXT_LIGHT),
                               height=280)
        st.plotly_chart(fig_rec, use_container_width=True)

    with col5:
        avg_bud_nepo = nepo_df["Debut_Budget_Cr"].mean()
        avg_bud_self = self_df["Debut_Budget_Cr"].mean()
        fig_bud = go.Figure(go.Bar(
            x=["Nepo", "Self-Made"],
            y=[avg_bud_nepo, avg_bud_self],
            marker_color=[NEPO_COLOR, SELF_COLOR],
            text=[f"₹{avg_bud_nepo:.0f}Cr", f"₹{avg_bud_self:.0f}Cr"],
            textposition="outside",
        ))
        fig_bud.update_layout(title="Avg Debut Film\nBudget (Cr)",
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color=TEXT_LIGHT, title_font_color=ACCENT,
                               yaxis=dict(color=TEXT_LIGHT), xaxis=dict(color=TEXT_LIGHT),
                               height=280)
        st.plotly_chart(fig_bud, use_container_width=True)

    insight(f"Nepo actors debut with **₹{avg_bud_nepo:.0f}Cr** budgets on average vs **₹{avg_bud_self:.0f}Cr** for self-made actors — "
            f"a **{avg_bud_nepo/avg_bud_self:.1f}x advantage** before a single frame is shot.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 – DESCRIPTIVE STATS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊  Descriptive Stats":
    st.title("📊 Descriptive Statistics")
    st.caption("Distribution and summary of key performance metrics across TFI")

    tab1, tab2, tab3 = st.tabs(["Summary Table", "Distributions", "Correlations"])

    with tab1:
        st.subheader("Statistical Summary by Background")
        numeric_cols = ["Total_Movies", "Success_Rate_Pct", "Avg_Movies_Per_Year",
                        "Debut_Budget_Cr", "Total_BO_Collection_Cr", "Awards_Won",
                        "Opportunities_First_3Yrs", "Recovery_Chances_After_Flops",
                        "Social_Media_Followers_M", "Brand_Endorsements"]
        summary = fdf.groupby("Background")[numeric_cols].mean().round(2).T
        summary.columns = ["🔴 Nepo Avg", "🔵 Self-Made Avg"]
        summary["Nepo Advantage"] = ((summary["🔴 Nepo Avg"] - summary["🔵 Self-Made Avg"]) /
                                      summary["🔵 Self-Made Avg"] * 100).round(1).astype(str) + "%"
        st.dataframe(summary, use_container_width=True)

        st.markdown("---")
        st.subheader("Top 10 by Box Office Collection")
        top10 = fdf.nlargest(10, "Total_BO_Collection_Cr")[
            ["Name","Background","Total_BO_Collection_Cr","Success_Rate_Pct","Career_Tier"]
        ]
        fig_top = px.bar(top10, x="Total_BO_Collection_Cr", y="Name", orientation="h",
                         color="Background",
                         color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                         title="Top 10 by Total Box Office (₹ Cr)")
        fig_top.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color=TEXT_LIGHT, title_font_color=ACCENT,
                               yaxis=dict(color=TEXT_LIGHT, autorange="reversed"),
                               xaxis=dict(color=TEXT_LIGHT))
        st.plotly_chart(fig_top, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig_sr = px.histogram(fdf, x="Success_Rate_Pct", color="Background",
                                  nbins=15, barmode="overlay", opacity=0.75,
                                  color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                                  title="Success Rate Distribution (%)",
                                  labels={"Success_Rate_Pct": "Success Rate (%)"})
            fig_sr.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font_color=TEXT_LIGHT, title_font_color=ACCENT)
            st.plotly_chart(fig_sr, use_container_width=True)

        with col2:
            fig_box = px.box(fdf, x="Background", y="Success_Rate_Pct", color="Background",
                             points="all", color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                             title="Success Rate Box Plot", labels={"Success_Rate_Pct": "Success Rate (%)"})
            fig_box.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   font_color=TEXT_LIGHT, title_font_color=ACCENT,
                                   showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            fig_yrs = px.scatter(fdf, x="Years_in_Industry", y="Total_Movies",
                                 color="Background", size="Success_Rate_Pct",
                                 hover_name="Name", hover_data=["Career_Tier"],
                                 color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                                 title="Years in Industry vs Movies Made")
            fig_yrs.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   font_color=TEXT_LIGHT, title_font_color=ACCENT)
            st.plotly_chart(fig_yrs, use_container_width=True)

        with col4:
            fig_bo = px.violin(fdf, y="Total_BO_Collection_Cr", x="Background", color="Background",
                               box=True, points="all", hover_name="Name",
                               color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                               title="Box Office Collection Distribution (₹ Cr)")
            fig_bo.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font_color=TEXT_LIGHT, title_font_color=ACCENT, showlegend=False)
            st.plotly_chart(fig_bo, use_container_width=True)

    with tab3:
        numeric_only = fdf.select_dtypes(include=np.number).drop(
            columns=["Actor_ID", "Background_Binary", "Debut_Year", "Age"], errors="ignore"
        )
        corr = numeric_only.corr()
        fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                              title="Correlation Matrix – Key Metrics",
                              aspect="auto", zmin=-1, zmax=1)
        fig_corr.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                font_color=TEXT_LIGHT, title_font_color=ACCENT,
                                width=800, height=600)
        st.plotly_chart(fig_corr, use_container_width=True)
        insight("Strong positive correlation between **Opportunities_First_3Yrs** and **Total_BO_Collection_Cr** "
                "suggests that early exposure—heavily biased toward nepo actors—is a primary growth driver.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 – NEPO vs SELF-MADE DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚔️  Nepo vs Self-Made":
    st.title("⚔️ Nepo vs Self-Made – Deep Dive")

    tab1, tab2, tab3 = st.tabs(["Opportunity Bias", "Success Metrics", "Actor Profiles"])

    with tab1:
        st.subheader("The Hidden Advantage: Opportunities Before Talent Is Proven")
        col1, col2 = st.columns(2)

        with col1:
            opp_compare = fdf.groupby("Background")[
                ["Opportunities_First_3Yrs", "Recovery_Chances_After_Flops", "Debut_Budget_Cr"]
            ].mean().reset_index()
            opp_long = opp_compare.melt(id_vars="Background",
                                         var_name="Metric", value_name="Value")
            fig_opp = px.bar(opp_long, x="Metric", y="Value", color="Background",
                              barmode="group",
                              color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                              title="Opportunity Metrics: Nepo vs Self-Made",
                              labels={"Value": "Average", "Metric": ""})
            fig_opp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   font_color=TEXT_LIGHT, title_font_color=ACCENT,
                                   xaxis=dict(color=TEXT_LIGHT), yaxis=dict(color=TEXT_LIGHT))
            st.plotly_chart(fig_opp, use_container_width=True)

        with col2:
            # Failure tolerance bubble
            fig_tol = px.scatter(fdf, x="Total_Movies", y="Recovery_Chances_After_Flops",
                                  size="Debut_Budget_Cr", color="Background",
                                  hover_name="Name",
                                  color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                                  title="Failure Tolerance: Movie Count vs Recovery Chances",
                                  labels={"Recovery_Chances_After_Flops": "Recovery Chances After Flops",
                                          "Total_Movies": "Total Movies"})
            fig_tol.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   font_color=TEXT_LIGHT, title_font_color=ACCENT)
            st.plotly_chart(fig_tol, use_container_width=True)

        insight(f"Nepo actors receive on average **{nepo_df['Recovery_Chances_After_Flops'].mean():.1f}** "
                f"films after consecutive flops vs **{self_df['Recovery_Chances_After_Flops'].mean():.1f}** "
                f"for self-made actors. This unequal 'failure tolerance' is the invisible force sustaining nepotism.")

    with tab2:
        st.subheader("Success Metrics Breakdown")
        col1, col2 = st.columns(2)

        with col1:
            fig_radar_data = fdf.groupby("Background")[
                ["Success_Rate_Pct", "Genre_Versatility_Score", "Critical_Acclaim_Score",
                 "Brand_Endorsements", "OTT_Projects"]
            ].mean()

            categories = ["Success Rate", "Genre Versatility", "Critical Acclaim",
                          "Brand Endorsements", "OTT Projects"]

            fig_radar = go.Figure()
            for bg, color in [("Nepo", NEPO_COLOR), ("Self-Made", SELF_COLOR)]:
                values = fig_radar_data.loc[bg].values.tolist()
                # Normalise for radar (0-100 scale)
                vals_norm = [
                    values[0],
                    values[1] * 10,
                    values[2] * 10,
                    values[3] * 10,
                    values[4] * 15,
                ]
                fig_radar.add_trace(go.Scatterpolar(
                    r=vals_norm + [vals_norm[0]],
                    theta=categories + [categories[0]],
                    fill="toself", name=bg,
                    line_color=color, fillcolor=color,
                    opacity=0.4
                ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100], color=TEXT_LIGHT),
                           bgcolor=CARD_BG),
                paper_bgcolor="rgba(0,0,0,0)",
                font_color=TEXT_LIGHT, title_font_color=ACCENT,
                title="Radar: Multi-Dimensional Performance",
                showlegend=True,
                legend=dict(font=dict(color=TEXT_LIGHT))
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col2:
            # Budget vs BO return
            fig_roi = px.scatter(fdf, x="Avg_Budget_Cr", y="BO_Per_Movie_Cr",
                                  color="Background", hover_name="Name",
                                  size="Total_Movies",
                                  color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                                  title="Budget Invested vs Box Office Return per Movie",
                                  labels={"Avg_Budget_Cr": "Avg Budget (Cr)",
                                          "BO_Per_Movie_Cr": "BO per Movie (Cr)"})
            # Add diagonal
            max_val = fdf["Avg_Budget_Cr"].max()
            fig_roi.add_shape(type="line", x0=0, y0=0, x1=max_val, y1=max_val,
                              line=dict(dash="dash", color="#888"))
            fig_roi.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   font_color=TEXT_LIGHT, title_font_color=ACCENT)
            st.plotly_chart(fig_roi, use_container_width=True)

        # Stacked flop/hit/blockbuster breakdown
        st.subheader("Hit-Flop Breakdown by Background")
        breakdown = fdf.groupby("Background")[
            ["Hit_Movies", "Blockbuster_Movies", "Flop_Movies"]
        ].mean().reset_index()
        breakdown_long = breakdown.melt(id_vars="Background", var_name="Type", value_name="Avg")
        color_map = {"Hit_Movies": "#2ECC71", "Blockbuster_Movies": ACCENT, "Flop_Movies": NEPO_COLOR}
        fig_stk = px.bar(breakdown_long, x="Background", y="Avg", color="Type",
                          barmode="stack",
                          color_discrete_map=color_map,
                          title="Average Hit/Blockbuster/Flop Composition",
                          labels={"Avg": "Avg Movies", "Type": "Movie Type"})
        fig_stk.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color=TEXT_LIGHT, title_font_color=ACCENT)
        st.plotly_chart(fig_stk, use_container_width=True)

    with tab3:
        st.subheader("Individual Actor Profiles")
        selected = st.selectbox("Select an Actor", fdf["Name"].sort_values().tolist())
        actor = fdf[fdf["Name"] == selected].iloc[0]
        bg_badge = f'<span class="nepo-badge">Nepo</span>' if actor["Background"] == "Nepo" else f'<span class="self-badge">Self-Made</span>'
        st.markdown(f"## {actor['Name']}  {bg_badge}", unsafe_allow_html=True)
        st.caption(f"*{actor['Family_Connection']}*")

        c1, c2, c3, c4 = st.columns(4)
        metric_card(c1, f"{actor['Success_Rate_Pct']}%", "Success Rate")
        metric_card(c2, actor["Total_Movies"], "Total Movies")
        metric_card(c3, f"₹{actor['Total_BO_Collection_Cr']}Cr", "Total Box Office")
        metric_card(c4, actor["Career_Tier"], "Career Tier")

        c5, c6, c7, c8 = st.columns(4)
        metric_card(c5, actor["Opportunities_First_3Yrs"], "Opp. in First 3 Yrs")
        metric_card(c6, actor["Recovery_Chances_After_Flops"], "Recovery Chances")
        metric_card(c7, f"₹{actor['Debut_Budget_Cr']}Cr", "Debut Budget")
        metric_card(c8, actor["Awards_Won"], "Awards Won")

        # Mini bar chart
        movie_types = pd.DataFrame({
            "Type": ["Hits", "Blockbusters", "Flops"],
            "Count": [actor["Hit_Movies"], actor["Blockbuster_Movies"], actor["Flop_Movies"]],
            "Color": ["#2ECC71", ACCENT, NEPO_COLOR]
        })
        fig_mini = px.bar(movie_types, x="Type", y="Count", color="Type",
                          color_discrete_map={"Hits": "#2ECC71", "Blockbusters": ACCENT, "Flops": NEPO_COLOR},
                          title=f"Movie Performance – {actor['Name']}")
        fig_mini.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                font_color=TEXT_LIGHT, title_font_color=ACCENT, showlegend=False)
        st.plotly_chart(fig_mini, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 – K-MEANS CLUSTERING
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔵  K-Means Clustering":
    st.title("🔵 K-Means Clustering")
    st.caption("Grouping actors by performance profile — independent of background label")

    cluster_features = ["Success_Rate_Pct", "Total_Movies", "Avg_Budget_Cr",
                        "Opportunities_First_3Yrs", "Recovery_Chances_After_Flops",
                        "BO_Per_Movie_Cr", "Awards_Won", "Social_Media_Followers_M"]

    cluster_df = fdf[cluster_features + ["Name", "Background"]].dropna()
    X = cluster_df[cluster_features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Elbow chart
    tab1, tab2, tab3 = st.tabs(["Elbow Method", "Cluster Profiles", "Actor Cluster Map"])

    with tab1:
        st.subheader("Finding the Optimal K – Elbow Method")
        inertias = []
        silhouettes = []
        K_range = range(2, 9)
        for k in K_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            inertias.append(km.inertia_)
            silhouettes.append(silhouette_score(X_scaled, km.labels_))

        col1, col2 = st.columns(2)
        with col1:
            fig_elbow = go.Figure()
            fig_elbow.add_trace(go.Scatter(x=list(K_range), y=inertias, mode="lines+markers",
                                            marker=dict(color=ACCENT, size=10),
                                            line=dict(color=ACCENT)))
            fig_elbow.update_layout(title="Elbow Plot (Inertia vs K)",
                                     xaxis_title="Number of Clusters (K)",
                                     yaxis_title="Inertia",
                                     paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                     font_color=TEXT_LIGHT, title_font_color=ACCENT)
            st.plotly_chart(fig_elbow, use_container_width=True)

        with col2:
            fig_sil = go.Figure()
            fig_sil.add_trace(go.Scatter(x=list(K_range), y=silhouettes, mode="lines+markers",
                                          marker=dict(color=SELF_COLOR, size=10),
                                          line=dict(color=SELF_COLOR)))
            fig_sil.update_layout(title="Silhouette Score vs K",
                                   xaxis_title="Number of Clusters (K)",
                                   yaxis_title="Silhouette Score",
                                   paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   font_color=TEXT_LIGHT, title_font_color=ACCENT)
            st.plotly_chart(fig_sil, use_container_width=True)

        insight("The elbow at K=4 and the peak silhouette score around K=4 suggest four distinct actor profiles exist in TFI.")

    with tab2:
        k = st.slider("Select number of clusters (K)", 2, 7, 4)
        km_final = KMeans(n_clusters=k, random_state=42, n_init=10)
        cluster_df = cluster_df.copy()
        cluster_df["Cluster"] = km_final.fit_predict(X_scaled)

        # Cluster label naming
        cluster_means = cluster_df.groupby("Cluster")[cluster_features].mean()
        cluster_labels = {}
        for c in range(k):
            row = cluster_means.loc[c]
            if row["Success_Rate_Pct"] > 70 and row["BO_Per_Movie_Cr"] > 80:
                cluster_labels[c] = f"C{c}: Elite Performers"
            elif row["Success_Rate_Pct"] > 50 and row["Total_Movies"] > 15:
                cluster_labels[c] = f"C{c}: Consistent Stars"
            elif row["Total_Movies"] < 12 and row["Success_Rate_Pct"] > 55:
                cluster_labels[c] = f"C{c}: Rising Talents"
            else:
                cluster_labels[c] = f"C{c}: Struggling/Mid-Tier"

        cluster_df["Cluster_Label"] = cluster_df["Cluster"].map(cluster_labels)

        st.subheader("Cluster Profiles – Average Feature Values")
        profile = cluster_df.groupby("Cluster_Label")[cluster_features].mean().round(2)
        st.dataframe(profile.style.background_gradient(cmap="YlOrRd", axis=0), use_container_width=True)

        # Nepo % per cluster
        st.subheader("Background Composition per Cluster")
        bg_cluster = cluster_df.groupby(["Cluster_Label", "Background"]).size().reset_index(name="Count")
        fig_bg_c = px.bar(bg_cluster, x="Cluster_Label", y="Count", color="Background",
                           barmode="stack",
                           color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                           title="Who's in Each Cluster?")
        fig_bg_c.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                font_color=TEXT_LIGHT, title_font_color=ACCENT,
                                xaxis=dict(color=TEXT_LIGHT), yaxis=dict(color=TEXT_LIGHT))
        st.plotly_chart(fig_bg_c, use_container_width=True)

    with tab3:
        st.subheader("2D Cluster Visualisation (PCA)")
        k2 = st.slider("Clusters for map", 2, 7, 4, key="k_pca")
        km2 = KMeans(n_clusters=k2, random_state=42, n_init=10)
        labels2 = km2.fit_predict(X_scaled)

        pca = PCA(n_components=2, random_state=42)
        X_pca = pca.fit_transform(X_scaled)

        pca_df = pd.DataFrame({
            "PC1": X_pca[:, 0], "PC2": X_pca[:, 1],
            "Cluster": [f"C{l}" for l in labels2],
            "Background": cluster_df["Background"].values,
            "Name": cluster_df["Name"].values,
            "Success_Rate_Pct": cluster_df["Success_Rate_Pct"].values,
        })

        fig_pca = px.scatter(pca_df, x="PC1", y="PC2", color="Cluster",
                              symbol="Background", hover_name="Name",
                              size="Success_Rate_Pct",
                              title=f"PCA Cluster Map (K={k2}) – Symbol = Background",
                              labels={"PC1": f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var)",
                                      "PC2": f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var)"})
        fig_pca.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color=TEXT_LIGHT, title_font_color=ACCENT)
        st.plotly_chart(fig_pca, use_container_width=True)

        explained = sum(pca.explained_variance_ratio_) * 100
        insight(f"The two principal components explain **{explained:.1f}%** of total variance. "
                f"Notice how background (circle=Self-Made, diamond=Nepo) distributes across clusters — "
                f"nepo actors tend to cluster near high-opportunity, high-budget regions even when success is moderate.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 – REGRESSION ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈  Regression Analysis":
    st.title("📈 Regression Analysis")
    st.caption("What actually drives success in TFI? Let the numbers speak.")

    tab1, tab2 = st.tabs(["Linear Regression – Success Rate", "Logistic Regression – Nepo Predictor"])

    with tab1:
        st.subheader("Linear Regression: Predictors of Success Rate (%)")
        features = ["Background_Binary", "Opportunities_First_3Yrs", "Recovery_Chances_After_Flops",
                    "Debut_Budget_Cr", "Years_in_Industry", "Genre_Versatility_Score",
                    "Critical_Acclaim_Score", "OTT_Projects"]
        target = "Success_Rate_Pct"

        reg_df = fdf[features + [target]].dropna()
        X = reg_df[features]
        y = reg_df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        y_pred = lr.predict(X_test)
        r2 = r2_score(y_test, y_pred)

        col1, col2 = st.columns(2)

        with col1:
            coef_df = pd.DataFrame({
                "Feature": features,
                "Coefficient": lr.coef_,
                "Direction": ["Positive" if c > 0 else "Negative" for c in lr.coef_]
            }).sort_values("Coefficient", key=abs, ascending=False)

            fig_coef = px.bar(coef_df, x="Coefficient", y="Feature", orientation="h",
                               color="Direction",
                               color_discrete_map={"Positive": "#2ECC71", "Negative": NEPO_COLOR},
                               title=f"Regression Coefficients (R² = {r2:.3f})",
                               labels={"Feature": "", "Coefficient": "Impact on Success Rate"})
            fig_coef.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                    font_color=TEXT_LIGHT, title_font_color=ACCENT,
                                    yaxis=dict(color=TEXT_LIGHT, autorange="reversed"),
                                    xaxis=dict(color=TEXT_LIGHT), showlegend=False)
            st.plotly_chart(fig_coef, use_container_width=True)

        with col2:
            fig_pred = px.scatter(x=y_test, y=y_pred,
                                   labels={"x": "Actual Success Rate", "y": "Predicted Success Rate"},
                                   title="Actual vs Predicted Success Rate")
            fig_pred.add_shape(type="line",
                                x0=y_test.min(), y0=y_test.min(),
                                x1=y_test.max(), y1=y_test.max(),
                                line=dict(dash="dash", color=ACCENT))
            fig_pred.update_traces(marker=dict(color=SELF_COLOR, size=10))
            fig_pred.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                    font_color=TEXT_LIGHT, title_font_color=ACCENT)
            st.plotly_chart(fig_pred, use_container_width=True)

        # Equation
        intercept = lr.intercept_
        top_feature = coef_df.iloc[0]
        st.subheader("Regression Equation (Key Terms)")
        eq = f"**Success Rate = {intercept:.2f}**"
        for _, row in coef_df.head(4).iterrows():
            sign = "+" if row["Coefficient"] > 0 else ""
            eq += f" {sign} {row['Coefficient']:.2f}×{row['Feature']}"
        st.markdown(eq)

        insight(f"**Critical Acclaim Score** and **Opportunities in First 3 Years** are the top positive predictors. "
                f"Notably, 'Background_Binary' (Nepo=1) has coefficient **{coef_df[coef_df['Feature']=='Background_Binary']['Coefficient'].values[0]:.2f}** — "
                f"meaning being nepo alone does NOT add success, but the *structural advantages* (budget, recovery) it brings do.")

    with tab2:
        st.subheader("Logistic Regression: Can We Predict Background from Performance Metrics?")
        st.caption("If nepo actors had the same opportunities as self-made actors, could we tell them apart by results alone?")

        log_features = ["Success_Rate_Pct", "BO_Per_Movie_Cr", "Genre_Versatility_Score",
                        "Critical_Acclaim_Score", "Awards_Won", "Total_Movies"]
        log_target = "Background_Binary"

        log_df = fdf[log_features + [log_target]].dropna()
        Xl = log_df[log_features]
        yl = log_df[log_target]

        scaler_l = StandardScaler()
        Xl_s = scaler_l.fit_transform(Xl)

        Xl_train, Xl_test, yl_train, yl_test = train_test_split(Xl_s, yl, test_size=0.3, random_state=42)
        log_reg = LogisticRegression(random_state=42, max_iter=500)
        log_reg.fit(Xl_train, yl_train)
        yl_pred = log_reg.predict(Xl_test)

        from sklearn.metrics import confusion_matrix, accuracy_score
        acc = accuracy_score(yl_test, yl_pred)
        cm = confusion_matrix(yl_test, yl_pred)

        col1, col2 = st.columns(2)
        with col1:
            log_coef_df = pd.DataFrame({
                "Feature": log_features,
                "Coefficient": log_reg.coef_[0],
            }).sort_values("Coefficient", ascending=True)

            fig_lc = px.bar(log_coef_df, x="Coefficient", y="Feature", orientation="h",
                             title=f"Logistic Regression Coefficients (Accuracy: {acc:.2%})",
                             color="Coefficient", color_continuous_scale="RdBu")
            fig_lc.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font_color=TEXT_LIGHT, title_font_color=ACCENT,
                                  yaxis=dict(color=TEXT_LIGHT), xaxis=dict(color=TEXT_LIGHT))
            st.plotly_chart(fig_lc, use_container_width=True)

        with col2:
            cm_df = pd.DataFrame(cm, index=["Actual Self-Made", "Actual Nepo"],
                                  columns=["Pred Self-Made", "Pred Nepo"])
            fig_cm = px.imshow(cm_df, text_auto=True,
                                color_continuous_scale="Blues",
                                title="Confusion Matrix",
                                labels=dict(color="Count"))
            fig_cm.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font_color=TEXT_LIGHT, title_font_color=ACCENT)
            st.plotly_chart(fig_cm, use_container_width=True)

        insight(f"Model accuracy: **{acc:.2%}**. The model struggles to correctly classify background purely from performance — "
                f"suggesting that when evaluated on *merit alone*, nepo and self-made actors are not easily distinguishable. "
                f"The real difference lies in structural advantages, NOT inherent talent.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 – SEGMENTATION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧩  Segmentation":
    st.title("🧩 Actor Segmentation")
    st.caption("Multi-dimensional grouping: Career Stage × Background × Success Tier")

    tab1, tab2, tab3 = st.tabs(["2×2 Matrix", "Treemap", "Cohort Analysis"])

    with tab1:
        st.subheader("The Nepotism Quadrant – Success vs Opportunity")
        med_success = fdf["Success_Rate_Pct"].median()
        med_opp     = fdf["Opportunity_Index"].median()

        fdf2 = fdf.copy()
        def quadrant(row):
            hi_s = row["Success_Rate_Pct"] >= med_success
            hi_o = row["Opportunity_Index"] >= med_opp
            if hi_s and hi_o:   return "High Success\n+ High Opportunity"
            elif hi_s and not hi_o: return "High Success\n+ Low Opportunity"
            elif not hi_s and hi_o: return "Low Success\n+ High Opportunity"
            else: return "Low Success\n+ Low Opportunity"

        fdf2["Quadrant"] = fdf2.apply(quadrant, axis=1)

        fig_q = px.scatter(fdf2, x="Opportunity_Index", y="Success_Rate_Pct",
                            color="Background", symbol="Gender",
                            hover_name="Name", size="Total_BO_Collection_Cr",
                            color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                            title="Nepotism Quadrant: Success Rate vs Opportunity Index")
        fig_q.add_hline(y=med_success, line_dash="dash", line_color="#888",
                         annotation_text=f"Median Success ({med_success:.0f}%)", annotation_font_color="#888")
        fig_q.add_vline(x=med_opp, line_dash="dash", line_color="#888",
                         annotation_text=f"Median Opp ({med_opp:.1f})", annotation_font_color="#888")
        fig_q.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             font_color=TEXT_LIGHT, title_font_color=ACCENT)
        st.plotly_chart(fig_q, use_container_width=True)

        q_bg = fdf2.groupby(["Quadrant", "Background"]).size().reset_index(name="Count")
        st.dataframe(q_bg, use_container_width=True)
        insight("The **bottom-right quadrant** (Low Success + High Opportunity) is almost exclusively Nepo actors — "
                "they are sustained in the industry despite underperformance. "
                "The **top-left quadrant** (High Success + Low Opportunity) is dominated by Self-Made actors who outperformed against structural disadvantage.")

    with tab2:
        st.subheader("Career Treemap – Proportional View")
        tm_df = fdf.copy()
        tm_df["Label"] = tm_df["Name"] + "<br>(" + tm_df["Background"] + ")"
        fig_tm = px.treemap(tm_df, path=["Background", "Gender", "Career_Tier", "Name"],
                             values="Total_BO_Collection_Cr",
                             color="Success_Rate_Pct",
                             color_continuous_scale="RdYlGn",
                             title="Actor Treemap: Box Office Contribution by Background → Gender → Tier → Name",
                             hover_data=["Success_Rate_Pct", "Total_Movies"])
        fig_tm.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                              font_color=TEXT_LIGHT, title_font_color=ACCENT)
        st.plotly_chart(fig_tm, use_container_width=True)

    with tab3:
        st.subheader("Decade Debut Cohort Analysis")
        fdf3 = fdf.copy()
        fdf3["Decade"] = (fdf3["Debut_Year"] // 5 * 5).astype(str) + "s"
        cohort = fdf3.groupby(["Decade", "Background"]).agg(
            Count=("Name", "count"),
            Avg_Success=("Success_Rate_Pct", "mean"),
            Avg_BO=("Total_BO_Collection_Cr", "mean"),
            Avg_Opp=("Opportunities_First_3Yrs", "mean"),
        ).reset_index()

        col1, col2 = st.columns(2)
        with col1:
            fig_coh1 = px.line(cohort, x="Decade", y="Avg_Success", color="Background",
                                markers=True, line_dash="Background",
                                color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                                title="Avg Success Rate by Debut Era")
            fig_coh1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                    font_color=TEXT_LIGHT, title_font_color=ACCENT)
            st.plotly_chart(fig_coh1, use_container_width=True)

        with col2:
            fig_coh2 = px.bar(cohort, x="Decade", y="Count", color="Background",
                               barmode="group",
                               color_discrete_map={"Nepo": NEPO_COLOR, "Self-Made": SELF_COLOR},
                               title="Debut Counts by Era")
            fig_coh2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                    font_color=TEXT_LIGHT, title_font_color=ACCENT)
            st.plotly_chart(fig_coh2, use_container_width=True)

        insight("Post-2015 cohorts show a rising wave of Self-Made actors with competitive success rates — "
                "driven by OTT democratisation and social media reach reducing the traditional marketing moat of nepo families.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 – RAW DATA
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗂️  Raw Data":
    st.title("🗂️ Raw Dataset")
    st.caption("Full TFI Actor dataset — filterable and downloadable")

    search = st.text_input("🔍 Search by actor name")
    display_df = fdf[fdf["Name"].str.contains(search, case=False, na=False)] if search else fdf

    st.markdown(f"**Showing {len(display_df)} actors**")
    st.dataframe(
        display_df.drop(columns=["Background_Binary"], errors="ignore")
                  .set_index("Actor_ID"),
        use_container_width=True,
        height=500
    )

    # Download button
    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv,
        file_name="TFI_Nepotism_Analysis.csv",
        mime="text/csv"
    )

    xlsx_bytes = open("TFI_Nepotism_Analysis.xlsx", "rb").read()
    st.download_button(
        label="⬇️ Download as Excel",
        data=xlsx_bytes,
        file_name="TFI_Nepotism_Analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("---")
    st.subheader("📋 Column Definitions")
    definitions = {
        "Success_Rate_Pct":             "% of movies that were Hits or Blockbusters",
        "Opportunities_First_3Yrs":     "Number of films offered/completed in debut 3 years",
        "Recovery_Chances_After_Flops": "Films given after 2+ consecutive flops — key nepotism proxy",
        "Debut_Budget_Cr":              "Production budget of debut film (₹ Crore)",
        "BO_Per_Movie_Cr":              "Average box office collection per film",
        "Budget_ROI_Ratio":             "Total BO / (Avg Budget × Total Movies)",
        "Opportunity_Index":            "Composite score: Opp_First3Yrs + Recovery + Debut Budget / 10",
        "Career_Tier":                  "Superstar / A-List / Mid-Tier / Struggling — based on success rate & BO",
        "Genre_Versatility_Score":      "1–10 scale of range across genres",
        "Critical_Acclaim_Score":       "1–10 scale of critical reception quality",
        "Background_Binary":            "1 = Nepo, 0 = Self-Made (for regression)",
    }
    def_df = pd.DataFrame(list(definitions.items()), columns=["Column", "Definition"])
    st.dataframe(def_df, use_container_width=True, hide_index=True)
