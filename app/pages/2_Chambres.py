import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import query  # Utilise votre module db.py configuré pour Docker

# ================== CONFIG ==================
st.set_page_config(
    page_title="🛏️ Catalogue des Chambres",
    page_icon="🛏️",
    layout="wide"
)

# ================== STYLE ==================
st.markdown("""
<style>
body { background: linear-gradient(180deg, #F1F8E9, #FFFFFF); }
h1,h2,h3 { color: #1B5E20; font-weight: 800; }
.hero-title { font-size: 46px; font-weight: 900; color: #1B5E20; }
.hero-subtitle { font-size: 20px; color: #388E3C; }
div[data-testid="metric-container"] { background: linear-gradient(135deg, #FFFFFF, #E8F5E9); border-radius: 20px; padding: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
.card { background: white; padding: 30px; border-radius: 22px; box-shadow: 0 12px 30px rgba(0,0,0,0.1); margin-bottom: 25px; }
.filter-panel { background: linear-gradient(135deg, #E8F5E9, #C8E6C9); padding: 25px; border-radius: 20px; margin-bottom: 30px; border: 2px solid #A5D6A7; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ================== HERO ==================
st.markdown("<div class='hero-title'>🛏️ Catalogue des Chambres & Suites</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Explorez notre collection complète d'hébergements</div>", unsafe_allow_html=True)
st.divider()

# ================== FILTRES ==================
st.markdown("<div class='filter-panel'>", unsafe_allow_html=True)
st.subheader("🔍 Options de recherche")

col_f1, col_f2, col_f3 = st.columns([1, 1, 1])

with col_f1:
    # Radio button avec option "Toutes"
    type_choisi = st.radio(
        "**Type d'hébergement**",
        ["Toutes", "single", "double", "triple", "suite"],
        index=0,
        horizontal=True
    )

with col_f2:
    # Sélection multiple pour les options/équipements
    options_sup = st.multiselect(
        "**Équipements souhaités**",
        ["Balcon", "Vue mer", "Climatisation", "Wifi", "Mini-bar"],
        default=[]
    )

with col_f3:
    # Checkbox pour la cuisine
    a_cuisine = st.checkbox("**Avec Cuisine / Kitchenette**", value=False)

st.divider()

st.markdown("</div>", unsafe_allow_html=True)

# ================== CONSTRUCTION REQUÊTE SQL SIMPLIFIÉE ==================
sql = "SELECT CodR as code_chambre, SurfaceArea, Floor, Type FROM ROOM WHERE 1=1"

# Filtre Type (Radio Button)
if type_choisi != "Toutes":
    sql += f" AND Type = '{type_choisi}'"

# Filtre Cuisine (Checkbox)
if a_cuisine:
    sql += " AND HasKitchen = 1"

sql += " ORDER BY CodR"

# ================== EXÉCUTION & AFFICHAGE ==================
try:
    df = query(sql)
except Exception as e:
    st.error(f"❌ Erreur SQL : {e}")
    df = pd.DataFrame()

if not df.empty:
    # KPI
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    k1.metric("🛏️ Total", len(df))
    k2.metric("📐 Surface Moy.", f"{df['SurfaceArea'].mean():.1f} m²")
    k3.metric("🏢 Étages", df['Floor'].nunique())
    st.markdown("</div>", unsafe_allow_html=True)

    # Tableau
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Liste des chambres")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Graphiques
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["📊 Répartition par Type", "📈 Surface par Étage"])
    with t1:
        st.bar_chart(df['Type'].value_counts())
    with t2:
        fig, ax = plt.subplots()
        df.groupby('Floor')['SurfaceArea'].mean().plot(kind='bar', ax=ax, color='#4CAF50')
        st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Aucune chambre ne correspond à ces critères.")

# ================== SIDEBAR ==================
with st.sidebar:

    st.title("Paramètres")
    if st.button("🔄 Actualiser les données"):
        st.rerun()
    st.divider()
    
