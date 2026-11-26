# Prochainement 
Voici les choses qui pourraient être améliorées. 
1. Le ColumnTransformer pourrait ne pas être refitté chaque fois (src\donnees.py, ligne 44-46), on pourrait le save et le réutiliser. C'est toutefois complètement inutile à implémenter dans le programme considérant qu'on utilise jamais deux fois cette fonction.
2. Même chose que `1` mais pour la pipeline (src\modele.py, lignes 32-38)