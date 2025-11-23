import os
import sys

# On ajoute src/ dans le PYTHONPATH pour pouvoir importer les modules métier
RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from datetime import date
from entretien import Entretien


class TestEntretien(unittest.TestCase):
    """Tests de la classe Entretien."""

    def test_initialisation_entretien_avec_attributs_service(self):
        """
        Vérifie qu'un Entretien est correctement initialisé avec les
        attributs hérités de Service (dateDemande, dateService, rapport).

        Scénario prévu :
        - Choisir une date de demande et une date de service.
        - Créer un Entretien avec ces dates et un rapport initial (éventuellement vide).
        - Vérifier que les attributs internes de l'objet (dateDemande,
          dateService, rapport) correspondent aux valeurs fournies.
        """
        pass

    def test_effectuer_entretien_met_a_jour_rapport(self):
        """
        Vérifie que effectuerEntretien() met à jour le rapport d'entretien.

        Scénario prévu :
        - Créer un Entretien avec un rapport initial (par exemple vide).
        - Appeler effectuerEntretien().
        - Vérifier qu'un rapport d'entretien plus détaillé est enregistré
          (contenu non vide, éventuellement contenant certaines informations
          clés comme la nature des opérations réalisées).
        """
        pass

    def test_effectuer_entretien_met_a_jour_date_service_si_non_fixee(self):
        """
        Vérifie que effectuerEntretien() met à jour la date de service si
        celle-ci n'était pas encore fixée.

        Scénario possible :
        - Créer un Entretien avec dateService à None ou à une valeur par défaut.
        - Appeler effectuerEntretien().
        - Vérifier que dateService est mise à la date du jour ou à une date
          cohérente avec l'exécution de l'entretien.
        """
        pass

    def test_effectuer_entretien_ne_fait_rien_si_deja_effectue(self):
        """
        Vérifie que effectuerEntretien() gère le cas où l'entretien a déjà
        été réalisé.

        Comportement possibles :
        - Soit la méthode ne modifie plus le rapport ni les dates si l'entretien
          est déjà marqué comme effectué
        - soit elle lève une exception ou retourne une information indiquant
          que l'entretien a déjà été réalisé.
        """
        pass

    def test_effectuer_entretien_sur_date_anterieure_a_date_demande(self):
        """
        Vérifie que effectuerEntretien() ne permet pas de fixer une date
        de service antérieure à la date de demande.

        Scénario possibles :
        - Créer un Entretien avec une dateDemande donnée.
        - Simuler un appel à effectuerEntretien() qui tenterait de placer
          la dateService avant dateDemande.
        - Vérifier que ce cas est refusé (exception, correction automatique,
          etc.), conformément aux règles qui seront définies.
        """
        pass


if __name__ == "__main__":
    unittest.main()
