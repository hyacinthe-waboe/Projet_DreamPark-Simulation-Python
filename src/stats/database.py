import sqlite3
import os

class DatabaseManager:
    """Gère uniquement l'affichage visuel (qui est garé où ?)"""
    def __init__(self):
        # 1. On calcule le chemin vers la racine du projet
        # On remonte 3 crans : database.py -> noyau -> src -> RACINE
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # 2. On définit le dossier data
        data_dir = os.path.join(base_dir, "data")
        
        # 3. On crée le dossier s'il n'existe pas (sécurité)
        os.makedirs(data_dir, exist_ok=True)
        
        # 4. On fixe le chemin final de la DB
        self.db_name = os.path.join(data_dir, "visuel_parking.db")
        
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS occupation (
                place_id TEXT PRIMARY KEY,
                client_nom TEXT,
                immatriculation TEXT,
                ticket_id TEXT,
                is_vip INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def garer_voiture(self, place_id, client_nom, immat, ticket, is_vip):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            vip_int = 1 if is_vip else 0
            cursor.execute("""
                INSERT INTO occupation (place_id, client_nom, immatriculation, ticket_id, is_vip)
                VALUES (?, ?, ?, ?, ?)
            """, (place_id, client_nom, immat, ticket, vip_int))
            conn.commit()
            return True
        except: return False
        finally: conn.close()

    def liberer_place(self, place_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM occupation WHERE place_id = ?", (place_id,))
        conn.commit()
        conn.close()

    def charger_etat(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM occupation")
        rows = cursor.fetchall()
        conn.close()
        
        data = {}
        for row in rows:
            data[row["place_id"]] = {
                "client": row["client_nom"],
                "immat": row["immatriculation"],
                "ticket": row["ticket_id"],
                "vip": bool(row["is_vip"])
            }
        return data
    
    def tout_effacer(self):
        """Vide complètement la table d'occupation."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM occupation") # Supprime toutes les lignes
        conn.commit()
        conn.close()