"""
Voiture.

Ce module définit la classe Voiture, qui représente un véhicule
susceptible d'être garé dans le parking.
"""

from noyau.placement import Placement


class Voiture:
    """
    Voiture.

    Une voiture est caractérisée par ses dimensions, son immatriculation
    et le fait qu'elle soit actuellement dans le parking ou non.

    Attribues
    ----------
    hauteur : float
        Hauteur du véhicule.
    longueur : float
        Longueur du véhicule.
    _immatriculation : str
        Immatriculation de la voiture.
    estDansParking : bool
        True si la voiture se trouve actuellement dans le parking,
        False sinon.
    """

    def __init__(self, hauteur: float, longueur: float, immatriculation: str, estDansParking: bool):
        """
        Initialise une voiture.

        Parametres
        ----------
        hauteur : float
            Hauteur du véhicule.
        longueur : float
            Longueur du véhicule.
        _immatriculation : str
            Immatriculation de la voiture.
        estDansParking : bool
            Indique si la voiture est présente dans le parking.
        """
        if hauteur <= 0:
            raise ValueError(f"Erreur capteur : La hauteur détectée est invalide ({hauteur}).")
        if longueur <= 0:
            raise ValueError(f"Erreur capteur : La longueur détectée est invalide ({longueur}).")
        if not immatriculation:
            raise ValueError("Erreur capteur : Aucune immatriculation détectée.")
        
        self.hauteur = hauteur
        self.longueur = longueur
        self.immatriculation = immatriculation
        self.estDansParking = estDansParking

        self.placementCourant = None 

    def addPlacementV(self, p: Placement) -> None :
        """
        Ajoute un placement associé à cette voiture.

        Parametres
        ----------
        p : Placement
            Placement représentant l'occupation d'une place par la voiture.
        """
        self.placementCourant = p
        self.estDansParking = True
