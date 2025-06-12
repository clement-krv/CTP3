import requests             # Pour les appels réseau
import json                 # Pour la manipulation JSON
import csv                  # Pour les fichiers CSV
from pathlib import Path    # Pour gérer les chemins multiplateforme
from datetime import datetime

# 📁 Charger la configuration depuis un fichier externe
def charger_config(path="config.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# 🧾 Fonction utilitaire pour journaliser tout type d’événement
def log_event(message: str, type_: str = "info"):
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    suffixe = "errors.log" if type_ == "error" else "success.log"
    with open(log_dir / suffixe, "a", encoding="utf-8") as logfile:
        timestamp = datetime.now().isoformat(timespec='seconds')
        logfile.write(f"[{timestamp}] {message}\n")

# 🌐 Appel API avec vérification du contenu
def appeler_api(url: str) -> list:
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # 🧠 Vérification défensive du contenu
        if "data" in data and isinstance(data["data"], list):
            return data["data"]
        else:
            raise ValueError("Structure de réponse inattendue.")

    except (requests.RequestException, json.JSONDecodeError, ValueError) as e:
        log_event(f"Erreur API : {e}", type_="error")
        return []

# 🖥️ Affichage brut des formations
def afficher_formations(formations: list):
    for i, f in enumerate(formations, 1):
        print(f"{i}. {f.get('title', 'Inconnu')} – {f.get('duration')}h – {f.get('level')}")

# 💾 Enregistrement JSON
def sauvegarder_json(data: list, chemin: Path):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 💾 Enregistrement CSV
def sauvegarder_csv(data: list, chemin: Path):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# 🧠 Dispatcher des formats via stratégie
def sauvegarder_donnees(data: list, format_: str):
    export_path = Path("exports") / f"formations.{format_}"

    actions = {
        "json": sauvegarder_json,
        "csv": sauvegarder_csv
    }

    try:
        if format_ in actions:
            actions[format_](data, export_path)
            log_event(f"Sauvegarde réussie : {export_path}")
        else:
            raise ValueError("Format non pris en charge.")
    except Exception as e:
        log_event(f"Erreur de sauvegarde : {e}", type_="error")

# 🚀 Fonction principale
def main():
    config = charger_config()
    url = config.get("api_url")
    format_sortie = config.get("output_format", "json")

    donnees = appeler_api(url)

    if not donnees:
        print("❌ Aucune donnée récupérée.")
        return

    afficher_formations(donnees)
    sauvegarder_donnees(donnees, format_sortie)

if __name__ == "__main__":
    main()
