"""
Camera.

Ce module définit la classe Camera, qui permet de récupérer différentes
informations sur une voiture passant devant l'accès, qui rentre dans le parking, qui
en sort etc...
"""

import voiture

class Camera:
    """
    Caméra associée à un accès du parking.

    La caméra fournit des opérations pour mesurer les caractéristiques
    d'une voiture et lire son immatriculation.
    """

    def capturerHauteur(self, v : voiture) -> float:
        """
        Capture la hauteur d'une voiture.

        Parametres
        ----------
        v :
            Voiture observée par la caméra.

        Returns
        -------
        float
            Hauteur de la voiture.
        """
        pass

    def capturerLongueur(self, v : voiture) -> float:
        """
        Capture la longueur d'une voiture.

        Parametres
        ----------
        v :
            Voiture observée par la caméra.

        Returns
        -------
        float
            Longueur de la voiture.
        """
        pass

    def capturerImmatr(self, v : voiture) -> str:
        """
        Capture l'immatriculation d'une voiture.

        Parametres
        ----------
        v :
            Voiture observée par la caméra.

        Returns
        -------
        str
            Immatriculation lue par la caméra.
        """
        pass
