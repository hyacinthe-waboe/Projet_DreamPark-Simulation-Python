# projet-parking-miashs

## Partie 0 – Squelette & spécifications

Cette branche correspond à la mise en place du projet sans implémentation métier.

### Contenu de la partie 0

- **Architecture du projet** :
  - `src/` : toutes les classes du diagramme UML (squelettes uniquement, méthodes avec `pass`).
  - `tests/` : fichiers de tests unitaires, sous forme de **spécifications** (méthodes `test_...` décrites mais non implémentées).
  - `doc/` :
    - `style.css` : feuille de style pour la documentation HTML.
    - `index.html` : page d’entrée de la documentation (générée automatiquement).
    - `pydoc/` : contiendra la documentation HTML générée (non versionnée dans le dépôt).
  - `gen_doc.py` : script de génération automatique de la documentation.

### Générer la documentation (pydoc)

La documentation n’est **pas** stockée dans le dépôt : le dossier `doc/pydoc/` est ignoré par `.gitignore`.  
Pour (re)générer la documentation, se placer à la racine du projet et exécuter :

```bash
python gen_doc.py
