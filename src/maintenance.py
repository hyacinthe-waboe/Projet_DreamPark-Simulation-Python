"""
Maintenance.

Ce module définit la classe Maintenance, qui représente un service
de maintenance réalisé sur un véhicule.
"""
from datetime import date
from service import Service
from voiture import Voiture


class Maintenance(Service):
    """
    Service de maintenance de véhicule.

    Cette classe spécialise un service en précisant qu'il s'agit
    d'une opération de maintenance sur une voiture.
    """
    def __init__(self, dateDemande, dateService, rapport):
        super().__init__(dateDemande, dateService, rapport)
        self.maintenance = False 

    def effectuerMaintenance(self, v : Voiture) -> None:
        """
        Effectue la maintenance prévue sur la voiture.

        Parametres
        ----------
        v :
            Voiture concernée par la maintenance.
        """
        if v is None or not isinstance(v, Voiture):
            raise ValueError("Une voiture valide est requise pour la maintenance")

        if self.maintenance:
            raise ValueError("La maintenance a déjà été effectuée")

        today = date.today()

        if today < self.dateDemande:
            raise ValueError("Impossible d'effectuer la maintenance avant la date de demande")
        
        if self.dateService is None or self.dateService > today:
            self.dateService = today

        self.rapport = (
            f"Maintenance effectuée le {self.dateService} "
            f"sur le véhicule {v}."
        )

        self.maintenance = True
