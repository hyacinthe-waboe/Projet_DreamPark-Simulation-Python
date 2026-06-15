"""
Contrat.

Ce module définit la classe Contrat, qui représente un contrat d'abonnement
liant un client à un service de stationnement.
"""

from datetime import date


class Contrat:
    """
    Contrat d'abonnement.

    Un contrat d'abonnement est défini par une période de validité et un état
    indiquant s'il est actuellement en cours ou non.

    Attribues
    ----------
    dateDebut : date
        Date de début de validité du contrat.
    dateFin : date
        Date de fin de validité du contrat.
    estEnCours : bool
        Indique si le contrat est actuellement en cours.
    """

    def __init__(self, dateDebut: date, dateFin: date, estEnCours: bool):
        """
        Initialise un contrat d'abonnement.

        Parametres
        ----------
        dateDebut : date
            Date de début de validité du contrat.
        dateFin : date
            Date de fin de validité du contrat.
        estEnCours : bool
            État initial du contrat : True s'il est en cours, False sinon.
        """
        if dateFin < dateDebut:
            raise ValueError(f"La date de fin ({dateFin}) ne peut pas être antérieure à la date de début ({dateDebut}).")
        
        self.dateDebut = dateDebut
        self.dateFin = dateFin
        self.estEnCours = estEnCours

    def rompreContrat(self)-> None:
        """
        Rompt le contrat.

        Met le contrat dans un état où il n'est plus en cours. La manière
        précise dont l'état et les dates sont modifiés est définie par
        l'implémentation.
        """
        self.estEnCours = False
        self.dateFin = date.today()
