"""
Téléporteur.

Ce module définit la classe Teleporteur, qui est chargée de déplacer
les voitures entre l'extérieur et les places de stationnement du parking.
"""
from voiture import Voiture
from place import Place
from placement import Placement

class Teleporteur:
    """
    Téléporteur de voitures.

    Le téléporteur permet de :
    - placer une voiture sur une place donnée,
    - gérer un mode particulier pour les super abonnés.
    """

    def teleporterVoiture(self, v : Voiture, p : Place) -> Placement:
        """
        Téléporte une voiture vers une place de stationnement.

        Parametres
        ----------
        v :
            Voiture à téléporter.
        p :
            Place de stationnement sur laquelle la voiture doit être déposée.

        Returns
        -------
        Placement
            Placement associé à la voiture sur la place.
        """
        pass

    def teleporterVoitureSuperAbonne(self, v : Voiture ) -> str:
        """
        Téléporte une voiture appartenant à un super abonné.

        Parametres
        ----------
        v :
            Voiture du super abonné à téléporter.

        Returns
        -------
        str
            Information sur le résultat de la téléportation
            (format à préciser lors de l'implémentation).
        """
        pass
