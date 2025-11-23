"""
Place.

Ce module définit la classe Place, qui représente une place de
stationnement dans le parking.
"""
from placement import Placement

class Place:
    """
    Place de stationnement.

    Une place de stationnement est caractérisée par :
    - un niveau,
    - un numéro sur ce niveau,
    - ses dimensions,
    - un état (libre ou occupée),
    - un identifiant textuel unique combinant niveau et numéro
      (par exemple : "A1", "B1", "C15").

    Attribues
    ----------
    idPlace : str
        Identifiant unique de la place, calculé à partir du niveau
        et du numéro (exemples : "A1", "B1", "C15").
    numero : int
        Numéro de la place sur le niveau.
    _niveau : str
        Identifiant du niveau (par exemple 'A', 'B', 'C', ...).
    _longueur : float
        Longueur maximale acceptée pour un véhicule sur cette place.
    _hauteur : float
        Hauteur maximale acceptée pour un véhicule sur cette place.
    _estLibre : bool
        True si la place est libre, False si elle est occupée.
    """

    def __init__(self, idPlace: str, numero: int, niveau: str,longueur: float, hauteur: float, estLibre: bool):
        """
        Initialise une place de stationnement.

        Parametres
        ----------
        idPlace : str
            Identifiant unique de la place (par exemple "A1", "B1", "C15").
        numero : int
            Numéro de la place sur le niveau.
        _niveau : str
            Identifiant du niveau (par exemple 'A', 'B', 'C', ...).
        _longueur : float
            Longueur maximale acceptée pour un véhicule sur cette place.
        _hauteur : float
            Hauteur maximale acceptée pour un véhicule sur cette place.
        _estLibre : bool
            True si la place est libre, False si elle est occupée.
        """
        pass

    def addPlacement(self, p : Placement) -> None:
        """
        Ajoute un placement associé à cette place.

        Parametres
        ----------
        p :
            Placement à associer à la place.
        """
        pass
