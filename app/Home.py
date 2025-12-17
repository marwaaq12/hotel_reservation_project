import sys
import os

# Get the path to the project root (one level up from 'app')
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the root directory to the system path
sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd
from db import query  # Assurez-vous que cette fonction fonctionne pour exécuter vos requêtes MySQL

# ================== CONFIG ==================
st.set_page_config(
    page_title="🏨 Hôtel Management System",
    page_icon="🏨",
    layout="wide"
)

# ================== STYLE PREMIUM ==================
st.markdown("""
<style>
/* ----- BACKGROUND ----- */
body {
    background: linear-gradient(180deg, #F1F8E9, #FFFFFF);
}
/* ----- TITRES ----- */
h1, h2, h3 {
    color: #1B5E20;
    font-weight: 800;
}
.hero-title {
    font-size: 52px;
    font-weight: 900;
    color: #1B5E20;
}
.hero-subtitle {
    font-size: 22px;
    color: #388E3C;
}
/* ----- METRICS ----- */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #FFFFFF, #E8F5E9);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}
div[data-testid="metric-container"]:hover {
    transform: scale(1.05);
}
/* ----- CARDS ----- */
.card {
    background: white;
    padding: 30px;
    border-radius: 22px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.1);
    text-align: center;
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}
/* ----- BUTTONS ----- */
.stButton > button {
    background: linear-gradient(135deg, #1B5E20, #4CAF50) !important;
    color: white !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    border: none !important;
}
/* ----- SIDEBAR ----- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E8F5E9, #C8E6C9);
}
/* ----- FOOTER ----- */
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ================== HERO SECTION ==================
st.markdown("<div class='hero-title'>🏨 Hôtel Management System</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Plateforme intelligente de gestion hôtelière</div>", unsafe_allow_html=True)
st.markdown("### ✨ Gérez vos agences, chambres et réservations en toute simplicité")
st.divider()

# ================== METRICS ==================
col1, col2, col3 = st.columns(3)

try:
    tables_in_db = [t.upper() for t in query("SHOW TABLES")['Tables_in_hotel_db'].tolist()]
    nb_agences = query("SELECT COUNT(*) as total FROM TRAVEL_AGENCY").iloc[0, 0] if 'TRAVEL_AGENCY' in tables_in_db else 0
    nb_chambres = query("SELECT COUNT(*) as total FROM ROOM").iloc[0, 0] if 'ROOM' in tables_in_db else 0
    nb_reservations = query("SELECT COUNT(*) as total FROM BOOKING").iloc[0, 0] if 'BOOKING' in tables_in_db else 0

except Exception as e:
    st.warning(f"Certaines tables n'existent pas encore: {e}")
    nb_agences = nb_chambres = nb_reservations = 0

col1.metric("📍 Agences partenaires", nb_agences)
col2.metric("🛏️ Chambres disponibles", nb_chambres)
col3.metric("📅 Réservations totales", nb_reservations)

st.divider()

# ================== GALERIE IMMERSIVE ==================
st.subheader("🖼️ Expérience & Confort")

tabs = st.tabs(["🛏️ Chambre Simple", "👫 Chambre Double", "👑 Suite de Luxe"])

with tabs[0]:
    st.image(
        "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=1200",
        use_container_width=True,
        caption="Chambre simple – confort et élégance"
    )

with tabs[1]:
    st.image(
        "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=1200",
        use_container_width=True,
        caption="Chambre double – idéale pour les couples"
    )

with tabs[2]:
    st.image(
        "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=1200",
        use_container_width=True,
        caption="Suite de luxe – espace et raffinement"
    )

st.divider()

# ================== SERVICES ==================
st.subheader("🌟 Fonctionnalités Principales")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class='card'>
        📍<br><br>
        <b>Gestion des Agences</b><br><br>
        Visualisation géographique, statistiques et recherche par ville.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='card'>
        🛏️<br><br>
        <b>Gestion des Chambres</b><br><br>
        Filtres par type, équipements et affichage interactif.
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='card'>
        📊<br><br>
        <b>Analyse des Réservations</b><br><br>
        Évolution des prix et tendances mensuelles.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ================== À PROPOS ==================
st.subheader("💼 À propos du projet")

left, right = st.columns(2)

with left:
    st.info("""
🎯 **Objectif**

Concevoir une application web moderne permettant la gestion complète
des réservations d'une chaîne hôtelière à l'aide de Streamlit et MySQL.
""")

with right:
    st.success("""
    👩‍🎓 **Réalisé par**
    * **Sophia Yassfouli**
    * **Asma Bennani**
    * **Zakaria Zaki**
    * **Marwa Aqrir**
    * **Badr Eddaoudi**
    * **Ayoub Sabri**

    **ENSA** | Python • Streamlit • MySQL
    """)

# ================== SIDEBAR ==================
with st.sidebar:
    st.header("🧭 Navigation")

    page = st.selectbox(
        "Choisissez une page",
        ["🏠 Accueil", "📍 Agences", "🛏️ Chambres", "📅 Réservations", "📊 Statistiques"]
    )

    st.divider()

    if st.button("🔌 Tester la connexion", use_container_width=True):
        try:
            tables = query("SHOW TABLES")
            st.success("✅ Connexion réussie")
            st.write(f"Tables trouvées: {len(tables)}")
            with st.expander("Voir les tables"):
                st.dataframe(tables)
        except Exception as e:
            st.error(f"❌ Erreur de connexion: {e}")

    st.divider()

    with st.expander("📊 Info Base de Données"):
        try:
            db_info = query("SELECT DATABASE() as current_db, USER() as current_user")
            st.write(f"Base: {db_info.iloc[0, 0]}")
            st.write(f"Utilisateur: {db_info.iloc[0, 1]}")
        except:
            st.write("Impossible de récupérer les infos DB")

    st.caption("🏨 Hôtel Management System • 2025")