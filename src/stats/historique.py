"""
Historique.

Ce module définit la classe Historique, qui garde la trace des
événements du parking (entrées, sorties, services) afin de permettre
leur exploitation ultérieure (statistiques, exports, étude du marché).
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import csv

class Historique:
    """
    Historique des événements du parking.

    Cette classe enregistre des événements "bruts" décrivant ce qui
    se passe dans le parking (entrée, sortie, service), avec les
    informations nécessaires pour produire ensuite des statistiques
    détaillées.

    Chaque événement est représenté par un dictionnaire contenant
    au minimum :

    - "type" : str
        Type d'événement. Les valeurs prévues sont :
        * "entree"   : entrée d'une voiture dans le parking ;
        * "sortie"   : sortie d'une voiture du parking ;
        * "service"  : service réalisé sur une voiture.
    - "date" : datetime
        Date et heure de l'événement.
    - "immat" : str
        Immatriculation de la voiture concernée.

    Des clés supplémentaires peuvent être ajoutées pour enrichir
    l'analyse, par exemple :

        Identifiant ou description de l'accès utilisé.
    - "type_service" : str
        Type de service ("entretien", "maintenance", "livraison", ...).
    - "est_abonne" : bool
        Indique si le client est abonné au moment de l'événement.
    - "est_super_abonne" : bool
        Indique si le client est super abonné au moment de l'événement.

    Attribues
    ----------
    evenements : list[dict]
        Liste des événements enregistrés. Chaque élément est un
        dictionnaire structuré comme décrit ci-dessus.
    """

    def __init__(self, fichier_csv: Optional[str] = None) -> None:
        """
        Initialise un historique vide.

        A la création, aucun événement n'est enregistré.
        """
        self.evenements: List[Dict[str, Any]] = []
        self.fichier_csv = fichier_csv

        if self.fichier_csv is not None:
            Path(self.fichier_csv).parent.mkdir(parents=True, exist_ok=True)

    def enregistrer_entree(self,imma: str,date: datetime, est_abonne: bool = False,est_super_abonne: bool = False,) -> None:
        """
        Enregistre un événement d'entrée dans l'historique.

        Parametres
        ----------
        imma : str
            Immatriculation de la voiture qui entre.
        date : datetime
            Date et heure de l'entrée.
        est_abonne : bool, optionnel
            True si le client est abonné au moment de l'entrée,
            False sinon. Par défaut False.
        est_super_abonne : bool, optionnel
            True si le client est super abonné au moment de l'entrée,
            False sinon. Par défaut False.
        """
        evenement = {
            "type": "entree",
            "immat": imma,
            "date": date,
            "est_abonne": est_abonne,
            "est_super_abonne": est_super_abonne,
        }
        
        self.evenements.append(evenement)
        self._append_to_csv(evenement)

    def enregistrer_sortie(self,imma: str, date: datetime, est_abonne: bool = False,est_super_abonne: bool = False,) -> None:
        """
        Enregistre un événement de sortie dans l'historique.

        Parametres
        ----------
        imma : str
            Immatriculation de la voiture qui sort.
        date : datetime
            Date et heure de la sortie.
        est_abonne : bool, optionnel
            True si le client est abonné au moment de la sortie,
            False sinon.
        est_super_abonne : bool, optionnel
            True si le client est super abonné au moment de la sortie,
            False sinon.
        """
        evenement = {
            "type": "sortie",
            "immat": imma,
            "date": date,
            "est_abonne": est_abonne,
            "est_super_abonne": est_super_abonne,
        }

        self.evenements.append(evenement)
        self._append_to_csv(evenement)

    def enregistrer_service(self,imma: str,date: datetime,type_service: str,est_abonne: bool = False, est_super_abonne: bool = False,) -> None:
        """
        Enregistre un événement de service dans l'historique.

        Parametres
        ----------
        imma : str
            Immatriculation de la voiture concernée.
        date : datetime
            Date et heure du service.
        type_service : str
            Type de service réalisé (par exemple "entretien",
            "maintenance", "livraison").
        est_abonne : bool, optionnel
            True si le client est abonné au moment du service,
            False sinon.
        est_super_abonne : bool, optionnel
            True si le client est super abonné au moment du service,
            False sinon.
        """
        if type_service not in ("entretien", "maintenance", "livraison"):
            raise ValueError("Type de service inconnu")
        
        evenement = {
            "type" : "service",
            "type_service": type_service,
            "immat": imma,
            "date": date,
            "est_abonne": est_abonne,
            "est_super_abonne": est_super_abonne,
        }

        self.evenements.append(evenement)
        self._append_to_csv(evenement)

    def evenements_dans_intervalle(self, debut: datetime,fin: datetime) -> List[Dict[str, Any]]:
        """
        Renvoie les événements dont la date est comprise dans un intervalle.

        Cette méthode ne réalise aucun calcul statistique : elle se
        contente de filtrer les événements selon leurs dates, ce qui
        permet ensuite aux classes de statistiques d'exploiter ces
        données (comptages, regroupements, etc.).

        Parametres
        ----------
        debut : datetime
            Date et heure de début de la période.
        fin : datetime
            Date et heure de fin de la période.

        Returns
        -------
        list[dict]
            Liste des événements dont la date est comprise entre
            `debut` et `fin` (bornes incluses ou non selon la
            convention retenue lors de l'implémentation).
        """
        if fin < debut:
            raise ValueError("La date de fin doit être postérieure à la date de début")
        
        resultats: List[Dict[str, Any]] = []
        for evenement in self.evenements:
            if debut <= evenement["date"] <= fin:
                resultats.append(evenement)
        return resultats

    def _append_to_csv(self, evenement: Dict[str, Any]) -> None:
        """
        Ajoute un événement à la fin du fichier CSV (si configuré).

        L'ouverture se fait en mode 'append' pour ne jamais écraser
        les anciennes données.
        """
        if self.fichier_csv is None:
            return

        evt_csv = {
            "type": evenement.get("type"),
            "immat": evenement.get("immat"),
            "date": evenement.get("date").isoformat()
            if isinstance(evenement.get("date"), datetime)
            else evenement.get("date"),
            "type_service": evenement.get("type_service") or "",
            "est_abonne": str(bool(evenement.get("est_abonne", False))),
            "est_super_abonne": str(bool(evenement.get("est_super_abonne", False))),
        }

        fichier = Path(self.fichier_csv)
        fichier_existe = fichier.exists()

        with fichier.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "type",
                    "immat",
                    "date",
                    "type_service",
                    "est_abonne",
                    "est_super_abonne",
                ],
            )
            if not fichier_existe:
                writer.writeheader()
            writer.writerow(evt_csv)

    @classmethod
    def depuis_csv(cls, fichier_csv: str) -> "Historique":
        """
        Construit un Historique en lisant tous les événements depuis un CSV.

        Paramètres
        ----------
        fichier_csv : str
            Chemin du fichier CSV contenant les événements
            précédemment enregistrés.

        Returns
        -------
        Historique
            Instance dont la liste `evenements` est remplie à partir
            du contenu du CSV.
        """
        hist = cls(fichier_csv=fichier_csv)
        path = Path(fichier_csv)

        if not path.exists():
            return hist

        with path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                type_evt = row.get("type")
                immat = row.get("immat") or ""
                date_str = row.get("date") or ""
                type_service = row.get("type_service") or None
                est_abonne_str = row.get("est_abonne") or "False"
                est_super_abonne_str = row.get("est_super_abonne") or "False"

                try:
                    date_val = datetime.fromisoformat(date_str)
                except ValueError:
                    continue

                evenement = {
                    "type": type_evt,
                    "immat": immat,
                    "date": date_val,
                    "type_service": type_service,
                    "est_abonne": est_abonne_str == "True",
                    "est_super_abonne": est_super_abonne_str == "True",
                }

                hist.evenements.append(evenement)

        return hist
