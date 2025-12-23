# 🚗 DREAMPARK — MJEKU_WABOE (MIASHS) 🅿️

Simulation d’un **parking intelligent** développée en **Python** dans le cadre de la **Licence MIASHS (UT2J)**.

Le dépôt est structuré pour séparer clairement :
- le **code source** (`src/`)
- les **tests unitaires** (`tests/`)
- la **documentation** et les artefacts de conception (`doc/`)
- les **données locales** (`data/`) *(non versionnées)*

---

## ✨ Fonctionnalités principales

Le projet simule notamment :

- ✅ **Entrée / sortie** de véhicules (abonnés ou non)
- ✅ **Attribution automatique** d’une place via un **téléporteur**
- ✅ **Services annexes** (maintenance, entretien, livraison, voiturier)
- ✅ **Historisation** des événements (entrées/sorties/services)
- ✅ **Statistiques** (taux d’occupation, entrées du jour, recettes, répartition, etc.)
- ✅ **Interface superviseur** (carte des places + tableau de bord)


---

## 🧱 Architecture du projet

Arborescence (vue d’ensemble) :

```text
PROJET-PARKING-MIASHS/
├── data/               # Données locales (sauvegarde / exports) — non versionnées
│
├── doc/                # Documentation + outils doc
│   ├── pydoc/          # (généré) documentation technique pydoc
│   ├── diagrammeDeClasse.pdf
│   ├── style.css
│   └── gen_doc.py      # 📚 Générateur de documentation (pydoc → HTML)
│
├── src/                # Code source
│   ├── interface.py    # 🖥️ Interface graphique (point d'entrée UI)
│   ├── noyau/          # Parking, Place, Acces, Placement...
│   ├── usagers/        # Client, Voiture, Abonnement, Contrat...
│   ├── materiel/       # Camera, BorneTicket, PanneauAffichage, Teleporteur...
│   ├── services/       # Entretien, Maintenance, Livraison, Voiturier...
│   ├── stats/          # Historique, Statistiques...
│   └── __init__.py
│
├── tests/              # Tests unitaire (même sous-dossiers que src/)
│   ├── noyau/
│   ├── usagers/
│   ├── materiel/
│   ├── services/
│   ├── stats/
│   └── __init__.py
│
├── run_tests.py        # 🚀 Lanceur de tests (recommandé)
├── .gitignore
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

---

## 🖥️ Lancer l’interface (GUI)

📍 L’interface se trouve ici : **`src/interface.py`**

### Dépendance nécessaire
L’interface utilise **CustomTkinter** :

```bash
pip install customtkinter
```
---

## 🧭 Comment utiliser l’interface (Vue Superviseur)

L’interface se découpe en 3 zones :

### 1 - Barre de gauche (actions)
- **+ Nouvel arrivant** : simule l’arrivée d’un client et lance la procédure d’entrée.
- **Simulation auto** : enchaîne automatiquement des arrivées (mode démo / test).
- **Sortir véhicule** : lance une procédure de sortie pour la voiture sélectionnée.
- **Maintenance / Livraison (Voiturier)** : déclenche des services sur un véhicule.

### 2 - Zone centrale (carte des places)
- Les places sont affichées par zones (ex. **Zone A**, **Zone B**)
- Chaque place est indiquée :
  - **LIBRE** (disponible)
  - **OCCUPÉ** (déjà prise)

👉 Tu peux **sélectionner une place** dans la carte (utile si l’interface propose le stationnement forcé via clic).

### 3 - Colonne de droite (statistiques)
- **Entrées du jour**
- **Recettes (historique)**
- **Tendance du trafic**
- **Répartition / occupation**
