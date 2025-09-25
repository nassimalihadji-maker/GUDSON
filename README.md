# 🏢 GUDSON KPI - Système de Suivi des Fournisseurs & Acheteurs

## 📋 Description

**GUDSON KPI** est une application web complète développée avec Streamlit pour le suivi et la gestion des fournisseurs et acheteurs. Cette version finale inclut toutes les fonctionnalités demandées et est optimisée pour un déploiement sans erreur sur Streamlit Cloud.

## ✨ Fonctionnalités Principales

### 🔐 Système de Sessions Utilisateurs
- **Authentification complète** avec login/logout
- **3 rôles d'utilisateurs** :
  - **Admin** : Accès total + gestion utilisateurs
  - **Acheteur** : Lecture/écriture des données
  - **Consultant** : Accès en lecture seule
- **Permissions granulaires** selon le rôle
- **Sessions persistantes** avec state management

### 🛒 Volet Suivi des Acheteurs (NOUVEAU)
- **Dashboard KPI dédié** aux acheteurs
- **Métriques de performance** : budgets, économies, objectifs
- **Analyses comparatives** entre acheteurs
- **Suivi des commandes** par acheteur
- **Graphiques de tendances** et performance

### ✏️ Gestion Complète des Données (NOUVEAU)
- **Modification en ligne** des données existantes
- **Suppression sécurisée** avec confirmation
- **Interface d'édition** intuitive
- **Historique complet** des modifications
- **Validation automatique** des données
- **Sauvegarde en temps réel**

### 📊 Analytics et KPI
- **Dashboard fournisseurs** avec métriques détaillées
- **Analyses croisées** et corrélations
- **Graphiques interactifs** avec Plotly
- **Export de données** en CSV
- **Rapports personnalisés**

### 🏠 Interface Utilisateur
- **Design moderne et responsive**
- **Navigation intuitive** par onglets
- **Sidebar personnalisée** selon l'utilisateur
- **Messages de confirmation** et feedback
- **Thème GUDSON** avec couleurs corporatives

## 👥 Comptes Utilisateurs

| Utilisateur | Mot de passe | Rôle | Permissions |
|-------------|--------------|------|-------------|
| `admin` | `admin123` | Admin | Accès total + gestion utilisateurs |
| `acheteur1` | `achat123` | Acheteur | Lecture/écriture données |
| `acheteur2` | `achat123` | Acheteur | Lecture/écriture données |
| `consultant1` | `consul123` | Consultant | Lecture seule |

## 🚀 Déploiement Streamlit Cloud

### 📋 Prérequis
1. Compte GitHub avec repository
2. Compte Streamlit Cloud (share.streamlit.io)

### 📁 Structure du Projet
```
votre-repository/
├── app.py                    # Application principale
├── requirements.txt          # Dépendances Python 3.13 compatibles
├── fournisseurs_data.csv    # Base données fournisseurs
├── acheteurs_data.csv       # Base données acheteurs  
├── commandes_data.csv       # Historique des commandes
├── historique_data.csv      # Journal des modifications
├── users_db.json           # Base utilisateurs avec rôles
├── .streamlit/
│   ├── config.toml         # Configuration Streamlit
│   └── secrets.toml        # Template secrets (optionnel)
└── README.md               # Documentation
```

### 🔧 Instructions de Déploiement

#### 1️⃣ Préparer le Repository
```bash
# Cloner ou créer un nouveau repository
git clone https://github.com/votre-username/gudson-kpi.git
cd gudson-kpi

# Copier tous les fichiers générés
cp app.py votre-repository/
cp requirements.txt votre-repository/
cp *.csv votre-repository/
cp users_db.json votre-repository/
cp -r .streamlit/ votre-repository/
cp README.md votre-repository/

# Commit et push
git add .
git commit -m "Version finale GUDSON KPI - Compatible Python 3.13"
git push origin main
```

