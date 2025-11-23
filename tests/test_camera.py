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
        pass

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
        pass

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
        pass

    def test_capturer_hauteur_voiture_non_initialisee(self):
        """
        Vérifie que capturerHauteur() gère le cas d'une voiture dont
        la hauteur n'est pas correctement initialisée.

        Comportement attendu :
        - Soit la méthode lève une exception.
        - soit elle retourne une valeur spéciale (None, -1, etc.).
        """
        pass

    def test_capturer_longueur_voiture_non_initialisee(self):
        """
        Vérifie que capturerLongueur() gère le cas d'une voiture dont
        la longueur n'est pas correctement initialisée.

        Comportement attendu :
        - Soit la méthode lève une exception.
        - soit elle retourne une valeur spéciale (None, -1, etc.).
        """
        pass

    def test_capturer_immatr_voiture_sans_immatriculation(self):
        """
        Vérifie que capturerImmatr() gère le cas d'une voiture sans
        immatriculation enregistrée.

        Comportement attendu :
        - Soit une exception est levée,
        - soit une valeur particulière est renvoyée (par ex. chaîne vide
          ou message d'erreur).
        """
        pass


if __name__ == "__main__":
    unittest.main()
