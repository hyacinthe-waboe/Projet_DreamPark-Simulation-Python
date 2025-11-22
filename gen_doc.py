# gen_doc.py
import os
import sys
import pydoc

RACINE = os.path.dirname(os.path.abspath(__file__))

SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

DOC_DIR = os.path.join(RACINE, "doc", "pydoc")
os.makedirs(DOC_DIR, exist_ok=True)

MODULES = [
    "client",
    "abonnement",
    "contrat",
    "camera",
    "borne_ticket",
    "service",
    "entretien",
    "maintenance",
    "livraison",
    "acces",
    # ajoute ici le reste de tes modules (parking, voiture, etc.)
]

# 5) Génération des fichiers HTML
os.chdir(DOC_DIR)  # pydoc écrit les .html dans le dossier courant
for module_name in MODULES:
    print(f"Génération de la doc pour {module_name}...")
    try:
        pydoc.writedoc(module_name)
    except Exception as e:
        print(f"  ERREUR sur {module_name} : {e}")


index_path = os.path.join(DOC_DIR, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n<html>\n<head>\n")
    f.write("<meta charset='utf-8'>\n")
    f.write("<title>Documentation du projet Parking</title>\n")
    f.write("</head>\n<body>\n")
    f.write("<h1>Documentation du projet Parking</h1>\n")
    f.write("<ul>\n")
    for module_name in MODULES:
        f.write(f"  <li><a href='{module_name}.html'>{module_name}</a></li>\n")
    f.write("</ul>\n")
    f.write("</body>\n</html>\n")

print(f"\nDocumentation générée dans : {DOC_DIR}")
print("Ouvre doc/pydoc/index.html dans ton navigateur pour la consulter.")
