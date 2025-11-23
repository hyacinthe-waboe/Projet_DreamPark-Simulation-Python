"""
Parking.

Ce module définit la classe Parking, qui centralise la gestion des places,
des niveaux et des abonnements du parking.
"""

from voiture import Voiture
from place import Place
from abonnement import Abonnement

class Parking:
    """
    Parking principal.

    Le parking est caractérisé par un nombre fixe de places par niveau,
    un nombre total de places libres, un nombre de niveaux et un prix
    de stationnement. Cette classe est pensée pour être utilisée comme
    une instance unique dans l'application.

    Attribues
    ----------
    _nbPlacesParNiveau : int
        Nombre de places disponibles sur chaque niveau.
    _nbPlacesLibres : int
        Nombre total de places actuellement libres dans le parking.
    _prix : int
        Prix de stationnement associé au parking.
    nbNiveaux : int
        Nombre de niveaux (étages) du parking.
    """

    def __init__(self, nbPlacesParNiveau: int, nbPlacesLibres: int, prix: int, nbNiveaux: int):
        """
        Initialise le parking.

        Parametres
        ----------
        _nbPlacesParNiveau : int
            Nombre de places sur chaque niveau.
        _nbPlacesLibres : int
            Nombre initial de places libres dans le parking.
        _prix : int
            Prix de stationnement.
        nbNiveaux : int
            Nombre de niveaux du parking.
        """
        pass

    def rechercherPlace(self, v : Voiture) -> Place:
        """
        Recherche une place adaptée pour une voiture.

        Parametres
        ----------
        v :
            Voiture pour laquelle on souhaite trouver une place.

        Returns
        -------
        Place
            Place attribuée à la voiture.
        """
        pass

    def NbPlacesLibresParNiveau(self, niveau: str) -> int:
        """
        Renvoie le nombre de places libres sur un niveau donné.

        Parametres
        ----------
        niveau : str
            Identifiant du niveau (par exemple 'A', 'B', 'C', ...).

        Returns
        -------
        int
            Nombre de places libres sur ce niveau.
        """
        pass

    def addAbonnement(self, ab : Abonnement) -> None:
        """
        Ajoute un abonnement géré par le parking.

        Parametres
        ----------
        ab :
            Abonnement à enregistrer dans le parking.
        """
        pass
