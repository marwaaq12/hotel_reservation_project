import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import query  # Assurez-vous que votre module db.query fonctionne

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
    type_choisi = st.radio(
        "**Type d'hébergement**",
        ["Toutes", "single", "double", "triple", "suite"],
        index=0,
        horizontal=True
    )

with col_f2:
    # Ces options doivent correspondre aux valeurs dans votre table HAS_SPACES
    options_sup = st.multiselect(
        "**Équipements souhaités**",
        ["Balcon", "Vue mer", "Climatisation", "Wifi", "Mini-bar"],
        default=[]
    )

with col_f3:
    a_cuisine = st.checkbox("**Avec Cuisine / Kitchenette**", value=False)

st.markdown("</div>", unsafe_allow_html=True)

# ================== CONSTRUCTION REQUÊTE SQL ==================
# On utilise R pour ROOM pour faciliter les jointures ou sous-requêtes
sql = "SELECT CodR as code_chambre, SurfaceArea, Floor, Type FROM ROOM R WHERE 1=1"

# 1. Filtre Type
if type_choisi != "Toutes":
    sql += f" AND R.Type = '{type_choisi}'"

# 2. Filtre Cuisine (via la table HAS_SPACES)
if a_cuisine:
    sql += """ 
    AND R.CodR IN (
        SELECT ROOM_CodR 
        FROM HAS_SPACES 
        WHERE SPACES_Space = 'kitchen'
    )
    """

# 3. Filtre Équipements (via la table HAS_SPACES)
if options_sup:
    # Formatage de la liste pour SQL IN (...)
    if len(options_sup) == 1:
        options_sql = f"('{options_sup[0]}')"
    else:
        options_sql = tuple(options_sup)
    
    sql += f""" 
    AND R.CodR IN (
        SELECT ROOM_CodR 
        FROM HAS_SPACES 
        WHERE SPACES_Space IN {options_sql}
    )
    """

sql += " ORDER BY R.CodR"

# ================== EXÉCUTION & AFFICHAGE ==================
try:
    df = query(sql)
except Exception as e:
    st.error(f"❌ Erreur lors de l'exécution de la requête: {str(e)}")
    df = pd.DataFrame()

if not df.empty:
    # KPI
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    k1.metric("🛏️ Chambres trouvées", len(df))
    k2.metric("📐 Surface moyenne", f"{df['SurfaceArea'].mean():.1f} m²")
    k3.metric("🏢 Étages couverts", df["Floor"].nunique())
    st.markdown("</div>", unsafe_allow_html=True)

    # Tableau des résultats
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Liste détaillée")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


else:
    st.markdown("<div class='card' style='background: #FFF3E0;'>", unsafe_allow_html=True)
    st.warning("⚠️ Aucune chambre ne correspond à ces critères.")
    st.info("💡 Essayez de modifier vos filtres (notamment la cuisine ou les équipements).")
    st.markdown("</div>", unsafe_allow_html=True)

# ================== SIDEBAR ==================
with st.sidebar:
    st.header("⚙️ Paramètres")
    if st.button("🔄 Actualiser l'affichage"):
        st.rerun()
    st.divider()
    with st.expander("📖 Debug SQL"):
        st.write("Requête exécutée :")
        st.code(sql, language="sql")
    st.caption("🏨 Hôtel Management System • 2025")