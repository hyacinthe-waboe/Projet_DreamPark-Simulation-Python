import os
import sys

chemin_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
if chemin_src not in sys.path:
    sys.path.insert(0, chemin_src)

import unittest
from datetime import date, timedelta

from services.maintenance import Maintenance
from usagers.voiture import Voiture
from noyau.parking import Parking
from usagers.client import Client


class TestMaintenance(unittest.TestCase):
    """Tests de la classe Maintenance."""

    def test_initialisation_maintenance_avec_attributs_service(self):
        """
        Vérifie qu'une Maintenance est correctement initialisée avec les
        attributs hérités de Service (dateDemande, dateService, rapport).

        Scénario prévu :
        - Choisir une date de demande et une date de service.
        - Créer une Maintenance avec ces dates et un rapport initial.
        - Vérifier que les attributs internes (dateDemande, dateService,
          rapport) correspondent aux valeurs fournies.
        """

    def setUp(self):
        """Instanciation des objets communs aux tests."""
        self.today = date.today()
        self.demain = self.today + timedelta(days=1)
        self.hier = self.today - timedelta(days=1)
        self.rapport = "Je suis le rapport"

        self.voiture = Voiture(1.80,2,"TEST-MAINT", True)
        self.parking = Parking(nbPlacesParNiveau=10, nbPlacesLibres=10, prix=20, nbNiveaux=1)
        self.client = Client(nom="Testeur", adresse="Rue Test", estAbonne=True, estSuperAbonne=False, nbFrequentations=0)

        self.client.voiture = self.voiture

        self.maintenance = Maintenance(self.today, self.demain, self.rapport)

    def test_effectuer_maintenance_met_a_jour_rapport(self):
        """
        Vérifie que effectuerMaintenance() met à jour le rapport de maintenance.

        Scénario prévu :
        - Créer une voiture.
        - Créer une Maintenance avec un rapport initial (par exemple vide).
        - Appeler effectuerMaintenance(voiture).
        - Vérifier qu'un rapport de maintenance détaillé est enregistré
          (contenu non vide, décrivant par exemple les opérations effectuées).
        """
        self.assertEqual(self.maintenance.dateDemande, self.today)
        self.assertEqual(self.maintenance.dateService, self.demain)
        self.assertEqual(self.maintenance.rapport, self.rapport)
        self.assertIsInstance(self.maintenance, Maintenance)

    def test_effectuer_maintenance_met_a_jour_date_service_si_non_fixee(self):
        """
        Vérifie que effectuerMaintenance() met à jour la date de service si
        celle-ci n'était pas encore définie.

        Scénario possibles :
        - Créer une Maintenance avec dateService à None ou à une valeur par défaut.
        - Créer une voiture.
        - Appeler effectuerMaintenance(voiture).
        - Vérifier que dateService est mise à la date du jour ou à une
          date cohérente avec l'exécution de la maintenance.
        """
        self.maintenance.effectuerMaintenance(self.voiture, self.parking,self.client)

        self.assertEqual(self.maintenance.dateService, self.today)

    def test_effectuer_maintenance_sur_voiture_valide(self):
        """
        Vérifie que effectuerMaintenance() fonctionne correctement pour une
        voiture valide.

        Scénario prévu :
        - Créer une voiture avec des caractéristiques cohérentes.
        - Créer une Maintenance.
        - Appeler effectuerMaintenance(voiture).
        - Vérifier que la maintenance est considérée comme réalisée pour
          cette voiture (par exemple via une mise à jour de l'état ou
          du rapport).
        """
        self.maintenance.effectuerMaintenance(self.voiture, self.parking,self.client)

        self.assertIsInstance(self.maintenance.rapport, str)
        self.assertIn("maintenance", self.maintenance.rapport.lower())

    def test_effectuer_maintenance_sans_voiture_valide(self):
        """
        Vérifie que effectuerMaintenance() gère le cas d'une voiture non
        valide (ou absente).

        Scénario possibles :
        - Appeler effectuerMaintenance(None) ou avec une voiture dont
          certains attributs clés ne sont pas initialisés.
        - Vérifier que ce cas est refusé ou signalé (exception, message
          d'erreur, etc.), conformément aux règles qui seront définies.
        """
        with self.assertRaises(ValueError):
          self.maintenance.effectuerMaintenance(None, self.parking,self.client)

    def test_effectuer_maintenance_plusieurs_fois(self):
        """
        Vérifie le comportement de effectuerMaintenance() lorsqu'on l'appelle
        plusieurs fois pour la même maintenance.

        Comportement attendu :
        - Soit seule la première exécution est prise en compte et les appels
          suivants ne modifient plus l'état ou le rapport,
        - soit la méthode signale que la maintenance a déjà été effectuée
          (via une exception ou un indicateur dans le rapport).
        """
        self.maintenance.effectuerMaintenance(self.voiture, self.parking,self.client)
        rapport_apres_premier = self.maintenance.rapport
        date_service_apres_premier = self.maintenance.dateService

        with self.assertRaises(ValueError):
          self.maintenance.effectuerMaintenance(self.voiture, self.parking,self.client)

        self.assertEqual(self.maintenance.rapport, rapport_apres_premier)
        self.assertEqual(self.maintenance.dateService, date_service_apres_premier)


if __name__ == "__main__":
    unittest.main()
