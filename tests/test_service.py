import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from datetime import date, timedelta
from service import Service


class TestService(unittest.TestCase):
    """Tests de la classe Service."""

    def test_initialisation_attributs_corrects(self):
        """
        Vérifie qu'un service est correctement initialisé avec les valeurs fournies.

        Scénario prévu :
        - Choisir une date de demande et une date de service cohérentes
          (dateService >= dateDemande).
        - Créer un Service avec ces deux dates et un rapport descriptif.
        - Vérifier que les attributs internes (dateDemande, dateService, rapport)
          correspondent exactement aux valeurs passées au constructeur.
        """
        pass

    def test_initialisation_date_service_avant_date_demande_declenche_erreur(self):
        """
        Vérifie qu'un service ne peut pas être initialisé avec une date de service
        antérieure à la date de demande.

        Comportement attendu :
        - Si dateService < dateDemande, le constructeur doit refuser la création
          du service (par exemple en levant une exception comme ValueError),
          plutôt que d'accepter un service incohérent.
        """
        pass

    def test_initialisation_rapport_peut_etre_vide_ou_non(self):
        """
        Vérifie le comportement du constructeur lorsqu'on fournit un rapport vide.

        Scénario possibles :
        - Créer un Service avec un rapport vide ('').
        - Décider si :
          * le rapport vide est accepté (et simplement stocké tel quel), ou
          * le constructeur doit imposer un rapport minimal (non vide) et
            refuser un rapport vide.
        - Le test devra vérifier le comportement retenu.
        """
        pass

    def test_service_planifie_date_service_dans_le_futur(self):
        """
        Vérifie qu'un service planifié peut avoir une date de service dans le futur.

        Scénario prévu :
        - Utiliser la date du jour comme dateDemande.
        - Choisir une dateService strictement postérieure à dateDemande.
        - Créer un Service avec ces dates.
        - Vérifier que la dateService reflète bien une planification dans le futur
          et qu'elle est correctement enregistrée.
        """
        pass

    def test_service_immediat_date_service_egale_date_demande(self):
        """
        Vérifie qu'un service peut être réalisé le jour même de la demande.

        Scénario prévu :
        - Fixer dateDemande = dateService.
        - Créer un Service avec ces dates.
        - Vérifier que le service est accepté et que les deux dates sont bien
          enregistrées comme identiques.
        """
        pass


if __name__ == "__main__":
    unittest.main()
