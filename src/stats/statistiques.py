"""
Statistiques.

Ce module définit la classe StatistiquesParking, qui regroupe les
méthodes d'étude statistique de l'activité du parking DreamPark.
"""

from datetime import datetime
from typing import Any, Dict

class StatistiquesParking:
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

    def __init__(self, historique: Any) -> None:
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
