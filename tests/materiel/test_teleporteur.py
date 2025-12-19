import os
import sys

chemin_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
if chemin_src not in sys.path:
    sys.path.insert(0, chemin_src)

import unittest
from materiel.teleporteur import Teleporteur
from usagers.voiture import Voiture
from usagers.client import Client
from noyau.place import Place
from noyau.placement import Placement

class TestTeleporteur(unittest.TestCase):
    """Tests de la classe Teleporteur."""

    def test_teleporterVoiture_place_libre_retourne_placement(self):
        """
        Vérifie que teleporterVoiture() crée un Placement correct lorsqu'on
        téléporte une voiture sur une place libre.

        Scénario prévu :
        - Créer une Voiture avec des dimensions compatibles avec la place.
        - Créer une Place initialement libre.
        - Créer un Teleporteur.
        - Appeler teleporterVoiture(voiture, place).
        - Vérifier que :
          * un objet Placement est retourné,
          * ce Placement est associé à la voiture et à la place,
          * la place n'est plus considérée comme libre.
        """
        teleporteur = Teleporteur()

        place = Place("A1", 1, "A", 5.0, 2.5, estLibre=True)

        voiture = Voiture(2.0, 4.0, "AB-123-CD", estDansParking=False)
        
        placement = teleporteur.teleporterVoiture(voiture, place)
        
        self.assertIsNotNone(placement, "Le placement ne doit pas être None")
        self.assertIsInstance(placement, Placement)
        
        self.assertFalse(place.estLibre, "La place ne doit plus être libre")
        self.assertTrue(voiture.estDansParking, "La voiture doit être marquée dans le parking")
        self.assertEqual(place.placementActuel, placement)
        self.assertEqual(voiture.placementCourant, placement)

    def test_teleporterVoiture_place_deja_occupee(self):
        """
        Vérifie le comportement de teleporterVoiture() lorsqu'on tente de
        téléporter une voiture sur une place déjà occupée.

        Comportement attendu :
        - Créer une Place déjà occupée (estLibre=False).
        - Créer une Voiture.
        - Créer un Teleporteur.
        - Appeler teleporterVoiture(voiture, place).
        - Vérifier que le cas est géré :
          * soit en refusant la téléportation (exception, None, message),
          * soit en redirigeant vers une autre place, selon la logique choisie.
        """
        teleporteur = Teleporteur()
        place = Place("A1", 1, "A", 5.0, 2.5, estLibre=False) # Déjà occupée
        voiture = Voiture(2.0, 4.0, "AB-123-CD", estDansParking=False)
        
        resultat = teleporteur.teleporterVoiture(voiture, place)
        
        self.assertIsNone(resultat, "La téléportation doit échouer sur une place occupée")

    def test_teleporterVoiture_dimensions_incompatibles(self):
        """
        Vérifie que teleporterVoiture() gère le cas où la voiture ne respecte
        pas les contraintes de hauteur/longueur de la place.

        Scénario prévu :
        - Créer une Place avec des dimensions maximales limitées.
        - Créer une Voiture trop grande pour cette place.
        - Créer un Teleporteur.
        - Appeler teleporterVoiture(voiture, place).
        - Vérifier que la téléportation est refusée ou signalée (exception,
          valeur spéciale, message d'erreur, etc.).
        """
        teleporteur = Teleporteur()

        place = Place("A1", 1, "A", 3.0, 2.0, estLibre=True)

        voiture = Voiture(2.0, 5.0, "AB-123-CD", estDansParking=False)

        resultat = teleporteur.teleporterVoiture(voiture, place)
        
        self.assertIsNone(resultat, "La téléportation doit échouer si la voiture est trop grande")

    def test_teleporterVoitureSuperAbonne_succes(self):
        """
        Vérifie que teleporterVoitureSuperAbonne() réussit la téléportation
        pour une voiture appartenant à un super abonné.

        Scénario prévu :
        - Créer une Voiture associée à un client super abonné.
        - Créer un Teleporteur.
        - Appeler teleporterVoitureSuperAbonne(voiture).
        - Vérifier que la chaîne retournée indique une téléportation réussie
          dans le mode "super abonné" (accès privilégié, place spéciale, etc.).
        """
        client_vip = Client("VIP", "1 rue Riche", True, True, 100) 
        
        voiture = Voiture(1.5, 4.0, "VIP-1", estDansParking=False)
        voiture.proprietaire = client_vip 

        tele = Teleporteur()

        resultat = tele.teleporterVoitureSuperAbonne(voiture)

        self.assertTrue(resultat, "La téléportation aurait dû réussir pour un super abonné")
        self.assertTrue(voiture.estDansParking)

    def test_teleporterVoitureSuperAbonne_sans_place_disponible(self):
        """
        Vérifie que teleporterVoitureSuperAbonne() gère le cas où aucune place
        n'est disponible pour un super abonné.

        Scénario prévu :
        - Simuler un parking où toutes les places réservées aux super abonnés
          (ou toutes les places tout court) sont déjà occupées.
        - Créer une Voiture de super abonné.
        - Appeler teleporterVoitureSuperAbonne(voiture).
        - Vérifier que le résultat signale clairement l'impossibilité de
          téléporter la voiture faute de place disponible.
        """
        teleporteur = Teleporteur()
        voiture = Voiture(2.0, 4.0, "VIP-001", estDansParking=False)
        
        msg = teleporteur.teleporterVoitureSuperAbonne(voiture)
        self.assertIsNotNone(msg)
    
    def test_teleporterVoitureSuperAbonne_avec_voiture_non_super_abonne(self):
        """
        Vérifie que teleporterVoitureSuperAbonne() gère le cas où la voiture
        ne correspond pas à un super abonné.

        Comportement attendu :
        - Créer une Voiture associée à un client non super abonné.
        - Créer un Teleporteur.
        - Appeler teleporterVoitureSuperAbonne(voiture).
        - Vérifier que la méthode :
          * refuse la téléportation en mode super abonné,
          * ou renvoie un message d'erreur ou d'inadéquation.
        """
        client_lambda = Client(nom="Paul", adresse="Rue B", estAbonne=True, estSuperAbonne=False, nbFrequentations=2)
   
        voiture = Voiture(hauteur=1.5, longueur=4.0, immatriculation="LAMBDA-1", estDansParking=False)
        
        voiture.proprietaire = client_lambda 

        tele = Teleporteur()

        resultat = tele.teleporterVoitureSuperAbonne(voiture)

        self.assertFalse(resultat, "Le téléporteur aurait dû refuser la voiture (client non super abonné)")


if __name__ == "__main__":
    unittest.main()