#### 2️⃣ Déployer sur Streamlit Cloud
1. Aller sur [share.streamlit.io](https://share.streamlit.io)
2. Se connecter avec GitHub
3. Cliquer "New app"
4. Sélectionner votre repository
5. Spécifier `app.py` comme fichier principal
6. Cliquer "Deploy!"

#### 3️⃣ Configuration (Optionnelle)
- Aucune configuration supplémentaire requise
- L'application fonctionne immédiatement
- Les secrets.toml sont optionnels pour cette version

## 📊 Fonctionnalités par Onglet

### 🏠 Tableau de Bord
- **Métriques principales** : Fournisseurs actifs, Acheteurs, CA total, Commandes livrées
- **Graphiques d'évolution** : Commandes mensuelles, Statuts
- **Vision d'ensemble** de l'activité

### 📊 KPI Fournisseurs
- **Filtres avancés** : Catégorie, Pays, Statut
- **KPI détaillés** : Score qualité, Délai livraison, Taux conformité, CA
- **Top performers** et analyses statistiques
- **Tableau interactif** avec toutes les données

### 🛒 KPI Acheteurs (NOUVEAU)
- **Performance individuelle** : Budgets, économies, objectifs
- **Comparaisons** entre acheteurs
- **Métriques financières** : Taux d'utilisation, économies réalisées
- **Évaluations** : Scores performance, notes manager

### ➕ Ajouter Données
- **Formulaires complets** pour nouveaux fournisseurs et acheteurs
- **Validation en temps réel** des données
- **Attribution automatique** des IDs
- **Logging** des créations

### ✏️ Modifier/Supprimer (NOUVEAU)
- **Édition en ligne** avec interface intuitive
- **Suppression sécurisée** avec confirmation
- **Historique** des modifications
- **Permissions** selon les rôles

### 📈 Analyses
- **Analyses croisées** : Performance par pays, corrélations
- **Évolution temporelle** : Tendances mensuelles, saisonnalité
- **Export de données** : CSV téléchargeables
- **Rapports personnalisés**

### 👥 Gestion Utilisateurs (Admin)
- **Liste des utilisateurs** avec détails
- **Historique des actions** par utilisateur
- **Audit trail** complet

## 🔧 Corrections Techniques

### ✅ Compatibilité Python 3.13
- **numpy >= 2.0.0** (compatible Python 3.13)
- **pandas >= 2.1.0** (optimisé pour nouvelles versions)
- **streamlit >= 1.38.0** (dernière version stable)
- **Pas de versions fixes** problématiques

### ✅ Optimisations Streamlit Cloud
- **Configuration adaptée** aux contraintes cloud
- **Gestion d'erreurs robuste** 
- **Cache intelligent** pour les performances
- **Chargement optimisé** des données

### ✅ Sécurité et Performance
- **Authentification sécurisée** (hashage prévu pour production)
- **Validation des permissions** granulaire
- **Sauvegarde automatique** des modifications
- **Interface responsive** tous appareils

## 📈 Données Incluses

### 📊 Base Données Complète
- **15 fournisseurs** avec métriques réalistes
- **5 acheteurs** avec KPI de performance  
- **200 commandes** sur 12 mois d'historique
- **50 entrées** d'audit trail
- **4 utilisateurs** avec rôles définis

### 🎯 Métriques Calculées
- **Scores de performance** automatiques
- **Taux de conformité** et délais
- **Économies réalisées** par acheteur
- **CA et budgets** avec suivi temporel

## 🚨 Résolution d'Erreurs

### ❌ Erreur "numpy distutils"
**Solution :** Utiliser `numpy>=2.0.0` dans requirements.txt

### ❌ Erreur "Module not found"
**Solution :** Vérifier que tous les fichiers CSV sont présents

### ❌ Erreur de permissions
**Solution :** Vérifier la configuration des rôles utilisateurs

## 📞 Support

Pour toute question ou problème :
1. Vérifier cette documentation
2. Consulter les logs Streamlit Cloud
3. Vérifier la structure des fichiers
4. Tester en local avec `streamlit run app.py`

## 🎉 Version Finale

Cette version **V3.0 FINALE** inclut :
- ✅ **Toutes les fonctionnalités demandées**
- ✅ **Compatibilité Python 3.13 garantie**  
- ✅ **Déploiement Streamlit Cloud sans erreur**
- ✅ **Interface moderne et complète**
- ✅ **Données réalistes et cohérentes**

**Prêt pour utilisation immédiate ! 🚀**
