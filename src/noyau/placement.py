"""
Placement.

Ce module définit la classe Placement, qui représente l'occupation
d'une place de parking par une voiture pendant une période donnée.
"""

from datetime import date


class Placement:
    """
    Placement d'une voiture sur une place du parking.

    Un placement est défini par une période (date de début, date de fin)
    et un état indiquant s'il est encore en cours ou non.

    Attribues
    ----------
    dateDebut : date
        Date de début du placement.
    dateFin : date
        Date de fin du placement.
    estEnCours : bool
        True si le placement est toujours en cours, False sinon.
    """

    def __init__(self, dateDebut: date, dateFin: date, estEnCours: bool):
        """
        Initialise un placement.

        Parametres
        ----------
        dateDebut : date
            Date de début du placement.
        dateFin : date
            Date de fin du placement.
        estEnCours : bool
            État initial du placement (en cours ou non).
        """
        if dateFin < dateDebut:
            raise ValueError(f"La date de fin {dateFin} ne peut pas être antérieure à la date de début {dateDebut}")
        
        self.dateDebut = dateDebut
        self.dateFin = dateFin
        self.estEnCours = estEnCours

        self.voiture = None
        self.place = None

    def partirPlace(self) -> None:
        """
        Met fin au placement sur la place.

        Cette méthode représente le départ de la voiture de la place
        de stationnement.
        """
        if not self.estEnCours:
            return
        
        self.estEnCours = False
        self.dateFin = date.today()
