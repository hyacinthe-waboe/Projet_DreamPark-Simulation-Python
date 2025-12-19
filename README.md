# 🚗 MJEKU_SAÏD - PARKING MIASHS 🅿️

Simulation d’un **parking intelligent** développée en **Python pur** (bibliothèque standard uniquement) dans le cadre de la **Licence MIASHS (UT2J)**.

Le dépôt est structuré pour séparer clairement :
- Le **code source** (`src/`)
- Les **tests unitaires** (`tests/`)
- La **documentation** et les artefacts de conception (`doc/`)

---

## ✨ Fonctionnalités principales

Le projet simule notamment :

- ✅ **Entrée / sortie** de véhicules (abonnés ou non)
- ✅ **Attribution automatique** d’une place via un **téléporteur**
- ✅ **Services annexes** (maintenance, entretien, livraison, voiturier)
- ✅ **Historisation** des événements (entrées/sorties/services)
- ✅ **Statistiques** (ex. taux d’occupation, chiffre d’affaires)

---

## 🧱 Architecture du projet

Arborescence (vue d’ensemble) :

```text
PROJET-PARKING-MIASHS/
├── src/
│   ├── noyau/          # Parking, Place, Acces, Placement
│   ├── usagers/        # Client, Voiture, Abonnement, Contrat
│   ├── materiel/       # Camera, BorneTicket, PanneauAffichage, Teleporteur
│   ├── services/       # Entretien, Maintenance, Livraison, Voiturier
│   ├── stats/          # Historique, Statistiques
│   └── __init__.py
│
├── tests/              # Tests unitaires (mêmes sous-dossiers que src/)
│   ├── noyau/
│   ├── usagers/
│   ├── materiel/
│   ├── services/
│   └── stats/
│
├── doc/                # Documentation HTML, style.css, diagramme UML
│   ├── index.html
│   ├── style.css
│   └── pydoc/          # (généré) documentation technique pydoc
│
├── run_tests.py        # 🚀 Lanceur de tests (recommandé)
├── gen_doc.py          # 📚 Générateur de documentation (pydoc → HTML)
└── README.md
```
---
## 📚 Lancer la générationd de document (méthode recommandée)

Utiliser le script racine **`gen_doc.py`** :

```bash
python gen_doc.py
```
---

## 🧪 Lancer les tests (méthode recommandée)

Utiliser le script racine **`run_tests.py`** :

```bash
python run_tests.py
```
---
## 🧠 Conception (UML)

📌 Le **diagramme UML complet** de la conception est disponible dans :

- **`doc/`** ✅

Vous pourrez y visualiser la structure des classes et leurs relations.