import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from place import Place
from placement import Placement


class TestPlace(unittest.TestCase):
    """Tests de la classe Place."""

    def test_initialisation_attributs_corrects(self):
        """
        Vérifie qu'une place est correctement initialisée avec les valeurs fournies.

        Scénario prévu :
        - Créer une Place avec un idPlace, un numéro, un niveau, une longueur,
          une hauteur et un état (libre/occupée).
        - Vérifier que les attributs internes (idPlace, numero, _niveau,
          _longueur, _hauteur, _estLibre) correspondent aux valeurs passées
          au constructeur.
        """
        pass

    def test_place_libre_au_depart(self):
        """
        Vérifie qu'une place initialisée comme libre est bien considérée
        comme libre.

        Scénario prévu :
        - Créer une Place avec estLibre=True.
        - Vérifier que l'état interne de la place reflète bien qu'elle est libre
          (par exemple via _estLibre ou une future méthode d'accès).
        """
        pass

    def test_place_occupee_au_depart(self):
        """
        Vérifie qu'une place initialisée comme occupée est bien considérée
        comme occupée.

        Scénario prévu :
        - Créer une Place avec estLibre=False.
        - Vérifier que l'état interne de la place reflète bien qu'elle est
          occupée.
        """
        pass

    def test_add_placement_associe_placement_a_la_place(self):
        """
        Vérifie que addPlacement() associe correctement un placement à la place.

        Scénario prévu :
        - Créer une Place libre.
        - Créer un Placement.
        - Appeler addPlacement(placement) sur la place.
        - Vérifier que le placement est bien enregistré dans la structure
          interne de la place.
        - Vérifier éventuellement que la place n'est plus considérée comme libre.
        """
        pass

    def test_add_placement_sur_place_deja_occupee(self):
        """
        Vérifie le comportement de addPlacement() lorsqu'on tente d'ajouter
        un placement sur une place déjà occupée.

        Comportement attendu :
        - Soit la méthode refuse le nouveau placement (exception ou retour
          d'erreur),
        - soit elle gère explicitement ce cas (par exemple file d'attente,
          ou remplacement), mais ce comportement doit être testé.
        """
        pass

    def test_identifiant_place_coherent_avec_niveau_et_numero(self):
        """
        Vérifie que l'identifiant de place (idPlace) est cohérent avec
        le niveau et le numéro.

        Scénario possibles :
        - Créer une Place avec niveau='A' et numero=1, idPlace='A1'.
        - Vérifier que l'idPlace correspond bien à la combinaison du niveau
          et du numéro, conformément à la convention choisie.
        - Si l'idPlace est calculé automatiquement dans le futur, adapter le
          test pour refléter cette logique.
        """
        pass


if __name__ == "__main__":
    unittest.main()
