import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from datetime import date, timedelta
from contrat import Contrat


class TestContrat(unittest.TestCase):
    """Tests de la classe Contrat."""

    def test_initialisation_attributs_corrects(self):
        """
        Vérifie qu'un contrat est correctement initialisé avec des dates
        cohérentes et un état donné.

        Scénario prévu :
        - Créer deux dates : dateDebut < dateFin.
        - Créer un contrat avec ces deux dates et estEnCours=True ou False.
        - Vérifier que les attributs internes (dateDebut, dateFin, estEnCours)
          correspondent aux valeurs passées au constructeur.
        """
        pass

    def test_initialisation_date_fin_avant_date_debut_declenche_erreur(self):
        """
        Vérifie que l'initialisation d'un contrat avec une date de fin
        antérieure à la date de début est refusée.

        Comportement attendu :
        - Si dateFin < dateDebut, le constructeur doit lever une exception
          (par exemple ValueError) au lieu d'accepter un contrat invalide.
        """
        pass

    def test_contrat_est_en_cours_pendant_la_periode(self):
        """
        Vérifie qu'un contrat initialisé avec estEnCours=True est bien considéré
        comme en cours lorsque la date du jour est comprise entre dateDebut
        et dateFin.

        Scénario prévu :
        - Choisir des dates dateDebut et dateFin autour de la date du jour.
        - Créer un contrat avec estEnCours=True.
        - Vérifier que l'état est cohérent avec ces dates.
        """
        pass

    def test_contrat_non_en_cours_apres_date_fin(self):
        """
        Vérifie que le contrat n'est plus en cours lorsque la date actuelle
        est postérieure à dateFin.

        Comportement attendue :
        - L'attribut estEnCours est mis à jour automatiquement lorsqu'on
          met fin au contrat
        """
        pass

    def test_rompre_contrat_met_est_en_cours_a_false(self):
        """
        Vérifie que rompreContrat() met le contrat dans un état non en cours.

        Scénario prévu :
        - Créer un contrat avec estEnCours=True.
        - Appeler rompreContrat().
        - Vérifier que estEnCours vaut désormais False.
        """
        pass

    def test_rompre_contrat_met_a_jour_date_fin_eventuellement(self):
        """
        Vérifie que rompreContrat() met éventuellement à jour la date de fin.

        Comportement possible :
        - Lors de l'appel à rompreContrat(), dateFin peut être mise à la date
          du jour pour refléter une rupture anticipée.
        - Le test devra vérifier que dateFin est cohérente avec cette logique
          si elle est retenue.
        """
        pass


if __name__ == "__main__":
    unittest.main()
