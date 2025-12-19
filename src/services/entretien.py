"""
Entretien.

Ce module définit la classe Entretien, qui représente un service
d'entretien réalisé sur un véhicule.
"""

from datetime import date, datetime

from services.service import Service


class Entretien(Service):
    """
    Service d'entretien.

    Cette classe spécialise un service en précisant qu'il s'agit
    d'une opération d'entretien. Elle hérite des attributs généraux
    d'un service (dateDemande, dateService, rapport).
    """
    def __init__(self, dateDemande, dateService, rapport):
        super().__init__(dateDemande, dateService, rapport)
        self.effectue = False  

    def effectuerEntretien(self, parking, voiture, client) -> None:
        """
        Effectue l'entretien prévu.

        Cette méthode représente l'exécution de l'entretien associé
        au service (contrôle, nettoyage, révision, etc.).
        """
        if self.effectue:
            raise ValueError("L'entretien a déjà été effectué")
        
        today = date.today()

        if today < self.dateDemande:
            raise ValueError("Impossible d'effectuer l'entretien avant la date de demande")
        
        if self.dateService is None or self.dateService > today:
            self.dateService = today

        self.rapport = f"L'entretien a été effectué le {self.dateService}"

        self.effectue = True

        parking.historique.enregistrer_service(
            imma=voiture.immatriculation,
            date=datetime.now(),
            type_service="entretien",
            est_abonne=client.estAbonne if client else False,
            est_super_abonne=client.estSuperAbonne if client else False
        )
        