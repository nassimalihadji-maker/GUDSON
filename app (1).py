import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import hashlib
import uuid
import os

# Configuration de la page
st.set_page_config(
    page_title="GUDSON KPI - Suivi Fournisseurs & Acheteurs",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-msg {
        padding: 0.5rem;
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
    }
    .error-msg {
        padding: 0.5rem;
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
    }
    .sidebar-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
        background: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Fonctions utilitaires
@st.cache_data
def load_data():
    """Charger toutes les données depuis les fichiers CSV"""
    try:
        df_fournisseurs = pd.read_csv('fournisseurs_data.csv')
        df_acheteurs = pd.read_csv('acheteurs_data.csv')
        df_commandes = pd.read_csv('commandes_data.csv')
        df_historique = pd.read_csv('historique_data.csv')

        return df_fournisseurs, df_acheteurs, df_commandes, df_historique
    except FileNotFoundError as e:
        st.error(f"Fichier manquant: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def load_users():
    """Charger la base de données des utilisateurs"""
    try:
        with open('users_db.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def hash_password(password):
    """Hasher le mot de passe pour sécurité"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authentifier un utilisateur"""
    users_db = load_users()
    if username in users_db:
        if users_db[username]['password'] == password:  # En production, utiliser des hash
            return users_db[username]
    return None

def has_permission(user_data, permission):
    """Vérifier si l'utilisateur a une permission spécifique"""
    if user_data and 'permissions' in user_data:
        return permission in user_data['permissions']
    return False

def log_action(user, action, table, record_id, details=""):
    """Enregistrer une action dans l'historique"""
    if 'df_historique' not in st.session_state:
        return

    new_entry = {
        'ID_Historique': f"H{len(st.session_state.df_historique)+1:04d}",
        'Date_Action': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Utilisateur': user,
        'Action': action,
        'Table_Modifiee': table,
        'ID_Enregistrement': record_id,
        'Champ_Modifie': '',
        'Ancienne_Valeur': '',
        'Nouvelle_Valeur': '',
        'Commentaire': details
    }

    new_df = pd.DataFrame([new_entry])
    st.session_state.df_historique = pd.concat([st.session_state.df_historique, new_df], ignore_index=True)

def save_data():
    """Sauvegarder les modifications dans les fichiers"""
    try:
        if 'df_fournisseurs' in st.session_state:
            st.session_state.df_fournisseurs.to_csv('fournisseurs_data.csv', index=False)
        if 'df_acheteurs' in st.session_state:
            st.session_state.df_acheteurs.to_csv('acheteurs_data.csv', index=False)
        if 'df_commandes' in st.session_state:
            st.session_state.df_commandes.to_csv('commandes_data.csv', index=False)
        if 'df_historique' in st.session_state:
            st.session_state.df_historique.to_csv('historique_data.csv', index=False)
        return True
    except Exception as e:
        st.error(f"Erreur sauvegarde: {e}")
        return False

# Initialisation de la session
def init_session():
    """Initialiser les variables de session"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'data_loaded' not in st.session_state:
        df_fournisseurs, df_acheteurs, df_commandes, df_historique = load_data()
        st.session_state.df_fournisseurs = df_fournisseurs
        st.session_state.df_acheteurs = df_acheteurs
        st.session_state.df_commandes = df_commandes
        st.session_state.df_historique = df_historique
        st.session_state.data_loaded = True

# Page de connexion
def login_page():
    """Interface de connexion"""
    st.markdown('<div class="main-header"><h1>🏢 GUDSON KPI SYSTEM</h1><p>Système de Suivi des Fournisseurs & Acheteurs</p></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### 🔐 Connexion")

        with st.form("login_form"):
            username = st.text_input("👤 Nom d'utilisateur")
            password = st.text_input("🔒 Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter", use_container_width=True)

            if submit:
                user_data = authenticate_user(username, password)
                if user_data:
                    st.session_state.authenticated = True
                    st.session_state.user_data = user_data
                    st.session_state.username = username
                    st.success(f"Bienvenue {user_data['nom_complet']} ({user_data['role']})")
                    st.rerun()
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect")

        # Informations de connexion pour demo
        st.markdown("---")
        st.markdown("### 📋 Comptes de démonstration:")
        st.markdown("""
        **Admin:** `admin` / `admin123`  
        **Acheteur:** `acheteur1` / `achat123`  
        **Consultant:** `consultant1` / `consul123`
        """)

# Interface principale
def main_interface():
    """Interface principale de l'application"""

    # Sidebar avec profil utilisateur
    with st.sidebar:
        st.markdown('<div class="sidebar-logo"><h2>📊 GUDSON KPI</h2></div>', unsafe_allow_html=True)

        # Profil utilisateur
        user_data = st.session_state.user_data
        st.markdown("### 👤 Profil Utilisateur")
        st.write(f"**Nom:** {user_data['nom_complet']}")
        st.write(f"**Rôle:** {user_data['role']}")
        st.write(f"**Email:** {user_data['email']}")

        # Bouton déconnexion
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.rerun()

        st.markdown("---")

        # Menu navigation selon les permissions
        menu_items = ["🏠 Tableau de Bord"]

        if has_permission(user_data, "lecture"):
            menu_items.extend(["📊 KPI Fournisseurs", "🛒 KPI Acheteurs", "📈 Analyses"])

        if has_permission(user_data, "ecriture"):
            menu_items.extend(["➕ Ajouter Données", "✏️ Modifier/Supprimer"])

        if has_permission(user_data, "gestion_utilisateurs"):
            menu_items.append("👥 Gestion Utilisateurs")

        # Sélection du menu
        selected = st.selectbox("Navigation", menu_items)

    # Contenu principal selon la sélection
    if selected == "🏠 Tableau de Bord":
        dashboard_page()
    elif selected == "📊 KPI Fournisseurs":
        kpi_fournisseurs_page()
    elif selected == "🛒 KPI Acheteurs":
        kpi_acheteurs_page()
    elif selected == "➕ Ajouter Données":
        add_data_page()
    elif selected == "✏️ Modifier/Supprimer":
        edit_data_page()
    elif selected == "📈 Analyses":
        analytics_page()
    elif selected == "👥 Gestion Utilisateurs":
        user_management_page()

def dashboard_page():
    """Page tableau de bord principal"""
    st.markdown('<div class="main-header"><h1>📊 Tableau de Bord GUDSON</h1></div>', unsafe_allow_html=True)

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)

    df_fournisseurs = st.session_state.df_fournisseurs
    df_acheteurs = st.session_state.df_acheteurs  
    df_commandes = st.session_state.df_commandes

    with col1:
        total_fournisseurs = len(df_fournisseurs)
        st.metric("🏢 Fournisseurs Actifs", total_fournisseurs)

    with col2:
        total_acheteurs = len(df_acheteurs)
        st.metric("👤 Acheteurs", total_acheteurs)

    with col3:
        ca_total = df_commandes['Montant_Total'].sum()
        st.metric("💰 CA Total", f"{ca_total:,.0f} €")

    with col4:
        commandes_livrees = len(df_commandes[df_commandes['Statut'] == 'Livrée'])
        st.metric("📦 Commandes Livrées", commandes_livrees)

    # Graphiques
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Évolution des Commandes")
        df_commandes['Date_Commande'] = pd.to_datetime(df_commandes['Date_Commande'])
        monthly_orders = df_commandes.groupby(df_commandes['Date_Commande'].dt.to_period('M'))['Montant_Total'].sum()

        fig = px.line(x=monthly_orders.index.astype(str), y=monthly_orders.values,
                     title="Montant des Commandes par Mois")
        fig.update_traces(line_color='#1f77b4')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Statut des Commandes")
        status_counts = df_commandes['Statut'].value_counts()

        fig = px.pie(values=status_counts.values, names=status_counts.index,
                    title="Répartition par Statut")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

def kpi_fournisseurs_page():
    """Page KPI des fournisseurs"""
    st.markdown('<div class="main-header"><h1>📊 KPI Fournisseurs</h1></div>', unsafe_allow_html=True)

    df_fournisseurs = st.session_state.df_fournisseurs

    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        categories = ['Tous'] + list(df_fournisseurs['Categorie'].unique())
        cat_filter = st.selectbox("Catégorie", categories)

    with col2:
        pays = ['Tous'] + list(df_fournisseurs['Pays'].unique())
        pays_filter = st.selectbox("Pays", pays)

    with col3:
        statuts = ['Tous'] + list(df_fournisseurs['Statut'].unique())
        statut_filter = st.selectbox("Statut", statuts)

    # Appliquer les filtres
    df_filtered = df_fournisseurs.copy()
    if cat_filter != 'Tous':
        df_filtered = df_filtered[df_filtered['Categorie'] == cat_filter]
    if pays_filter != 'Tous':
        df_filtered = df_filtered[df_filtered['Pays'] == pays_filter]
    if statut_filter != 'Tous':
        df_filtered = df_filtered[df_filtered['Statut'] == statut_filter]

    # KPI principaux
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        score_moyen = df_filtered['Score_Qualite'].mean()
        st.metric("📊 Score Qualité Moyen", f"{score_moyen:.1f}/10")

    with col2:
        delai_moyen = df_filtered['Delai_Moyen_Livraison'].mean()
        st.metric("⏱️ Délai Moyen", f"{delai_moyen:.1f} jours")

    with col3:
        taux_conformite = df_filtered['Taux_Conformite'].mean()
        st.metric("✅ Taux Conformité", f"{taux_conformite:.1f}%")

    with col4:
        ca_moyen = df_filtered['CA_Total'].mean()
        st.metric("💰 CA Moyen", f"{ca_moyen:,.0f} €")

    # Graphiques détaillés
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏆 Top 10 Fournisseurs par Performance")
        top_fournisseurs = df_filtered.nlargest(10, 'Note_Performance')

        fig = px.bar(top_fournisseurs, x='Note_Performance', y='Nom_Fournisseur',
                    orientation='h', title="Classement par Performance")
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📊 Distribution des Scores Qualité")

        fig = px.histogram(df_filtered, x='Score_Qualite', nbins=20,
                          title="Répartition des Scores Qualité")
        fig.update_traces(marker_color='#ff7f0e')
        st.plotly_chart(fig, use_container_width=True)

    # Tableau détaillé
    st.markdown("### 📋 Liste Détaillée des Fournisseurs")

    columns_to_show = [
        'Nom_Fournisseur', 'Categorie', 'Pays', 'Score_Qualite',
        'Delai_Moyen_Livraison', 'Taux_Conformite', 'CA_Total', 'Statut'
    ]

    st.dataframe(
        df_filtered[columns_to_show],
        use_container_width=True,
        hide_index=True
    )

def kpi_acheteurs_page():
    """Page KPI des acheteurs - NOUVELLE FONCTIONNALITÉ"""
    st.markdown('<div class="main-header"><h1>🛒 KPI Acheteurs</h1></div>', unsafe_allow_html=True)

    df_acheteurs = st.session_state.df_acheteurs
    df_commandes = st.session_state.df_commandes

    # KPI principaux des acheteurs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        budget_total = df_acheteurs['Budget_Alloue'].sum()
        st.metric("💰 Budget Total", f"{budget_total:,.0f} €")

    with col2:
        economies_totales = df_acheteurs['Economies_Realisees'].sum()
        st.metric("💸 Économies Totales", f"{economies_totales:,.0f} €")

    with col3:
        performance_moyenne = df_acheteurs['Score_Performance'].mean()
        st.metric("📊 Performance Moyenne", f"{performance_moyenne:.1f}/10")

    with col4:
        delai_moyen = df_acheteurs['Delai_Moyen_Traitement'].mean()
        st.metric("⚡ Délai Moyen", f"{delai_moyen:.1f} jours")

    # Graphiques détaillés
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏆 Performance des Acheteurs")

        fig = px.bar(df_acheteurs, x='Nom_Acheteur', y='Score_Performance',
                    title="Score de Performance par Acheteur",
                    color='Score_Performance', color_continuous_scale='Viridis')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 💰 Utilisation du Budget")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Budget Alloué',
            x=df_acheteurs['Nom_Acheteur'],
            y=df_acheteurs['Budget_Alloue'],
            marker_color='lightblue'
        ))
        fig.add_trace(go.Bar(
            name='Budget Utilisé',
            x=df_acheteurs['Nom_Acheteur'],
            y=df_acheteurs['Budget_Utilise'],
            marker_color='darkblue'
        ))

        fig.update_layout(title='Comparaison Budget Alloué vs Utilisé', barmode='group')
        st.plotly_chart(fig, use_container_width=True)

    # Analyse détaillée par acheteur
    st.markdown("### 🔍 Analyse Détaillée par Acheteur")

    acheteur_selected = st.selectbox(
        "Sélectionner un acheteur",
        df_acheteurs['Nom_Acheteur'].tolist()
    )

    acheteur_data = df_acheteurs[df_acheteurs['Nom_Acheteur'] == acheteur_selected].iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📊 Métriques Clés")
        st.write(f"**Département:** {acheteur_data['Departement']}")
        st.write(f"**Spécialité:** {acheteur_data['Specialite']}")
        st.write(f"**Nombre de commandes:** {acheteur_data['Nombre_Commandes']}")
        st.write(f"**Fournisseurs gérés:** {acheteur_data['Nombre_Fournisseurs_Geres']}")

    with col2:
        st.markdown("#### 💰 Performance Financière")
        taux_utilisation = (acheteur_data['Budget_Utilise'] / acheteur_data['Budget_Alloue']) * 100
        st.write(f"**Taux d'utilisation:** {taux_utilisation:.1f}%")
        st.write(f"**Taux d'économie:** {acheteur_data['Taux_Economie']}%")

        # Progression vers objectif
        progression_objectif = (acheteur_data['Economies_Realisees'] / acheteur_data['Objectif_Economies']) * 100
        st.write(f"**Progression objectif:** {progression_objectif:.1f}%")

    with col3:
        st.markdown("#### 🎯 Évaluation")
        st.write(f"**Score performance:** {acheteur_data['Score_Performance']}/10")
        st.write(f"**Note manager:** {acheteur_data['Note_Manager']}/10")
        st.write(f"**Certification:** {acheteur_data['Certification']}")
        st.write(f"**Statut:** {acheteur_data['Statut']}")

    # Tableau récapitulatif
    st.markdown("### 📋 Tableau de Bord Acheteurs")

    columns_acheteurs = [
        'Nom_Acheteur', 'Departement', 'Score_Performance', 'Budget_Alloue',
        'Budget_Utilise', 'Economies_Realisees', 'Taux_Economie', 'Statut'
    ]

    st.dataframe(
        df_acheteurs[columns_acheteurs],
        use_container_width=True,
        hide_index=True
    )

