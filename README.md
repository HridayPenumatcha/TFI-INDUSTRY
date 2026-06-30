# 🎬 TFI Nepotism Analysis Dashboard

> *Does your last name write your first script?*

A data-driven Streamlit dashboard analysing **nepotism vs self-made success** in the **Telugu Film Industry (TFI)**, built as part of the **SP Jain GMBA Data Analytics Course**.

---

## 📊 What's Inside

| Page | What It Shows |
|---|---|
| 🏠 Home | KPIs, industry composition, opportunity gap snapshot |
| 📊 Descriptive Stats | Distributions, box plots, correlation matrix |
| ⚔️ Nepo vs Self-Made | Radar charts, failure tolerance, hit-flop breakdown |
| 🔵 K-Means Clustering | Elbow method, silhouette scores, PCA cluster map |
| 📈 Regression Analysis | Linear regression (success drivers) + Logistic (background predictor) |
| 🧩 Segmentation | 2×2 opportunity matrix, treemap, cohort analysis |
| 🗂️ Raw Data | Full dataset, downloadable CSV/Excel |

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/tfi-nepotism-analysis.git
cd tfi-nepotism-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the dataset (first time only)
python generate_data.py

# 4. Launch the app
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (all 4 files)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set **Main file**: `app.py`
4. Click **Deploy** — the app auto-generates the Excel on first run

---

## 📁 File Structure

```
tfi-nepotism-analysis/
├── app.py                        ← Main Streamlit app (7 pages)
├── generate_data.py              ← Generates TFI_Nepotism_Analysis.xlsx
├── requirements.txt              ← Python dependencies
└── README.md                     ← This file
```

> **Note:** `TFI_Nepotism_Analysis.xlsx` is auto-generated on first run if not present.

---

## 🔬 Analytics Techniques Used

| Technique | Applied To |
|---|---|
| **K-Means Clustering** | Group actors by performance profile (K=2–7, elbow + silhouette) |
| **PCA** | 2D visualisation of high-dimensional cluster space |
| **Linear Regression** | Identify drivers of Success Rate (R² score) |
| **Logistic Regression** | Can we predict background from merit metrics alone? |
| **Segmentation** | 2×2 opportunity-success matrix, treemap, cohort analysis |
| **Descriptive Stats** | Distribution, box plots, violin plots, correlation matrix |

---

## 📌 Key Dataset Columns

| Column | Description |
|---|---|
| `Success_Rate_Pct` | % of movies that were Hits or Blockbusters |
| `Opportunities_First_3Yrs` | Films offered/completed in debut 3 years |
| `Recovery_Chances_After_Flops` | Films given after 2+ consecutive flops |
| `Debut_Budget_Cr` | Debut film budget (₹ Crore) |
| `Opportunity_Index` | Composite nepotism-proxy score |
| `Career_Tier` | Superstar / A-List / Mid-Tier / Struggling |
| `Background_Binary` | 1 = Nepo, 0 = Self-Made |

---

## 🎓 Course Context

**Subject:** Data Analytics | SP Jain School of Global Management — Global MBA  
**Key Concepts:** Clustering, Regression, Segmentation, EDA, Feature Engineering  

---

*Data is curated and estimated from publicly available sources. All figures are approximate and for academic analysis only.*
