"""
Client.

Ce module définit la classe Client, qui représente un utilisateur du
service de stationnement.
"""

from datetime import date
from abonnement import Abonnement

class Client:
    """
    Client du service de stationnement.

    Attribues
    ----------
    nom : str
        Nom du client.
    adresse : str
        Adresse/Rue du client.
    estAbonne : bool
        Indique si le client possède un abonnement actif.
    estSuperAbonne : bool
        Indique si le client possède un statut « super abonné ».
    nbFrequentations : int
        Nombre de fréquentations du service par ce client.
    """

    def __init__(self, nom: str, adresse: str, estAbonne: bool, estSuperAbonne: bool,  nbFrequentations: int):
        """
        Initialise un client.

        Parametres
        ----------
        nom : str
            Nom du client.
        adresse : str
            Adresse postale du client.
        estAbonne : bool
            True si le client est abonné, False sinon.
        estSuperAbonne : bool
            True si le client est super abonné, False sinon.
        nbFrequentations : int
            Nombre initial de fréquentations du service.
        """
        pass

    def sAbonner(self, ab: Abonnement) -> None :
        """
        Associe un abonnement à ce client.

        Parametres
        ----------
        ab : Abonnement
            Abonnement à associer au client.
        """
        pass

    def nouvelleVoiture(self, imma: str, hautV: float, longV: float) -> None :
        """
        Déclare une nouvelle voiture pour ce client; si jamais le client en à une nouvelle.

        Parametres
        ----------
        imma : str
            Immatriculation de la voiture.
        hautV : float
            Hauteur du véhicule.
        longV : float
            Longueur du véhicule.
        """
        pass

    def seDesabonner(self) -> None:
        """
        Met fin à l'abonnement du client, s'il existe.
        """
        pass

    def demanderMaintenance(self) -> None:
        """
        Demande une opération de maintenance pour la voiture du client.
        """
        pass

    def demanderLivraison(self, dateLiv: date, heure: int, adresseLiv: str) -> None:
        """
        Demande la livraison de la voiture à une date, heure et adresse données.

        Parametres
        ----------
        dateLiv : date
            Date de la livraison souhaitée.
        heure : int
            Heure de la livraison (format entier, par exemple 14 pour 14h).
        adresseLiv : str
            Adresse de livraison de la voiture.
        """
        pass

    def demanderEntretien(self) -> None:
        """
        Demande une opération d'entretien pour la voiture du client.
        """
        pass

    def entrerParking(self, a) -> str:
        """
        Fait entrer le client dans le parking via un accès donné.

        Parametres
        ----------
        a : Acces
            Accès utilisé pour entrer dans le parking.

        Returns
        -------
        str
            Résultat de la procédure d'entrée (message, identifiant, etc.).
        """
        pass
