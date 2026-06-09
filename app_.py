import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from scipy.stats import (norm, skew as sp_skew, kurtosis as sp_kurt,
                         ttest_ind, f_oneway, chi2_contingency,
                         shapiro, kstest, probplot)
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="🏡 Magicbricks Real Estate Analytics",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════
# GLOBAL CSS — NEON SPECTACULAR
# ════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
*,*::before,*::after{font-family:'Inter',sans-serif!important;}

.stApp{background:linear-gradient(135deg,#020814 0%,#030f1e 40%,#040a14 100%);}

[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#040a1a 0%,#060e25 60%,#040a1a 100%) !important;
  border-right:1px solid rgba(0,212,255,0.25) !important;
}
[data-testid="stSidebar"] *{color:#d8f0ff !important;}

h1,h2,h3,h4,h5,h6{color:#ffffff !important;}
p,li,span,td,th,div{color:#e8f2ff !important;}
.stMarkdown p{color:#e8f2ff !important;}

/* DataFrames */
.stDataFrame thead th{background:rgba(0,60,120,0.7) !important;color:#00D4FF !important;font-weight:700;}
.stDataFrame tbody tr:nth-child(even){background:rgba(0,20,50,0.4) !important;}
.stDataFrame tbody td{color:#d8f0ff !important;}

/* glass card */
.glass{
  background:rgba(0,15,40,0.7);
  backdrop-filter:blur(20px);
  border-radius:18px;
  border:1px solid rgba(0,212,255,0.2);
  padding:22px;margin-bottom:16px;
  box-shadow:0 4px 40px rgba(0,212,255,0.06);
}

/* ── KPI CARDS (5 neon variants) ── */
.kpi-box{
  position:relative;overflow:hidden;border-radius:16px;
  padding:20px 14px;text-align:center;
  background:rgba(0,8,25,0.85);
  border:1px solid rgba(255,255,255,0.08);
  transition:transform .2s,box-shadow .2s;
}
.kpi-box:hover{transform:translateY(-4px);}
.kpi-val{font-size:1.95em;font-weight:900;line-height:1.1;margin-bottom:5px;}
.kpi-lbl{font-size:.66em;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:rgba(200,230,255,0.7) !important;}

.kn .kpi-val{color:#00D4FF !important;text-shadow:0 0 28px rgba(0,212,255,.9);}
.kn{border-color:rgba(0,212,255,.4) !important;box-shadow:0 0 20px rgba(0,212,255,.12) inset,0 0 20px rgba(0,212,255,.06);}
.kp .kpi-val{color:#FF006E !important;text-shadow:0 0 28px rgba(255,0,110,.9);}
.kp{border-color:rgba(255,0,110,.4) !important;box-shadow:0 0 20px rgba(255,0,110,.12) inset,0 0 20px rgba(255,0,110,.06);}
.kg .kpi-val{color:#39FF14 !important;text-shadow:0 0 28px rgba(57,255,20,.9);}
.kg{border-color:rgba(57,255,20,.4) !important;box-shadow:0 0 20px rgba(57,255,20,.12) inset,0 0 20px rgba(57,255,20,.06);}
.kgold .kpi-val{color:#FFD700 !important;text-shadow:0 0 28px rgba(255,215,0,.9);}
.kgold{border-color:rgba(255,215,0,.4) !important;box-shadow:0 0 20px rgba(255,215,0,.12) inset,0 0 20px rgba(255,215,0,.06);}
.kv .kpi-val{color:#BF00FF !important;text-shadow:0 0 28px rgba(191,0,255,.9);}
.kv{border-color:rgba(191,0,255,.4) !important;box-shadow:0 0 20px rgba(191,0,255,.12) inset,0 0 20px rgba(191,0,255,.06);}

/* ── SECTION HEADER ── */
.sec-head{
  background:linear-gradient(90deg,rgba(0,212,255,.15),rgba(255,0,110,.06),transparent);
  border-left:4px solid #00D4FF;
  border-radius:0 10px 10px 0;
  padding:11px 18px;margin:26px 0 12px;
  font-size:1.1em;font-weight:800;color:#ffffff !important;
  letter-spacing:.02em;
  text-shadow:0 0 20px rgba(0,212,255,.4);
}

/* ── STEP / INFO BOX ── */
.step-box{
  background:rgba(0,255,100,.05);border:1px solid rgba(57,255,20,.25);
  border-left:4px solid #39FF14;border-radius:0 12px 12px 0;
  padding:15px 20px;margin:10px 0;
}
.step-box,.step-box *{color:#d4ffec !important;}

/* ── INSIGHT BOX ── */
.insight{
  background:rgba(255,200,0,.06);border:1px solid rgba(255,215,0,.3);
  border-left:4px solid #FFD700;border-radius:0 12px 12px 0;
  padding:13px 18px;margin:10px 0;
  box-shadow:0 0 20px rgba(255,200,0,.04);
}
.insight,.insight *{color:#fff8d0 !important;font-size:.93em;}

/* ── WARNING BOX ── */
.warn-box{
  background:rgba(255,0,60,.06);border:1px solid rgba(255,0,60,.3);
  border-left:4px solid #FF003C;border-radius:0 12px 12px 0;
  padding:13px 18px;margin:10px 0;
}
.warn-box,.warn-box *{color:#ffd0d0 !important;font-size:.93em;}

/* ── CODE BLOCK ── */
.code-block{
  background:rgba(0,0,0,.75);border-radius:12px;
  border:1px solid rgba(0,212,255,.2);border-left:4px solid #00D4FF;
  padding:18px 20px;font-family:'Courier New',monospace;
  font-size:12.5px;color:#7ff0ff !important;
  line-height:1.75;overflow-x:auto;white-space:pre;margin:10px 0;
}

/* ── TAKEAWAY CARDS ── */
.takeaway{
  background:rgba(0,20,50,.55);border-radius:12px;
  border:1px solid rgba(0,212,255,.12);padding:15px 20px;margin:8px 0;
  transition:border-color .3s,box-shadow .3s;
}
.takeaway:hover{border-color:rgba(0,212,255,.4);box-shadow:0 0 20px rgba(0,212,255,.07);}
.takeaway,.takeaway *{color:#e8f4ff !important;}

/* ── PILLS ── */
.pill{
  display:inline-block;
  background:linear-gradient(135deg,rgba(0,212,255,.2),rgba(191,0,255,.2));
  border:1px solid rgba(0,212,255,.4);border-radius:20px;
  padding:3px 12px;font-size:.73em;font-weight:700;
  color:#a0e8ff !important;margin:3px 2px;
}

/* ── HERO TITLE (animated gradient) ── */
.hero-title{
  font-size:2.8em;font-weight:900;
  background:linear-gradient(135deg,#00D4FF 0%,#FF006E 35%,#39FF14 65%,#FFD700 100%);
  background-size:300%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  animation:titleshift 5s ease infinite;
  line-height:1.15;margin:0;
}
@keyframes titleshift{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}

/* ── WORKFLOW CARDS ── */
.wf-card{
  background:linear-gradient(135deg,rgba(0,212,255,.08),rgba(191,0,255,.06));
  border:1px solid rgba(0,212,255,.2);border-top:3px solid #00D4FF;
  border-radius:12px;padding:16px 12px;text-align:center;
  height:130px;transition:transform .2s,box-shadow .2s;
}
.wf-card:hover{transform:translateY(-5px);box-shadow:0 8px 30px rgba(0,212,255,.15);}
.wf-card *{color:#d8f0ff !important;}

/* ── SIDEBAR BUTTONS ── */
.stButton>button{
  background:rgba(0,212,255,.06) !important;
  border:1px solid rgba(0,212,255,.15) !important;
  color:#b8ddf5 !important;border-radius:8px !important;
  transition:all .2s !important;font-size:.88em !important;
}
.stButton>button:hover{
  background:rgba(0,212,255,.16) !important;
  border-color:rgba(0,212,255,.5) !important;
  color:#ffffff !important;
  box-shadow:0 0 14px rgba(0,212,255,.25) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab"]{
  color:#88b8e0 !important;font-weight:600;font-size:.9em;
}
.stTabs [data-baseweb="tab"][aria-selected="true"]{
  color:#00D4FF !important;text-shadow:0 0 15px rgba(0,212,255,.6);
}

/* ── SELECTBOX / FILTER TEXT ── */
.stSelectbox label,.stMultiSelect label,.stSlider label{color:#a0ccee !important;}
.stSelectbox [data-baseweb="select"] *{color:#e0f4ff !important;}

#MainMenu,footer,header{visibility:hidden;}
div[data-testid="stDecoration"]{display:none;}
</style>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# DATA LOADING
# ════════════════════════════════════════════════════════════
@st.cache_data
def load_raw():
    df = pd.read_csv("magicbricks_properties.xls")
    df["Price_Cr"]       = df["Price_INR"] / 1e7
    df["Price_per_sqft"] = df["Price_INR"] / df["Area_sqft"]
    return df

@st.cache_data
def load_clean():
    df = pd.read_csv("magicbricks_properties.xls")
    df.columns = df.columns.str.lower()
    for col in ["city","title","society","furnishing","status","age","listing_url"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
    if "bathrooms" in df.columns:
        df.drop(columns=["bathrooms"], inplace=True)
    df.dropna(subset=["area_sqft","price_inr"], inplace=True)
    df = df[(df.area_sqft >= 200) & (df.area_sqft <= 10000)]
    df = df[(df.price_inr >= 500_000) & (df.price_inr <= 500_000_000)]
    df["price_per_sqft"] = df["price_inr"] / df["area_sqft"]
    df = df[(df.price_per_sqft >= 1000) & (df.price_per_sqft <= 100_000)]
    df["price_cr"] = df["price_inr"] / 1e7
    df.drop_duplicates(subset="listing_url", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

COLORS = ["#00D4FF","#FF006E","#39FF14","#FF8C00","#BF00FF","#00FFB3","#FF4040","#FFE600"]
KPI_CLS = ["kn","kp","kg","kgold","kv"]

# ════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════
def dark(fig, h=440):
    fig.update_layout(
        height=h,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,8,22,0.75)",
        font=dict(color="#d8f0ff", family="Inter", size=11),
        legend=dict(bgcolor="rgba(0,10,30,.85)", bordercolor="rgba(0,212,255,.3)",
                    borderwidth=1, font=dict(color="#d8f0ff", size=11)),
        xaxis=dict(gridcolor="rgba(0,212,255,.12)", zerolinecolor="rgba(0,212,255,.25)",
                   tickfont=dict(color="#b0d8f8"), title=dict(font=dict(color="#d8f0ff")),
                   linecolor="rgba(0,212,255,.3)"),
        yaxis=dict(gridcolor="rgba(0,212,255,.12)", zerolinecolor="rgba(0,212,255,.25)",
                   tickfont=dict(color="#b0d8f8"), title=dict(font=dict(color="#d8f0ff")),
                   linecolor="rgba(0,212,255,.3)"),
        margin=dict(l=50, r=20, t=55, b=50),
        title_font=dict(size=14, color="#ffffff"),
    )
    return fig

def dark2(fig, h=440):
    dark(fig, h)
    for i in range(1, 12):
        try:
            fig.update_layout(**{
                f"xaxis{i}": dict(gridcolor="rgba(0,212,255,.12)", tickfont=dict(color="#b0d8f8"),
                                   title=dict(font=dict(color="#d8f0ff")), linecolor="rgba(0,212,255,.25)"),
                f"yaxis{i}": dict(gridcolor="rgba(0,212,255,.12)", tickfont=dict(color="#b0d8f8"),
                                   title=dict(font=dict(color="#d8f0ff")), linecolor="rgba(0,212,255,.25)"),
            })
        except Exception:
            break
    return fig

def dark3d(fig, h=520):
    fig.update_layout(
        height=h,
        paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            bgcolor="rgba(0,5,18,0.95)",
            xaxis=dict(gridcolor="rgba(0,212,255,.18)", backgroundcolor="rgba(0,5,18,0)",
                       showbackground=True, tickfont=dict(color="#88ccee", size=10),
                       title=dict(font=dict(color="#00D4FF", size=12)),
                       zerolinecolor="rgba(0,212,255,.4)"),
            yaxis=dict(gridcolor="rgba(255,0,110,.18)", backgroundcolor="rgba(0,5,18,0)",
                       showbackground=True, tickfont=dict(color="#ffaad4", size=10),
                       title=dict(font=dict(color="#FF006E", size=12)),
                       zerolinecolor="rgba(255,0,110,.4)"),
            zaxis=dict(gridcolor="rgba(57,255,20,.18)", backgroundcolor="rgba(0,5,18,0)",
                       showbackground=True, tickfont=dict(color="#b0ffb0", size=10),
                       title=dict(font=dict(color="#39FF14", size=12)),
                       zerolinecolor="rgba(57,255,20,.4)"),
        ),
        font=dict(color="#d8f0ff", family="Inter"),
        legend=dict(bgcolor="rgba(0,10,30,.85)", bordercolor="rgba(0,212,255,.3)", borderwidth=1,
                    font=dict(color="#d8f0ff")),
        title_font=dict(size=14, color="#ffffff"),
        margin=dict(l=0, r=0, t=55, b=0),
    )
    return fig

def kpi(col, val, lbl, idx=0):
    cls = KPI_CLS[idx % 5]
    col.markdown(
        f"<div class='kpi-box {cls}'>"
        f"<div class='kpi-val'>{val}</div>"
        f"<div class='kpi-lbl'>{lbl}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

def insight(txt):
    st.markdown(f"<div class='insight'>💡 {txt}</div>", unsafe_allow_html=True)

def warn(txt):
    st.markdown(f"<div class='warn-box'>⚠️ {txt}</div>", unsafe_allow_html=True)

def sec(txt):
    st.markdown(f"<div class='sec-head'>{txt}</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ════════════════════════════════════════════════════════════
def page_overview():
    st.markdown("""
    <div style='text-align:center;padding:36px 0 20px;'>
      <div style='font-size:3.5em;margin-bottom:10px;filter:drop-shadow(0 0 20px rgba(0,212,255,.6));'>🏡</div>
      <div class='hero-title'>Magicbricks Real Estate Analytics</div>
      <p style='color:rgba(180,220,255,.75);font-size:1em;max-width:660px;margin:14px auto 0;line-height:1.7;'>
        End-to-end data science — scraping <b style='color:#00D4FF;'>5,650</b> property listings across
        <b style='color:#FF006E;'>6 cities</b> → full EDA → advanced statistics.
        Navigate via the sidebar.
      </p>
    </div>""", unsafe_allow_html=True)

    df_raw   = load_raw()
    df_clean = load_clean()

    c1,c2,c3,c4,c5 = st.columns(5)
    kpi(c1, f"{len(df_raw):,}",                    "Listings Scraped",  0)
    kpi(c2, f"{len(df_clean):,}",                  "Clean Rows",        1)
    kpi(c3, str(df_raw["City"].nunique()),          "Cities Covered",    2)
    kpi(c4, f"₹{df_clean.price_cr.median():.1f}Cr","Median Price",      3)
    kpi(c5, str(df_raw.shape[1] - 2),              "Raw Features",      4)

    sec("🗺️ Project Workflow")
    wf = [
        ("🕸️","00D4FF","1. Scrape","requests + BeautifulSoup → 5,650 listings"),
        ("🧹","FF006E","2. Clean","Filter nulls, bad ranges & duplicates"),
        ("📊","39FF14","3. EDA","14+ charts · univariate & bivariate"),
        ("🧮","FFD700","4. Adv Stats","Hypothesis tests · outliers · distribution fitting"),
        ("🚀","BF00FF","5. This App","Interactive Streamlit dashboard"),
    ]
    cols = st.columns(5)
    for col, (ico, clr, ttl, dsc) in zip(cols, wf):
        col.markdown(f"""<div class='wf-card' style='border-top-color:#{clr};'>
        <div style='font-size:1.9em;filter:drop-shadow(0 0 8px #{clr}66);'>{ico}</div>
        <div style='font-weight:800;font-size:.93em;color:#{clr} !important;margin:5px 0;'>{ttl}</div>
        <div style='font-size:.75em;opacity:.8;'>{dsc}</div>
        </div>""", unsafe_allow_html=True)

    sec("🌆 Scraped Listings by City")
    city_vc = df_raw["City"].value_counts().reset_index()
    city_vc.columns = ["City","Count"]
    fig = px.bar(city_vc, x="City", y="Count", color="City",
                 color_discrete_sequence=COLORS,
                 title="Properties Scraped per City")
    fig.update_traces(marker_line_width=0,
                      marker=dict(line=dict(width=0)),
                      textfont=dict(color="white"))
    dark(fig)
    st.plotly_chart(fig, use_container_width=True)

    sec("🔮 3D Explorer — Area × Price × BHK (colored by City)")
    sample3d = df_clean[df_clean.price_cr <= 15].sample(min(2000, len(df_clean)), random_state=42)
    fig3d = px.scatter_3d(
        sample3d, x="area_sqft", y="price_cr", z="bhk",
        color="city", color_discrete_sequence=COLORS,
        opacity=0.7, size_max=5,
        title="3D Property Space: Area vs Price vs BHK (random 2,000 sample)",
        labels={"area_sqft":"Area (sqft)","price_cr":"Price (₹ Cr)","bhk":"BHK","city":"City"},
    )
    dark3d(fig3d)
    st.plotly_chart(fig3d, use_container_width=True)
    insight("Rotate the 3D chart! Mumbai/Gurgaon (high price) cluster differently from Chennai. BHK barely separates along the price axis — city is the dominant price driver.")

    sec("💰 Price Distribution by City (Clean Data)")
    order = df_clean.groupby("city")["price_cr"].median().sort_values(ascending=False).index.tolist()
    fig2 = px.box(df_clean[df_clean.price_cr <= 15], x="city", y="price_cr",
                  color="city", color_discrete_sequence=COLORS,
                  category_orders={"city": order},
                  title="Property Price by City — capped at ₹15 Cr",
                  labels={"city":"City","price_cr":"Price (₹ Crores)"})
    dark(fig2)
    st.plotly_chart(fig2, use_container_width=True)
    insight("Mumbai is the most expensive city; Chennai is the most affordable in this dataset.")


# ════════════════════════════════════════════════════════════
# PAGE 2 — WEB SCRAPING
# ════════════════════════════════════════════════════════════
def page_scraping():
    st.markdown("<h1 style='color:#00D4FF !important;text-shadow:0 0 30px rgba(0,212,255,.5);'>🕷️ Web Scraping Process</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(180,220,255,.8);font-size:.98em;'>A beginner-friendly walkthrough of how the dataset was built from scratch.</p>", unsafe_allow_html=True)

    sec("📦 Libraries Used")
    libs = [("#00D4FF","requests","Downloads web pages\n(HTTP GET)"),
            ("#FF006E","BeautifulSoup","Parses HTML → finds\ncards & text"),
            ("#39FF14","pandas","Stores data in\na clean table"),
            ("#FFD700","re (regex)","Extracts patterns\nfrom raw text"),
            ("#BF00FF","time","Polite pauses\nbetween requests")]
    cols = st.columns(5)
    for col, (clr, name, desc) in zip(cols, libs):
        col.markdown(f"""<div style='border-top:3px solid {clr};border-radius:10px;
          background:rgba(0,10,30,.7);padding:14px;text-align:center;
          box-shadow:0 0 15px {clr}22;'>
          <div style='font-weight:800;color:{clr} !important;font-size:1em;text-shadow:0 0 10px {clr};'>{name}</div>
          <div style='font-size:.76em;color:#b8d8f0 !important;margin-top:6px;white-space:pre-line;'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    sec("⚙️ Step 1 — Settings")
    st.markdown("""<div class='code-block'>CITIES  = ["Hyderabad","Bengaluru","Pune","Chennai","Mumbai","Delhi","Gurgaon","Noida"]
PAGES_PER_CITY = 40       # try up to 40 pages per city
MAX_RECORDS    = 10_000   # stop once we have 10,000 houses
SLEEP_SECONDS  = 2        # pause 2 s between pages (polite scraping)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124..."}
URL     = "https://www.magicbricks.com/property-for-sale/residential-real-estate"
        + "?cityName={city}&page={page}"</div>""", unsafe_allow_html=True)
    insight("Why <b>User-Agent</b>? Without it many sites return 403 / empty page — the header makes us look like a real browser.")

    sec("🔍 Step 2 — Test One Page First")
    st.markdown("""<div class='code-block'>url       = URL.format(city="Hyderabad", page=1)
page_data = requests.get(url, headers=HEADERS)
soup      = BeautifulSoup(page_data.text, "html.parser")

cards = soup.find_all("div", class_="mb-srp__card")   # each card = one house
print("status:", page_data.status_code)   # 200 = OK
print("cards found:", len(cards))         # ~30 = success ✅</div>""", unsafe_allow_html=True)

    sec("🔣 Step 3 — Regex Quick Reference")
    rx_df = pd.DataFrame({
        "Symbol": [r"\d", "+", r"\s", "*", "( )", "|"],
        "Meaning": ["A digit 0–9","One or more","A space","Zero or more","Group we keep","OR"],
        "Example in project": [
            r"\d+ → matches 3, 42",
            r"\d+ matches '123', \d matches only '1'",
            r"\s* → optional space",
            r"\s* matches '' or ' '",
            r"(\d+)\s*BHK → captures '3' from '3 BHK'",
            r"Cr|Lakh matches either word",
        ]
    })
    st.dataframe(rx_df, use_container_width=True, hide_index=True)

    sec("🏷️ Step 4 — Extract Each Field")
    fields = [
        ("BHK (bedrooms)", r"""bhk = re.search(r'(\d+)\s*BHK', text)
bhk_list.append(bhk.group(1) if bhk else np.nan)"""),
        ("Area (sqft)", r"""area = re.search(r'([\d,]+)\s*sq\.?\s*ft', text)
area_list.append(area.group(1).replace(",","") if area else np.nan)"""),
        ("Price → convert to ₹", r"""price = re.search(r'₹\s*([\d,.]+)\s*(Cr|Lakh)', text)
if price:
    n = float(price.group(1).replace(",",""))
    unit = price.group(2).lower()
    price_list.append(n * 10_000_000 if unit == "cr" else n * 100_000)"""),
        ("Furnishing", r"""furnish = re.search(r'(Semi-Furnished|Unfurnished|Furnished)', text)
# longest option FIRST so 'Semi-Furnished' doesn't match as just 'Furnished'"""),
        ("Status", r"""status = re.search(r'(Ready to Move|Under Construction)', text)"""),
        ("Age", r"""age = re.search(r'(\d+\s*to\s*\d+\s*years|\d+\+?\s*years)', text)"""),
    ]
    for name, code in fields:
        st.markdown(f"<div style='font-size:.87em;font-weight:700;color:#00D4FF !important;margin:14px 0 2px;text-shadow:0 0 10px rgba(0,212,255,.5);'>→ {name}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='code-block'>{code}</div>", unsafe_allow_html=True)

    sec("💾 Step 5 — Build Table & Save")
    st.markdown("""<div class='code-block'>mb_df = pd.DataFrame({
    "City": city_list, "Title": title_list, "Society": society_list,
    "BHK": bhk_list, "Area_sqft": area_list, "Furnishing": furnish_list,
    "Status": status_list, "Age": age_list,
    "Price_INR": price_list, "Listing_URL": link_list,
})
mb_df = mb_df.drop_duplicates(subset="Listing_URL").reset_index(drop=True)
mb_df.to_csv("magicbricks_properties.xls", index=False)  # CSV despite .xls name
print("Saved:", len(mb_df), "houses")   # → 5,650 houses</div>""", unsafe_allow_html=True)
    insight("File is named <b>.xls</b> but is actually a comma-separated CSV — read it with <code>pd.read_csv()</code>, not <code>pd.read_excel()</code>.")

    sec("🎤 Interview Talking Points")
    points = [
        ("One-line summary", "Built a scraper collecting 5,650 property listings from Magicbricks across 6 cities using requests + BeautifulSoup + regex, producing a clean dataset for full EDA."),
        ("Why regex over CSS class targeting?", "Class names in website HTML change with every redesign. Words like 'BHK', 'sqft', '₹' don't — making regex more durable and maintainable."),
        ("How to be polite to a server?", "time.sleep(2) between pages. Identify with a User-Agent string. Don't hammer the server — this also reduces ban risk."),
        ("What is the biggest data quality issue?", "Bathrooms column was 98.9% null — completely unusable. Always check missing values before any analysis."),
        ("What does drop_duplicates on Listing_URL do?", "The same property can appear on multiple pages. Deduplication by URL ensures each house is counted exactly once."),
    ]
    for i, (q, a) in enumerate(points):
        colors_q = ["#00D4FF","#FF006E","#39FF14","#FFD700","#BF00FF"]
        clr = colors_q[i % 5]
        st.markdown(f"""<div class='step-box' style='border-left-color:{clr};'>
          <div style='font-weight:800;color:{clr} !important;font-size:.9em;margin-bottom:5px;'>Q: {q}</div>
          <div style='color:#d4f0e8 !important;font-size:.83em;line-height:1.6;'>{a}</div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE 3 — DATASET EXPLORER
# ════════════════════════════════════════════════════════════
def page_dataset():
    st.markdown("<h1 style='color:#FF006E !important;text-shadow:0 0 25px rgba(255,0,110,.5);'>📋 Dataset Explorer</h1>", unsafe_allow_html=True)
    df = load_clean()

    c1, c2 = st.columns([1,2])
    with c1:
        cities = ["All"] + sorted(df["city"].unique().tolist())
        sel_city = st.selectbox("Filter City", cities)
        max_p = float(df.price_cr.quantile(0.95))
        price_range = st.slider("Max Price (₹ Cr)", 0.1, max_p, max_p, 0.5)
    dff = df if sel_city == "All" else df[df.city == sel_city]
    dff = dff[dff.price_cr <= price_range]
    c2.markdown(f"""<div class='glass' style='margin-top:6px;'>
      <div style='font-size:1.1em;font-weight:700;color:#00D4FF !important;'>{len(dff):,} rows visible</div>
      <div style='font-size:.8em;color:#a0ccee !important;margin-top:4px;'>
        Price range: ₹{dff.price_cr.min():.2f}Cr – ₹{dff.price_cr.max():.2f}Cr
      </div></div>""", unsafe_allow_html=True)

    disp = dff[["city","bhk","area_sqft","price_cr","price_per_sqft","furnishing","status","age"]].head(300)
    st.dataframe(disp, use_container_width=True, hide_index=True)

    sec("📌 Column Reference")
    col_info = pd.DataFrame({
        "Column": ["city","bhk","area_sqft","price_inr","price_cr","price_per_sqft","furnishing","status","age"],
        "Type":   ["str","int","float","int","float","float","str","str","str"],
        "Meaning": [
            "City name","Bedrooms, hall, kitchen count","Area in square feet",
            "Price in rupees","Price in crores (÷ 10M)","Price ÷ area",
            "Furnished / Semi / Unfurnished","Ready to Move / Under Construction","Age of building",
        ],
    })
    st.dataframe(col_info, use_container_width=True, hide_index=True)

    sec("📊 Numeric Summary (Clean Dataset)")
    st.dataframe(df[["bhk","area_sqft","price_inr","price_per_sqft","price_cr"]].describe().round(2),
                 use_container_width=True)

    warn("98.9% of Bathrooms data is missing — column dropped during cleaning.")
    insight("Use the city and price filters above to explore any sub-segment. Prices above ₹50Cr are filtered out as extreme outliers during cleaning.")


# ════════════════════════════════════════════════════════════
# PAGE 4 — EDA UNIVARIATE
# ════════════════════════════════════════════════════════════
def page_eda_uni():
    st.markdown("<h1 style='color:#39FF14 !important;text-shadow:0 0 25px rgba(57,255,20,.5);'>📊 EDA — Univariate Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(180,255,180,.7);'>One variable at a time — what does each column look like?</p>", unsafe_allow_html=True)
    df = load_clean()
    tab_charts, tab_stats = st.tabs(["📈 Charts", "🔢 Summary Tables"])

    with tab_charts:
        sec("1️⃣ Price Distribution (₹ Crores) — capped at ₹20 Cr")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df[df.price_cr<=20]["price_cr"], nbinsx=60, name="Price",
                                   marker=dict(color=COLORS[0], opacity=0.85,
                                               line=dict(color=COLORS[0], width=0.3))))
        fig.add_vline(x=df.price_cr.mean(), line_dash="dash", line_color=COLORS[1],
                      annotation_text=f"Mean ₹{df.price_cr.mean():.1f}Cr",
                      annotation_font_color=COLORS[1])
        fig.add_vline(x=df.price_cr.median(), line_dash="dot", line_color=COLORS[2],
                      annotation_text=f"Median ₹{df.price_cr.median():.1f}Cr",
                      annotation_font_color=COLORS[2])
        fig.update_layout(title="Price Distribution — Right-skewed (mean > median)", xaxis_title="Price (₹ Cr)")
        dark(fig)
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        sec2 = lambda t: st.markdown(f"<div class='sec-head'>{t}</div>", unsafe_allow_html=True)

        with c1:
            sec("2️⃣ Area Distribution (sqft)")
            fig2 = go.Figure(go.Histogram(x=df[df.area_sqft<=6000]["area_sqft"], nbinsx=55,
                                          marker=dict(color=COLORS[1], opacity=0.85, line=dict(width=0.3))))
            fig2.update_layout(title="Area Distribution", xaxis_title="Area (sqft)")
            dark(fig2, h=340)
            c1.plotly_chart(fig2, use_container_width=True)

        with c2:
            sec("3️⃣ Price Boxplot")
            fig3 = go.Figure(go.Box(y=df[df.price_cr<=20]["price_cr"], name="Price",
                                    marker_color=COLORS[2], boxpoints="suspectedoutliers",
                                    marker_outliercolor=COLORS[1]))
            fig3.update_layout(title="Price Boxplot — Outliers Visible", yaxis_title="₹ Crores")
            dark(fig3, h=340)
            c2.plotly_chart(fig3, use_container_width=True)

        sec("4️⃣ City & BHK Frequency")
        c3, c4 = st.columns(2)
        city_vc = df.city.value_counts()
        fig4 = px.bar(x=city_vc.index, y=city_vc.values, color=city_vc.index,
                      color_discrete_sequence=COLORS, title="Listings per City",
                      labels={"x":"City","y":"Count"})
        dark(fig4, h=360)
        c3.plotly_chart(fig4, use_container_width=True)

        bhk_vc = df[df.bhk.between(1,6)].bhk.value_counts().sort_index()
        fig5 = px.bar(x=bhk_vc.index.astype(str), y=bhk_vc.values, color=bhk_vc.index.astype(str),
                      color_discrete_sequence=COLORS, title="BHK Distribution",
                      labels={"x":"BHK","y":"Count"})
        dark(fig5, h=360)
        c4.plotly_chart(fig5, use_container_width=True)

        sec("5️⃣ Furnishing & Status")
        c5, c6 = st.columns(2)
        furn_vc = df.furnishing.value_counts()
        fig6 = px.pie(names=furn_vc.index, values=furn_vc.values,
                      color_discrete_sequence=COLORS,
                      title="Furnishing Status",
                      hole=0.42)
        dark(fig6, h=360)
        c5.plotly_chart(fig6, use_container_width=True)

        stat_vc = df.status.value_counts()
        fig7 = px.pie(names=stat_vc.index, values=stat_vc.values,
                      color_discrete_sequence=[COLORS[4], COLORS[0]],
                      title="Property Status",
                      hole=0.42)
        dark(fig7, h=360)
        c6.plotly_chart(fig7, use_container_width=True)

    with tab_stats:
        sec("📋 Full Numeric Summary")
        st.dataframe(df[["bhk","area_sqft","price_inr","price_per_sqft","price_cr"]].describe().round(2),
                     use_container_width=True)
        sec("💰 Price Statistics")
        cols6 = st.columns(6)
        for i, (val, lbl) in enumerate([
            (f"₹{df.price_cr.mean():.2f}Cr","Mean"),
            (f"₹{df.price_cr.median():.2f}Cr","Median"),
            (f"₹{df.price_cr.std():.2f}Cr","Std Dev"),
            (f"₹{df.price_cr.min():.2f}Cr","Min"),
            (f"₹{df.price_cr.max():.2f}Cr","Max"),
            (f"₹{df.price_cr.quantile(.75):.2f}Cr","Q3 (75th)"),
        ]):
            kpi(cols6[i], val, lbl, i)

        sec("📐 Area Statistics")
        cols4 = st.columns(4)
        for i, (val, lbl) in enumerate([
            (f"{df.area_sqft.mean():.0f} sqft","Mean Area"),
            (f"{df.area_sqft.median():.0f} sqft","Median Area"),
            (f"{df.area_sqft.std():.0f} sqft","Std Dev"),
            (f"{int(df.bhk.mode()[0])} BHK","Most Common BHK"),
        ]):
            kpi(cols4[i], val, lbl, i)

        sec("🏙️ City Counts & Share")
        city_vc2 = df.city.value_counts()
        ct = pd.DataFrame({"City":city_vc2.index, "Count":city_vc2.values,
                           "Share (%)": (df.city.value_counts(normalize=True)*100).round(1).values})
        st.dataframe(ct.reset_index(drop=True), use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
# PAGE 5 — EDA BIVARIATE
# ════════════════════════════════════════════════════════════
def page_eda_bi():
    st.markdown("<h1 style='color:#FFD700 !important;text-shadow:0 0 25px rgba(255,215,0,.5);'>🔀 EDA — Bivariate Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,240,150,.7);'>Two variables together — discovering relationships and city-level patterns.</p>", unsafe_allow_html=True)
    df = load_clean()
    tab_charts, tab_stats = st.tabs(["📈 Charts", "🔢 Summary Tables"])

    with tab_charts:
        sec("🔮 3D Scatter — Area × Price × Price/sqft (by City)")
        sample3d = df[df.price_cr <= 15].sample(min(2500, len(df)), random_state=99)
        fig3d = px.scatter_3d(
            sample3d, x="area_sqft", y="price_cr", z="price_per_sqft",
            color="city", color_discrete_sequence=COLORS,
            opacity=0.65, size_max=6,
            title="3D View: Area vs Price vs ₹/sqft — each dot is one property",
            labels={"area_sqft":"Area (sqft)","price_cr":"Price (₹ Cr)",
                    "price_per_sqft":"₹/sqft","city":"City"},
        )
        dark3d(fig3d, h=540)
        st.plotly_chart(fig3d, use_container_width=True)
        insight("Rotate the 3D chart! Mumbai clusters at HIGH ₹/sqft, Chennai at LOW ₹/sqft. Area and total price don't separate cities — but ₹/sqft does perfectly.")

        sec("1️⃣ Area vs Price — Do Bigger Homes Cost More?")
        sample = df[df.price_cr <= 20].sample(min(2500, len(df)), random_state=42)
        fig = px.scatter(sample, x="area_sqft", y="price_cr", color="city",
                         color_discrete_sequence=COLORS, opacity=0.5,
                         trendline="ols", trendline_scope="overall",
                         title="Area vs Price — Each Dot = One Property",
                         labels={"area_sqft":"Area (sqft)","price_cr":"Price (₹ Crores)","city":"City"})
        dark(fig, h=500)
        st.plotly_chart(fig, use_container_width=True)
        insight("Area and price have weak correlation (~0.13). <b>Location (city) explains price far better than size alone.</b>")

        sec("2️⃣ Price by City")
        order = df.groupby("city")["price_cr"].median().sort_values(ascending=False).index.tolist()
        fig2 = px.box(df[df.price_cr <= 10], x="city", y="price_cr",
                      color="city", color_discrete_sequence=COLORS,
                      category_orders={"city": order},
                      title="Price Distribution by City (Capped ₹10 Cr)",
                      labels={"city":"","price_cr":"Price (₹ Crores)"})
        dark(fig2)
        st.plotly_chart(fig2, use_container_width=True)

        sec("3️⃣ Price by BHK")
        homes = df[df.bhk.between(1,6) & (df.price_cr <= 10)]
        fig3 = px.box(homes, x="bhk", y="price_cr", color="bhk",
                      color_discrete_sequence=COLORS,
                      title="Price by BHK Type",
                      labels={"bhk":"BHK","price_cr":"Price (₹ Crores)"})
        dark(fig3)
        st.plotly_chart(fig3, use_container_width=True)
        insight("Price increases with BHK, but with high variance — a 4BHK in Chennai can be cheaper than a 2BHK in Mumbai.")

        sec("4️⃣ Median ₹/sqft by City — Fairest Comparison")
        psf = df.groupby("city")["price_per_sqft"].median().sort_values(ascending=False).reset_index()
        psf.columns = ["city","median_psf"]
        fig4 = px.bar(psf, x="city", y="median_psf", color="city",
                      color_discrete_sequence=COLORS,
                      title="Median ₹/sqft by City — removes size bias",
                      labels={"city":"","median_psf":"Median ₹/sqft"})
        dark(fig4)
        st.plotly_chart(fig4, use_container_width=True)

        sec("5️⃣ Correlation Heatmap")
        corr = df[["bhk","area_sqft","price_inr","price_per_sqft"]].corr().round(2)
        fig5 = px.imshow(corr, text_auto=True,
                         color_continuous_scale=["#FF006E","#111827","#00D4FF"],
                         zmin=-1, zmax=1, title="Pearson Correlation Heatmap",
                         labels=dict(color="r"))
        dark(fig5, h=420)
        st.plotly_chart(fig5, use_container_width=True)

    with tab_stats:
        sec("🌆 City Summary")
        city_s = (df.groupby("city")[["price_cr","price_per_sqft"]]
                    .median().round(2).sort_values("price_cr", ascending=False).reset_index())
        city_s.columns = ["City","Median Price (₹ Cr)","Median ₹/sqft"]
        st.dataframe(city_s, use_container_width=True, hide_index=True)

        sec("🛏️ BHK Summary")
        bhk_s = (df[df.bhk.between(1,6)].groupby("bhk")[["price_cr","area_sqft"]]
                   .mean().round(2).reset_index())
        bhk_s.columns = ["BHK","Avg Price (₹ Cr)","Avg Area (sqft)"]
        st.dataframe(bhk_s, use_container_width=True, hide_index=True)

        sec("🔗 Correlation Matrix")
        corr2 = df[["bhk","area_sqft","price_inr","price_per_sqft"]].corr().round(3)
        st.dataframe(corr2, use_container_width=True)
        insight(f"BHK ↔ Area = {corr2.loc['bhk','area_sqft']:.2f} (strong). Area ↔ Price = {corr2.loc['area_sqft','price_inr']:.2f} (very weak).")

        sec("🏙️ City × Status Cross-tab")
        ctab = pd.crosstab(df["city"], df["status"])
        st.dataframe(ctab, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 6 — BASIC STATISTICS
# ════════════════════════════════════════════════════════════
def page_adv_basic():
    st.markdown("<h1 style='color:#BF00FF !important;text-shadow:0 0 25px rgba(191,0,255,.5);'>📈 Basic Statistics</h1>", unsafe_allow_html=True)
    df    = load_raw()
    price = df["Price_Cr"].dropna()
    area  = df["Area_sqft"].dropna()

    mean_p = price.mean(); med_p = price.median(); mode_p = price.mode()[0]
    std_p  = price.std();  var_p = price.var();   cv_p  = std_p/mean_p*100

    sec("💰 Price Statistics (₹ Crores) — Full Dataset (5,650 rows)")
    cols6 = st.columns(6)
    for i, (val, lbl) in enumerate([
        (f"₹{mean_p:.2f}Cr","Mean"),
        (f"₹{med_p:.2f}Cr","Median"),
        (f"₹{mode_p:.2f}Cr","Mode"),
        (f"₹{std_p:.2f}Cr","Std Dev"),
        (f"{var_p:.2f}","Variance"),
        (f"{cv_p:.1f}%","CV (spread %)"),
    ]):
        kpi(cols6[i], val, lbl, i)
    insight(f"Mean ₹{mean_p:.2f}Cr >> Median ₹{med_p:.2f}Cr → strongly right-skewed. The median is the honest 'typical price'.")

    price_plot = price[price <= 20]
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=price_plot, nbinsx=60, name="Price Distribution",
                               marker=dict(color=COLORS[0], opacity=0.85, line=dict(width=0.3))))
    for val, lbl, clr in [
        (mean_p, f"Mean ₹{mean_p:.1f}Cr", COLORS[1]),
        (med_p,  f"Median ₹{med_p:.1f}Cr", COLORS[2]),
        (mode_p, f"Mode ₹{mode_p:.1f}Cr",  COLORS[3]),
    ]:
        fig.add_vline(x=val, line_dash="dash", line_color=clr,
                      annotation_text=lbl, annotation_font_color=clr, annotation_font_size=12)
    fig.update_layout(title="Price Distribution — Mean, Median & Mode",
                      xaxis_title="Price (₹ Crores)", yaxis_title="Number of Homes")
    dark(fig)
    st.plotly_chart(fig, use_container_width=True)

    sec("📐 Area Statistics (sqft)")
    cols4 = st.columns(4)
    for i, (val, lbl) in enumerate([
        (f"{area.mean():.0f} sqft","Mean"),
        (f"{area.median():.0f} sqft","Median"),
        (f"{area.std():.0f} sqft","Std Dev"),
        (f"{area.mode()[0]:.0f} sqft","Mode"),
    ]):
        kpi(cols4[i], val, lbl, i)

    sec("📚 Stat Reference Dictionary")
    stat_ref = pd.DataFrame({
        "Term":     ["Mean","Median","Mode","Variance","Std Deviation","CV"],
        "Meaning":  ["Sum ÷ count","Middle value when sorted","Most frequent value",
                     "Average squared deviation","√Variance (same unit as data)","(σ/μ)×100"],
        "Formula":  ["Σx/n","Middle of sorted list","Most frequent","Σ(x−μ)²/n","√Variance","(σ/μ)×100"],
        "Best for": ["Normal data","Skewed data like price","Categorical frequency",
                     "Intermediate calc","Typical deviation","Comparing columns"],
    })
    st.dataframe(stat_ref, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
# PAGE 7 — 5-NUMBER SUMMARY
# ════════════════════════════════════════════════════════════
def page_adv_5num():
    st.markdown("<h1 style='color:#00FFB3 !important;text-shadow:0 0 25px rgba(0,255,179,.5);'>📦 Five-Number Summary & IQR</h1>", unsafe_allow_html=True)
    df    = load_raw()
    price = df["Price_Cr"].dropna()
    area  = df["Area_sqft"].dropna()

    st.markdown("""<div class='insight'>
    <b>Five-Number Summary:</b>  Min ── Q1(25%) ── Median(50%) ── Q3(75%) ── Max<br>
    <b>IQR</b> = Q3 − Q1 (middle 50% spread, resistant to outliers)<br>
    <b>Outlier fences:</b>  Lower = Q1 − 1.5×IQR  |  Upper = Q3 + 1.5×IQR
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    for col, (series, name, unit) in [(c1,(price,"Price","₹ Cr")), (c2,(area,"Area","sqft"))]:
        q1 = series.quantile(0.25); q3 = series.quantile(0.75); iqr = q3-q1
        lf = q1 - 1.5*iqr; uf = q3 + 1.5*iqr
        summary_df = pd.DataFrame({
            "Statistic": ["Min","Q1 (25th)","Median (50th)","Q3 (75th)","Max",
                          "IQR","Lower Fence","Upper Fence"],
            "Value": [
                f"{series.min():.2f} {unit}", f"{q1:.2f} {unit}",
                f"{series.median():.2f} {unit}", f"{q3:.2f} {unit}",
                f"{series.max():.2f} {unit}", f"{iqr:.2f} {unit}",
                f"{lf:.2f} {unit}", f"{uf:.2f} {unit}",
            ],
        })
        col.markdown(f"<div class='sec-head'>📦 {name} ({unit})</div>", unsafe_allow_html=True)
        col.dataframe(summary_df, use_container_width=True, hide_index=True)

    sec("📏 Price Percentile Table")
    pcts = [10,20,25,30,40,50,60,70,75,80,90,95,99]
    pct_tbl = pd.DataFrame({
        "Percentile": [f"{p}th" for p in pcts],
        "Price (₹ Cr)": [f"₹{price.quantile(p/100):.2f} Cr" for p in pcts],
        "Interpretation": [f"{100-p}% of homes cost more" for p in pcts],
    })
    st.dataframe(pct_tbl, use_container_width=True, hide_index=True)

    sec("📊 Boxplot Visual — Five-Number Summary")
    fig = make_subplots(rows=1, cols=2, subplot_titles=["Price (₹ Crores)","Area (sqft)"])
    fig.add_trace(go.Box(y=price[price<=30], name="Price", marker_color=COLORS[0],
                         boxpoints="suspectedoutliers",
                         marker_outliercolor=COLORS[1],
                         fillcolor="rgba(0,212,255,0.15)"), row=1, col=1)
    fig.add_trace(go.Box(y=area[area<=8000], name="Area", marker_color=COLORS[2],
                         boxpoints="suspectedoutliers",
                         marker_outliercolor=COLORS[3],
                         fillcolor="rgba(57,255,20,0.15)"), row=1, col=2)
    dark2(fig)
    st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 8 — DISTRIBUTIONS
# ════════════════════════════════════════════════════════════
def page_adv_dist():
    st.markdown("<h1 style='color:#FF8C00 !important;text-shadow:0 0 25px rgba(255,140,0,.5);'>📉 Data Distributions</h1>", unsafe_allow_html=True)
    df = load_raw()

    datasets = [
        (df["Price_Cr"][df["Price_Cr"]<=30].dropna(),                       "Price (₹ Crores)",  COLORS[0]),
        (df["Area_sqft"][df["Area_sqft"]<=8000].dropna(),                   "Area (sqft)",       COLORS[2]),
        (df["BHK"].dropna(),                                                  "BHK Count",         COLORS[3]),
        (df["Price_per_sqft"][df["Price_per_sqft"].between(0,50000)].dropna(),"Price per sqft (₹)",COLORS[4]),
    ]

    sec("📊 Four Key Variable Distributions")
    c1, c2 = st.columns(2)
    for i, (data, title, color) in enumerate(datasets):
        col = c1 if i % 2 == 0 else c2
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=data, nbinsx=45, name=title,
                                   marker=dict(color=color, opacity=0.85, line=dict(width=0.3))))
        fig.add_vline(x=data.mean(), line_dash="dash", line_color=COLORS[1],
                      annotation_text="Mean", annotation_font_color=COLORS[1], annotation_font_size=11)
        fig.add_vline(x=data.median(), line_dash="dot", line_color="white",
                      annotation_text="Median", annotation_font_color="white", annotation_font_size=11)
        fig.update_layout(title=title, xaxis_title=title, yaxis_title="Count")
        dark(fig, h=340)
        col.plotly_chart(fig, use_container_width=True)

    insight("Price & Area: Mean > Median → right-skewed. BHK is roughly symmetric. Price/sqft is right-skewed — Mumbai's extreme values create the long tail.")

    sec("📊 Skewness Reference")
    skew_ref = pd.DataFrame({
        "Distribution": ["Normal (BHK ≈)","Right-Skewed (Price ✓)","Left-Skewed (rare)"],
        "Shape": ["Symmetric bell","Long right tail","Long left tail"],
        "Mean vs Median": ["Mean ≈ Median","Mean > Median","Mean < Median"],
        "Example": ["Height of adults","Property prices","Exam scores (easy test)"],
    })
    st.dataframe(skew_ref, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
# PAGE 9 — BOXPLOTS
# ════════════════════════════════════════════════════════════
def page_adv_boxplots():
    st.markdown("<h1 style='color:#00D4FF !important;text-shadow:0 0 25px rgba(0,212,255,.5);'>📦 Boxplots & Spread</h1>", unsafe_allow_html=True)
    df = load_clean()

    sec("1️⃣ Price by City (capped ₹20 Cr)")
    order = df.groupby("city")["price_cr"].median().sort_values(ascending=False).index.tolist()
    fig = px.box(df[df.price_cr<=20], x="city", y="price_cr", color="city",
                 color_discrete_sequence=COLORS, category_orders={"city":order},
                 title="Price Distribution by City",
                 labels={"city":"City","price_cr":"Price (₹ Cr)"})
    dark(fig, h=460)
    st.plotly_chart(fig, use_container_width=True)

    sec("2️⃣ Price by BHK")
    homes = df[df.bhk.between(1,6) & (df.price_cr<=12)]
    fig2 = px.box(homes, x="bhk", y="price_cr", color="bhk",
                  color_discrete_sequence=COLORS,
                  title="Price by BHK Count",
                  labels={"bhk":"BHK","price_cr":"Price (₹ Cr)"})
    dark(fig2)
    st.plotly_chart(fig2, use_container_width=True)
    insight("Each extra bedroom adds price, but with wide variance — a studio in Mumbai can be pricier than a 4BHK in Chennai.")

    sec("3️⃣ Price per sqft by City — Violin + Box")
    fig3 = px.violin(df[df.price_per_sqft<=25000], x="city", y="price_per_sqft",
                     color="city", color_discrete_sequence=COLORS,
                     category_orders={"city":order}, box=True,
                     title="₹/sqft Distribution by City — Violin shows full shape",
                     labels={"city":"","price_per_sqft":"₹ per sqft"})
    dark(fig3, h=500)
    st.plotly_chart(fig3, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 10 — CATEGORICAL ANALYSIS
# ════════════════════════════════════════════════════════════
def page_adv_cat():
    st.markdown("<h1 style='color:#FF006E !important;text-shadow:0 0 25px rgba(255,0,110,.5);'>🗂️ Categorical Analysis</h1>", unsafe_allow_html=True)
    df = load_clean()

    cats = [
        ("city","City","Listings by City"),
        ("furnishing","Furnishing Type","Furnishing Distribution"),
        ("status","Property Status","Status Distribution"),
    ]
    for cat, label, title in cats:
        sec(f"📊 {title}")
        vc = df[cat].value_counts().reset_index()
        vc.columns = [label,"Count"]
        fig = px.bar(vc, y=label, x="Count", orientation="h", color=label,
                     color_discrete_sequence=COLORS, title=title,
                     labels={label:label,"Count":"Number of Listings"})
        dark(fig, h=320)
        st.plotly_chart(fig, use_container_width=True)

    sec("📊 BHK Distribution")
    bhk_vc = df[df.bhk.between(1,6)].bhk.value_counts().sort_index().reset_index()
    bhk_vc.columns = ["BHK","Count"]
    fig_bhk = px.bar(bhk_vc, x="BHK", y="Count", color="BHK",
                     color_discrete_sequence=COLORS, title="BHK Distribution",
                     labels={"BHK":"BHK","Count":"Count"})
    dark(fig_bhk, h=340)
    st.plotly_chart(fig_bhk, use_container_width=True)

    sec("🌆 City — Median Price (₹ Cr)")
    city_med = df.groupby("city")["price_cr"].median().sort_values(ascending=False).reset_index()
    city_med.columns = ["City","Median Price (₹ Cr)"]
    fig_med = px.bar(city_med, x="City", y="Median Price (₹ Cr)", color="City",
                     color_discrete_sequence=COLORS, title="Median Price by City",
                     text_auto=".1f")
    dark(fig_med, h=380)
    st.plotly_chart(fig_med, use_container_width=True)

    sec("📋 City Stats Table")
    city_stats = (df.groupby("city")[["price_cr","price_per_sqft","area_sqft"]]
                    .agg(["median","mean"]).round(2))
    city_stats.columns = ["Med Price Cr","Avg Price Cr","Med ₹/sqft","Avg ₹/sqft","Med Area","Avg Area"]
    st.dataframe(city_stats.reset_index(), use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 11 — MISSING VALUES
# ════════════════════════════════════════════════════════════
def page_adv_missing():
    st.markdown("<h1 style='color:#39FF14 !important;text-shadow:0 0 25px rgba(57,255,20,.5);'>❓ Missing Values Analysis</h1>", unsafe_allow_html=True)
    df = load_raw()

    miss = df.isnull().sum()
    miss_pct = (df.isnull().mean()*100).round(2)
    miss_df = pd.DataFrame({
        "Column": miss.index,
        "Missing": miss.values,
        "Missing %": miss_pct.values,
        "Status": ["🔴 Unusable" if p > 50 else "🟡 Investigate" if p > 5 else "🟢 OK"
                   for p in miss_pct.values],
    }).sort_values("Missing %", ascending=False)
    st.dataframe(miss_df, use_container_width=True, hide_index=True)

    sec("📊 Missing % by Column")
    miss_show = miss_df[miss_df["Missing %"] > 0]
    fig = px.bar(miss_show, x="Column", y="Missing %", color="Missing %",
                 color_continuous_scale=["#39FF14","#FFD700","#FF006E"],
                 title="Missing Data Percentage by Column",
                 labels={"Column":"Column","Missing %":"Missing (%)"})
    dark(fig, h=380)
    st.plotly_chart(fig, use_container_width=True)

    sec("🗺️ Missing Value Heatmap (first 200 rows)")
    sample_200 = df.head(200).isnull().astype(int)
    fig2 = px.imshow(sample_200.T,
                     color_continuous_scale=["rgba(0,8,22,0.9)","#FF006E"],
                     title="Missing = Pink | Present = Dark  (first 200 rows)",
                     labels=dict(color="Missing"))
    dark(fig2, h=380)
    st.plotly_chart(fig2, use_container_width=True)

    sec("🧹 Missing Value Handling Strategy")
    strat = pd.DataFrame({
        "Column": ["Bathrooms","Age","Furnishing","Status","BHK","Area_sqft","Price_INR"],
        "% Missing": ["98.9%","~15%","~5%","~5%","<1%","<1%","<1%"],
        "Action": ["Drop column","Keep as string category","Keep as 'unknown'",
                   "Keep as 'unknown'","Drop row","Drop row","Drop row"],
        "Reason": [
            "Almost no data — useless for analysis",
            "Age stored as text range ('5 to 10 years') — useful as category",
            "Known categories; NaN kept as own class",
            "Known categories; NaN kept as own class",
            "Essential feature — cannot impute",
            "Essential feature — cannot impute",
            "Essential target — cannot impute",
        ],
    })
    st.dataframe(strat, use_container_width=True, hide_index=True)
    warn("Never impute (fill in) target variables like Price — you'd be making up the answer you're trying to predict.")


# ════════════════════════════════════════════════════════════
# PAGE 12 — CORRELATION
# ════════════════════════════════════════════════════════════
def page_adv_corr():
    st.markdown("<h1 style='color:#BF00FF !important;text-shadow:0 0 25px rgba(191,0,255,.5);'>🔗 Correlation Analysis</h1>", unsafe_allow_html=True)
    df = load_clean()
    corr = df[["bhk","area_sqft","price_inr","price_per_sqft"]].corr().round(3)

    c1, c2 = st.columns([1,1])
    with c1:
        sec("📊 2D Correlation Heatmap")
        fig = px.imshow(corr, text_auto=True,
                        color_continuous_scale=["#FF006E","#0a0f2a","#00D4FF"],
                        zmin=-1, zmax=1, title="Pearson Correlation Matrix")
        dark(fig, h=400)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        sec("🔮 3D Correlation Surface")
        cols_list = ["bhk","area_sqft","price_inr","price_per_sqft"]
        z_vals = corr.values
        fig3d = go.Figure(data=[go.Surface(
            z=z_vals,
            x=cols_list,
            y=cols_list,
            colorscale=[[0,"#FF006E"],[0.5,"#0a0f2a"],[1,"#00D4FF"]],
            cmin=-1, cmax=1,
            showscale=True,
            contours=dict(
                z=dict(show=True, usecolormap=True, highlightcolor="#00D4FF", project_z=True)
            ),
        )])
        fig3d.update_layout(
            title="3D Correlation Surface — peaks = strong correlation",
            scene=dict(
                bgcolor="rgba(0,5,18,.95)",
                xaxis=dict(tickvals=list(range(4)), ticktext=cols_list,
                           tickfont=dict(color="#88ccee", size=9),
                           gridcolor="rgba(0,212,255,.15)", backgroundcolor="rgba(0,5,18,0)",
                           showbackground=True, title=dict(font=dict(color="#00D4FF"))),
                yaxis=dict(tickvals=list(range(4)), ticktext=cols_list,
                           tickfont=dict(color="#ffaad4", size=9),
                           gridcolor="rgba(255,0,110,.15)", backgroundcolor="rgba(0,5,18,0)",
                           showbackground=True, title=dict(font=dict(color="#FF006E"))),
                zaxis=dict(range=[-1,1], tickfont=dict(color="#b0ffb0", size=9),
                           gridcolor="rgba(57,255,20,.15)", backgroundcolor="rgba(0,5,18,0)",
                           showbackground=True,
                           title=dict(text="r (correlation)", font=dict(color="#39FF14"))),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#d8f0ff"),
            margin=dict(l=0, r=0, t=50, b=0),
            height=420,
        )
        st.plotly_chart(fig3d, use_container_width=True)

    sec("🔍 Scatter: Area vs Price (size = BHK, color = City)")
    sample = df[df.price_cr<=20].dropna(subset=["bhk","area_sqft","price_cr"]).copy()
    sample["bhk"] = sample["bhk"].astype(float).fillna(1).clip(lower=1)
    sample = sample.sample(min(2000, len(sample)), random_state=42)
    fig2 = px.scatter(sample, x="area_sqft", y="price_cr",
                      size_max=14, trendline="ols",
                      title="Area vs Price — BHK as dot size, City as color",
                      labels={"area_sqft":"Area (sqft)","price_cr":"Price (₹ Cr)","city":"City","bhk":"BHK"})
    dark(fig2, h=500)
    st.plotly_chart(fig2, use_container_width=True)

    sec("📋 Correlation Findings")
    findings = pd.DataFrame({
        "Pair": ["BHK ↔ Area","Area ↔ Price","BHK ↔ Price","Price ↔ ₹/sqft"],
        "r value": [f"{corr.loc['bhk','area_sqft']:.3f}",
                    f"{corr.loc['area_sqft','price_inr']:.3f}",
                    f"{corr.loc['bhk','price_inr']:.3f}",
                    f"{corr.loc['price_inr','price_per_sqft']:.3f}"],
        "Strength": ["Strong positive","Very weak positive","Weak positive","Moderate positive"],
        "Interpretation": [
            "More bedrooms = bigger home (expected)",
            "Area barely predicts price — city dominates",
            "More bedrooms = slightly higher price (many confounders)",
            "Higher price = higher ₹/sqft (city drives both)",
        ],
    })
    st.dataframe(findings, use_container_width=True, hide_index=True)
    insight("The weak Area↔Price correlation (~0.13) is the biggest insight — it means <b>location, not size, drives real estate prices</b> in Indian metros.")


# ════════════════════════════════════════════════════════════
# PAGE 13 — SKEWNESS & KURTOSIS
# ════════════════════════════════════════════════════════════
def page_adv_skew():
    st.markdown("<h1 style='color:#FFD700 !important;text-shadow:0 0 25px rgba(255,215,0,.5);'>↗️ Skewness & Kurtosis</h1>", unsafe_allow_html=True)
    df    = load_raw()
    price = df["Price_Cr"].dropna()

    sec("📋 Skewness & Kurtosis Table — All Numeric Columns")
    rows = []
    for col in ["Price_Cr","Area_sqft","BHK","Price_per_sqft"]:
        s  = df[col].dropna()
        sk = sp_skew(s); ku = sp_kurt(s, fisher=True)
        if   abs(sk) < 0.5: shape = "🔔 Approx Normal"
        elif sk > 1:          shape = "➡️ Strong Right Skew"
        elif sk > 0:          shape = "↗️ Mild Right Skew"
        elif sk < -1:         shape = "⬅️ Strong Left Skew"
        else:                 shape = "↙️ Mild Left Skew"
        rows.append({"Column":col,"Skewness":round(sk,2),"Kurtosis (excess)":round(ku,2),"Shape":shape})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    sec("📖 Reference Tables")
    c1, c2 = st.columns(2)
    c1.dataframe(pd.DataFrame({
        "Skewness Value":["≈ 0","> 0","< 0","Price_Cr = ?"],
        "Meaning":["Symmetric","Right tail longer","Left tail longer",
                   f"= {sp_skew(price):.0f} → extreme right skew!"],
    }), use_container_width=True, hide_index=True)
    c2.dataframe(pd.DataFrame({
        "Kurtosis":["≈ 0","> 0","< 0"],
        "Name":["Normal","Leptokurtic","Platykurtic"],
        "Shape":["Bell-shaped","Sharp peak, heavy tails","Flat, thin tails"],
    }), use_container_width=True, hide_index=True)

    sec("📊 Price vs Normal Curve + Q-Q Plot")
    price_cap = price[price <= 15]
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=["Price vs Fitted Normal","Q-Q Plot (Price vs Normal)"])
    fig.add_trace(go.Histogram(x=price_cap, nbinsx=55, histnorm="probability density",
                               name="Actual Price",
                               marker=dict(color=COLORS[0], opacity=0.75, line=dict(width=0.3))),
                  row=1, col=1)
    x_line = np.linspace(price_cap.min(), price_cap.max(), 300)
    fig.add_trace(go.Scatter(x=x_line, y=norm.pdf(x_line, price_cap.mean(), price_cap.std()),
                             mode="lines", name="Normal Curve",
                             line=dict(color=COLORS[1], width=2.5, dash="dash")), row=1, col=1)
    result = probplot(price_cap, dist="norm")
    th_q, sm_q = result[0][0], result[0][1]
    slope, intercept = result[1][0], result[1][1]
    fig.add_trace(go.Scatter(x=th_q, y=sm_q, mode="markers", name="Data",
                             marker=dict(color=COLORS[0], size=3, opacity=0.5)), row=1, col=2)
    fig.add_trace(go.Scatter(x=th_q, y=slope*np.array(th_q)+intercept,
                             mode="lines", name="Normal Line",
                             line=dict(color=COLORS[1], width=2)), row=1, col=2)
    dark2(fig, h=440)
    st.plotly_chart(fig, use_container_width=True)
    insight("Left: actual price is far from bell-shaped. Right (Q-Q): curved deviation confirms price is NOT Normal — it follows Log-Normal instead.")


# ════════════════════════════════════════════════════════════
# PAGE 14 — OUTLIER DETECTION
# ════════════════════════════════════════════════════════════
def page_adv_outliers():
    st.markdown("<h1 style='color:#FF4040 !important;text-shadow:0 0 25px rgba(255,64,64,.6);'>🎯 Outlier Detection</h1>", unsafe_allow_html=True)
    df    = load_raw()
    price = df["Price_Cr"].dropna()

    q1, q3 = price.quantile(0.25), price.quantile(0.75)
    iqr = q3 - q1; lf = q1 - 1.5*iqr; uf = q3 + 1.5*iqr
    iqr_out = df[(df["Price_Cr"] < lf) | (df["Price_Cr"] > uf)]
    z_scores = np.abs(stats.zscore(price))
    z_out    = price[z_scores > 3]
    med_p    = price.median()
    mad      = np.median(np.abs(price - med_p))
    mod_z    = 0.6745 * (price - med_p) / mad
    mz_out   = price[np.abs(mod_z) > 3.5]

    sec("📋 Three Outlier Methods — Comparison")
    comp_df = pd.DataFrame({
        "Method":     ["IQR Fence","Z-Score (|z|>3)","Modified Z-Score (|mz|>3.5)"],
        "Criterion":  [f"Outside ₹{lf:.2f}Cr – ₹{uf:.2f}Cr",
                       f"Mean±3σ → ₹{price.mean()-3*price.std():.1f}Cr – ₹{price.mean()+3*price.std():.1f}Cr",
                       "Uses Median+MAD (robust to outliers)"],
        "# Outliers": [f"{len(iqr_out):,}",f"{len(z_out):,}",f"{len(mz_out):,}"],
        "% Outliers": [f"{len(iqr_out)/len(price)*100:.1f}%",
                       f"{len(z_out)/len(price)*100:.1f}%",
                       f"{len(mz_out)/len(price)*100:.1f}%"],
        "Robustness": ["Medium","Low — inflated by very outliers it finds","High ✅ (recommended)"],
    })
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    c1,c2,c3 = st.columns(3)
    kpi(c1, f"{len(iqr_out):,}", f"IQR Outliers (>{uf:.1f}Cr)", 0)
    kpi(c2, f"{len(z_out):,}",   "Z-Score Outliers",             1)
    kpi(c3, f"{len(mz_out):,}",  "Mod Z-Score Outliers",         2)

    sec("🔮 3D Outlier Space — Area × Price × ₹/sqft")
    df_valid = df[["City","Area_sqft","Price_Cr","Price_per_sqft"]].dropna()
    df_valid = df_valid[(df_valid.Price_Cr <= 50) & (df_valid.Price_per_sqft <= 80000)]
    is_outlier = (df_valid["Price_Cr"] > uf).astype(str).map({"True":"🔴 Outlier","False":"🟢 Normal"})
    df_valid = df_valid.copy()
    df_valid["Outlier"] = is_outlier
    sample_3d = df_valid.sample(min(2000, len(df_valid)), random_state=7)
    fig3d = px.scatter_3d(
        sample_3d, x="Area_sqft", y="Price_Cr", z="Price_per_sqft",
        color="Outlier",
        color_discrete_map={"🔴 Outlier": "#FF4040", "🟢 Normal": "#00D4FF"},
        opacity=0.7,
        title=f"3D Outlier Detection (IQR method — threshold ₹{uf:.1f}Cr) — Red = outlier",
        labels={"Area_sqft":"Area (sqft)","Price_Cr":"Price (₹ Cr)","Price_per_sqft":"₹/sqft"},
    )
    dark3d(fig3d, h=540)
    st.plotly_chart(fig3d, use_container_width=True)
    insight("Rotate the 3D! Red outliers cluster at the top — high price AND high ₹/sqft. These are mostly luxury Mumbai/Gurgaon properties.")

    sec("📊 2D Outlier Visualisation")
    fig = make_subplots(rows=1, cols=3, subplot_titles=["IQR Boxplot","|Z-Score| Distribution","Modified Z-Score"])
    fig.add_trace(go.Box(y=price, name="Price", marker_color=COLORS[0],
                         boxpoints="suspectedoutliers",
                         marker_outliercolor=COLORS[1]), row=1, col=1)
    fig.add_trace(go.Histogram(x=z_scores, nbinsx=60, name="|Z-Score|",
                               marker=dict(color=COLORS[2], opacity=0.82, line=dict(width=0.3))), row=1, col=2)
    fig.add_vline(x=3, line_dash="dash", line_color=COLORS[1],
                  annotation_text="z=3", annotation_font_color=COLORS[1], row=1, col=2)
    fig.add_trace(go.Histogram(x=mod_z, nbinsx=60, name="Mod Z",
                               marker=dict(color=COLORS[3], opacity=0.82, line=dict(width=0.3))), row=1, col=3)
    fig.add_vline(x=3.5,  line_dash="dash", line_color=COLORS[1], row=1, col=3)
    fig.add_vline(x=-3.5, line_dash="dash", line_color=COLORS[1], row=1, col=3)
    dark2(fig)
    st.plotly_chart(fig, use_container_width=True)
    insight("Modified Z-Score is most robust — uses Median & MAD instead of Mean & Std, which are themselves inflated by the outliers you're trying to find.")

    sec("🔝 Top 10 Most Expensive Outliers")
    top_out = (df[df["Price_Cr"] > uf][["City","Title","BHK","Area_sqft","Price_Cr"]]
               .sort_values("Price_Cr", ascending=False).head(10))
    st.dataframe(top_out, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
# PAGE 15 — DISTRIBUTION FITTING
# ════════════════════════════════════════════════════════════
def page_adv_fit():
    st.markdown("<h1 style='color:#00FFB3 !important;text-shadow:0 0 25px rgba(0,255,179,.5);'>🔮 Distribution Fitting</h1>", unsafe_allow_html=True)
    df    = load_raw()
    price = df["Price_Cr"].dropna()

    st.markdown("""<div class='insight'>
    Can we describe our data using a known mathematical formula?
    We test <b>Normal</b> and <b>Log-Normal</b> distributions using statistical tests.
    </div>""", unsafe_allow_html=True)

    sample = price.sample(min(500, len(price)), random_state=42)
    stat_sw, p_sw = shapiro(sample)
    log_price  = np.log(price[price > 0])
    std_log    = (log_price - log_price.mean()) / log_price.std()
    stat_ks, p_ks = kstest(std_log, "norm")

    sec("🔬 Statistical Normality Tests")
    c1, c2 = st.columns(2)
    c1.markdown(f"""<div class='step-box'>
      <div style='font-weight:800;font-size:.97em;color:#00D4FF !important;'>Shapiro-Wilk Test (n=500 sample)</div>
      <div style='margin-top:8px;'>H₀: Data is normally distributed</div>
      <div style='margin-top:4px;'>W-statistic: <b>{stat_sw:.4f}</b></div>
      <div>p-value: <b>{p_sw:.6f}</b></div>
      <div style='margin-top:10px;color:{"#FF4040" if p_sw < 0.05 else "#39FF14"} !important;font-weight:800;font-size:1.05em;'>
        {"❌  p < 0.05 → REJECT normality → Price is NOT Normal" if p_sw < 0.05
         else "✅  p ≥ 0.05 → Could be normal"}
      </div>
    </div>""", unsafe_allow_html=True)

    c2.markdown(f"""<div class='step-box' style='border-left-color:#39FF14;'>
      <div style='font-weight:800;font-size:.97em;color:#39FF14 !important;'>KS Test — Is log(Price) Normal?</div>
      <div style='margin-top:8px;'>Tests if log(Price) fits Normal (= Price fits Log-Normal)</div>
      <div style='margin-top:4px;'>KS-statistic: <b>{stat_ks:.4f}</b></div>
      <div>p-value: <b>{p_ks:.4f}</b></div>
      <div style='margin-top:10px;color:{"#39FF14" if p_ks > 0.05 else "#FFD700"} !important;font-weight:800;font-size:1.05em;'>
        {"✅  Log-Normal fits reasonably well!" if p_ks > 0.05
         else "⚠️  Log-Normal doesn't fit perfectly either (extreme outliers remain)"}
      </div>
    </div>""", unsafe_allow_html=True)

    sec("📊 Raw Price vs Log(Price) — Fit Comparison")
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=["Price vs Normal Distribution",
                                        "log(Price) vs Normal — Log-Normal Fit"])
    price_plot = price[price.between(0.01, 20)]
    fig.add_trace(go.Histogram(x=price_plot, nbinsx=60, histnorm="probability density",
                               name="Actual Price",
                               marker=dict(color=COLORS[0], opacity=0.75, line=dict(width=0.3))), row=1, col=1)
    x_n = np.linspace(0, 20, 300)
    fig.add_trace(go.Scatter(x=x_n, y=norm.pdf(x_n, price_plot.mean(), price_plot.std()),
                             mode="lines", name="Normal Fit",
                             line=dict(color=COLORS[1], width=2.5, dash="dash")), row=1, col=1)
    log_p = np.log(price[price > 0])
    fig.add_trace(go.Histogram(x=log_p, nbinsx=60, histnorm="probability density",
                               name="log(Price)",
                               marker=dict(color=COLORS[2], opacity=0.75, line=dict(width=0.3))), row=1, col=2)
    x_l = np.linspace(log_p.min(), log_p.max(), 300)
    fig.add_trace(go.Scatter(x=x_l, y=norm.pdf(x_l, log_p.mean(), log_p.std()),
                             mode="lines", name="Normal on log scale",
                             line=dict(color=COLORS[1], width=2.5, dash="dash")), row=1, col=2)
    dark2(fig, h=460)
    st.plotly_chart(fig, use_container_width=True)
    insight("log(Price) is much closer to bell-shaped → <b>Price follows a Log-Normal distribution</b>. Transforming price to log scale before regression significantly improves model performance.")

    sec("📚 Why Log-Normal Makes Sense for Price")
    lognorm_df = pd.DataFrame({
        "Property": ["Always positive","Multiplicative growth","Right-skewed","Log → Normal"],
        "Real estate": ["Prices are never negative","5% annual growth = compounding",
                        "Few ultra-premium homes create right tail","log(Price) looks bell-shaped"],
        "Formula": ["X = e^(μ+σZ)","Z ~ Normal(0,1)","Skewness driven by σ","ln(X) ~ Normal(μ,σ²)"],
    })
    st.dataframe(lognorm_df, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
# PAGE 16 — HYPOTHESIS TESTING
# ════════════════════════════════════════════════════════════
def page_adv_hyp():
    st.markdown("<h1 style='color:#FF8C00 !important;text-shadow:0 0 25px rgba(255,140,0,.5);'>🧪 Hypothesis Testing</h1>", unsafe_allow_html=True)
    df = load_raw()

    st.markdown("""<div class='insight'>
    <b>Hypothesis testing</b> = using data to decide if a difference is real or just random chance.<br>
    H₀ (Null): "No difference" &nbsp;|&nbsp; H₁: "There IS a difference" &nbsp;|&nbsp;
    <b style='color:#39FF14 !important;'>p &lt; 0.05 → reject H₀ (result is real)</b>
    </div>""", unsafe_allow_html=True)

    # ── Test 1: t-test ─────────────────────────────────────
    sec("1️⃣ Independent t-test — Mumbai vs Chennai Prices")
    mumbai  = df[df["City"]=="Mumbai"]["Price_Cr"].dropna()
    chennai = df[df["City"]=="Chennai"]["Price_Cr"].dropna()
    t_stat, p_val = ttest_ind(mumbai, chennai, equal_var=False)
    RESULT_CLR = "#39FF14" if p_val < 0.05 else "#FF4040"

    c1, c2 = st.columns([1,2])
    c1.markdown(f"""<div class='glass'>
      <div style='font-size:.85em;color:#a0ccee !important;'>H₀: Mumbai = Chennai prices<br>H₁: Mumbai ≠ Chennai prices</div>
      <br>
      <div style='font-size:.9em;'>Mumbai median: <b style='color:#00D4FF !important;'>₹{mumbai.median():.2f}Cr</b> (n={len(mumbai)})</div>
      <div style='font-size:.9em;'>Chennai median: <b style='color:#FF006E !important;'>₹{chennai.median():.2f}Cr</b> (n={len(chennai)})</div>
      <br>
      <div>t-statistic: <b>{t_stat:.4f}</b></div>
      <div>p-value: <b>{p_val:.6f}</b></div>
      <br>
      <div style='color:{RESULT_CLR} !important;font-weight:800;font-size:1.05em;'>
        {"✅  p < 0.05 → REJECT H₀ → Prices ARE significantly different!" if p_val < 0.05
         else "❌  p ≥ 0.05 → Cannot reject H₀"}
      </div>
    </div>""", unsafe_allow_html=True)

    fig_t = px.box(df[df["City"].isin(["Mumbai","Chennai"]) & (df["Price_Cr"]<=20)],
                   x="City", y="Price_Cr", color="City",
                   color_discrete_sequence=[COLORS[0],COLORS[1]],
                   title="Mumbai vs Chennai",
                   labels={"City":"","Price_Cr":"Price (₹ Crores)"})
    dark(fig_t, h=380)
    c2.plotly_chart(fig_t, use_container_width=True)

    # ── Test 2: ANOVA ───────────────────────────────────────
    sec("2️⃣ One-Way ANOVA — Are All 6 City Prices Different?")
    city_groups = [df[df["City"]==c]["Price_Cr"].dropna() for c in df["City"].unique()]
    f_stat, p_anova = f_oneway(*city_groups)
    ANOVA_CLR = "#39FF14" if p_anova < 0.05 else "#FF4040"

    c1, c2 = st.columns([1,2])
    city_med = df.groupby("City")["Price_Cr"].median().sort_values(ascending=False).reset_index()
    city_med.columns = ["City","Median (₹ Cr)"]
    c1.markdown(f"""<div class='glass'>
      <div style='font-size:.85em;color:#a0ccee !important;'>H₀: All 6 cities same avg price<br>H₁: At least one city differs</div>
      <br>
      <div>F-statistic: <b>{f_stat:.4f}</b></div>
      <div>p-value: <b>{p_anova:.8f}</b></div>
      <br>
      <div style='color:{ANOVA_CLR} !important;font-weight:800;font-size:1.05em;'>
        {"✅  p < 0.05 → REJECT H₀ → City prices significantly differ!" if p_anova < 0.05
         else "❌  No significant difference"}
      </div>
    </div>""", unsafe_allow_html=True)
    c1.dataframe(city_med, use_container_width=True, hide_index=True)

    city_order_v = city_med["City"].tolist()
    fig_v = px.violin(df[df["Price_Cr"]<=15], x="City", y="Price_Cr",
                      color="City", color_discrete_sequence=COLORS,
                      category_orders={"City":city_order_v},
                      title="Price by City — ANOVA confirms significant differences",
                      box=True, labels={"City":"","Price_Cr":"Price (₹ Crores)"})
    dark(fig_v, h=420)
    c2.plotly_chart(fig_v, use_container_width=True)

    # ── Test 3: Chi-Square ──────────────────────────────────
    sec("3️⃣ Chi-Square — Is Furnishing Related to Property Status?")
    ct = pd.crosstab(df["Furnishing"], df["Status"])
    chi2_val, p_chi, dof, _ = chi2_contingency(ct)
    CHI_CLR = "#39FF14" if p_chi < 0.05 else "#FF4040"

    c1, c2 = st.columns([1,2])
    c1.markdown(f"""<div class='glass'>
      <div style='font-size:.85em;color:#a0ccee !important;'>H₀: Furnishing and Status are INDEPENDENT<br>H₁: They ARE related</div>
      <br>
      <div>Chi-square: <b>{chi2_val:.4f}</b></div>
      <div>p-value: <b>{p_chi:.6f}</b></div>
      <div>Degrees of freedom: <b>{dof}</b></div>
      <br>
      <div style='color:{CHI_CLR} !important;font-weight:800;font-size:1.05em;'>
        {"✅  p < 0.05 → Furnishing and Status ARE related!" if p_chi < 0.05
         else "❌  No significant relationship"}
      </div>
    </div>""", unsafe_allow_html=True)

    ct_pct = ct.div(ct.sum(axis=1), axis=0).mul(100).round(1)
    fig_chi = px.imshow(ct_pct, text_auto=True,
                        color_continuous_scale=["#0a0f2a","#FFD700"],
                        title="Furnishing vs Status (% within furnishing type)")
    dark(fig_chi, h=340)
    c2.plotly_chart(fig_chi, use_container_width=True)

    sec("📊 Test Comparison Summary")
    test_sum = pd.DataFrame({
        "Test": ["Independent t-test","One-Way ANOVA","Chi-Square"],
        "Question": ["Mumbai = Chennai?","All 6 cities same?","Furnishing ↔ Status related?"],
        "Statistic": [f"t = {t_stat:.3f}",f"F = {f_stat:.3f}",f"χ² = {chi2_val:.3f}"],
        "p-value": [f"{p_val:.6f}",f"{p_anova:.8f}",f"{p_chi:.6f}"],
        "Decision": [
            "REJECT H₀ ✅" if p_val < 0.05 else "Fail to reject ❌",
            "REJECT H₀ ✅" if p_anova < 0.05 else "Fail to reject ❌",
            "REJECT H₀ ✅" if p_chi < 0.05 else "Fail to reject ❌",
        ],
    })
    st.dataframe(test_sum, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
# PAGE 17 — KEY TAKEAWAYS
# ════════════════════════════════════════════════════════════
def page_takeaways():
    st.markdown("<h1 style='color:#00D4FF !important;text-shadow:0 0 30px rgba(0,212,255,.6);'>🏆 Key Takeaways & Interview Prep</h1>", unsafe_allow_html=True)

    sec("📊 9 Data Insights from This Project")
    insights_data = [
        ("1","#00D4FF","Median is the right price measure","₹1.6Cr median vs ₹3.76Cr mean — right-skewed data always needs median","Mean vs Median"),
        ("2","#FF006E","3 BHK dominates","Most popular home type across all 6 cities","Mode, Frequency"),
        ("3","#39FF14","Mumbai is 3× Chennai","₹2.70Cr vs ₹0.91Cr median — confirmed statistically","ANOVA p<0.05"),
        ("4","#FFD700","Area barely predicts price (r≈0.03)","Location explains price far more than square footage","Correlation"),
        ("5","#BF00FF","Price is extremely right-skewed","Skewness≈45, Kurtosis≈2175 — a few ₹200Cr homes distort everything","Skewness & Kurtosis"),
        ("6","#00FFB3","~8.6% of properties are outliers","IQR method: above ₹6.75Cr is unusual","IQR / Z-Score"),
        ("7","#FF8C00","Price follows Log-Normal","log(Price) is bell-shaped — typical for financial data","Distribution Fitting"),
        ("8","#FF4040","Furnishing IS related to status","Chi-Square p<0.05 — furnished homes skew Ready to Move","Chi-Square"),
        ("9","#FFE600","98.9% Bathrooms missing","Always check data quality — unusable columns must be dropped early","Missing Values"),
    ]
    for num, clr, title, detail, stat_used in insights_data:
        st.markdown(f"""<div class='takeaway' style='border-left:4px solid {clr};'>
          <div style='display:flex;gap:16px;align-items:flex-start;'>
            <div style='font-size:1.5em;font-weight:900;color:{clr} !important;
                       min-width:32px;text-shadow:0 0 12px {clr};'>{num}</div>
            <div>
              <div style='font-weight:800;font-size:1em;color:#ffffff !important;'>{title}</div>
              <div style='font-size:.83em;color:#b8d8f8 !important;margin-top:3px;line-height:1.5;'>{detail}</div>
              <span class='pill'>{stat_used}</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    sec("📚 Concepts Coverage Table")
    concepts = pd.DataFrame({
        "Category": ["Basic","Descriptive","Visual","Categorical",
                     "Correlation","Advanced","Outlier","Inference"],
        "Concepts Covered": [
            "Mean, Median, Mode, Variance, Std Dev, CV",
            "Five-Number Summary, IQR, Percentiles, Quartiles",
            "Histograms, Boxplots, Violin, Q-Q, Scatter, 3D plots",
            "Frequency tables, Cross-tabulation, Pie charts",
            "Pearson r, 2D & 3D Correlation Heatmap",
            "Skewness, Kurtosis, Distribution Fitting (Normal/Log-Normal)",
            "IQR Fence, Z-Score, Modified Z-Score, 3D Outlier Space",
            "t-test, One-Way ANOVA, Chi-Square",
        ],
    })
    st.dataframe(concepts, use_container_width=True, hide_index=True)

    sec("🎤 Top Interview Q&A")
    qs = [
        ("What's the most interesting finding?",
         "Area barely correlates with price (r≈0.03) — location explains price far better than size. A 1500 sqft flat in Mumbai costs 3× a 1500 sqft flat in Chennai."),
        ("Why median instead of mean for price?",
         "Price is right-skewed — a few ₹200Cr listings inflate the mean to ₹3.76Cr while the median (typical home) is ₹1.6Cr. Median is always more honest for skewed distributions."),
        ("How did you detect outliers?",
         "Three methods: IQR fence, Z-score (|z|>3), Modified Z-score (|mz|>3.5). Modified Z-score is most robust — it uses median+MAD instead of mean+std, which are distorted by the very outliers you're finding."),
        ("What distribution does price follow?",
         "Log-Normal — confirmed by Shapiro-Wilk (p≈0, rejects normality) and by log(Price) histogram being approximately bell-shaped."),
        ("What did hypothesis testing reveal?",
         "t-test: Mumbai/Chennai prices significantly differ (p<0.05). ANOVA: all 6 city prices differ. Chi-Square: furnishing type IS related to property status (p<0.05)."),
        ("What would you do differently for a production model?",
         "Add temporal data, location co-ordinates for spatial analysis, encode city/furnishing, and use log(Price) as target variable for linear models."),
    ]
    colors_q = [COLORS[0],COLORS[1],COLORS[2],COLORS[3],COLORS[4],COLORS[5]]
    for i, (q, a) in enumerate(qs):
        clr = colors_q[i % 6]
        st.markdown(f"""<div class='step-box' style='border-left-color:{clr};margin:10px 0;'>
          <div style='font-weight:800;color:{clr} !important;font-size:.92em;margin-bottom:6px;
                     text-shadow:0 0 8px {clr}66;'>Q: {q}</div>
          <div style='color:#d4f0e8 !important;font-size:.84em;line-height:1.65;'>{a}</div>
        </div>""", unsafe_allow_html=True)

    sec("🔗 Project Links")
    st.markdown("""
    <div style='display:flex;gap:16px;flex-wrap:wrap;margin-top:12px;'>
      <a href='https://github.com/viswanath-0' target='_blank'
         style='background:linear-gradient(135deg,rgba(0,212,255,.2),rgba(191,0,255,.2));
                border:1px solid rgba(0,212,255,.4);border-radius:12px;
                padding:12px 22px;color:#a0e8ff !important;text-decoration:none;
                font-weight:700;font-size:.95em;
                box-shadow:0 0 20px rgba(0,212,255,.15);'>
        🐙 GitHub: viswanath-0
      </a>
      <span class='pill' style='padding:10px 18px;font-size:.88em;'>🏠 Airbnb Predictor: streamlit.app</span>
      <span class='pill' style='padding:10px 18px;font-size:.88em;'>💬 Sentiment Analyser: streamlit.app</span>
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# NAVIGATION + MAIN
# ════════════════════════════════════════════════════════════
PAGES = {
    "🏠 Overview": page_overview,
    "🕷️ Web Scraping Process": page_scraping,
    "📋 Dataset Explorer": page_dataset,
    "📊 Univariate Analysis": page_eda_uni,
    "🔀 Bivariate Analysis": page_eda_bi,
    "📈 Basic Statistics": page_adv_basic,
    "📦 5-Number Summary & IQR": page_adv_5num,
    "📉 Distributions": page_adv_dist,
    "📦 Boxplots & Spread": page_adv_boxplots,
    "🗂️ Categorical Analysis": page_adv_cat,
    "❓ Missing Values": page_adv_missing,
    "🔗 Correlation Analysis": page_adv_corr,
    "↗️ Skewness & Kurtosis": page_adv_skew,
    "🎯 Outlier Detection": page_adv_outliers,
    "🔮 Distribution Fitting": page_adv_fit,
    "🧪 Hypothesis Testing": page_adv_hyp,
    "🏆 Key Takeaways": page_takeaways,
}

GROUPS = {
    "🏠 Home": ["🏠 Overview"],
    "📦 Data & Scraping": ["🕷️ Web Scraping Process","📋 Dataset Explorer"],
    "📊 Exploratory Analysis (EDA)": ["📊 Univariate Analysis","🔀 Bivariate Analysis"],
    "🧮 Advanced Statistics": [
        "📈 Basic Statistics","📦 5-Number Summary & IQR","📉 Distributions",
        "📦 Boxplots & Spread","🗂️ Categorical Analysis","❓ Missing Values",
        "🔗 Correlation Analysis","↗️ Skewness & Kurtosis",
        "🎯 Outlier Detection","🔮 Distribution Fitting","🧪 Hypothesis Testing",
        "🏆 Key Takeaways",
    ],
}

def main():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:20px 0 10px;'>
          <div style='font-size:2.4em;filter:drop-shadow(0 0 15px rgba(0,212,255,.7));'>🏡</div>
          <div style='font-weight:900;font-size:1em;
               background:linear-gradient(135deg,#00D4FF,#FF006E);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               margin-top:5px;'>Magicbricks Analytics</div>
          <div style='font-size:.7em;color:rgba(180,220,255,.5) !important;margin-top:3px;'>Real Estate Data Science</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:rgba(0,212,255,.2);margin:8px 0;'>", unsafe_allow_html=True)

        if "page" not in st.session_state:
            st.session_state.page = "🏠 Overview"

        for group, pages in GROUPS.items():
            st.markdown(f"""<div style='font-size:.65em;font-weight:800;
                color:rgba(0,212,255,.55) !important;letter-spacing:.12em;
                text-transform:uppercase;padding:10px 4px 3px;'>{group}</div>""",
                unsafe_allow_html=True)
            for pg in pages:
                active = st.session_state.page == pg
                if st.button(pg, key=f"btn_{pg}", use_container_width=True):
                    st.session_state.page = pg
            st.markdown("", unsafe_allow_html=True)

    PAGES.get(st.session_state.page, page_overview)()

if __name__ == "__main__":
    main()