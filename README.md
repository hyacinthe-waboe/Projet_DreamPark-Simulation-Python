<h1 align="center">🅿️ DreamPark</h1>

<p align="center">
  <strong>Une simulation complète de parking intelligent, de l'entrée du véhicule jusqu'aux statistiques.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/CustomTkinter-Interface-1F6AA5?style=for-the-badge" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Tests-119_réussis-2EA44F?style=for-the-badge" alt="119 tests">
</p>

## 🚗 Le projet

DreamPark est une simulation développée en Python par **Olti Mjeku** et **Hyacinthe Waboe** pendant la Licence MIASHS à l'Université Toulouse - Jean Jaurès.

Le projet reproduit le fonctionnement d'un parking moderne : accueil des clients, attribution des places, équipements, services, sorties, historique et supervision. La branche `main` contient la version finale, tandis que les branches `partie0` à `partie4` racontent sa construction progressive.

## ✨ Fonctionnalités

- 🚘 entrée et sortie de véhicules abonnés ou occasionnels ;
- 🅿️ attribution automatique d'une place adaptée ;
- 📷 simulation d'une caméra et d'une borne de ticket ;
- 🤖 panneau d'affichage et téléporteur ;
- ⭐ abonnements, contrats et clients prioritaires ;
- 🧽 services d'entretien, maintenance, livraison et voiturier ;
- 📜 historique des entrées, sorties et services ;
- 📊 statistiques d'occupation, de fréquentation et de recettes ;
- 🖥️ interface de supervision avec CustomTkinter ;
- 💾 persistance locale avec SQLite et CSV.

## 🧱 Architecture

```text
.
├── src/
│   ├── noyau/        # Parking, places, accès et placements
│   ├── usagers/      # Clients, voitures, abonnements et contrats
│   ├── materiel/     # Caméra, borne, panneau et téléporteur
│   ├── services/     # Maintenance, entretien, livraison et voiturier
│   ├── stats/        # Historique, statistiques et base SQLite
│   └── interface.py  # Interface graphique
├── tests/            # Tests organisés comme le code source
├── doc/              # Diagramme UML et documentation
└── run_tests.py      # Lanceur de la suite de tests
```

## 🚀 Installation et utilisation

Installer la dépendance de l'interface :

```bash
python -m pip install customtkinter
```

Lancer DreamPark :

```bash
python src/interface.py
```

Lancer les tests :

```bash
python run_tests.py
```

Résultat actuel : **119 tests sur 119 réussis** ✅

Générer la documentation :

```bash
python doc/gen_doc.py
```

## 🧭 Une construction par étapes

| Branche | Étape |
|---|---|
| `partie0` | Initialisation et conception |
| `partie1` | Cas d'utilisation « se garer » |
| `partie2` | Sortie du véhicule et services |
| `partie3` | Historique et statistiques |
| `partie4` | Interface superviseur et version finale |

## 🚧 Limites actuelles

- les données sont enregistrées localement ;
- l'interface simule une supervision, sans matériel réel connecté ;
- DreamPark reste un projet universitaire et non un logiciel de production.

## 👥 Équipe

- **Olti Mjeku**
- **Hyacinthe Waboe**

<p align="center"><em>Un projet où chaque nouvelle partie a ajouté une vraie pièce au parking. 🚗</em></p>
