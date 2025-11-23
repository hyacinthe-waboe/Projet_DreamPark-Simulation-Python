"""
Abonnement.

Ce module définit la classe Abonnement, qui représente un l'abonnement
d'un client du parking DreamPark.
"""
from contrat import Contrat


class Abonnement:
    """
    Abonnement à un service de stationnement.

    Attribues
    ----------
    libelle : str
        Libellé de l'abonnement.
    prix : float
        Prix de l'abonnement.
    estPackGar : bool
        Indique si l'abonnement correspond à un pack garanti.
    """

    def __init__(self, libelle: str, prix: float, estPackGar: bool):
        """
        Initialise un abonnement.

        Parametres
        ----------
        libelle : str
            Libellé de l'abonnement.
        prix : float
            Prix de l'abonnement.
        estPackGar : bool
            True si l'abonnement est un pack garanti, False sinon.
        """
        pass

    def addContrat(self, contrat: Contrat) -> None :
        """
        Ajoute un contrat à cet abonnement.

        Parametres
        ----------
        contrat : Contrat
            Contrat associé à cet abonnement.
        """
        pass