def add_data_page():
    """Page d'ajout de nouvelles données"""
    if not has_permission(st.session_state.user_data, "ecriture"):
        st.error("❌ Vous n'avez pas les permissions pour ajouter des données")
        return

    st.markdown('<div class="main-header"><h1>➕ Ajouter Nouvelles Données</h1></div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏢 Nouveau Fournisseur", "👤 Nouvel Acheteur", "📦 Nouvelle Commande"])

    with tab1:
        st.markdown("### 🏢 Ajouter un Nouveau Fournisseur")

        with st.form("add_fournisseur"):
            col1, col2 = st.columns(2)

            with col1:
                nom = st.text_input("Nom du Fournisseur *")
                categorie = st.selectbox("Catégorie", 
                    ["Électronique", "Mécanique", "Chimique", "Textile", "Alimentaire", "Services"])
                pays = st.selectbox("Pays", 
                    ["France", "Allemagne", "Italie", "Espagne", "Maroc", "Tunisie", "Chine", "USA"])
                email = st.text_input("Email")
                telephone = st.text_input("Téléphone")

            with col2:
                score_qualite = st.slider("Score Qualité", 0.0, 10.0, 8.0, 0.1)
                delai_livraison = st.number_input("Délai Moyen Livraison (jours)", 1, 30, 7)
                taux_conformite = st.slider("Taux Conformité (%)", 0.0, 100.0, 95.0)
                certification_iso = st.selectbox("Certification ISO", ["Oui", "Non"])
                delai_paiement = st.selectbox("Délai Paiement", [30, 45, 60, 90])

            submit = st.form_submit_button("Ajouter Fournisseur", use_container_width=True)

            if submit and nom:
                # Générer nouvel ID
                max_id = st.session_state.df_fournisseurs['ID_Fournisseur'].str.extract('(\d+)').astype(int).max().iloc[0]
                new_id = f"F{str(max_id + 1).zfill(3)}"

                nouveau_fournisseur = {
                    'ID_Fournisseur': new_id,
                    'Nom_Fournisseur': nom,
                    'Categorie': categorie,
                    'Pays': pays,
                    'Date_Creation': datetime.now().strftime('%Y-%m-%d'),
                    'Contact_Email': email,
                    'Telephone': telephone,
                    'Score_Qualite': score_qualite,
                    'Delai_Moyen_Livraison': delai_livraison,
                    'Taux_Conformite': taux_conformite,
                    'Prix_Moyen_Commande': 0.0,
                    'Nombre_Commandes': 0,
                    'CA_Total': 0.0,
                    'Statut': 'En_Evaluation',
                    'Note_Performance': score_qualite,
                    'Certification_ISO': certification_iso,
                    'Delai_Paiement': delai_paiement,
                    'Responsable_Compte': st.session_state.user_data['nom_complet']
                }

                # Ajouter à la base de données
                new_df = pd.DataFrame([nouveau_fournisseur])
                st.session_state.df_fournisseurs = pd.concat([st.session_state.df_fournisseurs, new_df], ignore_index=True)

                # Logger l'action
                log_action(st.session_state.username, "Création fournisseur", "Fournisseurs", new_id, f"Nouveau fournisseur: {nom}")

                # Sauvegarder
                if save_data():
                    st.success(f"✅ Fournisseur '{nom}' ajouté avec succès (ID: {new_id})")
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de la sauvegarde")
            elif submit and not nom:
                st.error("❌ Le nom du fournisseur est obligatoire")

    with tab2:
        st.markdown("### 👤 Ajouter un Nouvel Acheteur")

        with st.form("add_acheteur"):
            col1, col2 = st.columns(2)

            with col1:
                nom_acheteur = st.text_input("Nom Complet *")
                email_acheteur = st.text_input("Email *")
                departement = st.selectbox("Département", 
                    ["Achats Généraux", "Achats IT", "Achats Production", "Achats Services"])
                specialite = st.selectbox("Spécialité", 
                    ["Électronique", "Mécanique", "Services", "IT", "Matières Premières"])

            with col2:
                budget_alloue = st.number_input("Budget Alloué (€)", 0.0, 1000000.0, 100000.0)
                objectif_economies = st.number_input("Objectif Économies (€)", 0.0, 100000.0, 20000.0)
                certification = st.selectbox("Certification", ["CIPS", "CDAF", "Aucune"])
                statut_acheteur = st.selectbox("Statut", ["Actif", "En Formation", "Senior"])

            submit_acheteur = st.form_submit_button("Ajouter Acheteur", use_container_width=True)

            if submit_acheteur and nom_acheteur and email_acheteur:
                # Générer nouvel ID
                max_id = st.session_state.df_acheteurs['ID_Acheteur'].str.extract('(\d+)').astype(int).max().iloc[0]
                new_id = f"A{str(max_id + 1).zfill(3)}"

                nouvel_acheteur = {
                    'ID_Acheteur': new_id,
                    'Nom_Acheteur': nom_acheteur,
                    'Email': email_acheteur,
                    'Departement': departement,
                    'Date_Embauche': datetime.now().strftime('%Y-%m-%d'),
                    'Specialite': specialite,
                    'Budget_Alloue': budget_alloue,
                    'Budget_Utilise': 0.0,
                    'Nombre_Commandes': 0,
                    'Valeur_Commandes': 0.0,
                    'Economies_Realisees': 0.0,
                    'Taux_Economie': 0.0,
                    'Delai_Moyen_Traitement': 5,
                    'Score_Performance': 8.0,
                    'Objectif_Economies': objectif_economies,
                    'Statut': statut_acheteur,
                    'Certification': certification,
                    'Nombre_Fournisseurs_Geres': 0,
                    'Note_Manager': 8.0
                }

                # Ajouter à la base de données
                new_df = pd.DataFrame([nouvel_acheteur])
                st.session_state.df_acheteurs = pd.concat([st.session_state.df_acheteurs, new_df], ignore_index=True)

                # Logger l'action
                log_action(st.session_state.username, "Création acheteur", "Acheteurs", new_id, f"Nouvel acheteur: {nom_acheteur}")

                # Sauvegarder
                if save_data():
                    st.success(f"✅ Acheteur '{nom_acheteur}' ajouté avec succès (ID: {new_id})")
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de la sauvegarde")
            elif submit_acheteur:
                st.error("❌ Nom et email sont obligatoires")

def edit_data_page():
    """Page de modification/suppression des données - NOUVELLE FONCTIONNALITÉ"""
    if not has_permission(st.session_state.user_data, "ecriture"):
        st.error("❌ Vous n'avez pas les permissions pour modifier des données")
        return

    st.markdown('<div class="main-header"><h1>✏️ Modifier / Supprimer Données</h1></div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏢 Fournisseurs", "👤 Acheteurs", "📦 Commandes"])

    with tab1:
        st.markdown("### ✏️ Modifier/Supprimer Fournisseurs")

        df_fournisseurs = st.session_state.df_fournisseurs

        # Sélection du fournisseur
        fournisseur_names = df_fournisseurs['Nom_Fournisseur'].tolist()
        selected_fournisseur = st.selectbox("Sélectionner un fournisseur", fournisseur_names)

        if selected_fournisseur:
            fournisseur_data = df_fournisseurs[df_fournisseurs['Nom_Fournisseur'] == selected_fournisseur].iloc[0]

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown("#### ✏️ Modifier les Informations")

                with st.form("edit_fournisseur"):
                    col_a, col_b = st.columns(2)

                    with col_a:
                        new_nom = st.text_input("Nom", value=fournisseur_data['Nom_Fournisseur'])
                        new_score = st.slider("Score Qualité", 0.0, 10.0, float(fournisseur_data['Score_Qualite']), 0.1)
                        new_delai = st.number_input("Délai Livraison", 1, 30, int(fournisseur_data['Delai_Moyen_Livraison']))

                    with col_b:
                        new_statut = st.selectbox("Statut", ["Actif", "En_Evaluation", "Suspendu"], 
                                                index=["Actif", "En_Evaluation", "Suspendu"].index(fournisseur_data['Statut']))
                        new_taux = st.slider("Taux Conformité", 0.0, 100.0, float(fournisseur_data['Taux_Conformite']))
                        new_performance = st.slider("Note Performance", 0.0, 10.0, float(fournisseur_data['Note_Performance']), 0.1)

                    submit_edit = st.form_submit_button("💾 Sauvegarder Modifications", use_container_width=True)

                    if submit_edit:
                        # Mettre à jour les données
                        index = df_fournisseurs[df_fournisseurs['Nom_Fournisseur'] == selected_fournisseur].index[0]

                        st.session_state.df_fournisseurs.loc[index, 'Nom_Fournisseur'] = new_nom
                        st.session_state.df_fournisseurs.loc[index, 'Score_Qualite'] = new_score
                        st.session_state.df_fournisseurs.loc[index, 'Delai_Moyen_Livraison'] = new_delai
                        st.session_state.df_fournisseurs.loc[index, 'Statut'] = new_statut
                        st.session_state.df_fournisseurs.loc[index, 'Taux_Conformite'] = new_taux
                        st.session_state.df_fournisseurs.loc[index, 'Note_Performance'] = new_performance

                        # Logger l'action
                        log_action(st.session_state.username, "Modification fournisseur", "Fournisseurs", 
                                 fournisseur_data['ID_Fournisseur'], f"Modification: {selected_fournisseur}")

                        # Sauvegarder
                        if save_data():
                            st.success("✅ Modifications sauvegardées")
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la sauvegarde")

            with col2:
                st.markdown("#### 🗑️ Supprimer")
                st.write(f"**ID:** {fournisseur_data['ID_Fournisseur']}")
                st.write(f"**Statut:** {fournisseur_data['Statut']}")
                st.write(f"**CA Total:** {fournisseur_data['CA_Total']:,.0f} €")

                if st.button("🗑️ Supprimer Fournisseur", type="secondary"):
                    # Confirmation de suppression
                    if st.checkbox(f"⚠️ Confirmer suppression de {selected_fournisseur}"):
                        if has_permission(st.session_state.user_data, "suppression") or st.session_state.user_data['role'] == 'Admin':
                            # Supprimer le fournisseur
                            st.session_state.df_fournisseurs = st.session_state.df_fournisseurs[
                                st.session_state.df_fournisseurs['Nom_Fournisseur'] != selected_fournisseur
                            ]

                            # Logger l'action
                            log_action(st.session_state.username, "Suppression fournisseur", "Fournisseurs",
                                     fournisseur_data['ID_Fournisseur'], f"Suppression: {selected_fournisseur}")

                            # Sauvegarder
                            if save_data():
                                st.success(f"✅ Fournisseur '{selected_fournisseur}' supprimé")
                                st.rerun()
                            else:
                                st.error("❌ Erreur lors de la suppression")
                        else:
                            st.error("❌ Permissions insuffisantes pour supprimer")

def analytics_page():
    """Page d'analyses avancées"""
    st.markdown('<div class="main-header"><h1>📈 Analyses Avancées</h1></div>', unsafe_allow_html=True)

    df_fournisseurs = st.session_state.df_fournisseurs
    df_acheteurs = st.session_state.df_acheteurs
    df_commandes = st.session_state.df_commandes

    # Analyses croisées
    st.markdown("### 🔍 Analyses Croisées")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🌍 Performance par Pays")

        # Grouper par pays et calculer les moyennes
        perf_pays = df_fournisseurs.groupby('Pays').agg({
            'Score_Qualite': 'mean',
            'Delai_Moyen_Livraison': 'mean',
            'Taux_Conformite': 'mean',
            'CA_Total': 'sum'
        }).round(1)

        fig = px.scatter(perf_pays.reset_index(), 
                        x='Score_Qualite', y='Taux_Conformite',
                        size='CA_Total', color='Pays',
                        title="Score Qualité vs Taux Conformité par Pays",
                        hover_data=['Delai_Moyen_Livraison'])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Correlation Métriques")

        # Matrice de corrélation
        metrics_cols = ['Score_Qualite', 'Delai_Moyen_Livraison', 'Taux_Conformite', 'Note_Performance']
        corr_matrix = df_fournisseurs[metrics_cols].corr()

        fig = px.imshow(corr_matrix, 
                       text_auto=True, aspect="auto",
                       title="Corrélations entre Métriques",
                       color_continuous_scale='RdYlBu')
        st.plotly_chart(fig, use_container_width=True)

    # Analyses temporelles
    st.markdown("### ⏱️ Analyses Temporelles")

    # Convertir les dates
    df_commandes['Date_Commande'] = pd.to_datetime(df_commandes['Date_Commande'])

    # Évolution mensuelle détaillée
    monthly_data = df_commandes.groupby(df_commandes['Date_Commande'].dt.to_period('M')).agg({
        'Montant_Total': ['sum', 'count', 'mean'],
        'Note_Qualite': 'mean'
    }).round(2)

    monthly_data.columns = ['CA_Total', 'Nb_Commandes', 'Montant_Moyen', 'Qualite_Moyenne']
    monthly_data = monthly_data.reset_index()
    monthly_data['Date_Commande'] = monthly_data['Date_Commande'].astype(str)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(monthly_data, x='Date_Commande', y='CA_Total',
                     title="Évolution du Chiffre d'Affaires")
        fig.update_traces(line_color='#1f77b4')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(monthly_data, x='Date_Commande', y='Nb_Commandes',
                    title="Nombre de Commandes par Mois")
        fig.update_traces(marker_color='#ff7f0e')
        st.plotly_chart(fig, use_container_width=True)

    # Export des données
    st.markdown("### 📥 Export des Données")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Exporter Fournisseurs CSV"):
            csv = df_fournisseurs.to_csv(index=False)
            st.download_button(
                label="⬇️ Télécharger CSV",
                data=csv,
                file_name=f"fournisseurs_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    with col2:
        if st.button("👤 Exporter Acheteurs CSV"):
            csv = df_acheteurs.to_csv(index=False)
            st.download_button(
                label="⬇️ Télécharger CSV",
                data=csv,
                file_name=f"acheteurs_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    with col3:
        if st.button("📦 Exporter Commandes CSV"):
            csv = df_commandes.to_csv(index=False)
            st.download_button(
                label="⬇️ Télécharger CSV",
                data=csv,
                file_name=f"commandes_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

def user_management_page():
    """Page de gestion des utilisateurs"""
    if not has_permission(st.session_state.user_data, "gestion_utilisateurs"):
        st.error("❌ Vous n'avez pas les permissions pour gérer les utilisateurs")
        return

    st.markdown('<div class="main-header"><h1>👥 Gestion des Utilisateurs</h1></div>', unsafe_allow_html=True)

    users_db = load_users()

    # Affichage des utilisateurs existants
    st.markdown("### 📋 Utilisateurs Existants")

    users_list = []
    for username, data in users_db.items():
        users_list.append({
            'Nom d'utilisateur': username,
            'Nom complet': data['nom_complet'],
            'Email': data['email'],
            'Rôle': data['role'],
            'Dernière connexion': data['derniere_connexion']
        })

    if users_list:
        df_users = pd.DataFrame(users_list)
        st.dataframe(df_users, use_container_width=True, hide_index=True)

    # Historique des actions
    st.markdown("### 📊 Historique des Actions")

    df_historique = st.session_state.df_historique

    # Filtrer par utilisateur
    user_filter = st.selectbox("Filtrer par utilisateur", ['Tous'] + df_historique['Utilisateur'].unique().tolist())

    if user_filter != 'Tous':
        df_hist_filtered = df_historique[df_historique['Utilisateur'] == user_filter]
    else:
        df_hist_filtered = df_historique

    # Afficher les dernières actions
    latest_actions = df_hist_filtered.head(20)[
        ['Date_Action', 'Utilisateur', 'Action', 'Table_Modifiee', 'ID_Enregistrement', 'Commentaire']
    ]

    st.dataframe(latest_actions, use_container_width=True, hide_index=True)

# Point d'entrée principal
def main():
    """Fonction principale de l'application"""
    init_session()

    # Vérifier l'authentification
    if not st.session_state.authenticated:
        login_page()
    else:
        main_interface()

if __name__ == "__main__":
    main()
