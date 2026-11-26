import os 
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
import joblib

try:
    from .donnees import DataManager
except ImportError:
    from donnees import DataManager


class ModeleBlockbuster:
    """
    Gestionnaire du modèle de prédiction de Blockbuster.
    """
    _meilleur_f1: float
    DOSSIER_EXECUTION = Path(__file__).resolve().parent.parent / "donnees_execution"
    CHEMIN_HISTORIQUE = DOSSIER_EXECUTION / "historique.json"
    CHEMIN_MODELE = DOSSIER_EXECUTION / "joblib_save"

    def __init__(self, data_manager:DataManager):
        """ 
        Création du modèle.
        """
        self.DOSSIER_EXECUTION.mkdir(parents=True, exist_ok=True)
        self.chemin_historique = self.CHEMIN_HISTORIQUE
        self.data_manager = data_manager
        self._matrice_confusion = None
        self._grille_recherche = GridSearchCV(
                    estimator = self.pipeline,   # regroupe toutes des information (préparation et entraînement)
                    param_grid = self.grille_parametres, 
                    scoring = "f1", 
                    cv = 5, 
                    n_jobs= -1
                )

    @property
    def grille_parametres(self) -> dict:
        "Grille des paramètres et des valeurs essayées par GridSearchCV"
        return {
                    "rf__n_estimators": [100, 200], 
                    "rf__max_depth": [6, 10, 15, None],
                    "rf__min_samples_split": [2, 5, 10],
                    "rf__class_weight": ['balanced', 'balanced_subsample', None]
                }

    @property 
    def pipeline(self) -> Pipeline:
        """
        Creation de Pipeline pour RandomForestClassifier

        NOTE: Le rôle de la pipeline c'est essentiellement de 
        contenir les informations nécessaires pour que le programme 
        fasse son étape de traitement des données et d'entraînement 
        sans faire plusieurs lignes de code.
        """
        donnees_traitees = self.data_manager.donnees_traitees
        return Pipeline([
            ("preparation", donnees_traitees),
            ("rf", RandomForestClassifier(random_state=42, n_jobs=1))
        ])

    @property 
    def matrice_confusion(self):
        return self._matrice_confusion

    @matrice_confusion.setter
    def matrice_confusion(self, informations_matrice_confusion:tuple[pd.DataFrame, np.ndarray, list[int]]):
        y_test, predictions_test, labels = informations_matrice_confusion
        self._matrice_confusion = confusion_matrix(y_test, predictions_test, labels=labels)

    @property
    def grille_recherche(self) -> GridSearchCV:
        return self._grille_recherche

    @grille_recherche.setter
    def grille_recherche(self, nouvelle_grille:GridSearchCV):
        self._grille_recherche = nouvelle_grille
        

    @property
    def meilleur_seuil(self):
        try:
            return self._meilleur_seuil
        except:
            return "Modèle n'est pas encore entraîné."

    @meilleur_seuil.setter 
    def meilleur_seuil(self, nouveau_seuil:float) -> None:
        self._meilleur_seuil = nouveau_seuil

    @property
    def meilleur_f1(self):
        try:
            return self._meilleur_f1
        except:
            return "Modèle n'est pas encore entraîné."

    @meilleur_f1.setter 
    def meilleur_f1(self, nouvel_f1:float) -> None:
        self._meilleur_f1 = nouvel_f1

    @property
    def grille_entrainee(self):
        try:
            return self._grille_entrainee
        except:
            return "Modèle n'est pas encore entraîné."

    @grille_entrainee.setter 
    def grille_entrainee(self, nouvelle_grille_entrainee:GridSearchCV) -> None:
        self._grille_entrainee = nouvelle_grille_entrainee

    def entrainer(self, X: pd.DataFrame, y: pd.Series) -> float:
        """
        Entraîne le modèle et retourne le F1 score.
        """
        colonnes_entree = list(X.columns)

        # Entraînement (séparation des données)
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y,
            test_size=0.4,
            random_state=42,
            stratify=y
        )

        # Test (séparation des données)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp,
            test_size=0.5,
            random_state=42,
            stratify=y_temp
        )

        # Entraînement 
        self.grille_entrainee = self.grille_recherche.fit(X_train, y_train)

        # Recherche du meilleur seuil (données de test utilisées, celles qu'on a séparé plus haut)
        # En gros, vu que tout est débalancé on veut savoir c'est quoi le tipping point auquel le model se dit qu'il dit que c'est un blockbuster 
        # On veut faire en sorte que notre tipping point laisse passer plus de blockbusters parce qu'actuellement il y a beaucoup de faux-négatifs
        probas_val = self.grille_recherche.predict_proba(X_val)[:, 1]

        seuils = np.linspace(0.01, 0.99, 100)
        meilleur_f1 = 0.0
        meilleur_seuil = 0.5    # On part que le default est le meilleur et on itère

        for seuil in seuils:
            predictions_seuil = (probas_val >= seuil).astype(int)
            score = float(f1_score(y_val, predictions_seuil))
            if score > meilleur_f1:
                meilleur_f1 = score 
                meilleur_seuil = float(seuil)

        self.meilleur_seuil = meilleur_seuil
        self.meilleur_f1 = float(meilleur_f1)

        # Évaluation sur les données de test
        probas_test = self.grille_recherche.predict_proba(X_test)[:, 1]
        predictions_test = (probas_test >= self.meilleur_seuil).astype(int)
        score_final = f1_score(y_test, predictions_test) # Le score F1 obtenu sur le jeu de test
        self.matrice_confusion = (y_test, predictions_test, [0, 1])

        # Enregistrement du modele dans joblib
        self.enregistrer_modele((y_test, predictions_test, [0, 1]))

        return float(score_final)

    def enregistrer_modele(self, informations_matrice_confusion:tuple[pd.DataFrame, np.ndarray, list[int]]):
        """
        Sauvegarde une copie du modèle entraîné pour que le programme soit moins lent.
        """
        try:
            donnees = {
                "grille_recherche": self.grille_recherche, 
                "meilleur_seuil": self.meilleur_seuil, 
                "meilleur_f1": self.meilleur_f1,
                "matrice_confusion": informations_matrice_confusion, # Vu que le setter construis la matrice, il faut enregistrer les données pour le constructeur plutôt que la matrice en tant que tel. Idéalement ce serait changé.
            }
            joblib.dump(donnees, self.CHEMIN_MODELE)
        except:
            raise ValueError("Entraînez le modèle avant de le sauvegarder.")

    def charger_modele(self) -> bool:
        if not self.CHEMIN_MODELE.exists():
            return False

        donnees_sauvegardees = joblib.load(self.CHEMIN_MODELE)

        self.grille_recherche = donnees_sauvegardees["grille_recherche"]
        self.meilleur_seuil = donnees_sauvegardees["meilleur_seuil"]
        self.meilleur_f1 = donnees_sauvegardees["meilleur_f1"]

        informations_matrice = donnees_sauvegardees.get("matrice_confusion")
        if informations_matrice is not None:
            self.matrice_confusion = informations_matrice

        return True

    def predire(self, film: pd.DataFrame) -> bool:
        """
        Retourne 1 pour blockbuster, sinon 0.

        film = pd.DataFrame([{
            "genre": str,
            "budget_usd": int,
            "rating": float,
            "runtime_min": int
        }])
        """
        if not hasattr(self.grille_recherche, "best_estimator_"): #Vérif que le modèle a un entraînement
            raise ValueError("Le modèle n'a pas encore été entraîné.")

        colonnes_attendues = [
            "genre",
            "budget_usd",
            "rating",
            "runtime_min"
        ]

        if list(film.columns) != colonnes_attendues: # Checkup que les colonnes contiennent les bons headers
            raise ValueError(
                f"Le DataFrame doit contenir exactement ces colonnes : "
                f"{colonnes_attendues}"
            )

        probabilites = self.grille_recherche.predict_proba(film) # Retourne les chances que ce soit blockbuster ou non dans une liste en pourcentage
        probabilite_blockbuster = probabilites[0, 1] # Get de la probabilité pour le premier film de la liste (celui qu'on analyse)

        return bool(probabilite_blockbuster >= self.meilleur_seuil) # Vérification si au-dessus du seuil à partir duquel on dit que c'est un blockbuster, si au-dessus, 1, blockbuster, sinon 0, flop


    def lire_historique(self):
        if not os.path.exists(self.chemin_historique):
            return []

        with open(self.chemin_historique, "r", encoding="utf-8") as fichier:
            try:
                historique = json.load(fichier)
            except json.JSONDecodeError as erreur:
                raise ValueError("Le fichier historique.json est invalide") from erreur
        if not isinstance(historique, list):
            raise ValueError("L'historique doit contenir une liste")
        return historique

    def enregistrer_prediction(self, prediction, film):
        historique = self.lire_historique()

        historique.append(prediction)

        with open(self.chemin_historique, "w", encoding="utf-8") as fichier:
            json.dump(historique, fichier, indent=4)
        # Probabilité classe 1
        probas = self.grille_recherche.predict_proba(film)[:, 1]
        
        seuil = self.meilleur_seuil
        print(seuil)
        
        resultat = (probas >= seuil).astype(int)
        return int(resultat[0])

if __name__ == "__main__":
    csv_path = Path(__file__).resolve().parent.parent / "movie_blockbusters.csv"
    data_manager = DataManager(str(csv_path))
    modele_test = ModeleBlockbuster(data_manager)

    film = pd.DataFrame([{
        "genre": "Action",
        "budget_usd": 200000000,
        "rating": 7.5,
        "runtime_min": 120
    }])


    if modele_test.charger_modele():
        print(f"Film est un blockbuster ?: {modele_test.predire(film)}")
    else:
        score_final = modele_test.entrainer(
            data_manager.donnees_clean[0], 
            data_manager.donnees_clean[1]
        )

    print("Meilleur seuil: ", modele_test.meilleur_seuil)
    print("Best parameters:", modele_test.grille_recherche.best_params_)
    print("Best mean CV F1 (données d'entraînement):", modele_test.grille_recherche.best_score_)
    print("F1 score final (sur données de test)", score_final)