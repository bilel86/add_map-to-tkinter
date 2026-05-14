import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tkintermapview
import requests
import threading


# ── Couleurs (charte Rose de Kairouan) ─────────────────────────────────────
C_BG        = "#1A1A1A"
C_SIDEBAR   = "#2A2A2A"
C_ROSE      = "#D63384"
C_ROSE_DARK = "#A8256A"
C_WHITE     = "#FFFFFF"
C_LIGHT     = "#F0F0F0"
C_GRAY      = "#555555"
C_ENTRY_BG  = "#3A3A3A"

KAIROUAN_LAT = 35.6781
KAIROUAN_LON = 10.0963

TILE_SERVERS = {
    "OpenStreetMap":       "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
    "Satellite (ESRI)":    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    "OpenTopoMap":         "https://tile.opentopomap.org/{z}/{x}/{y}.png",
    "CartoDB Dark":        "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
}

LIEUX_KAIROUAN = [
    ("Grande Mosquée de Kairouan", 35.6814, 10.0966),
    ("Médina de Kairouan",         35.6781, 10.0963),
    ("Bassin des Aghlabides",      35.6895, 10.0938),
    ("Bir Barouta",                35.6792, 10.0972),
    ("Musée de Kairouan",          35.6772, 10.0985),
]


class MapApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌹 Carte — Rose de Kairouan")
        self.geometry("1200x750")
        self.minsize(900, 600)
        self.configure(bg=C_BG)

        self.markers = []
        self.search_var  = tk.StringVar()
        self.tile_var    = tk.StringVar(value="OpenStreetMap")
        self.coord_var   = tk.StringVar(value="Lat: —   Lon: —")
        self.status_var  = tk.StringVar(value="Prêt")

        self._build_ui()
        self._add_default_markers()

    # ── Construction UI ──────────────────────────────────────────────────
    def _build_ui(self):
        self._build_sidebar()
        self._build_map_frame()
        self._build_statusbar()

    def _build_sidebar(self):
        sb = tk.Frame(self, bg=C_SIDEBAR, width=260)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # Logo / titre
        header = tk.Frame(sb, bg=C_ROSE, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="🌹", font=("Segoe UI", 28), bg=C_ROSE).pack()
        tk.Label(header, text="Rose de Kairouan",
                 font=("Segoe UI", 11, "bold"), bg=C_ROSE, fg=C_WHITE).pack()
        tk.Label(header, text="Carte Interactive",
                 font=("Segoe UI", 8), bg=C_ROSE, fg="#FFD6EC").pack()

        pad = dict(padx=14, pady=4)

        # ── Recherche ─────────────────────────────────────────────────
        self._section(sb, "🔍  Rechercher un lieu")
        entry_frame = tk.Frame(sb, bg=C_SIDEBAR)
        entry_frame.pack(fill="x", padx=14, pady=(0, 6))
        self.search_entry = tk.Entry(
            entry_frame, textvariable=self.search_var,
            bg=C_ENTRY_BG, fg=C_WHITE, insertbackground=C_ROSE,
            relief="flat", font=("Segoe UI", 10), bd=6
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<Return>", lambda e: self._search())
        self._btn(sb, "  Rechercher", self._search, icon="🔍")

        # ── Type de carte ──────────────────────────────────────────────
        self._section(sb, "🗺️  Type de carte")
        for name in TILE_SERVERS:
            rb = tk.Radiobutton(
                sb, text=name, variable=self.tile_var, value=name,
                bg=C_SIDEBAR, fg=C_LIGHT, selectcolor=C_BG,
                activebackground=C_SIDEBAR, activeforeground=C_ROSE,
                font=("Segoe UI", 9), command=self._change_tiles,
                cursor="hand2"
            )
            rb.pack(anchor="w", padx=18, pady=1)

        # ── Lieux de Kairouan ─────────────────────────────────────────
        self._section(sb, "📍  Lieux de Kairouan")
        for name, lat, lon in LIEUX_KAIROUAN:
            short = name if len(name) <= 28 else name[:25] + "…"
            btn = tk.Button(
                sb, text=short,
                bg=C_ENTRY_BG, fg=C_LIGHT, relief="flat",
                font=("Segoe UI", 8), anchor="w", cursor="hand2",
                activebackground=C_ROSE, activeforeground=C_WHITE,
                command=lambda la=lat, lo=lon, n=name: self._goto(la, lo, n)
            )
            btn.pack(fill="x", padx=14, pady=2)

        # ── Actions ───────────────────────────────────────────────────
        self._section(sb, "⚙️  Actions")
        self._btn(sb, "  Ajouter un marqueur", self._add_marker_click, icon="📌")
        self._btn(sb, "  Effacer marqueurs",   self._clear_markers,    icon="🗑️")
        self._btn(sb, "  Recentrer Kairouan",  self._recenter,         icon="🏠")

        # ── Coordonnées ───────────────────────────────────────────────
        tk.Label(sb, textvariable=self.coord_var,
                 bg=C_SIDEBAR, fg=C_GRAY, font=("Segoe UI", 8),
                 wraplength=230).pack(side="bottom", pady=6)

    def _build_map_frame(self):
        right = tk.Frame(self, bg=C_BG)
        right.pack(side="left", fill="both", expand=True)

        # Toolbar
        toolbar = tk.Frame(right, bg=C_BG, pady=6)
        toolbar.pack(fill="x", padx=10)
        tk.Label(toolbar, text="Kairouan, Tunisie 🇹🇳",
                 bg=C_BG, fg=C_ROSE, font=("Segoe UI", 11, "bold")).pack(side="left")

        # Zoom buttons
        zoom_f = tk.Frame(toolbar, bg=C_BG)
        zoom_f.pack(side="right")
        tk.Button(zoom_f, text=" + ", command=self._zoom_in,
                  bg=C_ROSE, fg=C_WHITE, relief="flat", font=("Segoe UI", 11, "bold"),
                  cursor="hand2", padx=8).pack(side="left", padx=2)
        tk.Button(zoom_f, text=" − ", command=self._zoom_out,
                  bg=C_ENTRY_BG, fg=C_WHITE, relief="flat", font=("Segoe UI", 11, "bold"),
                  cursor="hand2", padx=8).pack(side="left", padx=2)

        # Map widget
        self.map_widget = tkintermapview.TkinterMapView(
            right, corner_radius=10
        )
        self.map_widget.pack(fill="both", expand=True, padx=10, pady=(0, 0))
        self.map_widget.set_position(KAIROUAN_LAT, KAIROUAN_LON)
        self.map_widget.set_zoom(13)
        self.map_widget.add_left_click_map_command(self._on_map_click)

    def _build_statusbar(self):
        bar = tk.Frame(self, bg="#111111", height=26)
        bar.pack(side="bottom", fill="x")
        bar.pack_propagate(False)
        tk.Label(bar, textvariable=self.status_var,
                 bg="#111111", fg=C_GRAY, font=("Segoe UI", 8),
                 anchor="w", padx=10).pack(side="left", fill="y")
        tk.Label(bar, text="tkintermapview • OpenStreetMap",
                 bg="#111111", fg=C_GRAY, font=("Segoe UI", 8),
                 anchor="e", padx=10).pack(side="right", fill="y")

    # ── Helpers UI ───────────────────────────────────────────────────────
    def _section(self, parent, text):
        tk.Label(parent, text=text,
                 bg=C_SIDEBAR, fg=C_ROSE,
                 font=("Segoe UI", 9, "bold"),
                 anchor="w").pack(fill="x", padx=14, pady=(12, 2))

    def _btn(self, parent, text, cmd, icon=""):
        tk.Button(
            parent, text=text,
            bg=C_ROSE, fg=C_WHITE, relief="flat",
            font=("Segoe UI", 9, "bold"), cursor="hand2",
            activebackground=C_ROSE_DARK, activeforeground=C_WHITE,
            command=cmd, pady=5
        ).pack(fill="x", padx=14, pady=3)

    # ── Logique ──────────────────────────────────────────────────────────
    def _add_default_markers(self):
        for name, lat, lon in LIEUX_KAIROUAN:
            m = self.map_widget.set_marker(lat, lon, text=name,
                                           marker_color_circle=C_ROSE,
                                           marker_color_outside="#A8256A")
            self.markers.append(m)
        self._set_status(f"{len(LIEUX_KAIROUAN)} marqueurs chargés — Kairouan, Tunisie")

    def _search(self):
        query = self.search_var.get().strip()
        if not query:
            return
        self._set_status(f"Recherche : {query}…")

        def do_search():
            try:
                url = "https://nominatim.openstreetmap.org/search"
                params = {"q": query, "format": "json", "limit": 1}
                headers = {"User-Agent": "MapKairouan/1.0"}
                r = requests.get(url, params=params, headers=headers, timeout=8)
                data = r.json()
                if data:
                    lat = float(data[0]["lat"])
                    lon = float(data[0]["lon"])
                    name = data[0].get("display_name", query)
                    self.after(0, lambda: self._goto(lat, lon, name, zoom=14))
                else:
                    self.after(0, lambda: self._set_status("Lieu introuvable."))
            except Exception as e:
                self.after(0, lambda: self._set_status(f"Erreur réseau : {e}"))

        threading.Thread(target=do_search, daemon=True).start()

    def _goto(self, lat, lon, name="", zoom=15):
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_zoom(zoom)
        short = name[:60] + "…" if len(name) > 60 else name
        self._set_status(f"📍 {short}")
        self.coord_var.set(f"Lat: {lat:.5f}   Lon: {lon:.5f}")

    def _change_tiles(self):
        url = TILE_SERVERS[self.tile_var.get()]
        self.map_widget.set_tile_server(url, max_zoom=22)
        self._set_status(f"Carte : {self.tile_var.get()}")

    def _on_map_click(self, coords):
        lat, lon = coords
        self.coord_var.set(f"Lat: {lat:.5f}   Lon: {lon:.5f}")

    def _add_marker_click(self):
        name = simpledialog.askstring("Marqueur", "Nom du marqueur :",
                                      parent=self)
        if name:
            pos = self.map_widget.get_position()
            lat, lon = pos[0], pos[1]
            m = self.map_widget.set_marker(lat, lon, text=name,
                                           marker_color_circle=C_ROSE,
                                           marker_color_outside=C_ROSE_DARK)
            self.markers.append(m)
            self._set_status(f"Marqueur ajouté : {name}")

    def _clear_markers(self):
        for m in self.markers:
            m.delete()
        self.markers.clear()
        self._set_status("Marqueurs effacés.")

    def _recenter(self):
        self._goto(KAIROUAN_LAT, KAIROUAN_LON, "Kairouan, Tunisie", zoom=13)

    def _zoom_in(self):
        self.map_widget.set_zoom(min(self.map_widget.zoom + 1, 22))

    def _zoom_out(self):
        self.map_widget.set_zoom(max(self.map_widget.zoom - 1, 1))

    def _set_status(self, msg):
        self.status_var.set(msg)


if __name__ == "__main__":
    app = MapApp()
    app.mainloop()
