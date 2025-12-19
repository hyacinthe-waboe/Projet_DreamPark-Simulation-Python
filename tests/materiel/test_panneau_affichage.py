import os
import sys

chemin_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
if chemin_src not in sys.path:
    sys.path.insert(0, chemin_src)

import unittest
from materiel.panneau_affichage import PanneauAffichage   
from noyau.parking import Parking


class TestPanneauAffichage(unittest.TestCase):
    """Tests de la classe PanneauAffichage."""

    def test_afficher_nb_places_disponibles_parking_avec_places_libres(self):
        """
        Vérifie que afficherNbPlacesDisponibles() indique correctement le nombre
        de places lorsqu'il en reste plusieurs.

        Scénario prévu :
        - Créer un parking avec un certain nombre de places libres (> 1).
        - Créer un panneau d'affichage.
        - Appeler afficherNbPlacesDisponibles(parking).
        - Vérifier que la chaîne retournée mentionne le nombre de places libres.
        """
        p = Parking(nbPlacesParNiveau=10, nbPlacesLibres=10, prix=10, nbNiveaux=1)
        panneau = PanneauAffichage()
        
        msg = panneau.afficherNbPlacesDisponibles(p)
        
        self.assertIn("10 places disponibles", msg)

    def test_afficher_nb_places_disponibles_parking_complet(self):
        """
        Vérifie que afficherNbPlacesDisponibles() indique que le parking est
        complet lorsqu'il n'y a plus de place libre.

        Scénario possibles :
        - Créer un parking avec 0 place libre.
        - Créer un panneau d'affichage.
        - Appeler afficherNbPlacesDisponibles(parking).
        - Vérifier que le message retourné signale clairement que le parking
          est complet (ou qu'il n'y a aucune place disponible).
        """
        p = Parking(nbPlacesParNiveau=10, nbPlacesLibres=0, prix=10, nbNiveaux=1)
        
        for place in p.places:
            place._estLibre = False
        p._nbPlacesLibres = 0
        
        panneau = PanneauAffichage()
        
        msg = panneau.afficherNbPlacesDisponibles(p)
        
        self.assertIn("COMPLET", msg)

    def test_afficher_nb_places_disponibles_une_seule_place(self):
        """
        Vérifie le comportement de afficherNbPlacesDisponibles() lorsqu'il ne
        reste qu'une seule place libre.

        Scénario prévu :
        - Créer un parking avec exactement 1 place libre.
        - Créer un panneau d'affichage.
        - Appeler afficherNbPlacesDisponibles(parking).
        - Vérifier que le message retourné indique correctement qu'il reste
          une seule place (gestion éventuelle du singulier/pluriel).
        """
        p = Parking(nbPlacesParNiveau=1, nbPlacesLibres=1, prix=10, nbNiveaux=1)
        panneau = PanneauAffichage()
        
        msg = panneau.afficherNbPlacesDisponibles(p)
        
        self.assertIn("1 places disponibles", msg)

    def test_afficher_nb_places_disponibles_valeur_incoherente(self):
        """
        Vérifie que afficherNbPlacesDisponibles() gère une valeur incohérente
        pour le nombre de places libres (par exemple négative).

        Comportement attendu :
        - Si le nombre de places libres est négatif ou invalide, la méthode doit
          soit :
            * corriger/normaliser la valeur,
            * soit signaler l'erreur (message particulier, exception, etc.).
        - Le test devra vérifier le comportement retenu.
        """
        p = Parking(nbPlacesParNiveau=1, nbPlacesLibres=1, prix=10, nbNiveaux=1)
        p.places = [] 
        
        p._nbPlacesLibres = -5 
        
        panneau = PanneauAffichage()
        
        msg = panneau.afficherNbPlacesDisponibles(p)
        
        self.assertIn("Erreur", msg)


if __name__ == "__main__":
    unittest.main()
