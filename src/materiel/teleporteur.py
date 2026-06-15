"""
Téléporteur.

Ce module définit la classe Teleporteur, qui est chargée de déplacer
les voitures entre l'extérieur et les places de stationnement du parking.
"""

from datetime import date
from usagers.voiture import Voiture
from noyau.place import Place
from noyau.placement import Placement

class Teleporteur:
    """
    Téléporteur de voitures.

    Le téléporteur permet de :
    - placer une voiture sur une place donnée,
    - gérer un mode particulier pour les super abonnés.
    """

    def teleporterVoiture(self, v : Voiture, p : Place) -> Placement:
        """
        Téléporte une voiture vers une place de stationnement.

        Parametres
        ----------
        v :
            Voiture à téléporter.
        p :
            Place de stationnement sur laquelle la voiture doit être déposée.

        Returns
        -------
        Placement
            Placement associé à la voiture sur la place.
        """
        if not p.estLibre:
            print(f"Erreur: La place {p.idPlace} est déjà occupée.")
            return None

        if (v.hauteur > p.hauteur) or (v.longueur > p.longueur):
            print(f"Erreur: La voiture est trop grande pour la place {p.idPlace}.")
            return None

        nouveauPlacement = Placement(dateDebut=date.today(), dateFin=date.today(), estEnCours=True)

        v.estDansParking = True   
        p.estLibre = False

        p.voiture = v 

        p.addPlacementP(nouveauPlacement)   
        v.addPlacementV(nouveauPlacement)

        return nouveauPlacement

    def teleporterVoitureSuperAbonne(self, v : Voiture ) -> str:
        """
        Téléporte une voiture appartenant à un super abonné.

        Parametres
        ----------
        v :
            Voiture du super abonné à téléporter.

        Returns
        -------
        str
            Information sur le résultat de la téléportation
            (format à préciser lors de l'implémentation).
        """
        if not hasattr(v, 'proprietaire') or v.proprietaire is None:
            return False

        if not v.proprietaire.estSuperAbonne:
            return False 
        
        v.estDansParking = True
        return "Téléportation Super Abonné effectuée avec succès vers la zone VIP."

    def recupererVoiture(self, voiture, liste_places) -> bool:
        """
        Récupère une voiture garée dans le parking et libère sa place.

        Cette méthode recherche la voiture dans la liste des places du parking.
        Si elle est trouvée, la place correspondante est libérée (la place
        redevient disponible et n'est plus associée à une voiture) et le statut
        de la voiture est mis à jour pour indiquer qu'elle n'est plus dans le parking.

        Parametres
        ----------
        voiture : Voiture
            Voiture à récupérer.
        liste_places : list[Place]
            Liste des places de stationnement à parcourir.

        Returns
        -------
        bool
            True si la voiture a été trouvée et récupérée avec succès,
            False si la voiture n'est pas dans le parking ou est introuvable.
        """
        if not voiture.estDansParking:
            return False

        # On parcourt les places pour trouver où est garée cette voiture
        place_trouvee = None
        for p in liste_places:
            if not p.estLibre and hasattr(p, 'voiture') and p.voiture == voiture:
                place_trouvee = p
                break
        
        if place_trouvee:
            # On libère la place
            place_trouvee.estLibre = True
            place_trouvee.voiture = None 
            
            # On met à jour le statut de la voiture
            voiture.estDansParking = False
            return True
        
        return False
