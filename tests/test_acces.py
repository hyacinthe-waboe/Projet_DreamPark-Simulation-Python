import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from acces import Acces
from client import Client
from voiture import Voiture



class TestAcces(unittest.TestCase):
    """Tests de la classe Acces."""

    def test_actionner_camera_client_avec_voiture(self):
        """
        Vérifie que actionnerCamera() retourne bien la voiture du client
        lorsque celui-ci possède une voiture déclarée.

        Scénario prévu :
        - Créer un client avec une voiture associée.
        - Créer un accès disposant d'une caméra.
        - Appeler actionnerCamera(client).
        - Vérifier que la Voiture retournée correspond à la voiture du client.
        """
        pass

    def test_actionner_camera_client_sans_voiture_declenche_erreur(self):
        """
        Vérifie que actionnerCamera() gère le cas d'un client sans voiture.

        Comportement attendu :
        - Soit la méthode lève une exception 
        - soit elle retourne une valeur spéciale (None) ou un message d'erreur,
          mais le cas doit être traité !
        """
        pass

    def test_actionner_panneau_affiche_places_disponibles(self):
        """
        Vérifie que actionnerPanneau() renvoie un message cohérent sur
        le nombre de places disponibles.

        Scénario prévu :
        - Créer un parking avec un certain nombre de places libres.
        - Créer un panneau d'affichage associé au parking.
        - Créer un accès relié à ce panneau.
        - Appeler actionnerPanneau().
        - Vérifier que la chaîne retournée mentionne le nombre de places
          libres.
        - Eventuellement rajouter des places dans le parking pour voir si le nombre
          de place libres décrementes. 
        """
        pass

    def test_actionner_panneau_parking_complet(self):
        """
        Vérifie que actionnerPanneau() indique que le parking est complet
        lorsque aucune place n'est disponible.

        Scénario prévu :
        - Créer un parking sans aucune place libre.
        - Créer un accès relié à ce parking et à son panneau d'affichage.
        - Appeler actionnerPanneau().
        - Vérifier que le message retourné signale que le parking est complet.
        """
        pass

    def test_lancer_procedure_entree_client_abonne_place_disponible(self):
        """
        Vérifie que lancerProcedureEntree() fonctionne correctement pour
        un client abonné lorsqu'une place est disponible.

        Scénario prévu :
        - Créer un client abonné avec une voiture.
        - Créer un parking avec au moins une place libre.
        - Créer un accès relié au parking (et éventuellement au téléporteur,
          borne de ticket, etc.).
        - Appeler lancerProcedureEntree(client).
        - Vérifier que le résultat indique une entrée réussie.
        """
        pass

    def test_lancer_procedure_entree_client_non_abonne(self):
        """
        Vérifie que lancerProcedureEntree() traite correctement le cas
        d'un client non abonné.

        Scénario prévu :
        - Créer un client non abonné avec une voiture.
        - Créer un accès relié au reste du système.
        - Appeler lancerProcedureEntree(client).
        - Vérifier que le résultat reflète le parcours prévu pour un
          non-abonné (par exemple passage par la borne de ticket,
          proposition d'abonnement, etc.).
        """
        pass

    def test_lancer_procedure_entree_sans_place_disponible(self):
        """
        Vérifie que lancerProcedureEntree() signale l'absence de place
        lorsque le parking est complet.

        Scénario prévu :
        - Créer un client (abonné ou non) avec une voiture.
        - Créer un parking sans aucune place libre.
        - Créer un accès associé à ce parking.
        - Appeler lancerProcedureEntree(client).
        - Vérifier que le résultat indique clairement que l'entrée est
          impossible faute de place disponible.
        """
        pass


if __name__ == "__main__":
    unittest.main()
