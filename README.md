# DreamPark

Simulation d'un parking intelligent développée en Python par **Olti Mjeku** et **Hyacinthe Waboe** dans le cadre de la Licence MIASHS à l'Université Toulouse - Jean Jaurès.

La branche `main` contient désormais la version finale. Les branches `partie0` à `partie4` conservent les différentes étapes pédagogiques du projet.

## Fonctionnalités

- entrée et sortie de véhicules abonnés ou occasionnels ;
- attribution automatique d'une place ;
- simulation d'une caméra, d'une borne de ticket, d'un panneau et d'un téléporteur ;
- gestion des abonnements et des contrats ;
- services de maintenance, d'entretien, de livraison et de voiturier ;
- historique des entrées, sorties et services ;
- statistiques d'occupation, de fréquentation et de recettes ;
- interface superviseur réalisée avec CustomTkinter ;
- persistance locale avec SQLite et exports CSV.

## Architecture

```text
.
├── src/
│   ├── noyau/        # Parking, places, accès et placements
│   ├── usagers/      # Clients, voitures, abonnements et contrats
│   ├── materiel/     # Caméra, borne, panneau et téléporteur
│   ├── services/     # Maintenance, entretien, livraison et voiturier
│   ├── stats/        # Historique, statistiques et base SQLite
│   └── interface.py  # Interface graphique
├── tests/            # Tests unitaires organisés comme le code source
├── doc/              # Diagramme UML et génération de documentation
└── run_tests.py      # Lanceur de la suite de tests
```

## Installation

Le cœur du projet utilise la bibliothèque standard de Python. L'interface graphique demande une dépendance supplémentaire :

```bash
python -m pip install customtkinter
```

## Utilisation

Lancer l'interface :

```bash
python src/interface.py
```

Lancer les tests :

```bash
python run_tests.py
```

La suite actuelle contient **119 tests unitaires**.

Générer la documentation technique :

```bash
python doc/gen_doc.py
```

## Parcours pédagogique

Les branches retracent la construction progressive du projet :

- `partie0` : initialisation et conception ;
- `partie1` : cas d'utilisation « se garer » ;
- `partie2` : sortie du véhicule et services ;
- `partie3` : historique et statistiques ;
- `partie4` : interface superviseur et version finale.

## Limites actuelles

- les données sont enregistrées localement ;
- l'interface représente une vue de supervision, pas un système matériel réel ;
- le projet est une simulation universitaire et non une solution destinée à la production.

## Auteurs

- **Olti Mjeku**
- **Hyacinthe Waboe**
