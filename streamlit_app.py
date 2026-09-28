import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Plan de nettoyage - Hôtel 5★",
    page_icon="🧽",
    layout="wide"
)

st.title("🧽 Plan de Nettoyage - Cuisine Hôtel 5★")
st.caption("Suivi des opérations de nettoyage et désinfection")

# -----------------------------
# MENU
# -----------------------------
menu = st.sidebar.selectbox(
    "Menu",
    [
        "📊 Tableau de bord",
        "🧽 Nouvelle opération",
        "📋 Plan de nettoyage",
        "❌ Non-conformités"
    ]
)

# -----------------------------
# DONNÉES DU PLAN
# -----------------------------
plan = [
    ["Cuisine chaude", "Plans de travail", "Nettoyage + désinfection", "Après utilisation"],
    ["Cuisine chaude", "Fours", "Nettoyage", "Quotidien"],
    ["Cuisine chaude", "Plaques / grills", "Dégraissage + désinfection", "Après utilisation"],
    ["Cuisine froide", "Plans de travail", "Nettoyage + désinfection", "Après utilisation"],
    ["Plonge", "Bacs de plonge", "Nettoyage + désinfection", "Quotidien"],
    ["Plonge", "Lave-vaisselle", "Nettoyage des filtres et surfaces", "Quotidien"],
    ["Chambre froide", "Sols", "Nettoyage + désinfection", "Hebdomadaire"],
    ["Chambre froide", "Étagères", "Nettoyage + désinfection", "Hebdomadaire"],
    ["Chambre froide", "Parois", "Nettoyage", "Mensuel"],
    ["Économat", "Étagères", "Nettoyage + désinfection", "Hebdomadaire"],
    ["Local déchets", "Sols et surfaces", "Nettoyage + désinfection", "Quotidien"],
    ["Cuisine", "Caniveaux", "Nettoyage + désinfection", "Quotidien"],
    ["Cuisine", "Hotte / filtres", "Dégraissage", "Hebdomadaire"],
]

df_plan = pd.DataFrame(
    plan,
    columns=[
        "Zone",
        "Équipement",
        "Opération",
        "Fréquence"
    ]
)

# -----------------------------
# TABLEAU DE BORD
# -----------------------------
if menu == "📊 Tableau de bord":

    st.subheader("📊 Tableau de bord")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Opérations prévues", len(df_plan))
    col2.metric("Zones", df_plan["Zone"].nunique())
    col3.metric("Opérations quotidiennes",
                len(df_plan[df_plan["Fréquence"] == "Quotidien"]))
    col4.metric("Date", datetime.now().strftime("%d/%m/%Y"))

    st.divider()

    st.subheader("Plan de nettoyage")

    st.dataframe(
        df_plan,
        use_container_width=True,
        hide_index=True
    )

# -----------------------------
# NOUVELLE OPÉRATION
# -----------------------------
elif menu == "🧽 Nouvelle opération":

    st.subheader("🧽 Enregistrer une opération de nettoyage")

    with st.form("form_nettoyage"):

        col1, col2 = st.columns(2)

        with col1:
            zone = st.selectbox(
                "Zone",
                sorted(df_plan["Zone"].unique())
            )

            equipement = st.text_input(
                "Équipement / surface"
            )

            operation = st.text_input(
                "Opération réalisée"
            )

            produit = st.text_input(
                "Produit utilisé"
            )

        with col2:

            concentration = st.text_input(
                "Concentration"
            )

            temps_contact = st.number_input(
                "Temps de contact (minutes)",
                min_value=0,
                step=1
            )

            statut = st.selectbox(
                "Statut",
                ["Conforme", "Non conforme"]
            )

            operateur = st.text_input(
                "Nom de l'opérateur"
            )

        anomalie = st.text_area(
            "Anomalie / action corrective"
        )

        controleur = st.text_input(
            "Nom du contrôleur"
        )

        enregistrer = st.form_submit_button(
            "✅ Enregistrer"
        )

        if enregistrer:

            if not equipement or not operateur:
                st.error(
                    "Veuillez renseigner au minimum l'équipement et l'opérateur."
                )
            else:

                nouvelle_ligne = pd.DataFrame(
                    [{
                        "Date": datetime.now().strftime("%d/%m/%Y"),
                        "Heure": datetime.now().strftime("%H:%M"),
                        "Zone": zone,
                        "Équipement": equipement,
                        "Opération": operation,
                        "Produit": produit,
                        "Concentration": concentration,
                        "Temps contact": temps_contact,
                        "Statut": statut,
                        "Opérateur": operateur,
                        "Anomalie": anomalie,
                        "Contrôleur": controleur
                    }]
                )

                st.success(
                    "✅ Opération enregistrée avec succès."
                )

                st.dataframe(
                    nouvelle_ligne,
                    use_container_width=True,
                    hide_index=True
                )

# -----------------------------
# PLAN DE NETTOYAGE
# -----------------------------
elif menu == "📋 Plan de nettoyage":

    st.subheader("📋 Plan de nettoyage des cuisines")

    frequence = st.selectbox(
        "Filtrer par fréquence",
        [
            "Toutes",
            "Quotidien",
            "Après utilisation",
            "Hebdomadaire",
            "Mensuel"
        ]
    )

    if frequence != "Toutes":
        affichage = df_plan[
            df_plan["Fréquence"] == frequence
        ]
    else:
        affichage = df_plan

    st.dataframe(
        affichage,
        use_container_width=True,
        hide_index=True
    )

# -----------------------------
# NON-CONFORMITÉS
# -----------------------------
elif menu == "❌ Non-conformités":

    st.subheader("❌ Suivi des non-conformités")

    st.info(
        "Cette rubrique permet de suivre les anomalies constatées "
        "pendant les contrôles de nettoyage."
    )

    zone = st.selectbox(
        "Zone concernée",
        sorted(df_plan["Zone"].unique())
    )

    anomalie = st.text_area(
        "Description de la non-conformité"
    )

    action = st.text_area(
        "Action corrective"
    )

    responsable = st.text_input(
        "Responsable de l'action corrective"
    )

    if st.button("💾 Enregistrer la non-conformité"):

        if anomalie and action:
            st.success(
                "✅ Non-conformité enregistrée."
            )
        else:
            st.warning(
                "Veuillez renseigner l'anomalie et l'action corrective."
            )

st.sidebar.divider()
st.sidebar.caption("Hôtel 5★ — Gestion hygiène et nettoyage")
