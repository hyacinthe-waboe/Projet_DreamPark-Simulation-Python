"""
Livraison.

Ce module définit la classe Livraison, qui représente un service
de livraison de véhicule pour un client.
"""

from service import Service


class Livraison(Service):
    """
    Service de livraison de véhicule.

    Cette classe spécialise un service en précisant qu'il s'agit
    d'une livraison de la voiture du client à une adresse donnée
    à une date et une heure prévues.
    """

    def effectuerLivraison(self):
        """
        Effectue la livraison prévue.

        Cette méthode représente l'exécution de la livraison :
        préparation du véhicule et acheminement à l'adresse
        et au créneau prévus pour le client.
        """
        pass
