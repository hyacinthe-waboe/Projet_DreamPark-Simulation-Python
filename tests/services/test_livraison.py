import os
import sys

chemin_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
if chemin_src not in sys.path:
    sys.path.insert(0, chemin_src)

import unittest
from datetime import date
from services.livraison import Livraison
from services.entretien import Entretien
from noyau.parking import Parking
from usagers.client import Client
from usagers.voiture import Voiture


class TestLivraison(unittest.TestCase):
    """Tests de la classe Livraison."""

    def setUp(self):
        """Instanciation des objets communs aux tests."""
        self.today = date.today()
        self.rapport_initial = "Demande de livraison"
        self.adresse_valide = "12 rue du Test"

        self.parking = Parking(nbPlacesParNiveau=10, nbPlacesLibres=10, prix=20, nbNiveaux=1)
        self.client = Client(nom="Testeur", adresse="Rue Test", estAbonne=True, estSuperAbonne=False, nbFrequentations=0)
        self.voiture = Voiture(hauteur=1.5, longueur=4.0,immatriculation="AB-123-CD",estDansParking=True)

        self.client.voiture = self.voiture

        self.livraison = Livraison(self.today, None, self.rapport_initial)


    def test_initialisation_livraison_avec_attributs_service(self):
        """
        Vérifie qu'une Livraison est correctement initialisée avec les
        attributs hérités de Service (dateDemande, dateService, rapport).

        Scénario prévu :
        - Choisir une date de demande et une date de service.
        - Créer une Livraison avec ces dates et un rapport initial.
        - Vérifier que les attributs internes (dateDemande, dateService,
          rapport) correspondent aux valeurs fournies.
        """
        livraison = Livraison(self.today, self.today, self.rapport_initial)

        self.assertEqual(livraison.dateDemande, self.today)
        self.assertEqual(livraison.dateService, self.today)
        self.assertEqual(livraison.rapport, self.rapport_initial)
        self.assertIsInstance(livraison, Livraison)

    def test_effectuer_livraison_met_a_jour_rapport(self):
        """
        Vérifie que effectuerLivraison() met à jour le rapport de livraison.

        Scénario prévu :
        - Créer une Livraison avec un rapport initial (par exemple vide).
        - Appeler effectuerLivraison().
        - Vérifier qu'un rapport de livraison détaillé est enregistré
          (contenu non vide, décrivant par exemple la réussite de la livraison).
        """
        self.livraison.effectuerLivraison(self.parking, self.voiture, self.client)

        self.assertIsInstance(self.livraison.rapport, str)
        self.assertNotEqual(self.livraison.rapport, self.rapport_initial)
        self.assertIn("livraison", self.livraison.rapport.lower())


    def test_effectuer_livraison_met_a_jour_date_service_si_non_fixee(self):
        """
        Vérifie que effectuerLivraison() met à jour la date de service si
        celle-ci n'était pas encore définie.

        Scénario possible :
        - Créer une Livraison avec dateService à None ou à une valeur par défaut.
        - Appeler effectuerLivraison().
        - Vérifier que dateService est mise à la date du jour ou à une
          date cohérente avec l'exécution de la livraison.
        """
        self.assertIsNone(self.livraison.dateService)

        self.livraison.effectuerLivraison(self.parking, self.voiture, self.client)

        self.assertEqual(self.livraison.dateService, self.today)

    def test_effectuer_livraison_plusieurs_fois(self):
        """
        Vérifie le comportement de effectuerLivraison() lorsqu'on l'appelle
        plusieurs fois pour la même livraison.

        Comportement attendu :
        - Soit seule la première exécution est prise en compte et les appels
          suivants ne modifient plus l'état ou le rapport
        - soit la méthode signale que la livraison a déjà été effectuée
          (via une exception ou un message).
        """
        self.livraison.effectuerLivraison(self.parking, self.voiture, self.client)
        rapport_apres_premiere = self.livraison.rapport
        date_apres_premiere = self.livraison.dateService

        with self.assertRaises(ValueError):
            self.livraison.effectuerLivraison(self.parking, self.voiture, self.client)

        self.assertEqual(self.livraison.rapport, rapport_apres_premiere)
        self.assertEqual(self.livraison.dateService, date_apres_premiere)

if __name__ == "__main__":
    unittest.main()
