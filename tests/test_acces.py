import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from acces import Acces
from client import Client
from parking import Parking
from camera import Camera
from panneau_affichage import PanneauAffichage
from borne_ticket import BorneTicket
from teleporteur import Teleporteur



class TestAcces(unittest.TestCase):
    """Tests de la classe Acces."""

    def setUp(self):
        """
        Initialisation commune pour les tests.
        """
        self.parking = Parking(10, 10, 10, 1)
        self.camera = Camera()
        self.panneau = PanneauAffichage()
        self.borne = BorneTicket()
        self.teleporteur = Teleporteur()

        self.acces = Acces(self.parking, self.camera, self.panneau, self.borne, self.teleporteur)

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
        c = Client("Jean", "Rue A", False, False, 0)
        c.nouvelleVoiture("AB-123-CD", 2.0, 4.0)
        
        v_detectee = self.acces.actionnerCamera(c)
        
        self.assertEqual(v_detectee, c.voiture)
        self.assertEqual(v_detectee.immatriculation, "AB-123-CD")

    def test_actionner_camera_client_sans_voiture_declenche_erreur(self):
        """
        Vérifie que actionnerCamera() gère le cas d'un client sans voiture.

        Comportement attendu :
        - Soit la méthode lève une exception 
        - soit elle retourne une valeur spéciale (None) ou un message d'erreur,
          mais le cas doit être traité !
        """
        c = Client("Jean", "Rue A", False, False, 0)
        
        with self.assertRaises(ValueError):
            self.acces.actionnerCamera(c)

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
        msg = self.acces.actionnerPanneau()

        self.assertIn("10 places disponibles", msg)

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

        for p in self.parking.places:
            p._estLibre = False
        self.parking._nbPlacesLibres = 0 
        
        msg = self.acces.actionnerPanneau()
        self.assertIn("COMPLET", msg)

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
        c = Client("Marie", "Rue B", estAbonne=True, estSuperAbonne=False, nbFrequentations=5)
        c.nouvelleVoiture("CC-888-DD", 1.5, 3.0)

        resultat = self.acces.lancerProcedureEntree(c)
        
        self.assertIn("Bienvenue", resultat)
        self.assertIn("Voiture garée", resultat)

        self.assertTrue(c.voiture.estDansParking)

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
        c = Client("Paul", "Rue C", estAbonne=False, estSuperAbonne=False, nbFrequentations=0)
        c.nouvelleVoiture("XX-123-YY", 1.5, 3.0)
        
        resultat = self.acces.lancerProcedureEntree(c)
        
        self.assertIn("Bienvenue", resultat)
        self.assertTrue(c.voiture.estDansParking)

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
        c = Client("Luc", "Rue D", False, False, 0)
        c.nouvelleVoiture("ZZ-000-ZZ", 1.5, 3.0)
        
        for p in self.parking.places:
            p._estLibre = False
        self.parking._nbPlacesLibres = 0
            
        resultat = self.acces.lancerProcedureEntree(c)
        
        self.assertIn("aucune place disponible", resultat)
        self.assertFalse(c.voiture.estDansParking)


if __name__ == "__main__":
    unittest.main()
