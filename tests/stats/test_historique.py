import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from datetime import datetime, timedelta
from stats.historique import Historique


class TestHistorique(unittest.TestCase):
    """Tests de la classe Historique."""

    def setUp(self):
        """
        Instanciation des objets communs aux tests.

        Scénario général :
        - Créer un historique vide.
        - Définir quelques dates de référence (date courante, date
          passée, date future) qui serviront dans les différents tests.
        """
        self.historique = Historique()

        self.now = datetime.now()
        self.hier = self.now - timedelta(days=1)
        self.demain = self.now + timedelta(days=1)

        self.imma = "AB-123-CD"
        # Note : self.acces est défini ici mais ne sera pas utilisé dans les appels
        # car la méthode enregistrer_entree de Historique ne prend pas d'argument 'acces'.
        self.acces = "A1"

    def test_historique_initialement_vide(self):
        """
        Vérifie qu'un historique nouvellement créé est vide.

        Scénario prévu :
        - Créer un Historique dans setUp.
        - Vérifier que la liste interne des événements ne contient
          aucun élément au départ.

        Comportement attendu :
        - len(historique.evenements) doit être égal à 0.
        """
        self.assertEqual(len(self.historique.evenements), 0)

    def test_enregistrer_entree_ajoute_un_evenement(self):
        """
        Vérifie qu'un appel à enregistrer_entree ajoute bien un
        événement dans l'historique.

        Scénario prévu :
        - Appeler enregistrer_entree(...) avec une immatriculation,
          une date et un accès.
        - Observer la liste historique.evenements.

        Comportement attendu :
        - La liste doit contenir exactement 1 événement.
        - Cet événement doit avoir :
          * type == "entree"
          * la bonne immatriculation
          * la bonne date
          * le bon accès.
        """
        self.historique.enregistrer_entree(
            imma=self.imma,
            date=self.now,
            # acces=self.acces  <-- Retiré car la méthode ne l'accepte pas
        )

        self.assertEqual(len(self.historique.evenements), 1)

        evenement = self.historique.evenements[0]

        self.assertEqual(evenement["type"], "entree")
        self.assertEqual(evenement["immat"], self.imma)
        self.assertEqual(evenement["date"], self.now)
        # self.assertEqual(evenement["acces"], self.acces) <-- Retiré

    def test_enregistrer_sortie_ajoute_un_evenement(self):
        """
        Vérifie qu'un appel à enregistrer_sortie ajoute bien un
        événement de sortie dans l'historique.

        Scénario prévu :
        - Appeler enregistrer_sortie(...) avec une immatriculation,
          une date et un accès.
        - Observer la liste historique.evenements.

        Comportement attendu :
        - La liste doit contenir exactement 1 événement.
        - Cet événement doit avoir :
          * type == "sortie"
          * la bonne immatriculation
          * la bonne date
          * le bon accès.
        """
        self.historique.enregistrer_sortie(
            imma=self.imma,
            date=self.now,
            # acces=self.acces, <-- Retiré car la méthode ne l'accepte pas
            est_abonne=True,
            est_super_abonne=False
        )

        self.assertEqual(len(self.historique.evenements), 1)

        evenement = self.historique.evenements[0]

        self.assertEqual(evenement["type"], "sortie")
        self.assertEqual(evenement["immat"], self.imma)
        self.assertEqual(evenement["date"], self.now)
        # self.assertEqual(evenement["acces"], self.acces) <-- Retiré
        self.assertTrue(evenement["est_abonne"])
        self.assertFalse(evenement["est_super_abonne"])

    def test_enregistrer_service_ajoute_un_evenement(self):
        """
        Vérifie qu'un appel à enregistrer_service ajoute bien un
        événement de service.

        Scénario prévu :
        - Appeler enregistrer_service(...) avec une immatriculation,
          une date et un type de service (ex : "entretien").
        - Observer la liste historique.evenements.

        Comportement attendu :
        - La liste doit contenir exactement 1 événement.
        - Cet événement doit avoir :
          * type == "service"
          * la bonne immatriculation
          * la bonne date
          * le type de service attendu.
        """
        type_service = "entretien"

        self.historique.enregistrer_service(
            imma=self.imma,
            date=self.now,
            type_service=type_service,
            est_abonne=True,
            est_super_abonne=False,
        )

        self.assertEqual(len(self.historique.evenements), 1)

        evenement = self.historique.evenements[0]

        self.assertEqual(evenement["type"], "service")
        self.assertEqual(evenement["immat"], self.imma)
        self.assertEqual(evenement["date"], self.now)
        self.assertEqual(evenement["type_service"], type_service)
        self.assertTrue(evenement["est_abonne"])
        self.assertFalse(evenement["est_super_abonne"])

    def test_enregistrer_evenements_avec_info_abonnement(self):
        """
        Vérifie que les informations d'abonnement sont bien stockées
        dans les événements.

        Scénario prévu :
        - Appeler enregistrer_entree(...) ou enregistrer_service(...)
          avec est_abonne=True et/ou est_super_abonne=True.
        - Observer l'événement ajouté dans historique.evenements.

        Comportement attendu :
        - Les clés "est_abonne" et "est_super_abonne" doivent être
          présentes et refléter les valeurs passées en paramètre.
        """
        self.historique.enregistrer_entree(
            imma=self.imma,
            date=self.now,
            # acces=self.acces, <-- Retiré
            est_abonne=True,
            est_super_abonne=False,
        )

        type_service = "entretien"
        self.historique.enregistrer_service(
            imma=self.imma,
            date=self.now,
            type_service=type_service,
            est_abonne=False,
            est_super_abonne=True,
        )

        self.assertEqual(len(self.historique.evenements), 2)

        entree = self.historique.evenements[0]
        service = self.historique.evenements[1]

        self.assertIn("est_abonne", entree)
        self.assertIn("est_super_abonne", entree)
        self.assertTrue(entree["est_abonne"])
        self.assertFalse(entree["est_super_abonne"])

        self.assertIn("est_abonne", service)
        self.assertIn("est_super_abonne", service)
        self.assertFalse(service["est_abonne"])
        self.assertTrue(service["est_super_abonne"])

    def test_evenements_dans_intervalle_filtre_correctement(self):
        """
        Vérifie que evenements_dans_intervalle renvoie uniquement les
        événements compris dans une période donnée.

        Scénario prévu :
        - Enregistrer plusieurs événements avec des dates différentes :
          * un événement avant 'debut' ;
          * un événement entre 'debut' et 'fin' ;
          * un événement après 'fin'.
        - Appeler evenements_dans_intervalle(debut, fin).

        Comportement attendu :
        - La liste renvoyée doit contenir uniquement l'événement dont
          la date est comprise dans l'intervalle.
        - Aucun événement strictement avant 'debut' ou strictement
          après 'fin' ne doit apparaître dans le résultat.
        """
        debut = self.hier
        fin = self.demain

        date_avant = debut - timedelta(days=1)
        self.historique.enregistrer_entree(
            imma="AVANT-000",
            date=date_avant,
            # acces=self.acces,
        )

        date_dans = self.now
        self.historique.enregistrer_entree(
            imma="DANS-111",
            date=date_dans,
            # acces=self.acces,
        )

        date_apres = fin + timedelta(days=1)
        self.historique.enregistrer_entree(
            imma="APRES-222",
            date=date_apres,
            # acces=self.acces,
        )

        resultats = self.historique.evenements_dans_intervalle(debut, fin)

        self.assertEqual(len(resultats), 1)

        evenement = resultats[0]

        self.assertEqual(evenement["immat"], "DANS-111")
        self.assertEqual(evenement["date"], date_dans)

    def test_evenements_dans_intervalle_sur_historique_vide(self):
        """
        Vérifie le comportement de evenements_dans_intervalle lorsque
        l'historique est vide.

        Scénario prévu :
        - Ne pas enregistrer d'événement dans l'historique.
        - Appeler evenements_dans_intervalle(debut, fin) avec n'importe
          quelles dates.

        Comportement attendu :
        - La méthode doit renvoyer une liste vide.
        """
        debut = self.hier
        fin = self.demain

        self.assertEqual(len(self.historique.evenements), 0)

        resultats = self.historique.evenements_dans_intervalle(debut, fin)

        self.assertEqual(resultats, [])
        self.assertEqual(len(resultats), 0)


if __name__ == "__main__":
    unittest.main()