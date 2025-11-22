"""
Acces.

Ce module définit la classe Acces, qui représente un point d'accès
au parking (borne d'entrée/sortie).
"""


import client
import voiture


class Acces:
    """
    Point d'accès au parking.

    Un accès regroupe les opérations déclenchées lorsqu'un client arrive
    ou interagit avec le système : utilisation de la caméra, du panneau
    d'affichage et lancement de la procédure d'entrée.
    """

    def actionnerCamera(self, client: "client") :
        """
        Actionne la caméra pour le client donné.

        Parametres
        ----------
        client : Client
            Client qui se présente à l'accès.

        Returns
        -------
        Voiture
            Voiture associée au client.
        """
        pass

    def actionnerPanneau(self) :
        """
        Actionne le panneau d'affichage associé à l'accès.

        Returns
        -------
        str
            Message affiché ou résultat de l'action sur le panneau.
        """
        pass

    def lancerProcedureEntree(self, client: "client") :
        """
        Lance la procédure d'entrée pour un client.

        Parametres
        ----------
        client : Client
            Client qui souhaite entrer dans le parking.

        Returns
        -------
        str
            Résultat de la procédure d'entrée.
        """
        pass
