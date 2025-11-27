"""
Livraison.

Ce module définit la classe Livraison, qui représente un service
de livraison de véhicule pour un client.
"""
from datetime import date
from service import Service


class Livraison(Service):
    """
    Service de livraison de véhicule.

    Cette classe spécialise un service en précisant qu'il s'agit
    d'une livraison de la voiture du client à une adresse donnée
    à une date et une heure prévues.
    """

    def __init__(self, dateDemande, dateService, rapport):
            super().__init__(dateDemande, dateService, rapport)
            self.livree = False

    def effectuerLivraison(self) -> None:
        """
        Effectue la livraison prévue.

        Cette méthode représente l'exécution de la livraison :
        préparation du véhicule et acheminement à l'adresse
        et au créneau prévus pour le client.
        """

        if self.livree:
            raise ValueError("La livraison a déjà été effectuée")

        today = date.today()

        if today < self.dateDemande:
            raise ValueError("Impossible d'effectuer la livraison avant la date de demande")

        if self.dateService is None or self.dateService > today:
            self.dateService = today

        self.rapport = (
            f"Livraison effectuée le {self.dateService}"
        )

        self.livree = True