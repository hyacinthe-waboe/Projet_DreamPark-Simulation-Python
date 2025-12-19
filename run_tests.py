import sys
import os
import unittest

def run_all_tests():
    # 1. Configuration silencieuse des chemins
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # 2. Découverte des tests
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=project_root, pattern="test_*.py")
    
    # 3. Exécution (verbosity=0 pour réduire le bruit au maximum)
    # stream=open(os.devnull, 'w') permettrait de masquer même les erreurs, 
    # mais verbosity=0 est plus sûr (affiche les erreurs seulement si ça plante).
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    
    # 4. Calcul et Affichage du résultat
    nb_total = result.testsRun
    nb_echecs = len(result.failures) + len(result.errors)
    nb_succes = nb_total - nb_echecs

    print(f"\nRésultat : {nb_succes} / {nb_total} tests réussis.")

    # Retourne une erreur au système si tout n'est pas vert (utile pour les pipelines)
    sys.exit(not result.wasSuccessful())

if __name__ == "__main__":
    run_all_tests()