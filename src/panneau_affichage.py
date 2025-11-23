"""
Panneau d'affichage.

Ce module définit la classe PanneauAffichage, responsable de l'affichage
du nombre de places disponibles à l'entrée du parking.
"""

from parking import Parking


class PanneauAffichage:
    """
    Panneau d'affichage du parking.

    Le panneau indique au client le nombre de places disponibles dans
    le parking, afin qu'il sache s'il peut entrer ou non.
    """

    def afficherNbPlacesDisponibles(self, p: Parking) -> str:
        """
        Affiche le nombre de places disponibles pour un parking donné.

        Parametres
        ----------
        p : Parking
            Parking pour lequel on souhaite afficher le nombre de places
            disponibles.

        Returns
        -------
        str
            Message à afficher sur le panneau (par exemple : "35 places
            disponibles").
        """
        pass
