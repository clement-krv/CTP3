import requests       # Pour envoyer des requêtes HTTP
import json           # Pour gérer les fichiers JSON
import csv            # Pour sauvegarder les données CSV
from pathlib import Path  # Pour gérer les chemins de fichiers

# 🌐 URL de l'API simulant une liste de formations
URL = "https://fakerapi.it/api/v1/custom?_quantity=10&title=word&duration=number&level=word"

def appeler_api():
    """Appelle l'API pour récupérer les données JSON simulées."""
    try:
        # Envoyer une requête GET
        response = requests.get(URL)

        # Déclencher une erreur si le code HTTP n’est pas 200
        response.raise_for_status()

        # Retourner les données dans le champ 'data' du JSON
        return response.json()["data"]

    except requests.RequestException as e:
        print(f"❌ Erreur API : {e}")
        return []

def afficher_formations(data):
    """Affiche les formations récupérées dans la console"""
    for i, formation in enumerate(data, start=1):
        titre = formation['title']
        duree = formation['duration']
        niveau = formation['level']
        print(f"{i}. {titre} - Durée : {duree}h - Niveau : {niveau}")

def sauvegarder_json(data, fichier="exports/formations.json"):
    """Sauvegarde les données au format JSON dans un dossier 'exports'"""
    # Créer le dossier s’il n’existe pas
    Path("exports").mkdir(exist_ok=True)

    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("✅ Données enregistrées en JSON.")

def sauvegarder_csv(data, fichier="exports/formations.csv"):
    """Sauvegarde les données au format CSV"""
    Path("exports").mkdir(exist_ok=True)

    with open(fichier, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "duration", "level"])
        writer.writeheader()
        writer.writerows(data)

    print("✅ Données enregistrées en CSV.")

def main():
    # Récupérer les données depuis l’API
    data = appeler_api()

    # Ne rien faire si les données sont vides
    if not data:
        return

    # Affichage console
    afficher_formations(data)

    # Sauvegardes
    sauvegarder_json(data)
    sauvegarder_csv(data)

if __name__ == "__main__":
    main()
