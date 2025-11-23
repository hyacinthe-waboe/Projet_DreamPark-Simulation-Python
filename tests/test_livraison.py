import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from datetime import date
from livraison import Livraison


class TestLivraison(unittest.TestCase):
    """Tests de la classe Livraison."""

    def test_initialisation_livraison_avec_attributs_service(self):
        """
        Vérifie qu'une Livraison est correctement initialisée avec les
        attributs hérités de Service (dateDemande, dateService, rapport).

        Scénario prévu :
        - Choisir une date de demande et une date de service.
        - Créer une Livraison avec ces dates et un rapport initial.
        - Vérifier que les attributs internes (dateDemande, dateService,
          rapport) correspondent aux valeurs fournies.
        """
        pass

    def test_effectuer_livraison_met_a_jour_rapport(self):
        """
        Vérifie que effectuerLivraison() met à jour le rapport de livraison.

        Scénario prévu :
        - Créer une Livraison avec un rapport initial (par exemple vide).
        - Appeler effectuerLivraison().
        - Vérifier qu'un rapport de livraison détaillé est enregistré
          (contenu non vide, décrivant par exemple la réussite de la livraison).
        """
        pass

    def test_effectuer_livraison_met_a_jour_date_service_si_non_fixee(self):
        """
        Vérifie que effectuerLivraison() met à jour la date de service si
        celle-ci n'était pas encore définie.

        Scénario possible :
        - Créer une Livraison avec dateService à None ou à une valeur par défaut.
        - Appeler effectuerLivraison().
        - Vérifier que dateService est mise à la date du jour ou à une
          date cohérente avec l'exécution de la livraison.
        """
        pass

    def test_effectuer_livraison_plusieurs_fois(self):
        """
        Vérifie le comportement de effectuerLivraison() lorsqu'on l'appelle
        plusieurs fois pour la même livraison.

        Comportement attendu :
        - Soit seule la première exécution est prise en compte et les appels
          suivants ne modifient plus l'état ou le rapport
        - soit la méthode signale que la livraison a déjà été effectuée
          (via une exception ou un message).
        """
        pass

    def test_effectuer_livraison_sans_adresse_valide(self):
        """
        Vérifie que effectuerLivraison() gère le cas d'une livraison sans
        adresse valide.

        Scénario possible :
        - Créer une Livraison sans adresse ou avec une adresse invalide.
        - Appeler effectuerLivraison().
        - Vérifier que ce cas est refusé ou signalé (exception, message
          d'erreur, etc.), conformément aux règles qui seront définies.
        """
        pass


if __name__ == "__main__":
    unittest.main()
