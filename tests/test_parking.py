import os
import sys

RACINE = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import unittest
from parking import Parking
from abonnement import Abonnement
from voiture import Voiture
from place import Place


class TestParking(unittest.TestCase):
    """Tests de la classe Parking."""

    def test_initialisation_attributs_corrects(self):
        """
        Vérifie qu'un parking est correctement initialisé avec les valeurs fournies.

        Scénario prévu :
        - Créer un Parking avec un nombre de places par niveau, un nombre de
          places libres, un prix et un nombre de niveaux.
        - Vérifier que les attributs internes (_nbPlacesParNiveau,
          _nbPlacesLibres, _prix, nbNiveaux) correspondent aux valeurs
          passées au constructeur.
        """
        pass

    def test_rechercher_place_voiture_compatible_retourne_place(self):
        """
        Vérifie que rechercherPlace() retourne une place adaptée pour
        une voiture compatible.

        Scénario prévu :
        - Créer un Parking avec au moins une place libre de dimensions suffisantes.
        - Créer une Voiture avec hauteur et longueur compatibles avec au moins
          une place du parking.
        - Appeler rechercherPlace(voiture).
        - Vérifier que :
          * une Place est retournée,
          * cette place est marquée comme occupée (ou n'est plus disponible),
          * le nombre total de places libres (_nbPlacesLibres) est décrémenté.
        """
        pass

    def test_rechercher_place_voiture_trop_grande_ne_trouve_aucune_place(self):
        """
        Vérifie que rechercherPlace() signale l'absence de place adaptée
        pour une voiture trop grande.

        Scénario prévu :
        - Créer un Parking avec des places de dimensions limitées.
        - Créer une Voiture dont la hauteur ou la longueur dépasse les
          capacités de toutes les places.
        - Appeler rechercherPlace(voiture).
        - Vérifier que :
          * aucune place n'est retournée (par exemple None),
          * le nombre de places libres n'est pas modifié.
        """
        pass

    def test_rechercher_place_parking_complet(self):
        """
        Vérifie que rechercherPlace() se comporte correctement lorsque
        le parking est complet.

        Scénario prévu :
        - Créer un Parking avec 0 place libre (_nbPlacesLibres = 0).
        - Créer une Voiture quelconque.
        - Appeler rechercherPlace(voiture).
        - Vérifier qu'aucune place n'est attribuée (None ou erreur contrôlée).
        """
        pass

    def test_nb_places_libres_par_niveau_niveau_valide(self):
        """
        Vérifie que NbPlacesLibresParNiveau() retourne le bon nombre de
        places libres pour un niveau existant.

        Scénario prévu :
        - Créer un Parking avec plusieurs niveaux et un certain nombre
          de places libres sur chaque niveau.
        - Appeler NbPlacesLibresParNiveau('A') (ou un autre identifiant valide).
        - Vérifier que la valeur retournée correspond au nombre de places
          réellement libres sur ce niveau.
        """
        pass

    def test_nb_places_libres_par_niveau_niveau_inexistant(self):
        """
        Vérifie que NbPlacesLibresParNiveau() gère le cas d'un niveau
        inexistant.

        Comportement attendu :
        - Appeler NbPlacesLibresParNiveau() avec un identifiant de niveau
          qui n'existe pas dans le parking.
        - Vérifier que la méthode :
          * soit retourne 0,
          * soit lève une exception,
          * soit signale explicitement que le niveau n'existe pas.
        """
        pass

    def test_add_abonnement_ajoute_un_abonnement(self):
        """
        Vérifie que addAbonnement() enregistre un nouvel abonnement
        dans le parking.

        Scénario prévu :
        - Créer un Parking sans abonnement enregistré.
        - Créer un Abonnement.
        - Appeler addAbonnement(abonnement).
        - Vérifier que l'abonnement ajouté est bien présent dans la
          structure interne du parking.
        """
        pass

    def test_add_abonnement_plusieurs_abonnements(self):
        """
        Vérifie que addAbonnement() permet d'enregistrer plusieurs
        abonnements dans le même parking.

        Scénario prévu :
        - Créer un Parking.
        - Créer plusieurs Abonnements.
        - Appeler addAbonnement() pour chacun d'eux.
        - Vérifier que tous les abonnements sont bien enregistrés.
        """
        pass


if __name__ == "__main__":
    unittest.main()
