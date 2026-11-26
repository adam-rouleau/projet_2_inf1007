from abc import ABC, abstractmethod
from .dialogue import Dialogue

class Verificateur(ABC):
    @abstractmethod 
    def verification(input) -> bool:
        pass


class VerificateurGenre(Verificateur):
    def verification(self, valeur_reponse_genre:str) -> bool:
        if valeur_reponse_genre == "Sélectionnez un genre" or valeur_reponse_genre == "Genre":
            dialog = Dialogue("Veuillez entrer un genre valide.", "OK")
            dialog.activation()
            return False
        
        return True


class VerificateurRating(Verificateur):
    def verification(self, valeur_reponse_score: float) -> bool:
        try:
            valeur_reponse_score = float(valeur_reponse_score)

            if valeur_reponse_score < 0 or valeur_reponse_score > 10:
                dialog = Dialogue(
                    "Veuillez entrer un score sous forme de nombre à virgule entre 0 et 10.",
                    "OK"
                )
                dialog.activation()
                return False

        except (TypeError, ValueError):
            dialog = Dialogue(
                "Veuillez entrer un score sous forme de nombre à virgule entre 0 et 10.",
                "OK"
            )
            dialog.activation()
            return False

        return True


class VerificateurBudget(Verificateur):
    def verification(self, valeur_reponse_budget: float) -> bool:
        try:
            valeur_reponse_budget = float(valeur_reponse_budget)

            if valeur_reponse_budget <= 0:
                dialog = Dialogue(
                    "Veuillez entrer une réponse numérique valide pour le budget.",
                    "OK"
                )
                dialog.activation()
                return False

        except (TypeError, ValueError):
            dialog = Dialogue(
                "Veuillez entrer une réponse numérique valide pour le budget.",
                "OK"
            )
            dialog.activation()
            return False

        return True


class VerificateurRuntime(Verificateur):
    def verification(self, valeur_reponse_runtime: float) -> bool:
        try:
            valeur_reponse_runtime = float(valeur_reponse_runtime)

            if valeur_reponse_runtime < 60 or valeur_reponse_runtime > 185:
                dialog = Dialogue(
                    "Veuillez entrer un runtime sous forme de nombre à virgule entre X et XXXX.",
                    "OK"
                )
                dialog.activation()
                return False

        except (TypeError, ValueError):
            dialog = Dialogue(
                "Veuillez entrer un runtime sous forme de nombre à virgule entre X et XXXX.",
                "OK"
            )
            dialog.activation()
            return False

        return True