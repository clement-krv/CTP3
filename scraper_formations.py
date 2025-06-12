import requests  # Pour les requêtes HTTP
import json      # Pour manipuler les fichiers JSON
from pathlib import Path  # Pour créer des dossiers facilement (chemins de fichiers)

# Étape 1 – Définir l'URL de l'API à appeler
URL = "https://fakerapi.it/api/v1/custom?_quantity=10&title=word&duration=number&level=word"

def appeler_api():
    """
    Appelle l'API et retourne les données si la réponse est correcte.
    """
    try:
        # Compléter la ligne suivante pour envoyer une requête GET
        response = requests.get(URL)

        # Si le code de réponse est 200 (succès)
        if response.status_code == 200:
            # Retourner la liste des formations contenues dans le champ 'data'
            return response.json()["data"]
        else:
            print("Erreur lors de l'appel API :", response.status_code)
            return []
    except requests.RequestException as e:
        print("Exception lors de l'appel API :", e)
        return []

def afficher_formations(data):
    """
    Affiche chaque formation dans la console.
    """
    for i, formation in enumerate(data, start=1):
        print(f"{i}. {formation['title']} - {formation['duration']}h - Niveau : {formation['level']}")

def sauvegarder_json(data, chemin_fichier):
    """
    Enregistre les données dans un fichier JSON.
    """
    dossier = Path("exports")
    dossier.mkdir(exist_ok=True)

    with open(chemin_fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    # Appel de l'API
    formations = appeler_api()

    if formations:
        # Affichage console
        afficher_formations(formations)

        # Enregistrement dans un fichier JSON
        sauvegarder_json(formations, "exports/formations.json")
    else:
        print("Aucune formation trouvée.")

if __name__ == "__main__":
    main()
