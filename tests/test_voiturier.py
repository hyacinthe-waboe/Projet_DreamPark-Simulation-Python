import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from datetime import date,timedelta
from voiturier import Voiturier
from voiture import Voiture


class TestVoiturier(unittest.TestCase):
    """Tests de la classe Voiturier."""
    def setUp(self):
        """Instanciation des objets communs aux tests."""
        self.today = date.today()
        self.demain = self.today + timedelta(days=1)
        self.hier = self.today - timedelta(days=1)

        self.voiturier = Voiturier(1)
        self.voiture = Voiture(1.80,2,"TEST-VOIT", True)

    def test_initialisation_numero_correct(self):
        """
        Vérifie qu'un voiturier est correctement initialisé avec un numéro.

        Scénario prévu :
        - Créer un Voiturier avec un numVoiturier donné (par ex. 1).
        - Vérifier que l'attribut interne (_numVoiturier) correspond bien
          à la valeur passée au constructeur.
        """
        self.assertEqual(self.voiturier._numVoiturier, 1)
        self.assertIsInstance(self.voiturier, Voiturier)

    def test_initialisation_numero_negatif_declenche_erreur(self):
        """
        Vérifie que l'initialisation avec un numéro de voiturier négatif
        est refusée.

        Comportement attendu :
        - Si numVoiturier < 0, le constructeur doit refuser la création
          (par exemple en levant une exception comme ValueError), plutôt
          que d'accepter un identifiant incohérent.
        """
        with self.assertRaises(ValueError):
          Voiturier(-8)

    def test_livrerVoiture_date_et_heure_valides(self):
        """
        Vérifie que livrerVoiture() fonctionne correctement pour une
        date et une heure de livraison valides.

        Scénario prévu :
        - Créer une Voiture.
        - Créer un Voiturier.
        - Choisir une date de livraison (par ex. aujourd'hui ou une date
          dans le futur) et une heure valide (par ex. 14).
        - Appeler livrerVoiture(voiture, dateLivraison, heure).
        - Vérifier que la livraison est considérée comme programmée
          ou effectuée.
        """
        self.voiturier.livrerVoiture(self.voiture, self.demain, 14)

        self.assertFalse(self.voiture.estDansParking)

    def test_livrerVoiture_heure_invalide(self):
        """
        Vérifie que livrerVoiture() gère une heure de livraison invalide.

        Scénario possible :
        - Créer une Voiture et un Voiturier.
        - Appeler livrerVoiture() avec une heure hors plage (par ex. -1 ou 25).
        - Vérifier que ce cas est refusé ou signalé (exception, message
          d'erreur, etc.), conformément aux règles qui seront définies.
        """
        with self.assertRaises(ValueError):
          self.voiturier.livrerVoiture(self.voiture, self.demain, -90)

    def test_livrerVoiture_date_dans_le_passe(self):
        """
        Vérifie que livrerVoiture() gère une date de livraison située
        dans le passé.

        Scénario possible :
        - Créer une Voiture et un Voiturier.
        - Choisir une dateLivraison antérieure à la date du jour.
        - Appeler livrerVoiture(voiture, dateLivraison, heure).
        - Vérifier que la méthode refuse ou signale cette situation
          (exception, message, etc.).
        """
        with self.assertRaises(ValueError):
          self.voiturier.livrerVoiture(self.voiture, self.hier, 12)

    def test_livrerVoiture_sans_voiture_valide(self):
        """
        Vérifie que livrerVoiture() gère le cas où la voiture n'est pas valide
        ou absente.

        Scénario possible :
        - Créer un Voiturier.
        - Appeler livrerVoiture(None, dateLivraison, heure) ou avec une voiture
          dont certains attributs indispensables ne sont pas initialisés.
        - Vérifier que ce cas est refusé ou signalé clairement.
        """
        with self.assertRaises(ValueError):
          self.voiturier.livrerVoiture(None, self.hier, 12)

    def test_livrerVoiture_plusieurs_livraisons(self):
        """
        Vérifie le comportement de livrerVoiture() lorsqu'un même voiturier
        effectue plusieurs livraisons.

        Scénario prévu :
        - Créer un Voiturier.
        - Créer plusieurs Voiture (ou plusieurs demandes de livraison pour
          la même voiture à des dates/heures différentes).
        - Appeler livrerVoiture() plusieurs fois.
        - Vérifier que chaque livraison est correctement prise en compte.
        """
        self.voiturier.livrerVoiture(self.voiture, self.demain, 14)

        with self.assertRaises(ValueError):
          self.voiturier.livrerVoiture(self.voiture, self.demain, 14)

if __name__ == "__main__":
    unittest.main()
