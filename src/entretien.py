"""
Entretien.

Ce module définit la classe Entretien, qui représente un service
d'entretien réalisé sur un véhicule.
"""

from service import Service


class Entretien(Service):
    """
    Service d'entretien.

    Cette classe spécialise un service en précisant qu'il s'agit
    d'une opération d'entretien. Elle hérite des attributs généraux
    d'un service (dateDemande, dateService, rapport).
    """

    def effectuerEntretien(self):
        """
        Effectue l'entretien prévu.

        Cette méthode représente l'exécution de l'entretien associé
        au service (contrôle, nettoyage, révision, etc.).
        """
        pass
