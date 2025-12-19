import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Ajout du dossier courant au path pour importer les modules voisins
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from historique import Historique
from statistiques import StatistiquesParking

def main():
    print("Test du module Historique et Statistiques")

    # On définit le chemin du fichier CSV de test
    fichier_csv = "data_test.csv"

    # Nettoyage : on supprime l'ancien fichier s'il existe
    if os.path.exists(fichier_csv):
        os.remove(fichier_csv)

    # 1. Simulation de l'activité du parking
    print("Enregistrement des événements...")
    hist = Historique(fichier_csv)
    now = datetime.now()

    # Client A : Entrée -> Entretien -> Sortie
    hist.enregistrer_entree("AB-123-CD", now - timedelta(hours=4), est_abonne=True)
    hist.enregistrer_service("AB-123-CD", now - timedelta(hours=3), "entretien", est_abonne=True)
    hist.enregistrer_sortie("AB-123-CD", now - timedelta(hours=1), est_abonne=True)

    # Client B : Juste une livraison
    hist.enregistrer_entree("EF-456-GH", now - timedelta(hours=2), est_abonne=False)
    hist.enregistrer_service("EF-456-GH", now, "livraison", est_abonne=False)

    print(f"-> {len(hist.evenements)} événements ajoutés.")

    # 2. Vérification de la persistance (CSV)
    print("\nRelecture depuis le fichier CSV...")
    hist_relis = Historique.depuis_csv(fichier_csv)
    
    if len(hist_relis.evenements) == len(hist.evenements):
        print("-> Lecture CSV OK : le nombre d'événements correspond.")
    else:
        print("-> Erreur : perte de données lors de la lecture CSV.")

    # 3. Test des statistiques
    print("\nAffichage des statistiques :")
    stats = StatistiquesParking(hist_relis)
    
    # On prend une période assez large
    debut = now - timedelta(hours=5)
    fin = now + timedelta(hours=1)

    print(f" - Nombre de passages : {stats.nombre_passages(debut, fin)}")
    print(f" - Clients uniques : {stats.nombre_clients_distincts(debut, fin)}")
    print(f" - Services effectués : {stats.nombre_services_total(debut, fin)}")
    print(f" - Détail des services : {stats.repartition_services_par_type(debut, fin)}")

if __name__ == "__main__":
    main()