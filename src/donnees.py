from sklearn.linear_model import LogisticRegression
import numpy as np 
import pandas as pd 
import matplotlib.pylab as plt

df = pd.read_csv("movie_blockbusters.csv")
df = pd.get_dummies(df, columns=['genre'])

colonnes_retenues = [
    'year',
    'genre_Comedy', 
    'genre_Sci-Fi', 
    'genre_Horror', 
    'genre_Documentary', 
    'genre_Action', 
    'genre_Thriller', 
    'genre_Romance', 
    'genre_Drama', 
    'runtime_min',
    'budget_usd',
    'rating',
    'vote_count'
]

X = df[colonnes_retenues].values
Y = df['blockbuster'].values

print(f"Shapes of X={X.shape} Y={Y.shape}, #Blockbusters={Y.sum()}")