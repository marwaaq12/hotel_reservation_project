import streamlit as st
from db import query
import pandas as pd

# ================== CONFIG ==================
st.set_page_config(
    page_title="Chambres",
    page_icon="🛏️",
    layout="wide"
)

# ================== STYLE VERT ==================
st.markdown("""
<style>

/* PAGE */
[data-testid="stAppViewContainer"] {
    background-color: #f4fbf4;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #eaf5ea;
}

/* TITRES */
h1, h2, h3 {
    color: #1f6f2b;
}

/* KPI */
div[data-testid="metric-container"] {
    background-color: white;
    border-left: 6px solid #2e7d32;
    padding: 15px;
}

/* CARDS */
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #d9ead9;
}

/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid #c8e6c9;
}

/* FOOTER */
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ================== SIDEBAR - FILTRES ==================
with st.sidebar:
    st.header("🔍 Filtres de recherche")

    type_chambre = st.multiselect(
        "Type de chambre",
        ["Chambre Simple", "Suite"],
        default=["Chambre Simple", "Suite"]
    )

    surface_min, surface_max = st.slider(
        "Surface (m²)",
        min_value=10,
        max_value=100,
        value=(15, 50)
    )

# ================== TITRE ==================
st.markdown("# 🔍 Consultation & Filtrage des Chambres")
st.caption("Système de consultation avancée des chambres et suites")
st.divider()

# ================== REQUÊTE ==================
type_sql = []
if "Suite" in type_chambre:
    type_sql.append("s.CHCODE IS NOT NULL")
if "Chambre Simple" in type_chambre:
    type_sql.append("s.CHCODE IS NULL")

type_condition = " OR ".join(type_sql)

sql = f"""
SELECT 
    c.CHCODE,
    c.SURFACE,
    CASE 
        WHEN s.CHCODE IS NOT NULL THEN 'Suite'
        ELSE 'Chambre Simple'
    END AS type_chambre
FROM CHAMBRE c
LEFT JOIN SUITE s ON c.CHCODE = s.CHCODE
WHERE ({type_condition})
AND c.SURFACE BETWEEN {surface_min} AND {surface_max}
"""

df = query(sql)

# ================== KPI ==================
col1, col2, col3 = st.columns(3)

col1.metric("🛏️ Chambres trouvées", len(df))
col2.metric("👑 Suites", len(df[df["type_chambre"] == "Suite"]))
col3.metric("📐 Surface moyenne", round(df["SURFACE"].mean(), 2) if len(df) > 0 else 0)

st.divider()

# ================== TABLEAU ==================
st.subheader("📋 Tableau des Chambres")
st.dataframe(df, use_container_width=True)