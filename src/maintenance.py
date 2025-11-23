"""
Maintenance.

Ce module définit la classe Maintenance, qui représente un service
de maintenance réalisé sur un véhicule.
"""

from service import Service
from voiture import Voiture


class Maintenance(Service):
    """
    Service de maintenance de véhicule.

    Cette classe spécialise un service en précisant qu'il s'agit
    d'une opération de maintenance sur une voiture.
    """

    def effectuerMaintenance(self, v : Voiture) -> None:
        """
        Effectue la maintenance prévue sur la voiture.

        Parametres
        ----------
        v :
            Voiture concernée par la maintenance.
        """
        pass
