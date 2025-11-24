"""
Acces.

Ce module définit la classe Acces, qui représente un point d'accès
au parking (borne d'entrée/sortie).
"""


from client import Client
from voiture import Voiture
from parking import Parking
from camera import Camera
from panneau_affichage import PanneauAffichage
from borne_ticket import BorneTicket
from teleporteur import Teleporteur


class Acces:
    """
    Point d'accès au parking.

    Un accès regroupe les opérations déclenchées lorsqu'un client arrive
    ou interagit avec le système : utilisation de la caméra, du panneau
    d'affichage et lancement de la procédure d'entrée.
    """
    def __init__(self, parking: Parking, camera: Camera, panneau: PanneauAffichage, borne: BorneTicket, teleporteur: Teleporteur): #####################################################################################################Ajouté
        """
        On injecte les dependances : un acces est relie a un parking et possede des equipements.
        """
        self.parking = parking
        self.camera = camera
        self.panneau = panneau
        self.borne = borne
        self.teleporteur = teleporteur

    def actionnerCamera(self, c : Client) -> Voiture:
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

    def lancerProcedureEntree(self, c : Client ) -> str :
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
        if not hasattr(c, 'voiture') or c.voiture is None:
            return "Erreur : Pas de voiture."
        
        voitureClient = c.voiture

        # Si le client est superabonée
        if c.estSuperAbonne:
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
            return f"Bienvenue. Ticket {ticket}. Voiture garée en place {placeTrouvee.idPlace}."
        else:
            return "Erreur technique lors de la téléportation."
