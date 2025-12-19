import os
import sys

# Calcul dynamique du chemin pour trouver le dossier 'src'
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from datetime import datetime, timedelta

from stats.historique import Historique
from stats.statistiques import StatistiquesParking


class TestStatistiquesParking(unittest.TestCase):
    """Tests de la classe StatistiquesParking."""

    def setUp(self):
        """
        Instanciation des objets communs aux tests.

        Scénario général :
        - Créer un Historique vide.
        - Créer une instance de StatistiquesParking basée sur cet
          historique.
        - Définir quelques dates de référence (date courante, date
          passée, date future) qui serviront dans les différents tests.
        """
        self.historique = Historique()
        self.stats = StatistiquesParking(self.historique)

        self.now = datetime.now()
        self.hier = self.now - timedelta(days=1)
        self.demain = self.now + timedelta(days=1)

    def test_nombre_passages_periode_simple(self):
        """
        Vérifie le calcul du nombre de passages sur une période simple.

        Scénario prévu :
        - Enregistrer un seul événement de type "entree" dans
          l'intervalle [debut, fin].
        - Appeler nombre_passages(debut, fin).

        Comportement attendu :
        - La méthode doit renvoyer 1.
        """
        debut = self.now
        fin = self.now + timedelta(days=1)

        self.historique.enregistrer_entree(
          imma="AB-123-CD",
          date=self.now,
          # acces="A1" <--- Retiré car non supporté par ta classe Historique actuelle
        )

        resultat = self.stats.nombre_passages(debut, fin)

        self.assertEqual(resultat, 1)

    def test_nombre_passages_plusieurs_entrees_et_sorties(self):
        """
        Vérifie le calcul du nombre de passages avec plusieurs événements.

        Scénario prévu :
        - Enregistrer plusieurs événements "entree" et "sortie".
        - Appeler nombre_passages(debut, fin).

        Comportement attendu :
        - La méthode doit renvoyer le nombre exact d'événements de
          type "entree" ou "sortie" compris dans la période.
        """
        debut = self.now
        fin = self.now + timedelta(days=1)

        self.historique.enregistrer_entree(
          imma="AB-124-CD",
          date=self.now,
        )

        self.historique.enregistrer_sortie(
          imma="AB-125-CD",
          date=self.now,
        )

        self.historique.enregistrer_entree(
          imma="AB-126-CD",
          date=self.now,
        )

        resultat = self.stats.nombre_passages(debut, fin)

        self.assertEqual(resultat, 3)

    def test_nombre_passages_aucun_evenement_dans_periode(self):
        """
        Vérifie le comportement de nombre_passages lorsqu'il n'y a
        aucun passage dans la période étudiée.

        Scénario prévu :
        - Enregistrer des événements en dehors de [debut, fin].
        - Appeler nombre_passages(debut, fin).

        Comportement attendu :
        - La méthode doit renvoyer 0.
        """
        debut = self.now
        fin = self.now + timedelta(days=1)

        date_avant = debut - timedelta(days=1)
        self.historique.enregistrer_entree(
          imma="AVANT-000",
          date=date_avant,
        )

        date_apres = fin + timedelta(days=1)
        self.historique.enregistrer_sortie(
          imma="APRES-999",
          date=date_apres,
        )

        resultat = self.stats.nombre_passages(debut, fin)

        self.assertEqual(resultat, 0)

    def test_nombre_clients_distincts_immatriculations_identiques(self):
        """
        Vérifie le calcul du nombre de clients distincts lorsque
        plusieurs passages concernent la même voiture.

        Scénario prévu :
        - Enregistrer plusieurs entrées/sorties avec la même
          immatriculation.
        - Enregistrer au moins un passage avec une autre immatriculation.
        - Appeler nombre_clients_distincts(debut, fin).

        Comportement attendu :
        - La méthode doit renvoyer le nombre d'immatriculations
          distinctes, indépendamment du nombre total d'événements.
        """
        debut = self.now
        fin = self.now + timedelta(days=1)

        self.historique.enregistrer_entree(
          imma="AB-123-CD",
          date=self.now,
        )

        self.historique.enregistrer_sortie(
          imma="AB-123-CD",
          date=self.now,
        )

        self.historique.enregistrer_entree(
          imma="AB-123-CD",
          date=self.now,
        )

        self.historique.enregistrer_entree(
          imma="AB-124-CD",
          date=self.now,
        )

        resultat = self.stats.nombre_clients_distincts(debut, fin)

        self.assertEqual(resultat, 2)
        

    def test_nombre_clients_distincts_aucun_evenement(self):
        """
        Vérifie le comportement de nombre_clients_distincts sur une
        période sans événement.

        Scénario prévu :
        - Ne pas enregistrer d'événement dans l'historique, ou bien
          uniquement en dehors de l'intervalle.
        - Appeler nombre_clients_distincts(debut, fin).

        Comportement attendu :
        - La méthode doit renvoyer 0.
        """
        debut = self.now
        fin = self.now + timedelta(days=1)

        date_avant = debut - timedelta(days=1)
        self.historique.enregistrer_entree(
          imma="AVANT-000",
          date=date_avant,
        )

        date_apres = fin + timedelta(days=1)
        self.historique.enregistrer_sortie(
          imma="APRES-999",
          date=date_apres,
        )

        resultat = self.stats.nombre_clients_distincts(debut, fin)

        self.assertEqual(resultat, 0)

    def test_nombre_services_total_periode_simple(self):
        """
        Vérifie le calcul du nombre total de services sur une période.

        Scénario prévu :
        - Enregistrer plusieurs événements de type "service" dans
          l'intervalle [debut, fin].
        - Appeler nombre_services_total(debut, fin).

        Comportement attendu :
        - La méthode doit renvoyer le nombre total de services dans
          la période.
        """
        debut = self.now
        fin = self.now + timedelta(days=1)

        self.historique.enregistrer_service(
          imma="AB-124-CD",
          date=self.now,
          type_service="entretien",
        )

        self.historique.enregistrer_service(
          imma="AB-125-CD",
          date=self.now,
          type_service="livraison",
        )

        self.historique.enregistrer_service(
          imma="AB-126-CD",
          date=self.now,
          type_service="maintenance",
        )

        resultat = self.stats.nombre_services_total(debut, fin)

        self.assertEqual(resultat, 3)

    def test_nombre_services_total_ignore_evenements_non_service(self):
        """
        Vérifie que nombre_services_total ignore bien les entrées
        et sorties.

        Scénario prévu :
        - Enregistrer des "entree" et "sortie" dans [debut, fin].
        - Enregistrer quelques "service" dans la même période.
        - Appeler nombre_services_total(debut, fin).

        Comportement attendu :
        - Seuls les événements de type "service" doivent être comptés.
        """
        debut = self.now
        fin = self.now + timedelta(days=1)

        self.historique.enregistrer_entree(
          imma="ENTREE-1",
          date=self.now,
        )
        self.historique.enregistrer_sortie(
          imma="SORTIE-1",
          date=self.now + timedelta(hours=1),
        )

        self.historique.enregistrer_service(
          imma="SERV-1",
          date=self.now + timedelta(hours=2),
          type_service="entretien",
        )
        self.historique.enregistrer_service(
          imma="SERV-2",
          date=self.now + timedelta(hours=3),
          type_service="maintenance",
        )
        self.historique.enregistrer_service(
          imma="SERV-3",
          date=self.now + timedelta(hours=4),
          type_service="livraison",
        )

        resultat = self.stats.nombre_services_total(debut, fin)

        self.assertEqual(resultat, 3)

    def test_repartition_services_par_type_melange(self):
        """
        Vérifie la répartition des services par type.

        Scénario prévu :
        - Enregistrer plusieurs services de différents types, par
          exemple :
            * 2 "entretien" ;
            * 1 "maintenance" ;
            * 3 "livraison".
        - Appeler repartition_services_par_type(debut, fin).
        """
        debut = self.now
        fin = self.now + timedelta(days=1)

        # 2 services "entretien"
        self.historique.enregistrer_service(
          imma="ENT-1",
          date=self.now + timedelta(hours=1),
          type_service="entretien",
        )
        self.historique.enregistrer_service(
          imma="ENT-2",
          date=self.now + timedelta(hours=2),
          type_service="entretien",
        )

        # 1 service "maintenance"
        self.historique.enregistrer_service(
          imma="MAINT-1",
          date=self.now + timedelta(hours=3),
          type_service="maintenance",
        )

        # 3 services "livraison"
        self.historique.enregistrer_service(
          imma="LIV-1",
          date=self.now + timedelta(hours=4),
          type_service="livraison",
        )
        self.historique.enregistrer_service(
          imma="LIV-2",
          date=self.now + timedelta(hours=5),
          type_service="livraison",
        )
        self.historique.enregistrer_service(
          imma="LIV-3",
          date=self.now + timedelta(hours=6),
          type_service="livraison",
        )

        resultat = self.stats.repartition_services_par_type(debut, fin)

        attendu = {
          "entretien": 2,
          "maintenance": 1,
          "livraison": 3,
        }

        self.assertEqual(resultat, attendu)

    def test_repartition_services_par_type_aucun_service(self):
        """
        Vérifie le comportement de repartition_services_par_type
        lorsqu'il n'y a aucun service dans la période.

        Scénario prévu :
        - Ne pas enregistrer de service dans [debut, fin].
        - Appeler repartition_services_par_type(debut, fin).

        Comportement attendu :
        - La méthode doit renvoyer un dictionnaire vide ou sans
          entrée significative.
        """
        debut = self.now
        fin = self.now + timedelta(days=1)

        date_avant = debut - timedelta(days=1)
        self.historique.enregistrer_service(
          imma="AVANT-000",
          date=date_avant,
          type_service="entretien",
        )

        date_apres = fin + timedelta(days=1)
        self.historique.enregistrer_service(
          imma="APRES-999",
          date=date_apres,
          type_service="maintenance",
        )

        resultat = self.stats.repartition_services_par_type(debut, fin)

        self.assertEqual(resultat, {})
        self.assertEqual(len(resultat), 0)


if __name__ == "__main__":
    unittest.main()