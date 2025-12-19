import os
import sys
import pydoc

RACINE = os.path.dirname(os.path.abspath(__file__))

if RACINE not in sys.path:
    sys.path.insert(0, RACINE)

SRC_DIR = os.path.join(RACINE, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Dossiers de sortie
DOC_DIR = os.path.join(RACINE, "doc")
os.makedirs(DOC_DIR, exist_ok=True)

PYDOC_DIR = os.path.join(DOC_DIR, "pydoc")
os.makedirs(PYDOC_DIR, exist_ok=True)

MODULES_CLASSES = [
    "usagers.client",
    "usagers.abonnement",
    "usagers.contrat",
    "usagers.voiture",
    "materiel.camera",
    "materiel.borne_ticket",
    "materiel.panneau_affichage",
    "materiel.teleporteur",
    "noyau.acces",
    "noyau.parking",
    "noyau.place",
    "noyau.placement",
    "services.service",
    "services.entretien",
    "services.maintenance",
    "services.livraison",
    "services.voiturier",
]

MODULES_CLASSES_STAT = [
    "stats.statistiques",
    "stats.historique",
]

MODULES_TESTS = [
    "tests.usagers.test_client",
    "tests.usagers.test_abonnement",
    "tests.usagers.test_contrat",
    "tests.usagers.test_voiture",
    "tests.materiel.test_camera",
    "tests.materiel.test_borne_ticket",
    "tests.materiel.test_panneau_affichage",
    "tests.materiel.test_teleporteur",
    "tests.noyau.test_acces",
    "tests.noyau.test_parking",
    "tests.noyau.test_place",
    "tests.noyau.test_placement",
    "tests.services.test_service",
    "tests.services.test_entretien",
    "tests.services.test_maintenance",
    "tests.services.test_livraison",
    "tests.services.test_voiturier",
]

MODULES_TESTS_STAT = [
    "tests.stats.test_statistiques",
    "tests.stats.test_historique",
]

ALL_MODULES = (
    MODULES_CLASSES
    + MODULES_TESTS
    + MODULES_CLASSES_STAT
    + MODULES_TESTS_STAT
)

os.chdir(PYDOC_DIR)

for module_name in ALL_MODULES:
    print(f"Génération de la doc pour {module_name}...")
    try:
        pydoc.writedoc(module_name)
    except Exception as e:
        print(f"  ERREUR sur {module_name} : {e}")

for module_name in ALL_MODULES:
    html_path = os.path.join(PYDOC_DIR, f"{module_name}.html")
    
    if not os.path.exists(html_path):
        continue

    with open(html_path, "r", encoding="utf-8") as f:
        contenu = f.read()

    if "style.css" not in contenu:
        contenu = contenu.replace(
            "<head>",
            "<head>\n<link rel=\"stylesheet\" href=\"../style.css\">\n",
            1,
        )
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(contenu)

index_path = os.path.join(DOC_DIR, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n<html>\n<head>\n")
    f.write("<meta charset='utf-8'>\n")
    f.write("<title>Documentation du projet Parking</title>\n")
    f.write("<link rel=\"stylesheet\" href=\"style.css\">\n")
    f.write("</head>\n<body class='index-page'>\n")
    f.write("<h1>Documentation du projet Parking</h1>\n")

    f.write("<h2>Modules Métier</h2>\n<ul class='modules-list'>\n")
    for module_name in MODULES_CLASSES:
        f.write(f"  <li><a href='pydoc/{module_name}.html'>{module_name}</a></li>\n")
    f.write("</ul>\n")

    f.write("<h2>Modules Statistiques</h2>\n<ul class='modules-list'>\n")
    for module_name in MODULES_CLASSES_STAT:
        f.write(f"  <li><a href='pydoc/{module_name}.html'>{module_name}</a></li>\n")
    f.write("</ul>\n")

    f.write("<h2>Tests Unitaires</h2>\n<ul class='modules-list'>\n")
    for module_name in MODULES_TESTS + MODULES_TESTS_STAT:
        f.write(f"  <li><a href='pydoc/{module_name}.html'>{module_name}</a></li>\n")
    f.write("</ul>\n")

    f.write("</body>\n</html>\n")

print(f"\nDocumentation générée dans : {DOC_DIR}")
print("Ouvre doc/index.html dans ton navigateur pour voir le résultat.")