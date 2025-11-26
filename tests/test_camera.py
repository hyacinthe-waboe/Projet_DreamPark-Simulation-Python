import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from camera import Camera
from voiture import Voiture


class TestCamera(unittest.TestCase):
    """Tests de la classe Camera."""

    def test_capturer_hauteur_voiture_valide(self):
        """
        Vérifie que capturerHauteur() retourne la bonne hauteur
        pour une voiture dont les dimensions sont connues.

        Scénario prévu :
        - Créer une voiture avec une hauteur donnée.
        - Créer une caméra.
        - Appeler capturerHauteur(voiture).
        - Vérifier que la valeur retournée correspond à la hauteur
          enregistrée dans la voiture.
        """
        v = Voiture(hauteur=2.2, longueur=4.0, immatriculation="H-TEST", estDansParking=False)
        cam = Camera()
        
        self.assertEqual(cam.capturerHauteur(v), 2.2)

    def test_capturer_longueur_voiture_valide(self):
        """
        Vérifie que capturerLongueur() retourne la bonne longueur
        pour une voiture dont les dimensions sont connues.

        Scénario prévu :
        - Créer une voiture avec une longueur donnée.
        - Créer une caméra.
        - Appeler capturerLongueur(voiture).
        - Vérifier que la valeur retournée correspond à la longueur
          enregistrée dans la voiture.
        """
        v = Voiture(hauteur=2.2, longueur=4.8, immatriculation="L-TEST", estDansParking=False)
        cam = Camera()
        
        self.assertEqual(cam.capturerLongueur(v), 4.8)

    def test_capturer_immatr_voiture_valide(self):
        """
        Vérifie que capturerImmatr() retourne la bonne immatriculation.

        Scénario prévu :
        - Créer une voiture avec une immatriculation précise
          (par ex. 'AB-123-CD').
        - Créer une caméra.
        - Appeler capturerImmatr(voiture).
        - Vérifier que la chaîne retournée est exactement l'immatriculation
          de la voiture.
        """
        v = Voiture(hauteur=2.2, longueur=4.0, immatriculation="IMMAT-3", estDansParking=False)
        cam = Camera()
        
        self.assertEqual(cam.capturerImmatr(v), "IMMAT-3")


if __name__ == "__main__":
    unittest.main()
