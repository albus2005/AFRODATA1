import requests
import os

# Récupérer le token depuis l'environnement
token = os.environ.get("HF_TOKEN")

# Le modèle qu'on utilise
API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"

headers = {"Authorization": f"Bearer {token}"}

def analyser_texte(texte):
    reponse = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": texte}
    )
    return reponse.json()

# Test
resultat = analyser_texte("The cholera situation in Bukavu is getting worse.")
print(resultat)