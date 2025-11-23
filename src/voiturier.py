"""
Voiturier.

Ce module définit la classe Voiturier, qui prend en charge la livraison
des voitures pour les clients.
"""

from datetime import date
from voiture import Voiture


class Voiturier:
    """
    Voiturier.

    Le voiturier est identifié par un numéro et assure la livraison
    des véhicules aux dates et heures prévues.

    Attribues
    ----------
    _numVoiturier : int
        Numéro identifiant le voiturier.
    """

    def __init__(self, numVoiturier: int):
        """
        Initialise un voiturier.

        Parametres
        ----------
        _numVoiturier : int
            Numéro identifiant le voiturier.
        """
        pass

    def livrerVoiture(self, v: Voiture, dateLivraison: date, heure: int) -> None:
        """
        Livre une voiture au client à une date et une heure données.

        Parametres
        ----------
        v : Voiture
            Voiture à livrer.
        dateLivraison : date
            Date prévue de la livraison.
        heure : int
            Heure de la livraison (par exemple 14 pour 14h).
        """
        pass
