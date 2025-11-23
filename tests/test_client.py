import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from client import Client
from datetime import date
from abonnement import Abonnement
from acces import Acces 


class TestClient(unittest.TestCase):
    """Tests de la classe Client."""

    def test_initialisation_attributs_corrects(self):
        """
        Vérifie qu'un client est correctement initialisé avec les valeurs fournies.

        Scénario prévu :
        - Créer un client avec un nom, une adresse, les indicateurs estAbonne et
          estSuperAbonne, ainsi qu'un nombre de fréquentations.
        - Vérifier que les attributs internes de l'objet correspondent aux valeurs
          passées au constructeur.
        """
        pass

    def test_s_abonner_client_non_abonne(self):
        """
        Vérifie qu'un client non abonné devient abonné après sAbonner()
        avec un abonnement valide.

        Scénario prévu :
        - Créer un client non abonné.
        - Créer un abonnement.
        - Appeler sAbonner(abonnementVoulu).
        - Vérifier que le client est désormais marqué comme abonné et que
          l'abonnement est associé au client.
        """
        pass

    def test_s_abonner_client_deja_abonne(self):
        """
        Vérifie que sAbonner() gère correctement le cas d'un client déjà abonné.

        Comportement attendu :
        - Soit la méthode ne modifie pas l'abonnement existant
        - soit elle lève une exception ou retourne une information indiquant que
          le client était déjà abonné.
        """
        pass

    def test_se_desabonner_client_abonne(self):
        """
        Vérifie que seDesabonner() met fin à l'abonnement d'un client abonné.

        Scénario prévu :
        - Créer un client avec estAbonne=True et un abonnement associé.
        - Appeler seDesabonner().
        - Vérifier que le client n'est plus abonné et que l'abonnement est
          correctement supprimé/désactivé.
        """
        pass

    def test_se_desabonner_client_non_abonne(self):
        """
        Vérifie que seDesabonner() gère le cas d'un client non abonné.

        Comportement attendu :
        - Appeler seDesabonner() sur un client non abonné ne doit pas provoquer
          d'erreur et ne doit pas modifier l'état du client, juste informé qu'il
          le client n'est pas abonné.
        """
        pass

    def test_nouvelle_voiture_ajoute_voiture_au_client(self):
        """
        Vérifie que nouvelleVoiture() associe une nouvelle voiture au client.

        Scénario prévu :
        - Créer un client sans voiture enregistrée.
        - Appeler nouvelleVoiture(imma, hautV, longV).
        - Vérifier qu'une voiture correspondant aux paramètres est désormais
          associée au client.
        """
        pass

    def test_demander_maintenance_cree_demande_pour_voiture(self):
        """
        Vérifie que demanderMaintenance() enregistre une demande de maintenance.

        Scénario prévu :
        - Créer un client avec une voiture.
        - Appeler demanderMaintenance().
        - Vérifier qu'une demande de maintenance est créée/programmée pour
          la voiture du client.
        """
        pass

    def test_demander_livraison_enregistre_date_heure_adresse(self):
        """
        Vérifie que demanderLivraison() enregistre la livraison à une date,
        une heure et une adresse données.

        Scénario prévu :
        - Créer un client avec une voiture.
        - Appeler demanderLivraison(dateLiv, heure, adresseLiv).
        - Vérifier que les informations de livraison (date, heure, adresse)
          sont bien stockées dans la structure de données associée au client
          ou au service de livraison.
        """
        pass

    def test_demander_entretien_cree_demande_pour_voiture(self):
        """
        Vérifie que demanderEntretien() enregistre une demande d'entretien.

        Scénario prévu :
        - Créer un client avec une voiture.
        - Appeler demanderEntretien().
        - Vérifier qu'une demande d'entretien est créée/programmée pour la
          voiture du client.
        """
        pass

    def test_entrer_parking_incremente_nb_frequentations(self):
        """
        Vérifie que entrerParking() incrémente le nombre de fréquentations
        du client lorsqu'il entre dans le parking.

        Scénario prévu :
        - Créer un client avec un nbFrequentations initial.
        - Créer un accès relié au parking.
        - Appeler entrerParking(acces).
        - Vérifier que nbFrequentations a été incrémenté de 1.
        """
        pass

    def test_entrer_parking_retour_succes_ou_message_erreur(self):
        """
        Vérifie que entrerParking() retourne un message cohérent.

        Scénario prévu :
        - Créer un client (abonné ou non).
        - Créer un accès relié au système (parking, téléporteur, etc.).
        - Appeler entrerParking(acces).
        - Vérifier que la chaîne retournée indique soit une entrée réussie
          (par exemple identifiant de place ou confirmation), soit une raison
          d'échec (parking complet, refus, etc.).
        """
        pass


if __name__ == "__main__":
    unittest.main()
