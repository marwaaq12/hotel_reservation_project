import streamlit as st
from db import query
import matplotlib.pyplot as plt

# ================== CONFIG ==================
st.set_page_config(
    page_title="📅 Réservations",
    page_icon="📅",
    layout="wide"
)

# ================== STYLE ULTRA VERT ==================
st.markdown("""
<style>

/* ===== PAGE BACKGROUND ===== */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #E8F5E9 0%, #FFFFFF 60%);
}

/* ===== TITRES ===== */
h1, h2, h3 {
    color: #1B5E20 !important;
    font-weight: 900;
}

/* ===== METRICS ===== */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #C8E6C9, #E8F5E9);
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 12px 30px rgba(27,94,32,0.25);
    border: 2px solid #81C784;
}

div[data-testid="metric-container"] * {
    color: #1B5E20 !important;
    font-weight: 800;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] {
    background-color: #F1F8E9;
    border-radius: 20px;
    border: 2px solid #A5D6A7;
}

/* ===== PLOTS ===== */
svg {
    background-color: #F1F8E9;
    border-radius: 18px;
}

/* ===== REMOVE FOOTER ===== */
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("## 📅 Analyse des Réservations")
st.markdown("### 💚 Tableau de bord des prix journaliers")
st.divider()

# ================== KPI ==================
col1, col2, col3 = st.columns(3)

total_res = query("SELECT COUNT(*) total FROM RESERVER").iloc[0, 0]
prix_moy = query("SELECT ROUND(AVG(PRIX),2) prix FROM RESERVER").iloc[0, 0]
best = query("""
    SELECT CHCODE
    FROM RESERVER
    GROUP BY CHCODE
    ORDER BY AVG(PRIX) DESC
    LIMIT 1
""").iloc[0, 0]

col1.metric("📌 Réservations", total_res)
col2.metric("💰 Prix moyen", f"{prix_moy} €")
col3.metric("🏆 Chambre la plus chère", best)

st.divider()

# ================== TABLE ==================
st.subheader("📊 Coût journalier moyen par mois")

df = query("""
    SELECT 
        MONTH(DATE_DEBUT) AS mois,
        ROUND(AVG(PRIX),2) AS prix_moyen
    FROM RESERVER
    GROUP BY mois
    ORDER BY mois
""")

st.dataframe(df, use_container_width=True)

# ================== GRAPH ==================
st.subheader("📈 Évolution mensuelle")

plt.figure()
plt.plot(
    df["mois"],
    df["prix_moyen"],
    marker="o",
    linewidth=3,
    color="green"
)
plt.xlabel("Mois")
plt.ylabel("Prix moyen (€)")
plt.title("Évolution du coût journalier moyen")
plt.grid(True)

st.pyplot(plt)

st.divider()

# ================== TOP ROOMS ==================
st.subheader("🏆 Chambres les plus chères")

top = query("""
    SELECT CHCODE, ROUND(AVG(PRIX),2) prix_moyen
    FROM RESERVER
    GROUP BY CHCODE
    ORDER BY prix_moyen DESC
""")

st.dataframe(top, use_container_width=True)