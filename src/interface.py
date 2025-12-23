import customtkinter as ctk
from tkinter import messagebox
import datetime
import random 
import os

from noyau.parking import Parking
from noyau.acces import Acces
from noyau.placement import Placement 

from materiel.camera import Camera
from materiel.panneau_affichage import PanneauAffichage
from materiel.borne_ticket import BorneTicket
from materiel.teleporteur import Teleporteur

from usagers.client import Client
from services.maintenance import Maintenance
from services.livraison import Livraison
from services.entretien import Entretien

from stats.historique import Historique
from stats.statistiques import Statistiques
from stats.database import DatabaseManager

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

COLORS = {
    "bg_main": "#0f172a", 
    "bg_sidebar": "#1e293b", 
    "card_bg": "#334155",
    "accent": "#3b82f6", 
    "success": "#10b981", 
    "danger": "#ef4444",
    "warning": "#f59e0b",
    "text_main": "#f8fafc", 
    "text_muted": "#94a3b8",
    "vip": "#d946ef", 
    "maintenance": "#f59e0b",
    "panel_bg": "#1e293b"
}

# --- CLASSE UTILITAIRE POUR STOPPER LES DOUBLONS ---
class GhostHistorique:
    """Un historique 'Fantôme' qui ne fait rien. On le donne au Parking pour le faire taire."""
    def enregistrer_entree(self, *args, **kwargs): pass
    def enregistrer_sortie(self, *args, **kwargs): pass
    def enregistrer_service(self, *args, **kwargs): pass

