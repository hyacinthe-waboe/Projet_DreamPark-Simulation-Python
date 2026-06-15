"""
Acces.

Ce module définit la classe Acces, qui représente un point d'accès
au parking (borne d'entrée/sortie).
"""

from typing import TYPE_CHECKING
from datetime import datetime

# Imports du matériel (pas de risque de cycle ici, on peut laisser en haut)
from materiel.camera import Camera
from materiel.panneau_affichage import PanneauAffichage
from materiel.borne_ticket import BorneTicket
from materiel.teleporteur import Teleporteur
from stats.historique import Historique

# On utilise TYPE_CHECKING pour éviter que Python ne charge ces fichiers tout de suite
if TYPE_CHECKING:
    from noyau.parking import Parking
    from usagers.client import Client
    from usagers.voiture import Voiture

class Acces:
    """
    Point d'accès au parking.

    Un accès regroupe les opérations déclenchées lorsqu'un client arrive
    ou interagit avec le système : utilisation de la caméra, du panneau
    d'affichage et lancement de la procédure d'entrée.
    """
    def __init__(self, parking: "Parking", camera: Camera, panneau: PanneauAffichage, borne: BorneTicket, teleporteur: Teleporteur): 
        """
        On injecte les dependances : un acces est relie a un parking et possede des equipements.
        """
        self.parking = parking
        self.camera = camera
        self.panneau = panneau
        self.borne = borne
        self.teleporteur = teleporteur

    def actionnerCamera(self, c : "Client") -> "Voiture":
        """
        Actionne la caméra pour le client donné.

        Parametres
        ----------
        c : Client
            Client qui se présente à l'accès.

        Returns
        -------
        Voiture
            Voiture associée au client.
        """
        if not hasattr(c, 'voiture') or c.voiture is None:
             raise ValueError("Le client n'a pas de voiture.")
        
        v = c.voiture
        _ = self.camera.capturerImmatr(v)
        return v

    def actionnerPanneau(self) -> str:
        """
        Actionne le panneau d'affichage associé à l'accès.

        Returns
        -------
        str
            Message affiché ou résultat de l'action sur le panneau.
        """
        return self.panneau.afficherNbPlacesDisponibles(self.parking)

    def lancerProcedureEntree(self, c : "Client", date: datetime | None = None ) -> str :
        """
        Lance la procédure d'entrée pour un client.

        Parametres
        ----------
        c : Client
            Client qui souhaite entrer dans le parking.

        Returns
        -------
        str
            Résultat de la procédure d'entrée.
        """
        d = date or datetime.now()
        
        if not hasattr(c, 'voiture') or c.voiture is None:
            return "Erreur : Pas de voiture."
        
        voitureClient = c.voiture

        # Si le client est superabonée
        if c.estSuperAbonne:
            self.parking.historique.enregistrer_entree(
                imma=voitureClient.immatriculation,
                date=d,              
                est_abonne=True,
                est_super_abonne=True,
            )
            res = self.teleporteur.teleporterVoitureSuperAbonne(voitureClient)
            return f"Bienvenue Super Abonné. {res}"
        
        # abonnée normal
        placeTrouvee = self.parking.rechercherPlace(voitureClient)

        if placeTrouvee is None:
            return "Désolé, aucune place disponible pour votre véhicule."

        # Délivrance ticket et Téléportation
        ticket = self.borne.deliverTicket(c)
        
        # Teleportation de la voiture sur la place
        placement = self.teleporteur.teleporterVoiture(voitureClient, placeTrouvee)
        
        if placement:
            self.parking.historique.enregistrer_entree(
                imma=voitureClient.immatriculation,
                date=datetime.now(),
                est_abonne=c.estAbonne,
                est_super_abonne=c.estSuperAbonne,
            )
            if c.estSuperAbonne: 
                return f"Bienvenue VIP: Ticket {ticket}. Place {placeTrouvee.idPlace}."
            else:
                return f"Bienvenue : Ticket {ticket}. Place {placeTrouvee.idPlace}. Voiture garée."
        
    def forcerStationnement(self, client, id_place):
        """
        Force le stationnement d'une voiture sur une place précise.

        Cette méthode est prévue pour une interface (ex. clic sur une carte)
        permettant de choisir directement une place. Elle recherche la place
        par son identifiant, délivre un ticket, téléporte la voiture vers la
        place choisie, puis enregistre l'entrée dans l'historique en cas de succès.

        Parametres
        ----------
        client : Client
            Client qui souhaite entrer dans le parking.
        id_place : str
            Identifiant de la place ciblée (ex. "A1").

        Returns
        -------
        str
            Message indiquant le résultat (succès, refus, ou place indisponible).
        """
        # On cherche la place correspondant à l'ID (ex: "A1")
        place_cible = next((p for p in self.parking.places if p.idPlace == id_place), None)
        
        if place_cible and place_cible.estLibre:
            # On reprend la logique standard d'entrée
            ticket = self.borne.deliverTicket(client)
            
            # On utilise le téléporteur vers cette place spécifique
            succes = self.teleporteur.teleporterVoiture(client.voiture, place_cible)
            
            if succes:
                self.parking.historique.enregistrer_entree(
                    imma=client.voiture.immatriculation,
                    date=datetime.now(),
                    est_abonne=client.estAbonne,
                    est_super_abonne=client.estSuperAbonne
                )
                
                return f"Bienvenue. Ticket {ticket}. Place {place_cible.idPlace}."
            else:
                 return f"REFUS : Le véhicule est trop grand pour la place {id_place}."
        else:
            return "Place indisponible ou inexistante."


    def reprendreVoiture(self, client, ticket: str) -> str:
        """
        Lance la procédure de sortie et récupère la voiture du client.

        Cette méthode demande au téléporteur de ramener la voiture du client
        depuis les places du parking. En cas de succès, elle calcule le montant
        à payer (tarif normal ou VIP), enregistre la sortie dans l'historique,
        puis renvoie un message de fin de session.

        Parametres
        ----------
        client : Client
            Client qui souhaite récupérer sa voiture.
        ticket : str
            Identifiant du ticket associé au stationnement.

        Returns
        -------
        str
            Message indiquant le résultat (paiement et sortie, ou erreur).
        """
        if not client.voiture:
            return "Erreur: Ce client n'a pas de voiture."

        succes = self.teleporteur.recupererVoiture(client.voiture, self.parking.places)
        
        if succes:
            if client.estSuperAbonne:
                montant = self.parking.prix_vip
                msg_client = f"A BIENTÔT ! Ticket {ticket} payé ({montant}€)"
            else:
                montant = self.parking.prix
                msg_client = f"Au revoir ! Ticket {ticket} payé ({montant}€)."

            if self.parking.historique:
                self.parking.historique.enregistrer_sortie(
                    imma=client.voiture.immatriculation,
                    date=datetime.now(),
                    est_abonne=client.estAbonne,
                    est_super_abonne=client.estSuperAbonne 
                )
            
            return msg_client
        else:
            return "Erreur: Voiture introuvable ou déjà sortie."
