"""
Borne de ticket.

Ce module définit la classe BorneTicket, qui gère l'interaction avec le client
à l'entrée du parking pour la délivrance des tickets, la proposition de
services et d'abonnements, ainsi que la saisie des informations de paiement.
"""

from client import Client
from parking import Parking
import random

class BorneTicket:
    """
    Borne de ticket à l'entrée du parking.

    La borne permet au client de récupérer un ticket, de consulter les services
    disponibles, de souscrire un abonnement et de choisir un mode de paiement.
    """

    def deliverTicket(self, c: Client) -> str:
        """
        Délivre un ticket pour le client donné.

        Parametres
        ----------
        c : Client
            Client qui se présente à la borne.

        Returns
        -------
        str
            Représentation du ticket délivré (par exemple un identifiant ou
            un code encodé).
        """
        # Generation d'un ID random
        ticketId = f"TICKET-{random.randint(1000, 9999)}"
        return ticketId

    def proposerServices(self) -> str:
        """
        Propose au client les services disponibles.

        Returns
        -------
        str
            Description des services proposés.
        """
        return "Services disponibles : Maintenance, Entretien, Livraison."

    def proposerAbonnements(self, c: Client, p: Parking) -> str:
        """
        Propose des offres d'abonnement au client.

        Parametres
        ----------
        c : Client
            Client concerné par les propositions d'abonnement.
        p : Parking
            Parking dans lequel l'abonnement s'applique.

        Returns
        -------
        str
            Description des abonnements proposés.
        """
        if c.estAbonne:
            return "Vous êtes déjà abonné."
        
        return "Abonnements disponibles : Standard, Premium, Pack Garanti."

    def recupererInfosCarte(self, c: Client) -> str:
        """
        Récupère les informations de carte de paiement du client.

        Parametres
        ----------
        c : Client
            Client dont les informations de paiement sont saisies.

        Returns
        -------
        str
            Représentation des informations de carte collectées.
        """
        return "Lecture carte bancaire... OK"

    def proposerTypePaiement(self) -> str:
        """
        Propose au client les différents types de paiement disponibles.

        Returns
        -------
        str
            Description des modes de paiement proposés (cartes,espèce,paypal etc...).
        """
        return "Modes de paiement : CB, Espèces."
