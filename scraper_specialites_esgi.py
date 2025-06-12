import requests
from bs4 import BeautifulSoup
import json
import csv
from pathlib import Path

URL = "https://www.esgi.fr/ecole-informatique/programmes.html"

def recuperer_html():
    """Télécharge le code HTML de la page ESGI avec un User-Agent pour éviter l'erreur 403"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"❌ Erreur réseau : {e}")
        return ""

def extraire_specialites(html: str) -> list:
    """Extrait les spécialités à partir des balises div.font_monument_bold"""
    soup = BeautifulSoup(html, "html.parser")
    specialites = []

    blocs = soup.select("div.font_monument_bold")

    for bloc in blocs:
        titre = bloc.get_text(strip=True)
        if titre:
            specialites.append({"title": titre})

    return specialites

def sauvegarder_json(data, fichier="exports/specialites_esgi.json"):
    Path("exports").mkdir(exist_ok=True)
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("✅ JSON enregistré.")

def sauvegarder_csv(data, fichier="exports/specialites_esgi.csv"):
    Path("exports").mkdir(exist_ok=True)
    with open(fichier, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title"])
        writer.writeheader()
        writer.writerows(data)
    print("✅ CSV enregistré.")

def main():
    html = recuperer_html()
    if not html:
        return

    specialites = extraire_specialites(html)

    for i, s in enumerate(specialites, 1):
        print(f"{i}. {s['title']}")

    sauvegarder_json(specialites)
    sauvegarder_csv(specialites)

if __name__ == "__main__":
    main()
