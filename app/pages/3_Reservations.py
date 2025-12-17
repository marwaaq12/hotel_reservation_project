import streamlit as st
from db import query  # Assurez-vous que cette fonction exécute bien vos requêtes SQL

# ================== CONFIG ==================
st.set_page_config(
    page_title="📅 Réservations",
    page_icon="📅",
    layout="wide"
)

# ================== STYLE ==================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg, #F1F8E9, #FFFFFF); }
h1, h2, h3 { color: #1B5E20; font-weight: 800; }
div[data-testid="metric-container"] { 
    background: linear-gradient(135deg, #FFFFFF, #E8F5E9);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ================== HERO ==================
st.title("📅 Gestion des Réservations")
st.divider()

# ================== METRICS ==================
col1, col2, col3 = st.columns(3)

try:
    total = query("SELECT COUNT(*) FROM BOOKING").iloc[0, 0]
    revenu = query("SELECT SUM(Cost) FROM BOOKING").iloc[0, 0]
    prix_moy = query("SELECT AVG(Cost) FROM BOOKING").iloc[0, 0]

    chambre_pop = query("""
        SELECT ROOM_CodR, COUNT(*) as nb_reservations
        FROM BOOKING 
        GROUP BY ROOM_CodR 
        ORDER BY nb_reservations DESC 
        LIMIT 1
    """)

    chambre_top = chambre_pop.iloc[0, 0] if not chambre_pop.empty else "N/A"

except Exception as e:
    total = revenu = prix_moy = 0
    chambre_top = "N/A"

col1.metric("📅 Réservations", total)
col2.metric("💰 Revenu total", f"{revenu:,.0f} €" if revenu else "0 €")
col3.metric("👑 Chambre populaire", chambre_top)

st.divider()


# ================== DERNIÈRES RÉSERVATIONS ==================
st.divider()
st.subheader("📋 Dernières réservations")

try:
    recent = query("""
        SELECT 
            B.ROOM_CodR as Chambre,
            B.StartDate as Début,
            B.EndDate as Fin,
            B.Cost as `Prix (€)`,
            A.CodA as Agence,
            A.City_Address as `Ville agence`
        FROM BOOKING B
        JOIN TRAVEL_AGENCY A ON B.TRAVEL_AGENCY_CodA = A.CodA
        ORDER BY B.StartDate DESC
        LIMIT 10
    """)

    if not recent.empty:
        st.dataframe(recent, use_container_width=True)
    else:
        st.info("Aucune réservation récente")

except Exception as e:
    st.warning("Impossible de charger les réservations")

# ================== CHAMBRE LA PLUS CHÈRE PAR MOIS ==================
st.subheader("💸 Chambre la Plus Chère par Mois")

try:
    monthly_cost = query("""
        SELECT 
            MONTH(B.StartDate) as Mois,
            R.CodR,
            R.Floor,
            R.SurfaceArea,
            R.Type,
            AVG(B.Cost) as Cout_moy
        FROM BOOKING B
        JOIN ROOM R ON B.ROOM_CodR = R.CodR
        GROUP BY MONTH(B.StartDate), R.CodR, R.Floor, R.SurfaceArea, R.Type
    """)
    
    if not monthly_cost.empty:
        idx = monthly_cost.groupby('Mois')['Cout_moy'].idxmax()
        top_rooms = monthly_cost.loc[idx].sort_values('Mois')
        st.dataframe(top_rooms[['Mois','CodR','Floor','SurfaceArea','Type','Cout_moy']], use_container_width=True)
        
        # Graphique du coût moyen journalier
        st.subheader("📈 Évolution du Coût Journalier Moyen")
        monthly_avg = monthly_cost.groupby('Mois')['Cout_moy'].mean()
        st.line_chart(monthly_avg)
    else:
        st.info("Aucune donnée disponible")
        
except Exception as e:
    st.warning(f"Impossible de charger l'analyse du coût journalier: {e}")

st.markdown("---")
st.caption("📅 Module Réservations • Base: hotel")

st.divider()
st.caption("📅 Module Réservations • Base: hotel")