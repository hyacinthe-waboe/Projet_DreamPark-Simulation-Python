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

    def __init__(self, _numVoiturier: int) -> None:
        """
        Initialise un voiturier.

        Parametres
        ----------
        _numVoiturier : int
            Numéro identifiant le voiturier.
        """
        if _numVoiturier < 0 :
            raise ValueError(f"Erreur l'id du voiturier ne peut être négatif")
        
        self._numVoiturier = _numVoiturier

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
        if v is None or not isinstance(v, Voiture):
            raise ValueError("Une voiture valide est requise pour la livraison")

        if hasattr(v, "estDansParking") and v.estDansParking is False:
            raise ValueError("Cette voiture a déjà été livrée ou n'est pas dans le parking")

        if not isinstance(heure, int) or heure < 0 or heure > 23:
            raise ValueError("Heure de livraison invalide (doit être entre 0 et 23)")

        today = date.today()
        if dateLivraison < today:
            raise ValueError("La date de livraison ne peut pas être dans le passé")

        if hasattr(v, "estDansParking"):
            v.estDansParking = False
