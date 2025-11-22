"""
Service.

Ce module définit la classe Service, qui représente un service
planifié pour un véhicule.
"""

from datetime import date


class Service:
    """
    Service planifié.

    Un service est caractérisé par la date à laquelle il a été demandé,
    la date à laquelle il doit être réalisé et un rapport décrivant
    son déroulement ou son résultat.

    Attribues
    ----------
    dateDemande : date
        Date à laquelle le service a été demandé.
    dateService : date
        Date prévue (ou effective) de réalisation du service.
    rapport : str
        Rapport associé au service (compte-rendu, commentaire, etc.).
    """

    def __init__(self, dateDemande: date, dateService: date, rapport: str):
        """
        Initialise un service.

        Parametres
        ----------
        dateDemande : date
            Date de demande du service.
        dateService : date
            Date de réalisation prévue du service.
        rapport : str
            Rapport associé au service.
        """
        pass
