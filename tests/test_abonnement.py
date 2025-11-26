import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from abonnement import Abonnement
from contrat import Contrat


class TestAbonnement(unittest.TestCase):
    """Tests de la classe Abonnement."""

    def test_initialisation_attributs_corrects(self):
        """
        Vérifie qu'un abonnement est correctement initialisé avec des
        valeurs valides (libellé, prix positif, indicateur de pack garanti).

        - Créer un abonnement avec un libellé, un prix positif et estPackGar=False.
        - Vérifier que les attributs internes de l'objet correspondent aux
          valeurs fournies au constructeur.
        """
        ab = Abonnement(libelle="PackGarantie", prix=10,estPackGar=False)
        
        self.assertEqual(ab.libelle, "PackGarantie")
        self.assertEqual(ab.prix, 10)
        self.assertFalse(ab.estPackGar)

    def test_initialisation_pack_garanti(self):
        """
        Vérifie que l'on peut créer un abonnement correspondant au pack garanti.

        - Créer un abonnement avec estPackGar=True.
        - Vérifier que l'attribut indiquant le pack garanti est bien positionné.
        """
        ab = Abonnement(libelle="PackGarantie", prix=10,estPackGar=True)

        self.assertTrue(ab.estPackGar)

    def test_initialisation_prix_negatif_declenche_erreur(self):
        """
        Vérifie que l'initialisation d'un abonnement avec un prix négatif est refusée.

        Comportement attendu  :
        - Le constructeur doit détecter un prix invalide (négatif) et provoquer
          une erreur (par exemple ValueError) plutôt que d'accepter la valeur.
        """
        with self.assertRaises(ValueError):
            ab = Abonnement(libelle="PackGarantie", prix=-10,estPackGar=True)
        

    def test_add_contrat_ajoute_contrat_a_l_abonnement(self):
        """
        Vérifie que addContrat() associe un contrat à l'abonnement.

        Ce qu'on doit faire :
        - Créer un abonnement sans contrat associé.
        - Créer un contrat.
        - Appeler addContrat(contrat).
        - Vérifier que le contrat ajouté est bien enregistré dans la structure
          interne de l'abonnement.
        """
        ab = Abonnement("Standard", 50.0, False)
        ab.addContrat("Test")
        self.assertEqual(len(ab.contrats), 1)

    def test_add_contrat_peut_ajouter_plusieurs_contrats(self):
        """
        Vérifie que plusieurs contrats peuvent être associés au même abonnement.

        Ce qu'on doit faire  :
        - Créer un abonnement.
        - Créer plusieurs contrats.
        - Appeler addContrat() pour chacun d'eux.
        - Vérifier que l'abonnement référence l'ensemble des contrats ajoutés.
        """
        ab = Abonnement("Pro", 100.0, True)

        ab.addContrat("c1")
        ab.addContrat("c2")

        self.assertEqual(len(ab.contrats), 2)
        self.assertEqual(ab.contrats, ["c1", "c2"])


if __name__ == "__main__":
    unittest.main()
