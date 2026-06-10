# IMPORTATIONS
import os 
import pandas as pd 


'''
AFRODATA 1 v011
Traitement et analyse des données excel sur l'epidemie d'Ebola 2026

1. Charger le fichier Excel
creer le chemin du ficher excel 
retourner un dataframe et une EDA 

2. Nettoyer -- valeurs manquantes, colonnes inutiles
3. Filtrer -- garder seulement les zones actives (cas > 0)
4. Agréger -- totaux par province
5. Afficher -- indicateurs clés en console

'''

BASE = os.path.dirname(os.path.abspath(__file__))
path_file = os.path.join(BASE, "data", "drc_ebola_cases_20mai.xlsx")

# FONCTION CHARGER 
def excel_loader(path) :
    df = pd.read_excel(path)
    
    return df.head(10)
    
print(excel_loader(path_file))

