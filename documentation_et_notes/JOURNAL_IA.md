1. Déplacement partiel des erreurs dans vérification valuers
2. Interface 
3. Déplacement de  Dialogue vers dialogue.py
4. Gestion des errurs d'importation dans les différents fichiers (try: import except: print())
5. Redirection des fichiers d'execution vers un dossier séparé, ignoré par git

# Journal d'utilisation de l'IA --- CinePredict

## Réorganiser la gestion des erreurs lors de la validation des valeurs.

-   **Outil :** gemini
-   **Réponse reçue :** Piste de déplacement partiel des contrôles dans les méthodes de vérification.
-   **Vérification :** Brouillon : déplacement mentionné ; scénario de test final non documenté.
-   **Décision :** Modifié selon le brouillon.

## Aider à concevoir et organiser l'interface graphique.

-   **Outil :** gemini
-   **Réponse reçue :** Pistes d'organisation des champs et boutons.
-   **Vérification :** Le code PyQt6 de développement contient un formulaire, des boutons et des dialogues ; exécution finale à confirmer.
-   **Décision :** Gardé et adapté.

## Séparer la classe `Dialogue` de l'interface.

-   **Outil :** Claude
-   **Réponse reçue :** Déplacement proposé vers `dialogue.py`.
-   **Vérification :** Le code actuel importe `Dialogue` depuis `utils.dialogue` ; le module lui-même reste à vérifier.
-   **Décision :** Modifié selon le brouillon.

## Gérer les erreurs d'importation.

-   **Outil :** claude
-   **Réponse reçue :** Utilisation de `try` et `except` autour de certains imports avec un message explicatif.
-   **Vérification :** Le code actuel utilise try/except ImportError pour essayer les imports relatifs puis absolus ; aucun test d'import manquant documenté.
-   **Décision :**Modifié selon le brouillon.

## Organiser les fichiers générés lors de l'exécution.

-   **Outil :** IA conversationnelle (outil exact à confirmer)
-   **Réponse reçue :** Les placer dans un dossier séparé ignoré par Git.
-   **Vérification :** Le code actuel crée `donnees_execution` avec pathlib et y place le modèle et l'historique ; vérifier les règles `.gitignore`.
-   **Décision :** Gardé selon le brouillon, à confirmer.

## Intégrer la matrice de confusion à une fenêtre PyQt6.

-   **Outil :** ChatGPT
-   **Réponse reçue :** Utiliser Matplotlib, `imshow()` et `FigureCanvas` pour afficher les quatre cases.
-   **Vérification :** **L'exécution a révélé une erreur `TypeError: Image data of dtype object cannot be converted to float`.** La comparaison du code avec la réponse a montré qu'il fallait transmettre une matrice numérique et non un objet d'affichage `ConfusionMatrixDisplay`.
-   **Décision :** **Modifié après vérification :** calculer une matrice numérique avec `confusion_matrix` et la transmettre au graphique.

## 9. Préparer les trois livrables à partir des brouillons et des consignes.

-   **Outil :** ChatGPT
-   **Réponse reçue :** Structurer le README, la fiche de décisions et le journal, sans inventer les résultats manquants.
-   **Vérification :** Comparaison avec les brouillons et les consignes de remise ; licence exacte, score final, couverture, dates de validation non confirmées ; les décorateurs intégrés sont présents dans le code actuel.
-   **Décision :** À relire et compléter par les deux membres avant remise.

L'IA a servi d'aide à la compréhension, au débogage, à la structuration et à la rédaction. Les décisions finales et la validation du fonctionnement du programme restent sous la responsabilité de l'équipe.