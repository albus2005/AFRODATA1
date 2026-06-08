import requests
import pandas as pd
from io import StringIO
import logging
import signal
import sys
from datetime import datetime

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ebola_data.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Gestionnaire de signaux
def signal_handler(signum, frame):
    """Gère les signaux système (Ctrl+C, etc.)"""
    logger.warning(f"Signal {signum} reçu. Arrêt gracieux en cours...")
    print("\n\033[91m⚠️ Programme interrompu par l'utilisateur\033[0m")
    sys.exit(0)

# Enregistrer les gestionnaires de signaux
signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # Terminaison

def load_ebola_data(url):
    """
    Charge les données Ebola depuis une URL et les retourne sous forme de DataFrame pandas.
    
    Paramètres
    ----------
    url : str
        L'URL du fichier CSV contenant les données Ebola à charger.
    
    Retourne
    -------
    pandas.DataFrame
        DataFrame contenant les données Ebola chargées depuis l'URL.
    
    Lève
    -------
    Exception
        Si la requête HTTP échoue (status code != 200).
    
    Exemples
    --------
    >>> url = "https://data.humdata.org/dataset/ebola-cases-and-deaths-who-oms-situation-reports/resource/6e05b07f-2b16-4b2d-8b91-0bedae814b6c"
    >>> df = load_ebola_data(url)
    >>> print(df.shape)
    """
    logger.info(f"Début du chargement des données depuis {url}")
    
    try:
        # Faire requête HTTP GET sur url
        logger.debug("Envoi de la requête HTTP GET...")
        response = requests.get(url, timeout=30)
        
        # Si statut != 200 : lever une erreur
        if response.status_code != 200:
            logger.error(f"Erreur HTTP {response.status_code}")
            raise Exception(f"Erreur HTTP {response.status_code}: Impossible de charger les données depuis {url}")
        
        logger.info(f"Requête réussie - Status code: {response.status_code}")
        
        # Charger le contenu en DataFrame
        logger.debug("Conversion du contenu en DataFrame...")
        data = StringIO(response.text)
        df = pd.read_csv(data)
        
        logger.info(f"DataFrame chargé avec succès - Dimensions: {df.shape}")
        logger.info(f"Colonnes disponibles: {list(df.columns)}")
        
        # Retourner le DataFrame
        return df
        
    except requests.exceptions.Timeout:
        logger.error("Timeout lors de la requête HTTP")
        raise Exception("La requête a expiré après 30 secondes")
    except requests.exceptions.ConnectionError:
        logger.error("Erreur de connexion - Impossible d'atteindre le serveur")
        raise Exception("Erreur de connexion réseau")
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")
        raise

# Affichage console avec AFRODATA-1 v0.1.0 en rouge clignotant
def display_banner():
    """Affiche la bannière AFRODATA en rouge clignotant"""
    # Rouge clignotant: \033[91m pour rouge, \033[5m pour clignotant
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   \033[91m\033[5m██████╗ ███████╗██████╗  ██████╗ ██████╗  █████╗ ████████╗ █████╗ \033[0m    ║
    ║   \033[91m\033[5m██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗\033[0m    ║
    ║   \033[91m\033[5m██████╔╝█████╗  ██║  ██║██║   ██║██║  ██║███████║   ██║   ███████║\033[0m    ║
    ║   \033[91m\033[5m██╔══██╗██╔══╝  ██║  ██║██║   ██║██║  ██║██╔══██║   ██║   ██╔══██║\033[0m    ║
    ║   \033[91m\033[5m██║  ██║███████╗██████╔╝╚██████╔╝██████╔╝██║  ██║   ██║   ██║  ██║\033[0m    ║
    ║   \033[91m\033[5m╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝\033[0m    ║
    ║                                                          ║
    ║              \033[91m\033[5mAFRODATA-1 v0.1.0\033[0m                        ║
    ║        \033[93mSystème de collecte de données Ebola\033[0m                  ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

# URL fournie
url = "https://data.humdata.org/dataset/ebola-cases-and-deaths-who-oms-situation-reports/resource/6e05b07f-2b16-4b2d-8b91-0bedae814b6c"

# Programme principal
if __name__ == "__main__":
    # Afficher la bannière avec texte rouge clignotant
    display_banner()
    
    logger.info("=== Démarrage de AFRODATA-1 v0.1.0 ===")
    print("\n\033[96m📊 Initialisation du système de collecte de données...\033[0m\n")
    
    # Utilisation de la fonction
    try:
        ebola_data = load_ebola_data(url)
        print("\n\033[92m✅ Données chargées avec succès!\033[0m")
        print(f"\033[93m📈 Shape du DataFrame: {ebola_data.shape}\033[0m")
        print(f"\033[93m📅 Date et heure du chargement: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
        
        print("\n\033[96m📋 Aperçu des données:\033[0m")
        print(ebola_data.head(10))
        
        print("\n\033[96mℹ️ Informations sur les colonnes:\033[0m")
        for col in ebola_data.columns:
            print(f"  - {col}: {ebola_data[col].dtype}")
        
        logger.info("Programme terminé avec succès")
        print("\n\033[92m✨ Fin du programme - Données prêtes pour l'analyse\033[0m")
        
    except KeyboardInterrupt:
        logger.info("Programme interrompu par l'utilisateur")
        print("\n\033[91m⏹️ Programme arrêté par l'utilisateur\033[0m")
    except Exception as e:
        logger.error(f"Erreur fatale: {str(e)}")
        print(f"\n\033[91m❌ Erreur: {e}\033[0m")
        sys.exit(1)