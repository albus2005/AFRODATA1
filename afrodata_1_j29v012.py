# IMPORTATIONS
import os 
import pandas as pd


# CHEMINS DES FICHIERS ET DES DOSSIERS 
BASE = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(BASE, "data")
path_file = os.path.join(data_directory, "drc_ebola_cases_20mai.xlsx")


#                =====UTILITAIRES DU PROGRAMMES=====
separator_1 = "-" * 42
separator_2 = "=" * 42
projet_name_M = "AFRODATA-1"
projet_name_m = "afrodata-1"
version = "v0.1.0"

# COULEURS ANSI pour terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Fonction pour centrer le texte selon la largeur du terminal
def center_text(text, width=None):
    if width is None:
        try:
            width = os.get_terminal_size().columns
        except:
            width = 80  # largeur par défaut
    # Limiter la largeur à 80 max pour l'esthétique
    width = min(width, 80)
    padding = (width - len(text)) // 2
    return " " * max(padding, 0) + text


#               =====AFRODATA1=====
# FONCTION CHARGER 
def excel_loader(path):
    """
    Cette fonction sert au chargement du fichier excel qu'on va traiter 
    
    parametres:
            path -                      paramètre renvoyant au chemin du fichier excel a traiter
            df -                        dataframe retourner a la fin de la fonction 
    """
    try: 
        df = pd.read_excel(path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier Introuvable: {path}")

# FONCTION NETTOYEUSE
def excel_cleaner(df) :
    """
    Cette fonction enlève les codes des zones administratves
    parametres :
            df -                    parametres de référence ppur le df ebola_data
    """
    # j'élimine les code de zone administratif en creant un noiveau df sans ces colonnes 
    # les csv a deja les valeurs manquantes remplacer par zero 
    df = df[["Admin1","CasSuspect","DecesSuspect","CasConfirmes","DecesConfirmes","Contacts"]]
    # on ne va plus supprimer les lignes avec moins de 1 cas  mais il faut que je sache comment faire
    
    return df 
    

# EDA 
def df_explorer(df) :
    texte = "INFORMATIONS GÉNÉRALES"
    centered_info = center_text(texte)
    print(Colors.RED + centered_info + Colors.RESET)
    print(df.info())



# FONCTION ACCUEIL 
def display():
    """
    Cette fonction est la page d'accueil de tout le projet en console
    En-tête centré, encadré et coloré en rouge
    """
    try:
        term_width = min(os.get_terminal_size().columns, 80)
    except:
        term_width = 80
    
    # Création du cadre
    border = Colors.RED + "=" * term_width + Colors.RESET
    
    # Ligne d'en-tête centrée
    header_text = f"{projet_name_M} {version}"
    centered_header = center_text(header_text, term_width)
    
    # Ligne de sous-titre (optionnelle)
    subtitle = "Analyse de l'épidémie d'Ebola 2026 - RDC"
    centered_subtitle = center_text(subtitle, term_width)
    
    # Affichage de l'en-tête
    print(border)
    print(Colors.RED + centered_header + Colors.RESET)
    print(Colors.RED + centered_subtitle + Colors.RESET)
    print(border)


def main():
    # Fonction d'accueil
    display()
    # Fonction loader excel 
    ebola_data = excel_loader(path_file)
    ebola_data_1 = excel_cleaner(ebola_data)
    # EDA 
    df_explorer(ebola_data_1) 
    
    

if __name__ == "__main__":
    main()