import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from borne_ticket import BorneTicket
from client import Client
from parking import Parking


class TestBorneTicket(unittest.TestCase):
    """Tests de la classe BorneTicket."""

    def test_deliver_ticket_client_non_abonne(self):
        """
        Vérifie que deliverTicket() délivre un ticket pour un client non abonné.

        Scénario prévu :
        - Créer un client non abonné.
        - Créer une borne de ticket.
        - Appeler deliverTicket(client).
        - Vérifier que la chaîne retournée correspond à un identifiant de ticket
          non vide (par exemple un code ou un numéro de ticket).
        - Vérifier que le ticket pourra ensuite être utilisé pour entrer
          dans le parking.
        """
        c = Client("NonAbo", "1 rue", False, False, 0)
        borne = BorneTicket()
        
        ticket = borne.deliverTicket(c)
        
        self.assertIsInstance(ticket, str)
        self.assertTrue(len(ticket) > 0)
        self.assertTrue(ticket.startswith("TICKET-"))

    def test_deliver_ticket_client_deja_abonne(self):
        """
        Vérifie le comportement de deliverTicket() pour un client déjà abonné.

        Scénario possible  :
        - Créer un client déjà abonné.
        - Créer une borne de ticket.
        - Appeler deliverTicket(client).
        - Vérifier que :
          * soit aucun nouveau ticket n'est généré et un message spécifique est
            retourné (par exemple 'Client déjà abonné')
          * soit un ticket particulier est délivré, mais le cas doit être
            explicitement géré.
        """
        c = Client("Abo", "1 rue", True, False, 0)
        borne = BorneTicket()
        
        ticket = borne.deliverTicket(c)
        
        self.assertIsNotNone(ticket)

    def test_proposer_services_liste_services_disponibles(self):
        """
        Vérifie que proposerServices() retourne la liste des services proposés.

        Scénario prévu :
        - Créer une borne de ticket.
        - Appeler proposerServices().
        - Vérifier que la chaîne retournée mentionne les principaux services
          disponibles (maintenance, entretien, livraison, etc. selon les
          services définis dans le système).
        """
        borne = BorneTicket()
        
        msg = borne.proposerServices()
        
        self.assertIn("Maintenance", msg)
        self.assertIn("Entretien", msg)
        self.assertIn("Livraison", msg)

    def test_proposer_abonnements_client_non_abonne(self):
        """
        Vérifie que proposerAbonnements() propose des offres à un client non abonné.

        Scénario prévu :
        - Créer un client non abonné.
        - Créer un parking (contenant des abonnements disponibles).
        - Créer une borne de ticket.
        - Appeler proposerAbonnements(client, parking).
        - Vérifier que la chaîne retournée décrit au moins une offre d'abonnement
          pertinente pour ce client.
        """
        c = Client("NonAbo", "1 rue", False, False, 0)
        p = Parking(10, 10, 10, 1)
        borne = BorneTicket()
        
        msg = borne.proposerAbonnements(c, p)
        
        self.assertIn("Abonnements", msg)
        self.assertIn("Standard", msg)

    def test_proposer_abonnements_client_deja_abonne(self):
        """
        Vérifie que proposerAbonnements() traite correctement un client déjà abonné.

        Scénario possible (à préciser en implémentation) :
        - Créer un client déjà abonné.
        - Créer un parking.
        - Créer une borne de ticket.
        - Appeler proposerAbonnements(client, parking).
        - Vérifier que le message retourné signale que le client possède déjà
          un abonnement, ou qu'aucune nouvelle offre n'est proposée.
        """
        c = Client("Abo", "1 rue", True, False, 0)
        p = Parking(10, 10, 10, 1)
        borne = BorneTicket()
        
        msg = borne.proposerAbonnements(c, p)
        
        self.assertIn("déjà abonné", msg)

    def test_recuperer_infos_carte_enregistre_donnees(self):
        """
        Vérifie que recupererInfosCarte() récupère et enregistre les infos de carte.

        Scénario prévu :
        - Créer un client.
        - Créer une borne de ticket.
        - Appeler recupererInfosCarte(client).
        - Vérifier que le résultat indique que les informations de carte
          ont été correctement collectées (format cohérent).
        - Vérifier que ces informations peuvent être utilisées ensuite pour
          un paiement.
        """
        c = Client("Test", "1 rue", False, False, 0)
        borne = BorneTicket()
        
        res = borne.recupererInfosCarte(c)
        
        self.assertIn("OK", res)

    def test_proposer_type_paiement_liste_modes_disponibles(self):
        """
        Vérifie que proposerTypePaiement() retourne la liste des modes de paiement.

        Scénario prévu :
        - Créer une borne de ticket.
        - Appeler proposerTypePaiement().
        - Vérifier que la chaîne retournée mentionne les principaux modes
          de paiement supportés (carte bancaire, espèces, etc.), conformément
          aux choix retenus dans le projet.
        """
        borne = BorneTicket()
        
        res = borne.proposerTypePaiement()
        
        self.assertIn("CB", res)
        self.assertIn("Espèces", res)


if __name__ == "__main__":
    unittest.main()
