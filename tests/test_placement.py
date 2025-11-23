import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from datetime import date, timedelta
from placement import Placement


class TestPlacement(unittest.TestCase):
    """Tests de la classe Placement."""

    def test_initialisation_attributs_corrects(self):
        """
        Vérifie qu'un placement est correctement initialisé avec les valeurs fournies.

        Scénario prévu :
        - Choisir une dateDebut et une dateFin telles que dateFin >= dateDebut.
        - Créer un Placement avec ces dates et un booléen estEnCours.
        - Vérifier que les attributs internes (dateDebut, dateFin, estEnCours)
          correspondent exactement aux valeurs passées au constructeur.
        """
        pass

    def test_initialisation_date_fin_avant_date_debut_declenche_erreur(self):
        """
        Vérifie qu'un placement ne peut pas être initialisé avec une date de fin
        antérieure à la date de début.

        Comportement attendu :
        - Si dateFin < dateDebut, le constructeur doit refuser la création du
          placement (par exemple en levant une exception comme ValueError),
          plutôt que d'accepter un état incohérent.
        """
        pass

    def test_placement_en_cours_durant_la_periode(self):
        """
        Vérifie qu'un placement marqué comme en cours est cohérent avec la période
        définie par dateDebut et dateFin.

        Scénario prévu :
        - Créer un Placement avec estEnCours=True et des dates couvrant la
          période actuelle (par exemple dateDebut <= aujourd'hui <= dateFin).
        - Vérifier que l'état estEnCours est compatible avec ces dates et que
          le placement est bien interprété comme toujours actif.
        """
        pass

    def test_partirPlace_met_est_en_cours_a_false(self):
        """
        Vérifie que partirPlace() met fin au placement.

        Scénario prévu :
        - Créer un Placement avec estEnCours=True.
        - Appeler partirPlace().
        - Vérifier que estEnCours vaut désormais False.
        """
        pass

    def test_partirPlace_met_a_jour_date_fin_eventuellement(self):
        """
        Vérifie que partirPlace() met éventuellement à jour la date de fin.

        Comportement possibles :
        - Créer un Placement avec une dateDebut donnée et une dateFin éventuellement
          non fixée ou éloignée dans le futur.
        - Appeler partirPlace().
        - Vérifier que dateFin est mise à une valeur cohérente avec la date de
          départ effective (par exemple la date du jour).
        """
        pass

    def test_partirPlace_sur_placement_deja_termine(self):
        """
        Vérifie le comportement de partirPlace() lorsqu'on l'appelle sur un
        placement déjà terminé (estEnCours=False).

        Comportement attendu :
        - Soit la méthode ne modifie plus l'état ni les dates,
        - soit elle signale que le placement est déjà terminé (exception ou
          message), mais ce cas doit être explicitement géré.
        """
        pass


if __name__ == "__main__":
    unittest.main()
