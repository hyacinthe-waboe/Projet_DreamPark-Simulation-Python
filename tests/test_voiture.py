import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from voiture import Voiture
from placement import Placement
from datetime import date


class TestVoiture(unittest.TestCase):
    """Tests de la classe Voiture."""

    def test_initialisation_attributs_corrects(self):
        """
        Vérifie qu'une voiture est correctement initialisée avec les valeurs fournies.

        Scénario prévu :
        - Créer une Voiture avec une hauteur, une longueur, une immatriculation
          et un booléen estDansParking.
        - Vérifier que les attributs internes (hauteur, longueur,
          _immatriculation, estDansParking) correspondent aux valeurs passées
          au constructeur.
        """
        v = Voiture(hauteur=1.8, longueur=4.5, immatriculation="XX-777-YY", estDansParking=False)
        
        self.assertEqual(v.hauteur, 1.8)
        self.assertEqual(v.longueur, 4.5)
        self.assertEqual(v.immatriculation, "XX-777-YY")
        self.assertFalse(v.estDansParking)

    def test_initialisation_est_dans_parking_true(self):
        """
        Vérifie qu'une voiture initialisée avec estDansParking=True est bien
        considérée comme présente dans le parking.

        Scénario prévu :
        - Créer une Voiture avec estDansParking=True.
        - Vérifier que l'état interne reflète bien que la voiture est dans
          le parking.
        """
        v = Voiture(hauteur=1.8, longueur=4.5, immatriculation="XX-777-YY", estDansParking=True)
        
        self.assertTrue(v.estDansParking)

    def test_initialisation_est_dans_parking_false(self):
        """
        Vérifie qu'une voiture initialisée avec estDansParking=False est bien
        considérée comme hors du parking.

        Scénario prévu :
        - Créer une Voiture avec estDansParking=False.
        - Vérifier que l'état interne reflète bien que la voiture n'est pas
          dans le parking.
        """
        v = Voiture(hauteur=1.8, longueur=4.5, immatriculation="XX-777-YY", estDansParking=False)
        
        self.assertFalse(v.estDansParking)

    def test_addPlacementV_associe_placement_a_la_voiture(self):
        """
        Vérifie que addPlacementV() associe correctement un placement à la voiture.

        Scénario prévu :
        - Créer une Voiture.
        - Créer un Placement.
        - Appeler addPlacementV(placement) sur la voiture.
        - Vérifier que le placement est bien enregistré dans la structure
          interne de la voiture.
        - Vérifier éventuellement que estDansParking passe à True si la
          voiture est considérée comme entrée dans le parking.
        """
        v = Voiture(1.8, 4.5, "XX-777-YY", False)
        p = Placement(date.today(), date.today(), True)
        
        v.addPlacementV(p)
        
        self.assertEqual(v.placementCourant, p)
        self.assertTrue(v.estDansParking)

    def test_addPlacementV_plusieurs_placements(self):
        """
        Vérifie que addPlacementV() permet d'associer plusieurs placements
        à la même voiture au cours du temps.

        Scénario prévu :
        - Créer une Voiture.
        - Créer plusieurs Placement.
        - Appeler addPlacementV() pour chacun d'eux.
        - Vérifier que tous les placements sont bien enregistrés.
        """
        v = Voiture(1.8, 4.5, "XX-777-YY", False)
        p1 = Placement(date.today(), date.today(), False)
        p2 = Placement(date.today(), date.today(), True)
        
        v.addPlacementV(p1)
        v.addPlacementV(p2) 
        
        self.assertEqual(v.placementCourant, p2)

    def test_immatriculation_invalide(self):
        """
        Vérifie que l'initialisation refuse ou signale une immatriculation
        vide ou invalide.

        Comportement possibles :
        - Créer une Voiture avec une immatriculation vide ('') ou invalide.
        - Vérifier que ce cas est refusé (exception) ou signalé, plutôt que
          d'accepter silencieusement une immatriculation incohérente.
        """
        with self.assertRaises(ValueError):
            Voiture(1.8, 4.5, "", False)
            
        with self.assertRaises(ValueError):
            Voiture(1.8, 4.5, None, False)

    def test_hauteur_invalide_leve_exception(self):
        """Vérifie qu'une hauteur négative ou nulle est refusée."""
        with self.assertRaises(ValueError):
            Voiture(-1.0, 4.0, "TEST", False)
        
        # Hauteur nulle
        with self.assertRaises(ValueError):
            Voiture(0.0, 4.0, "TEST", False)

    def test_longueur_invalide_leve_exception(self):
        """Vérifie qu'une longueur négative ou nulle est refusée."""
        with self.assertRaises(ValueError):
            Voiture(1.5, -4.0, "TEST", False)
            
        with self.assertRaises(ValueError):
            Voiture(1.5, 0.0, "TEST", False)

if __name__ == "__main__":
    unittest.main()
