import os
import sys

chemin_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
if chemin_src not in sys.path:
    sys.path.insert(0, chemin_src)

import unittest
from noyau.parking import Parking
from noyau.place import Place 

from usagers.abonnement import Abonnement 
from usagers.voiture import Voiture


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
        p = Parking(nbPlacesParNiveau=10, nbPlacesLibres=20, prix=15, nbNiveaux=2)
        
        self.assertEqual(p._nbPlacesParNiveau, 10)
        self.assertEqual(p.nbNiveaux, 2)
        self.assertEqual(p.prix, 15)
        # Dans notre implémentation, _nbPlacesLibres est recalculé dynamiquement (10 places * 2 niveaux = 20), donc on vérifie que le calcul est bon.
        self.assertEqual(p._nbPlacesLibres, 20)

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
          * (Note: l'occupation effective se fait via le Teleporteur, ici on vérifie
            surtout que la place retournée est valide et libre au moment de la recherche).
        """
        # Parking : 1 niveau, 5 places standard (5.0m x 2.5m)
        p = Parking(nbPlacesParNiveau=5, nbPlacesLibres=5, prix=10, nbNiveaux=1)
        
        # Voiture compatible (plus petite que la place)
        v = Voiture(hauteur=2.0, longueur=4.0, immatriculation="AB-123-CD", estDansParking=False)
        
        place_trouvee = p.rechercherPlace(v)
      
        self.assertIsNotNone(place_trouvee, "Une place devrait être trouvée")
        self.assertIsInstance(place_trouvee, Place)
        self.assertTrue(place_trouvee.estLibre, "La place trouvée doit être libre")
        # On vérifie que c'est bien la première place disponible (A1)
        self.assertEqual(place_trouvee.idPlace, "A1")

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
          * aucune place n'est retournée (par exemple None).
        """
        p = Parking(nbPlacesParNiveau=5, nbPlacesLibres=5, prix=10, nbNiveaux=1)
        
        v_longue = Voiture(hauteur=2.0, longueur=6.0, immatriculation="XX-999-XX", estDansParking=False)
      
        resultat = p.rechercherPlace(v_longue)
      
        self.assertIsNone(resultat, "Aucune place ne devrait être trouvée pour un véhicule trop long")

    def test_rechercher_place_parking_complet(self):
        """
        Vérifie que rechercherPlace() se comporte correctement lorsque
        le parking est complet.

        Scénario prévu :
        - Créer un Parking.
        - Rendre manuellement toutes les places occupées.
        - Créer une Voiture quelconque.
        - Appeler rechercherPlace(voiture).
        - Vérifier qu'aucune place n'est attribuée (None).
        """
        p = Parking(nbPlacesParNiveau=2, nbPlacesLibres=2, prix=10, nbNiveaux=1)
        v = Voiture(hauteur=1.5, longueur=3.0, immatriculation="AA-000-BB", estDansParking=False)
        
        for place in p.places:
            place._estLibre = False
          
        resultat = p.rechercherPlace(v)
        
        self.assertIsNone(resultat, "Le parking est complet, on ne doit rien trouver")

    def test_nb_places_libres_par_niveau_niveau_valide(self):
        """
        Vérifie que NbPlacesLibresParNiveau() retourne le bon nombre de
        places libres pour un niveau existant.

        Scénario prévu :
        - Créer un Parking avec plusieurs niveaux.
        - Appeler NbPlacesLibresParNiveau('A').
        - Vérifier que la valeur retournée correspond au nombre de places initial.
        """
        p = Parking(nbPlacesParNiveau=10, nbPlacesLibres=20, prix=10, nbNiveaux=2)
        
        nb_libres_A = p.NbPlacesLibresParNiveau('A')
        self.assertEqual(nb_libres_A, 10)

        p.places[0]._estLibre = False 
        
        nb_libres_A_apres = p.NbPlacesLibresParNiveau('A')
        self.assertEqual(nb_libres_A_apres, 9)

    def test_nb_places_libres_par_niveau_niveau_inexistant(self):
        """
        Vérifie que NbPlacesLibresParNiveau() gère le cas d'un niveau
        inexistant.

        Comportement attendu :
        - Appeler NbPlacesLibresParNiveau() avec un identifiant de niveau inexistant.
        - Vérifier que la méthode retourne 0.
        """
        p = Parking(nbPlacesParNiveau=5, nbPlacesLibres=5, prix=10, nbNiveaux=1)
        
        resultat = p.NbPlacesLibresParNiveau('Z')
        
        self.assertEqual(resultat, 0)

    def test_add_abonnement_ajoute_un_abonnement(self):
        """
        Vérifie que addAbonnement() enregistre un nouvel abonnement
        dans le parking.

        Scénario prévu :
        - Créer un Parking sans abonnement enregistré.
        - Créer un Abonnement.
        - Appeler addAbonnement(abonnement).
        - Vérifier que l'abonnement ajouté est bien présent.
        """
        p = Parking(10, 10, 10, 1)
        abo = Abonnement("Standard", 50.0, False)
        
        p.addAbonnement(abo)
        
        self.assertIn(abo, p.abonnements)
        self.assertEqual(len(p.abonnements), 1)

    def test_add_abonnement_plusieurs_abonnements(self):
        """
        Vérifie que addAbonnement() permet d'enregistrer plusieurs
        abonnements dans le même parking.
        """
        p = Parking(10, 10, 10, 1)
        abo1 = Abonnement("Standard", 50.0, False)
        abo2 = Abonnement("Premium", 100.0, True)
        
        p.addAbonnement(abo1)
        p.addAbonnement(abo2)
        
        self.assertEqual(len(p.abonnements), 2)
        self.assertIn(abo1, p.abonnements)
        self.assertIn(abo2, p.abonnements)


if __name__ == "__main__":
    unittest.main()