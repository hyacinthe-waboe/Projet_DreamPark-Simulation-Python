import os
import sys
import pydoc

RACINE = os.path.dirname(os.path.abspath(__file__))

SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

DOC_DIR1 = os.path.join(RACINE, "doc")
os.makedirs(DOC_DIR1, exist_ok=True)

DOC_DIR2 = os.path.join(RACINE, "doc", "pydoc")
os.makedirs(DOC_DIR2, exist_ok=True)

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
    "panneau_affichage",
    "parking",
    "place",
    "placement",
    "teleporteur",
    "voiture",
    "voiturier",
]

os.chdir(DOC_DIR2)
for module_name in MODULES:
    print(f"Génération de la doc pour {module_name}...")
    try:
        pydoc.writedoc(module_name)
    except Exception as e:
        print(f"  ERREUR sur {module_name} : {e}")

for module_name in MODULES:
    html_path = os.path.join(DOC_DIR2, f"{module_name}.html")
    if not os.path.exists(html_path):
        continue

    with open(html_path, "r", encoding="utf-8") as f:
        contenu = f.read()

    if "style.css" not in contenu:
        contenu = contenu.replace(
            "<head>",
            "<head>\n<link rel=\"stylesheet\" href=\"../style.css\">\n", 1, 
        )
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(contenu)

# 3) Génération de l'index avec CSS
index_path = os.path.join(DOC_DIR1, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n<html>\n<head>\n")
    f.write("<meta charset='utf-8'>\n")
    f.write("<title>Documentation du projet Parking</title>\n")
    f.write("<link rel=\"stylesheet\" href=\"style.css\">\n")
    f.write("</head>\n<body>\n")
    f.write("<h1>Documentation du projet Parking</h1>\n")
    f.write("<ul>\n")
    for module_name in MODULES:
        f.write(f"  <li><a href='pydoc/{module_name}.html'>{module_name}</a></li>\n")
    f.write("</ul>\n")
    f.write("</body>\n</html>\n")

print(f"\nDocumentation générée dans : {DOC_DIR2}")
print("Ouvre doc/index.html dans ton navigateur pour la consulter.")
