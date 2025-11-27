# Projet Parking MIASHS

Ce dépôt contient le projet de développement d'un système de gestion de parking (DreamPark) réalisé dans le cadre de la licence MIASHS. Le projet est structuré en plusieurs livraisons successives correspondant à différentes branches git.

---

## Partie 0 – Squelette & Spécifications

Cette branche correspond à la mise en place de l'architecture du projet et à la définition des spécifications, sans implémentation métier.

### Contenu de l'architecture

* **`src/`** : Contient tous les squelettes des classes du diagramme UML (méthodes définies avec `pass`).
* **`tests/`** : Contient les fichiers de tests unitaires sous forme de spécifications (méthodes `test_...` décrites par des docstrings mais non implémentées).
* **`doc/`** :
    * `style.css` : Feuille de style pour la documentation HTML.
    * `index.html` : Page d’entrée de la documentation.
    * `pydoc/` : Dossier de destination pour la documentation générée (ignoré par git).
* **`gen_doc.py`** : Script utilitaire pour la génération automatique de la documentation.

### Générer la documentation

La documentation technique n’est pas versionnée. Pour la générer localement :

```bash
python gen_doc.py
```

## Partie 1 – Implémentation du cas d'utilisation : Se Garer

Cette branche (`Partie1`) correspond à l'implémentation fonctionnelle du cas d'utilisation **"Se Garer"** et à la validation des tests unitaires associés.

### Objectifs
L'objectif principal était de rendre fonctionnel le circuit d'entrée d'un véhicule dans le parking, en respectant les contraintes de dimensions, de disponibilité et de gestion des droits (Abonnés vs Super Abonnés).

### Implémentation fonctionnelle (`src/`)

Le développement respecte les principes de la **Programmation Orientée Objet (POO)** et le patron **Modèle-Vue-Contrôleur (MVC)**. La convention de nommage *camelCase* est appliquée.

#### 1. Modèle de Données (Noyau)
Ces classes gèrent l'état du système et l'intégrité des données :

* **`parking.py`** : Génération automatique des places et méthode `rechercherPlace` (filtre par disponibilité et dimensions).
* **`place.py`** : Gestion de l'état d'occupation (`estLibre` avec setter) et méthode `addPlacement`.
* **`voiture.py`** : Association au parking via `addPlacementV` et programmation défensive (refus de dimensions invalides).
* **`placement.py`** : Gestion de la période d'occupation (`partirPlace`) et validation chronologique.
* **`contrat.py`** / **`abonnement.py`** : Gestion de la logique contractuelle et de l'état des abonnements.

#### 2. Contrôleurs et Orchestration
Ces classes gèrent la logique métier et les flux d'actions :

* **`acces.py`** : Contrôleur principal (`lancerProcedureEntree`). Gère les décisions (Super Abonné, ticket, parking complet).
* **`teleporteur.py`** : Composant transactionnel (`teleporterVoiture`). Assure la cohérence atomique entre la création du placement et la mise à jour des états (Voiture/Place).
* **`client.py`** : Point d'entrée utilisateur (`entrerParking`) déléguant l'action à l'accès.

#### 3. Outils et Matériel Simulé
Ces classes simulent les interactions physiques :

* **`camera.py`** : Simulation des capteurs (lecture immatriculation/dimensions) avec gestion d'erreurs.
* **`panneau_affichage.py`** : Affichage sécurisé des disponibilités (gestion du statut "COMPLET").
* **`borne_ticket.py`** : Interaction client (délivrance ticket, proposition d'abonnements).

### Tests Unitaires (`tests/`)

L'ensemble des tests définis en Partie 0 a été implémenté suivant une approche **TDD** (Test-Driven Development).

* **Stratégie** : Utilisation de **vrais objets** (pas de mocks excessifs) dans le `setUp` pour valider les interactions réelles (Tests d'intégration).
* **Couverture** :
    1.  **Tests d'Intégration** : Scénario complet `Client.entrerParking`.
    2.  **Tests de Composants** : Logique de recherche du `Parking` et transaction du `Teleporteur`.
    3.  **Tests Modèles** : Validation des états et contraintes de `Voiture`, `Place`, etc.

### Lancement des tests

Pour vérifier le bon fonctionnement de la Partie 1, exécuter la suite de tests à la racine du projet :

```bash
python -m unittest discover tests
```

## Partie 2 – Cas d'utilisation : Reprendre la voiture

Cette branche (`Partie2`) correspond à l’implémentation du cas d’utilisation **« Reprendre la voiture »**, via la gestion des **services associés** (entretien, maintenance, livraison) et du **voiturier** chargé des livraisons physiques.

### Objectifs

- Mutualiser la logique des services via une classe de base `Service`.
- Garantir la **cohérence temporelle** des services (`dateService` ≥ `dateDemande`, ou non définie au départ).
- Empêcher l’exécution multiple d’un même service (entretien, maintenance, livraison).
- Modéliser l’intervention du **voiturier** pour la sortie et la livraison des voitures.

### Implémentation fonctionnelle (`src/`)

- **`service.py`**  
  Classe de base des services :  
  - Attributs : `dateDemande`, `dateService`, `rapport`.  
  - Règles : refus d’une `dateService` antérieure à `dateDemande` ; refus d’un rapport vide.

- **`entretien.py`**  
  Service d’**entretien** (nettoyage / révision légère) :  
  - Attribut : `effectue` (booléen).  
  - Méthode : `effectuerEntretien()` met à jour `dateService` (si besoin), le `rapport`, et empêche un second appel.

- **`maintenance.py`**  
  Service de **maintenance** technique :  
  - Attributs : `maintenance` (booléen), `voiture`.  
  - Méthode : `effectuerMaintenance(voiture)` vérifie la validité de la voiture, met à jour `dateService` et `rapport`, et interdit plusieurs exécutions.

- **`livraison.py`**  
  Service de **livraison** de la voiture à une adresse :  
  - Attributs : `adresse`, `heureLivraison` (optionnel), `livree` (booléen).  
  - Méthode : `effectuerLivraison()` vérifie l’adresse, met à jour `dateService` et le `rapport`, et empêche plusieurs livraisons pour le même service.

- **`voiturier.py`**  
  Représentation du **voiturier** chargé de sortir et livrer les voitures :  
  - Attribut : `_numVoiturier` (numéro ≥ 0).  
  - Méthode : `livrerVoiture(voiture, dateLivraison, heure)` vérifie voiture/date/heure, sort la voiture du parking (`estDansParking = False`) et refuse les livraisons invalides (heure hors plage, date passée, voiture déjà livrée, etc.).

### Tests unitaires (`tests/`)

- **`test_service.py`** : validation de l’initialisation de `Service` et des contraintes sur les dates / rapport.  
- **`test_entretien.py`** : tests de `effectuerEntretien()` (mise à jour du rapport, de la date, exécution unique, cohérence avec `dateDemande`).  
- **`test_maintenance.py`** : tests de `effectuerMaintenance(voiture)` (voiture valide/invalides, mise à jour de la date et du rapport, exécution unique).  
- **`test_livraison.py`** : tests de `effectuerLivraison()` (rapport mis à jour, dateService mise en place, exécution unique, adresse obligatoire).  
- **`test_voiturier.py`** : tests de l’initialisation du voiturier et de `livrerVoiture()` (voiture sortie du parking, heures et dates invalides, double livraison refusée).

### Lancement des tests (Partie 2)

Depuis la racine du projet :

```bash
python -m unittest discover tests
```