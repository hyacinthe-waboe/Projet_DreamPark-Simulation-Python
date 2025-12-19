"""
Parking.

Ce module définit la classe Parking, qui centralise la gestion des places,
des niveaux et des abonnements du parking.
"""

from usagers.voiture import Voiture     
from usagers.abonnement import Abonnement 
from stats.historique import Historique

from noyau.place import Place                

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from noyau.acces import Acces

from typing import Optional

class Parking:
    """
    Parking principal.

    Le parking est caractérisé par un nombre fixe de places par niveau,
    un nombre total de places libres, un nombre de niveaux et un prix
    de stationnement. Cette classe est pensée pour être utilisée comme
    une instance unique dans l'application.

    Attribues
    ----------
    _nbPlacesParNiveau : int
        Nombre de places disponibles sur chaque niveau.
    _nbPlacesLibres : int
        Nombre total de places actuellement libres dans le parking.
    _prix : int
        Prix de stationnement associé au parking.
    nbNiveaux : int
        Nombre de niveaux (étages) du parking.
    """

    def __init__(self, nbPlacesParNiveau: int, nbPlacesLibres: int, prix: int, nbNiveaux: int, historique: Optional[Historique] = None,):
        """
        Initialise le parking.

        Parametres
        ----------
        _nbPlacesParNiveau : int
            Nombre de places sur chaque niveau.
        _nbPlacesLibres : int
            Nombre initial de places libres dans le parking.
        _prix : int
            Prix de stationnement.
        nbNiveaux : int
            Nombre de niveaux du parking.
        """
        self._nbPlacesParNiveau = nbPlacesParNiveau
        self._nbPlacesLibres = nbPlacesLibres 
        self._prix = prix
        self.nbNiveaux = nbNiveaux
        
        self.places = [] 
        self.abonnements = [] 
        self._historique = historique if historique is not None else Historique()

        #Initialisation automatique des places, n génère les niveaux A, B, C...
        for i in range(nbNiveaux):
            nomNiveau = chr(65 + i) 
            
            for j in range(1, nbPlacesParNiveau + 1):
                # On crée un ID unique ex: "A1", "B5"
                id_p = f"{nomNiveau}{j}"
                
                p = Place(idPlace=id_p, numero=j, niveau=nomNiveau, 
                          longueur=5.0, hauteur=2.5, estLibre=True)
                
                self.places.append(p)
        
        # On met à jour le compteur réel de places libres
        self._nbPlacesLibres = len(self.places) 

    def rechercherPlace(self, v : Voiture) -> Place:
        """
        Recherche une place adaptée pour une voiture.

        Parametres
        ----------
        v :
            Voiture pour laquelle on souhaite trouver une place.

        Returns
        -------
        Place
            Place attribuée à la voiture.
        """
        for place in self.places:
            if place.estLibre:
                if (place.hauteur >= v.hauteur) and (place.longueur >= v.longueur):
                    return place
        
        return None

    def NbPlacesLibresParNiveau(self, niveau: str) -> int:
        """
        Renvoie le nombre de places libres sur un niveau donné.

        Parametres
        ----------
        niveau : str
            Identifiant du niveau (par exemple 'A', 'B', 'C', ...).

        Returns
        -------
        int
            Nombre de places libres sur ce niveau.
        """
        count = 0
        for place in self.places:
            if place.niveau == niveau and place.estLibre:
                count += 1
        return count

    def addAbonnement(self, ab : Abonnement) -> None:
        """
        Ajoute un abonnement géré par le parking.

        Parametres
        ----------
        ab :
            Abonnement à enregistrer dans le parking.
        """
        self.abonnements.append(ab)

    @property
    def prix(self):
        return self._prix
    
    @property
    def historique(self) -> Historique:
        return self._historique