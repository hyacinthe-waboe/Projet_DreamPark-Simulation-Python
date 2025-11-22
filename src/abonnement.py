"""
Abonnement.

Ce module définit la classe Abonnement, qui représente un l'abonnement
d'un client du parking DreamPark.
"""
import contrat


class Abonnement:
    """
    Abonnement à un service de stationnement.

    Attribue
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

    def addContrat(self, contrat: contrat) :
        """
        Ajoute un contrat à cet abonnement.

        Parametres
        ----------
        contrat : Contrat
            Contrat associé à cet abonnement.
        """
        pass
