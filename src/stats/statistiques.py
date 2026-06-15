"""
Statistiques.

Ce module définit la classe StatistiquesParking, qui regroupe les
méthodes d'étude statistique de l'activité du parking DreamPark.
"""

from datetime import datetime
from typing import Any, Dict
from noyau.parking import Parking 
from stats.historique import Historique

class Statistiques:
    """
    Statistiques sur l'activité du parking.

    Cette classe permet de calculer différents indicateurs à partir
    d'un historique des événements (entrées, sorties, services).

    Attribues
    ----------
    historique : Any
        Source des données utilisées pour les statistiques. Il peut
        s'agir d'une liste d'événements en mémoire, d'un objet dédié
        ou d'un accès à une base de données.
    """

    def __init__(self, historique: Historique, parking: Parking ) -> None:
        """
        Initialise le module de statistiques pour un historique donné.

        Parametres
        ----------
        historique : Any
            Structure contenant les événements du parking (entrées,
            sorties, services) qui serviront de base au calcul des
            statistiques.
        """
        self.historique = historique
        self.parking = parking

    def nombre_passages(self, debut: datetime, fin: datetime) -> int:
        """
        Calcule le nombre total de passages sur une période.

        Un passage correspond à une entrée ou une sortie de voiture
        dans le parking, tous accès confondus.

        Parametres
        ----------
        debut : datetime
            Début de la période étudiée.
        fin : datetime
            Fin de la période étudiée.

        Returns
        -------
        int
            Nombre total d'événements de type « entrée » ou « sortie »
            observés entre `debut` et `fin`.
        """
        evenements = self.historique.evenements_dans_intervalle(debut, fin)

        compteur = 0
        for evt in evenements:
            if evt["type"] in ("entree", "sortie"):
                compteur += 1

        return compteur

    def nombre_clients_distincts(self, debut: datetime, fin: datetime) -> int:
        """
        Estime la fréquentation en nombre de clients distincts.

        Deux passages sont considérés comme appartenant au même client
        si l'immatriculation de la voiture est identique.

        Parametres
        ----------
        debut : datetime
            Début de la période étudiée.
        fin : datetime
            Fin de la période étudiée.

        Returns
        -------
        int
            Nombre d'immatriculations distinctes observées au moins
            une fois sur la période [debut, fin].
        """
        evenements = self.historique.evenements_dans_intervalle(debut, fin)

        immatriculations = set()

        for evt in evenements:
            immat = evt.get("immat")
            if immat:
                immatriculations.add(immat)

        return len(immatriculations)

    def nombre_services_total(self, debut: datetime, fin: datetime) -> int:
        """
        Calcule le nombre total de services réalisés sur une période.

        Les services pris en compte incluent par exemple les livraisons,
        les entretiens et les maintenances.

        Parametres
        ----------
        debut : datetime
            Début de la période étudiée.
        fin : datetime
            Fin de la période étudiée.

        Returns
        -------
        int
            Nombre total d'événements de type « service » observés
            entre `debut` et `fin`.
        """
        evenements = self.historique.evenements_dans_intervalle(debut, fin)

        compteur = 0
        for evt in evenements:
            if evt["type"] == "service":
                compteur += 1

        return compteur

    def repartition_services_par_type(self,debut: datetime,fin: datetime) -> Dict[str, int]:
        """
        Fournit la répartition des services par type sur une période.

        Chaque service doit être associé à un type (par exemple
        « entretien », « maintenance », « livraison »). Cette méthode
        renvoie pour chaque type le nombre de services réalisés.

        Parametres
        ----------
        debut : datetime
            Début de la période étudiée.
        fin : datetime
            Fin de la période étudiée.

        Returns
        -------
        dict[str, int]
            Dictionnaire associant à chaque type de service le nombre
            de services réalisés sur la période étudiée.
        """
        evenements = self.historique.evenements_dans_intervalle(debut, fin)

        repartition: Dict[str, int] = {}

        for evt in evenements:
            if evt["type"] == "service":
                type_service = evt.get("type_service")
                if type_service is not None:
                    repartition[type_service] = repartition.get(type_service, 0) + 1

        return repartition
    
    def recettes_du_jour(self) -> float:
        """
        Calcule le chiffre d'affaires généré sur la journée en cours.

        Cette méthode parcourt les événements de l'historique et additionne
        les recettes associées aux sorties effectuées aujourd'hui. Le tarif
        appliqué dépend du statut « super abonné » enregistré dans l'événement
        de sortie.

        Returns
        -------
        float
            Montant total des recettes du jour.
        """
        aujourdhui_str = datetime.now().strftime("%Y-%m-%d")
        total_recette = 0.0
        
        for evt in self.historique.evenements:
            if evt["type"] == "sortie":
                date_evt_str = str(evt["date"])
                
                if date_evt_str.startswith(aujourdhui_str):
                    # On gère le cas où c'est un booléen ou une string "True"/"False" (CSV)
                    val_vip = evt.get("est_super_abonne", False)
                    est_vip = str(val_vip).lower() == "true" or val_vip is True
                    
                    if est_vip:
                        total_recette += getattr(self.parking, "prix_vip", 50.0)
                    else:
                        total_recette += getattr(self.parking, "prix", 15.0)
                    
        return total_recette


    def _verifier_si_vip(self, immat: str) -> bool:
        """
        Vérifie si une voiture était super abonnée lors de son entrée.

        Cette méthode recherche dans l'historique l'événement d'entrée le plus
        récent correspondant à l'immatriculation fournie, puis renvoie le statut
        « super abonné » associé à cet événement.

        Parametres
        ----------
        immat : str
            Immatriculation de la voiture à vérifier.

        Returns
        -------
        bool
            True si la voiture était super abonnée lors de son entrée,
            False sinon.
        """
        for evt in reversed(self.historique.evenements):
            if evt["type"] == "entree" and evt.get("immat") == immat:
                val = evt.get("est_super_abonne", False)
                return str(val).lower() == "true" or val is True
        return False


    def total_entrees_jour(self) -> int:
        """
        Calcule le nombre total d'entrées sur la journée en cours.

        Cette méthode définit l'intervalle correspondant à la journée courante
        (de 00:00:00 à 23:59:59), récupère les événements de l'historique sur
        cet intervalle, puis compte uniquement ceux de type « entree ».

        Returns
        -------
        int
            Nombre d'événements de type « entree » sur la journée en cours.
        """
        now = datetime.now()
        debut = datetime(now.year, now.month, now.day, 0, 0, 0)
        fin = datetime(now.year, now.month, now.day, 23, 59, 59)
        
        try:
            evts = self.historique.evenements_dans_intervalle(debut, fin)
            return sum(1 for e in evts if e["type"] == "entree")
        except Exception:
            return 0