class ParkingEnterpriseGUI(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("DREAMPARK")
        
        # Configuration Responsive
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{int(screen_width*0.8)}x{int(screen_height*0.8)}+0+0")
        self.after(0, lambda: self.state("zoomed"))
        self.configure(fg_color=COLORS["bg_main"])

        # Gestion des chemins (Dossier Data)
        dossier_src = os.path.dirname(os.path.abspath(__file__))
        racine = os.path.dirname(dossier_src)
        dossier_data = os.path.join(racine, "data")
        os.makedirs(dossier_data, exist_ok=True)
        chemin_csv = os.path.join(dossier_data, "parking_log.csv")
        
        # Initialisation Base de données
        reset_mode = not os.path.exists(chemin_csv)
        self.db = DatabaseManager()

        if reset_mode:
            self.db.tout_effacer()
            print("RESET TOTAL : Historique supprimé détecté -> Base visuelle vidée.")

        # Création du Parking (Backend)
        self.parking = Parking(10, 20, 15, 3) 
        self.acces = Acces(self.parking, Camera(), PanneauAffichage(), BorneTicket(), Teleporteur())
        
        # On charge le VRAI historique pour l'interface 
        self.historique = Historique.depuis_csv(chemin_csv)
        
        # 2. On donne un FAUX historique au Parking (Backend)
        # Comme ça, quand le backend dit "J'enregistre une entrée", ça part dans le vide.
        # Seule l'interface enregistrera la ligne complète dans le CSV.
        self.parking.historique = GhostHistorique() 
        
        self.stats_manager = Statistiques(self.historique, self.parking)

        self.db_places = {} 
        self.place_widgets_map = {} 
        self.selected_place_id = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()      
        self.setup_main_area()    
        self.build_initial_map()  
        
        self.charger_persistance()
        self.log_message("SYSTÈME DÉMARRÉ. PRÊT.")
        if hasattr(self, 'db_places') and self.db_places:
            self._resynchroniser_backend()
            
        self.rafraichir_vue() 
        self.update_trend_monitor("STABLE")
        self.update_clock()

    # 2. GESTION PERSISTANCE & BACKEND

    def charger_persistance(self):
        data_sql = self.db.charger_etat()
        if not data_sql: return
        count = 0
        for place_id, info in data_sql.items():
            c = Client(info["client"], "Inconnu", bool(info["vip"]), bool(info["vip"]), 1)
            c.nouvelleVoiture(info["immat"], 1.5, 4.0)
            
            target_place = next((p for p in self.parking.places if p.idPlace == place_id), None)
            if target_place:
                target_place.estLibre = False
                p_obj = Placement(datetime.date.today(), datetime.date.today(), True)
                p_obj.place = target_place; p_obj.voiture = c.voiture
                c.voiture.addPlacementV(p_obj); target_place.addPlacementP(p_obj)
                
                self.db_places[place_id] = {
                    "client": c, "voiture": c.voiture, "ticket": info["ticket"], "statut": "STATIONNÉ"
                }
                count += 1
        if count > 0: self.log_message(f"RESTAURATION: {count} véhicules récupérés.")

    def _resynchroniser_backend(self):
        print("--- Synchronisation Interface -> Backend ---")
        for place_id, data in self.db_places.items():
            voiture = data["voiture"]
            place_reelle = next((p for p in self.parking.places if p.idPlace == place_id), None)
            
            if place_reelle:
                place_reelle.estLibre = False
                place_reelle.voiture = voiture
                voiture.estDansParking = True
            else:
                print(f"Erreur Sync: Place {place_id} introuvable dans le backend.")

    # 3. GUI SETUP

    def setup_sidebar(self):
        screen_h = self.winfo_screenheight()
        is_small_screen = screen_h < 900
        
        if is_small_screen:
            self.sidebar = ctk.CTkScrollableFrame(self, width=280, corner_radius=0, fg_color=COLORS["bg_sidebar"])
        else:
            self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=COLORS["bg_sidebar"])
        
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        lbl = ctk.CTkLabel(self.sidebar, text="DREAMPARK\nULTIMATE", font=ctk.CTkFont(family="Impact", size=32), text_color=COLORS["accent"])
        lbl.pack(pady=(30, 20), padx=20)

        self.frame_entry = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.frame_entry.pack(fill="x", padx=10)
        ctk.CTkLabel(self.frame_entry, text="GESTION ENTRÉES", font=("Arial", 12, "bold"), text_color=COLORS["text_muted"]).pack(anchor="w", pady=5)
        
        self.btn_new = ctk.CTkButton(self.frame_entry, text="+ NOUVEL ARRIVANT", command=self.open_entry_form, fg_color=COLORS["success"], height=45, state="disabled")        
        self.btn_new.pack(fill="x", pady=5)
        self.btn_sim = ctk.CTkButton(self.frame_entry, text="⚡ SIMULATION AUTO", command=self.simuler_entree, fg_color=COLORS["card_bg"], border_width=1, border_color=COLORS["accent"], height=40)
        self.btn_sim.pack(fill="x", pady=5)

        ctk.CTkFrame(self.sidebar, height=2, fg_color=COLORS["card_bg"]).pack(fill="x", padx=20, pady=20)

        self.frame_ctx = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.frame_ctx.pack(fill="both", expand=not is_small_screen, padx=10, pady=(0, 20))
        
        self.lbl_sel = ctk.CTkLabel(self.frame_ctx, text="AUCUNE SÉLECTION", font=("Arial", 14, "bold"))
        self.lbl_sel.pack(anchor="w", pady=(0, 5))

        self.info_box = ctk.CTkTextbox(self.frame_ctx, height=150 if is_small_screen else 200, fg_color=COLORS["bg_main"], text_color=COLORS["text_main"])
        self.info_box.pack(fill="both", expand=True, pady=(0, 15)) 
        self.info_box.insert("0.0", "Sélectionnez une place...")
        self.info_box.configure(state="disabled")

        self.btn_out = self.mk_btn(self.frame_ctx, "SORTIR VÉHICULE", self.action_sortir, COLORS["danger"])
        self.btn_mnt = self.mk_btn(self.frame_ctx, "MAINTENANCE", self.action_maintenance, COLORS["accent"])
        self.btn_liv = self.mk_btn(self.frame_ctx, "LIVRAISON (VOITURIER)", self.action_livraison, COLORS["warning"])
        self.btn_ent = self.mk_btn(self.frame_ctx, "LAVAGE / ENTRETIEN", self.action_entretien, COLORS["vip"])

    def mk_btn(self, parent, text, cmd, color):
        btn = ctk.CTkButton(parent, text=text, command=cmd, fg_color=color, state="disabled", height=55, font=("Arial", 13, "bold"))
        btn.pack(fill="x", pady=5)
        return btn

    def setup_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_columnconfigure(0, weight=7)
        self.main_area.grid_columnconfigure(1, weight=3)
        self.main_area.grid_rowconfigure(2, weight=1)

        h = ctk.CTkFrame(self.main_area, fg_color="transparent")
        h.grid(row=0, column=0, columnspan=2, sticky="ew")
        ctk.CTkLabel(h, text="VUE SUPERVISEUR", font=("Arial", 24, "bold")).pack(side="left")
        
        self.lbl_clock = ctk.CTkLabel(h, text="CHARGEMENT...", font=("Consolas", 18, "bold"), text_color=COLORS["accent"])
        self.lbl_clock.pack(side="right")
        
        self.stats_f = ctk.CTkFrame(self.main_area, fg_color=COLORS["bg_sidebar"], corner_radius=10)
        self.stats_f.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        ctk.CTkLabel(self.stats_f, text="TAUX D'OCCUPATION GLOBAL", font=("Arial", 12, "bold"), text_color=COLORS["text_muted"]).pack(side="top", anchor="w", padx=20, pady=(10, 5))
        self.prog_main = ctk.CTkProgressBar(self.stats_f, height=15, corner_radius=8); self.prog_main.pack(side="top", fill="x", padx=20, pady=(0, 15)); self.prog_main.set(0)

        screen_h = self.winfo_screenheight()
        is_small_screen = screen_h < 900
        
        if is_small_screen:
            self.map_frame = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent", label_text="ZONE DE STATIONNEMENT")
        else:
            self.map_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
            ctk.CTkLabel(self.map_frame, text="ZONE DE STATIONNEMENT", font=("Arial", 12, "bold"), text_color=COLORS["text_muted"]).grid(row=0, column=0, columnspan=5, sticky="w", pady=(5,0), padx=5)

        self.map_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10), padx=(0, 10))
        
        self.console = ctk.CTkTextbox(self.main_area, height=80, fg_color=COLORS["bg_sidebar"], text_color=COLORS["success"], font=("Courier New", 12))
        self.console.grid(row=3, column=0, sticky="ew", padx=(0, 10)); self.console.configure(state="disabled")

        self.setup_right_panel()

    def setup_right_panel(self):
        screen_h = self.winfo_screenheight()
        is_small_screen = screen_h < 900

        if is_small_screen:
            self.rp = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent", label_text="STATISTIQUES")
            self.rp.grid(row=2, column=1, rowspan=2, sticky="nsew")
            self.rp.grid_columnconfigure(0, weight=1)
        else:
            self.rp = ctk.CTkFrame(self.main_area, fg_color="transparent")
            self.rp.grid(row=2, column=1, rowspan=2, sticky="nsew")
            self.rp.grid_columnconfigure(0, weight=1)
            for i in range(4): self.rp.grid_rowconfigure(i, weight=1)

        self.c_entrees = self.mk_card(self.rp, "ENTRÉES DU JOUR", 0)
        self.lbl_nb_entrees = ctk.CTkLabel(self.c_entrees, text="0", font=("Arial", 28, "bold"))
        self.lbl_nb_entrees.pack(expand=True)
        
        self.c_ca = self.mk_card(self.rp, "RECETTES (HISTORIQUE)", 1)
        self.lbl_ca = ctk.CTkLabel(self.c_ca, text="0€", font=("Arial", 28, "bold"), text_color=COLORS["success"])
        self.lbl_ca.pack(expand=True)

        self.c_alert = self.mk_card(self.rp, "TENDANCE DU TRAFIC (IA)", 2)
        f_trend = ctk.CTkFrame(self.c_alert, fg_color="transparent")
        f_trend.pack(expand=True, fill="both", padx=10, pady=5)
        f_center = ctk.CTkFrame(f_trend, fg_color="transparent")
        f_center.pack(expand=True) 
        self.lbl_trend_icon = ctk.CTkLabel(f_center, text="⚓", font=("Arial", 42))
        self.lbl_trend_icon.grid(row=0, column=0, rowspan=2, padx=(0, 15), sticky="e")
        self.lbl_trend_title = ctk.CTkLabel(f_center, text="STABLE", font=("Arial", 18, "bold"), text_color=COLORS["text_muted"])
        self.lbl_trend_title.grid(row=0, column=1, sticky="w")
        self.lbl_trend_pred = ctk.CTkLabel(f_center, text="Aucune variation majeure", font=("Arial", 12), text_color=COLORS["text_muted"])
        self.lbl_trend_pred.grid(row=1, column=1, sticky="wn")

        self.c_det = ctk.CTkFrame(self.rp, fg_color=COLORS["panel_bg"], corner_radius=12)
        self.c_det.grid(row=3, column=0, sticky="nsew", pady=(0, 0 if not is_small_screen else 15))
        ctk.CTkLabel(self.c_det, text="RÉPARTITION", font=("Arial", 12, "bold"), text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=(15, 5))
        f = ctk.CTkFrame(self.c_det, fg_color="transparent"); f.pack(fill="both", expand=True, padx=15, pady=5)
        self.lbl_pa = ctk.CTkLabel(f, text="Zone A: 0/0", font=("Arial", 11, "bold")); self.lbl_pa.pack(anchor="w")
        self.bar_a = ctk.CTkProgressBar(f, height=8, progress_color=COLORS["accent"]); self.bar_a.pack(fill="x", pady=(0, 5)); self.bar_a.set(0)
        self.lbl_pb = ctk.CTkLabel(f, text="Zone B: 0/0", font=("Arial", 11, "bold")); self.lbl_pb.pack(anchor="w")
        self.bar_b = ctk.CTkProgressBar(f, height=8, progress_color=COLORS["warning"]); self.bar_b.pack(fill="x", pady=(0, 5)); self.bar_b.set(0)
        self.lbl_pc = ctk.CTkLabel(f, text="Zone C: 0/0", font=("Arial", 11, "bold")); self.lbl_pc.pack(anchor="w")
        self.bar_c = ctk.CTkProgressBar(f, height=8, progress_color=COLORS["success"]); self.bar_c.pack(fill="x", pady=(0, 10)); self.bar_c.set(0)
        ctk.CTkLabel(f, text="CLIENTS VIP", font=("Arial", 11, "bold"), text_color=COLORS["vip"]).pack(anchor="center")
        self.lbl_vip = ctk.CTkLabel(f, text="0", font=("Arial", 20, "bold"), text_color=COLORS["vip"]); self.lbl_vip.pack(pady=2)

    def mk_card(self, p, t, r):
        c = ctk.CTkFrame(p, fg_color=COLORS["panel_bg"], corner_radius=12)
        c.grid(row=r, column=0, sticky="nsew", pady=(0, 15))
        ctk.CTkLabel(c, text=t, font=("Arial", 12, "bold"), text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=10)
        return c

    def build_initial_map(self):
        for w in self.map_frame.winfo_children(): w.destroy()
        self.place_widgets_map.clear()
        screen_h = self.winfo_screenheight()
        is_small_screen = screen_h < 900
        start_row = 0
        if not is_small_screen:
            ctk.CTkLabel(self.map_frame, text="ZONE DE STATIONNEMENT", font=("Arial", 12, "bold"), text_color=COLORS["text_muted"]).grid(row=0, column=0, columnspan=5, sticky="w", pady=(5,10), padx=5)
            start_row = 1 
        for i in range(5): self.map_frame.grid_columnconfigure(i, weight=1)
        niveaux = sorted(list(set(p.niveau for p in self.parking.places)))
        curr_row = start_row
        for niv in niveaux:
            ctk.CTkLabel(self.map_frame, text=f"ZONE {niv}", font=("Arial Black", 16), text_color=COLORS["accent"]).grid(row=curr_row, column=0, columnspan=5, sticky="w", pady=10, padx=10)
            curr_row += 1
            places = [p for p in self.parking.places if p.niveau == niv]
            places.sort(key=lambda x: x.numero)
            for idx, p in enumerate(places):
                r = curr_row + (idx // 5); c = idx % 5
                btn = ctk.CTkButton(self.map_frame, text=f"{p.idPlace}\n...", height=70, font=("Arial", 14, "bold"), border_width=2, command=lambda o=p: self.on_click(o))
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                self.place_widgets_map[p.idPlace] = btn
            curr_row += (len(places)//5) + 2
        if not is_small_screen:
            for r in range(curr_row):
                self.map_frame.grid_rowconfigure(r, weight=1)

    # 4. LOGIC

    def rafraichir_vue(self):
        entrees = self.stats_manager.total_entrees_jour()
        recettes = self.stats_manager.recettes_du_jour()
        
        occ = len(self.db_places)
        tot = len(self.parking.places)
        ratio = occ/tot if tot > 0 else 0
        
        self.lbl_nb_entrees.configure(text=str(entrees))
        self.lbl_ca.configure(text=f"{recettes}€")
        self.prog_main.set(ratio)
        self.prog_main.configure(progress_color=COLORS["danger"] if ratio > 0.8 else COLORS["accent"])

        places_a = [p for p in self.parking.places if p.niveau == 'A']
        oc_a = len([p for p in places_a if not p.estLibre])
        self.bar_a.set(oc_a/len(places_a) if places_a else 0); self.lbl_pa.configure(text=f"Zone A: {oc_a}/{len(places_a)}")
        
        places_b = [p for p in self.parking.places if p.niveau == 'B']
        oc_b = len([p for p in places_b if not p.estLibre])
        self.bar_b.set(oc_b/len(places_b) if places_b else 0); self.lbl_pb.configure(text=f"Zone B: {oc_b}/{len(places_b)}")

        places_c = [p for p in self.parking.places if p.niveau == 'C']
        oc_c = len([p for p in places_c if not p.estLibre])
        self.bar_c.set(oc_c/len(places_c) if places_c else 0); self.lbl_pc.configure(text=f"Zone C: {oc_c}/{len(places_c)}")

        nb_vip = sum(1 for d in self.db_places.values() if d["client"].estSuperAbonne)
        self.lbl_vip.configure(text=str(nb_vip))

        self.update_context()
        for p in self.parking.places:
            btn = self.place_widgets_map.get(p.idPlace)
            if btn:
                d = self.db_places.get(p.idPlace)
                if p.estLibre:
                    btn.configure(fg_color=COLORS["card_bg"], border_color=COLORS["success"], text=f"{p.idPlace}\nLIBRE")
                else:
                    col = COLORS["danger"]
                    txt = f"{p.idPlace}\nOCCUPÉ"
                    if d:
                        if d.get("statut") == "MAINTENANCE": 
                            col = COLORS["maintenance"]; txt += "\nMAINT."
                        elif d.get("statut") == "ENTRETIEN":
                            col = "#06b6d4" 
                            txt += "\nLAVAGE"
                        elif d["client"].estSuperAbonne: 
                            col = COLORS["vip"]; txt += "\nVIP"
                    btn.configure(fg_color=COLORS["card_bg"], border_color=col, text=txt)
                
                if self.selected_place_id == p.idPlace:
                    btn.configure(fg_color="#475569", border_color=COLORS["warning"])

    def on_click(self, place):
        self.selected_place_id = place.idPlace if self.selected_place_id != place.idPlace else None
        self.rafraichir_vue()

    def update_context(self):
        target = "AUCUNE SÉLECTION"
        info = "Sélectionnez une place."
        
        enable_actions_occupied = False 
        enable_action_add = False       

        if self.selected_place_id:
            target = f"PLACE {self.selected_place_id}"
            
            d = self.db_places.get(self.selected_place_id)
            
            if d:
                c, v = d["client"], d["voiture"]
                info = (
                    f"CLIENT: {c.nom}\n"
                    f"IMMAT: {v.immatriculation}\n"
                    f"TICKET: {d['ticket']}\n"
                    f"VIP: {'OUI' if c.estSuperAbonne else 'NON'}\n"
                    f"STATUT: {d.get('statut')}"
                )
                enable_actions_occupied = True  
                enable_action_add = False       
            else:
                p = next((x for x in self.parking.places if x.idPlace == self.selected_place_id), None)
                if p and p.estLibre:
                    info = "STATUT: LIBRE\n\nVous pouvez ajouter un véhicule."
                    enable_actions_occupied = False
                    enable_action_add = True    
                else:
                    info = "OCCUPÉ (Inconnu)"

        self.lbl_sel.configure(text=target)
        self.info_box.configure(state="normal"); self.info_box.delete("0.0", "end"); self.info_box.insert("0.0", info); self.info_box.configure(state="disabled")
        
        state_occ = "normal" if enable_actions_occupied else "disabled"
        for b in [self.btn_out, self.btn_mnt, self.btn_liv, self.btn_ent]:
            b.configure(state=state_occ)

        self.btn_new.configure(state="normal" if enable_action_add else "disabled")

    def log_message(self, msg):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.console.configure(state="normal")
        self.console.insert("0.0", f"[{ts}] > {msg}\n")
        self.console.configure(state="disabled")

    def update_trend_monitor(self, last_action_type):
        """Moniteur IA pour prédire la saturation et afficher la tendance"""
        nb_occupees = len(self.db_places)
        nb_total = len(self.parking.places)
        places_libres = nb_total - nb_occupees
        
        if nb_occupees == 0:
            titre = "TRAFIC STABLE ⚓"
            icon = "■"
            color = COLORS["text_muted"]
            estimation = "Parking vide (En attente)"
        elif last_action_type == "ENTREE":
            titre = "FLUX ENTRANT 🌊"
            icon = "▲"
            color = COLORS["danger"]
            if places_libres > 0:
                estimation = f"Saturation estimée : {places_libres * 2} min"
            else:
                estimation = "PARKING COMPLET !"
        elif last_action_type == "SORTIE":
            titre = "FLUX SORTANT 🌪️"
            icon = "▼"
            color = COLORS["success"] 
            estimation = "Libération progressive"
        else:
            titre = "TRAFIC STABLE ⚓"
            icon = "■"
            color = COLORS["text_muted"]
            estimation = "Aucune variation majeure"

        self.lbl_trend_title.configure(text=titre, text_color=color)
        self.lbl_trend_icon.configure(text=icon, text_color=color)
        self.lbl_trend_pred.configure(text=estimation)

    def update_clock(self):
        # Format : JJ/MM/AAAA - HH:MM:SS
        now = datetime.datetime.now().strftime("%d/%m/%Y  •  %H:%M:%S")
        self.lbl_clock.configure(text=now)
        self.after(1000, self.update_clock)

    # 5. ACTIONS UTILISATEUR & SIMULATION

    def simuler_entree(self):
        n = random.randint(100,999)
        self.traiter_entree(f"Sim-{n}", f"RD-{n}", 1.5, 4.0, False)

    def open_entry_form(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Nouvelle Entrée")
        dialog.geometry("400x550")
        dialog.attributes("-topmost", True)

        ctk.CTkLabel(dialog, text="INFORMATIONS VÉHICULE", font=("Arial", 16, "bold"), text_color=COLORS["accent"]).pack(pady=(20, 10))

        ctk.CTkLabel(dialog, text="Nom du Client :").pack(pady=2)
        entry_nom = ctk.CTkEntry(dialog, width=250)
        entry_nom.pack(pady=5)

        ctk.CTkLabel(dialog, text="Immatriculation :").pack(pady=2)
        entry_immat = ctk.CTkEntry(dialog, width=250)
        entry_immat.pack(pady=5)

        ctk.CTkLabel(dialog, text="Hauteur (m) :").pack(pady=2)
        entry_haut = ctk.CTkEntry(dialog, width=250)
        entry_haut.insert(0, "1.5")
        entry_haut.pack(pady=5)

        ctk.CTkLabel(dialog, text="Longueur (m) :").pack(pady=2)
        entry_long = ctk.CTkEntry(dialog, width=250)
        entry_long.insert(0, "4.0")
        entry_long.pack(pady=5)

        switch_vip = ctk.CTkSwitch(dialog, text="Client VIP (Prioritaire)", progress_color=COLORS["vip"])
        switch_vip.pack(pady=20)

        def valider():
            try:
                n = entry_nom.get()
                i = entry_immat.get()
                h = float(entry_haut.get())
                l = float(entry_long.get())
                v = bool(switch_vip.get())

                self.traiter_entree(n, i, h, l, v, self.selected_place_id)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "La hauteur et la longueur doivent être des chiffres (ex: 1.5).")

        ctk.CTkButton(dialog, text="VALIDER L'ENTRÉE", command=valider, fg_color=COLORS["success"], height=40, width=200).pack(pady=10)

    def traiter_entree(self, nom, immat, h, l, vip, target_id=None):
        c = Client(nom or "Inconnu", "Adresse Inconnue", vip, vip, 0)
        c.nouvelleVoiture(immat or "XX-000-XX", h, l)
        
        if target_id:
            try: 
                res = self.acces.forcerStationnement(c, target_id)
            except: 
                res = c.entrerParking(self.acces)
        else:
            res = c.entrerParking(self.acces)

        if "Bienvenue" in res or "VIP" in res:
            try:
                sep = "Place " if "Place " in res else "place "
                partie_ticket = res.split("Ticket ")[1].split(".")[0].strip()
                partie_place = res.split(sep)[1].split(".")[0].strip()

                self.db_places[partie_place] = {
                    "client": c, 
                    "voiture": c.voiture, 
                    "ticket": partie_ticket, 
                    "statut": "STATIONNÉ"
                }
                self.db.garer_voiture(partie_place, nom, immat, partie_ticket, vip)
                
                if vip:
                    msg_log = f"★ ENTRÉE VIP ★: {nom} (Ticket: {partie_ticket}) -> {partie_place}"
                else:
                    msg_log = f"ENTRÉE: {nom} (Ticket: {partie_ticket}) -> {partie_place}"
                
                self.log_message(msg_log)
                
                # ENREGISTREMENT COMPLET DANS LE CSV
                self.historique.enregistrer_entree(
                    imma=immat,
                    date=datetime.datetime.now(),
                    est_abonne=vip, 
                    est_super_abonne=vip, 
                    nom_client=nom,
                    ticket_id=partie_ticket,
                    place_id=partie_place
                )
                
            except Exception as e: 
                self.log_message(f"ENTRÉE OK (Erreur affichage): {res}")
        else:
            self.log_message(f"REFUS D'ENTRÉE: {res}")
        
        self.rafraichir_vue()
        self.update_trend_monitor("ENTREE")

    def action_sortir(self):
        if not self.selected_place_id: return
        d = self.db_places[self.selected_place_id]
        
        res = self.acces.reprendreVoiture(d["client"], d["ticket"])
        
        if "revoir" in res or "payé" in res or "BIENTÔT" in res:
            self.db.liberer_place(self.selected_place_id)
            
           # ENREGISTREMENT COMPLET SORTIE
            self.historique.enregistrer_sortie(
                imma=d["voiture"].immatriculation,
                date=datetime.datetime.now(),
                est_abonne=d["client"].estAbonne, 
                est_super_abonne=d["client"].estSuperAbonne,
                ticket_id=d["ticket"],
                place_id=self.selected_place_id,
                nom_client=d["client"].nom
            )

            del self.db_places[self.selected_place_id]
            self.update_trend_monitor("SORTIE") 

            if d["client"].estSuperAbonne :
                self.log_message(f"★ SORTIE VIP ★: {res}")
                self.selected_place_id = None
            else : 
                self.log_message(f"SORTIE: {res}")
                self.selected_place_id = None
        else:
            self.log_message(f"ERREUR SORTIE: {res}")
        
        self.rafraichir_vue()

    def action_maintenance(self):
        if not self.selected_place_id: return
        d = self.db_places[self.selected_place_id]
        
        if d.get("statut") == "MAINTENANCE":
            d["statut"] = "STATIONNÉ"
            self.log_message(f"FIN MAINTENANCE: Véhicule prêt sur place {self.selected_place_id}")
        else:
            try:
                m = Maintenance(datetime.date.today(), datetime.date.today(), "Maintenance demandée via Interface")
                m.effectuerMaintenance(d["voiture"], self.parking, d["client"])
                d["statut"] = "MAINTENANCE"
                self.log_message(f"DÉBUT MAINTENANCE: {d['voiture'].immatriculation}")
                
                # ENREGISTREMENT MANUEL (Car Parking Muet)
                self.historique.enregistrer_service(
                    imma=d["voiture"].immatriculation,
                    date=datetime.datetime.now(),
                    type_service="maintenance",
                    est_abonne=d["client"].estAbonne,
                    est_super_abonne=d["client"].estSuperAbonne,
                    nom_client=d["client"].nom,
                    place_id=self.selected_place_id
                )
                
            except Exception as e: 
                self.log_message(f"Erreur Maintenance: {e}")
        
        self.rafraichir_vue()
        self.update_trend_monitor("STABLE") 

    def action_livraison(self):
        if not self.selected_place_id: return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Livraison")
        dialog.geometry("350x200")
        dialog.attributes("-topmost", True)
        
        ctk.CTkLabel(dialog, text="Adresse de livraison :", font=("Arial", 14)).pack(pady=(20, 5))
        
        entry_adresse = ctk.CTkEntry(dialog, width=250)
        entry_adresse.pack(pady=5)
        
        def valider():
            adresse = entry_adresse.get()
            if adresse:
                self._confirmer_livraison(adresse)
                dialog.destroy()
            else:
                messagebox.showwarning("Attention", "Veuillez entrer une adresse.")

        ctk.CTkButton(dialog, text="VALIDER LIVRAISON", command=valider, fg_color=COLORS["warning"]).pack(pady=20)

    def _confirmer_livraison(self, adresse):
        d = self.db_places[self.selected_place_id]
        ticket_id = d["ticket"]
        client = d["client"]
        
        try:
            l = Livraison(datetime.date.today(), datetime.date.today(), f"Livraison vers : {adresse}")
            l.effectuerLivraison(self.parking, d["voiture"], client)
            
            # ENREGISTREMENT MANUEL (Car Parking Muet)
            self.historique.enregistrer_service(
                imma=d["voiture"].immatriculation,
                date=datetime.datetime.now(),
                type_service="livraison",
                est_abonne=d["client"].estAbonne,
                est_super_abonne=d["client"].estSuperAbonne,
                nom_client=d["client"].nom,
                place_id=self.selected_place_id
            )
            
            self.acces.reprendreVoiture(client, ticket_id)
            
            # SORTIE AUTOMATIQUE AUSSI
            self.historique.enregistrer_sortie(
                imma=d["voiture"].immatriculation,
                date=datetime.datetime.now(),
                est_abonne=d["client"].estAbonne, 
                est_super_abonne=d["client"].estSuperAbonne,
                ticket_id=d["ticket"],
                place_id=self.selected_place_id
            )
            
            self.db.liberer_place(self.selected_place_id)
            del self.db_places[self.selected_place_id]
            
            if client.estSuperAbonne:
                self.log_message(f"★ SERVICE VOITURIER PRESTIGE ★")
                self.log_message(f"Destination VIP : {adresse}")
                self.log_message(f"Votre vehicule (Ticket {ticket_id}) est en route avec priorité absolue.")
            else:
                self.log_message(f"SERVICE LIVRAISON STANDARD")
                self.log_message(f"Destination : {adresse}")
                self.log_message(f"Ticket {ticket_id} validé. Le voiturier prend en charge le véhicule.")
            
            self.selected_place_id = None
            
        except Exception as e: 
            self.log_message(f"Erreur Livraison: {e}")
        
        self.rafraichir_vue()
        self.update_trend_monitor("SORTIE")
    
    def action_entretien(self):
        if not self.selected_place_id: return
        d = self.db_places[self.selected_place_id]
        
        if d.get("statut") == "ENTRETIEN":
            d["statut"] = "STATIONNÉ"
            self.log_message(f"FIN LAVAGE: Véhicule propre sur place {self.selected_place_id}")
        else:
            try:
                e = Entretien(datetime.date.today(), datetime.date.today(), "Lavage complet")
                
                if hasattr(e, 'effectuerEntretien'):
                    e.effectuerEntretien(self.parking, d["voiture"], d["client"])
                else:
                   pass

                d["statut"] = "ENTRETIEN"
                self.log_message(f"DÉBUT ENTRETIEN: Lavage en cours pour {d['voiture'].immatriculation}...")
                
                # ENREGISTREMENT MANUEL
                self.historique.enregistrer_service(
                    imma=d["voiture"].immatriculation,
                    date=datetime.datetime.now(),
                    type_service="entretien",
                    est_abonne=d["client"].estAbonne,
                    est_super_abonne=d["client"].estSuperAbonne,
                    nom_client=d["client"].nom,
                    place_id=self.selected_place_id
                )
                
            except Exception as err: 
                self.log_message(f"Erreur Entretien: {err}")
        
        self.rafraichir_vue()
        self.update_trend_monitor("STABLE")

if __name__ == "__main__":
    app = ParkingEnterpriseGUI()
    app.mainloop()