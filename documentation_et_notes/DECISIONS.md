# Fiche de décisions 

Cette fiche récapitule les choix du projet. Les options ci-dessous comprennent les alternatives discutées ou envisagées dans le cadre du projet ; les validations de l'auxiliaire doivent être renseignées à partir des échanges réels, sans inventer de date.

## Domaine

-   **Options :** Estimation de recettes ; classification du succès commercial
-   **Choix et justification :** Cinéma et prédiction de blockbusters : sujet concret et compréhensible, adapté à une application interactive.
   

## Jeu de données

-   **Options :** Données cinématographiques réelles ; jeu synthétique tabulaire
-   **Choix et justification :** [What Makes a Movie a Blockbuster? 5,000 Films](https://www.kaggle.com/datasets/vedauv/what-makes-a-movie-a-blockbuster-5000-films), au format CSV, avec une cible binaire et des variables numériques et catégorielles. 
   

## Cible

-   **Options :** Revenu (régression) ; statut blockbuster (classification)
-   **Choix et justification :** `blockbuster` : classification binaire Résultat facilement interprétable par l'utilisateur.
 

## Variables d'entrée

-   **Options :** Toutes les colonnes ; sélection des caractéristiques pertinentes
-   **Choix et justification :** Utiliser des caractéristiques telles que genre, budget, note et durée ; exclure les variables qui révèlent la cible, comme le revenu et le ROI.

## Métrique

-   **Options :** Accuracy ; précision ; rappel ; F1-score
-   **Choix et justification :** F1-score de la classe positive, car les blockbusters sont minoritaires. Il équilibre précision et rappel.


## Modèle

-   **Options :** Régression logistique ; arbre de décision ; forêt aléatoire
-   **Choix et justification :** Forêt aléatoire : plusieurs arbres combinés pour représenter des relations non linéaires et limiter la dépendance à un arbre unique.
  
## Prétraitement

-   **Options :** Encodage manuel avec `get_dummies` ; `OneHotEncoder` et `ColumnTransformer`
-   **Choix et justification :** Prétraitement intégré à la pipeline afin de traiter les catégories de manière cohérente entre entraînement et prédiction.


## Évaluation et réglages

-   **Options :** Séparation entraînement/test ; séparation entraînement/validation/test ; paramètres manuels
-   **Choix et justification :** Séparation reproductible et stratifiée, avec `GridSearchCV` pour rechercher les paramètres selon le F1-score. Répartition 60/20/20 et sélection du seuil parmi 100 valeurs sur la validation, puis évaluation indépendante sur le test.

## Interface

-   **Options :** Tkinter ; PyQt6
-   **Choix et justification :** PyQt6 pour organiser le formulaire, les boutons, les fenêtres secondaires et les tableaux.
 

## Graphique

-   **Options :** Graphique externe au lancement ; graphique intégré
-   **Choix et justification :** Matrice de confusion accessible via l'interface, afin de présenter les erreurs et réussites du modèle à la demande, avec effectifs et pourcentages par vraie catégorie.


## Historique

-   **Options :** CSV ; JSON ; stockage uniquement en mémoire
-   **Choix et justification :** JSON pour conserver les dictionnaires de prédictions après fermeture et les afficher dans un tableau.