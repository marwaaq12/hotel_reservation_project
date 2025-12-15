import streamlit as st
from db import query

# ================== CONFIG ==================
st.set_page_config(
    page_title="📍 Agences partenaires",
    page_icon="📍",
    layout="wide"
)

# ================== STYLE GLOBAL (MÊME QUE ACCUEIL) ==================
st.markdown("""
<style>

/* BACKGROUND */
body {
    background: linear-gradient(180deg, #F1F8E9, #FFFFFF);
}

/* TITRES */
h1, h2, h3 {
    color: #1B5E20;
    font-weight: 800;
}

/* HERO */
.hero-title {
    font-size: 46px;
    font-weight: 900;
    color: #1B5E20;
}

.hero-subtitle {
    font-size: 20px;
    color: #388E3C;
}

/* METRICS */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #FFFFFF, #E8F5E9);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

/* CARD */
.card {
    background: white;
    padding: 30px;
    border-radius: 22px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.1);
    margin-bottom: 25px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E8F5E9, #C8E6C9);
}

</style>
""", unsafe_allow_html=True)

# ================== HERO ==================
st.markdown("<div class='hero-title'>📍 Agences de Voyages</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Réseau international de partenaires hôteliers</div>", unsafe_allow_html=True)
st.divider()

# ================== METRICS ==================
col1, col2, col3 = st.columns(3)

nb_agences = query("SELECT COUNT(*) total FROM AGENCE").iloc[0, 0]
nb_villes = query("SELECT COUNT(DISTINCT VILLE) total FROM AGENCE").iloc[0, 0]

ville_top = query("""
SELECT VILLE
FROM AGENCE
GROUP BY VILLE
ORDER BY COUNT(*) DESC
LIMIT 1
""").iloc[0, 0]

col1.metric("🏢 Agences partenaires", nb_agences)
col2.metric("🌍 Villes couvertes", nb_villes)
col3.metric("🏆 Ville la plus active", ville_top)

st.divider()

# ================== MAP CARD ==================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🗺️ Localisation géographique")

map_df = query("""
SELECT V.LATITUDE, V.LONGITUDE
FROM AGENCE A
JOIN VILLE V ON A.VILLE = V.NOM
""")

st.map(map_df)
st.markdown("</div>", unsafe_allow_html=True)

# ================== TABLE CARD ==================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📋 Liste des agences")

villes = query("SELECT DISTINCT VILLE FROM AGENCE")["VILLE"].tolist()
villes.insert(0, "Toutes les villes")

ville_choisie = st.selectbox("Filtrer par ville", villes)

sql = """
SELECT 
    A.NOM AS "Agence",
    CONCAT(A.RUE, ', ', A.NUMERO, ', ', A.CPOSTAL, ' - ', A.VILLE) AS "Adresse complète",
    A.NTELEPHONE AS "Téléphone",
    A.SITEWEB AS "Site web"
FROM AGENCE A
"""

if ville_choisie != "Toutes les villes":
    sql += f" WHERE A.VILLE = '{ville_choisie}'"

df = query(sql)
st.dataframe(df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ================== FOOTER ==================
st.caption("🏨 Hôtel Management System • Agences partenaires")