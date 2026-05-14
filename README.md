<div align="center">

# 🗺️ Add Map to Tkinter
### Carte Interactive avec tkintermapview — Rose de Kairouan 🌹

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![tkinter](https://img.shields.io/badge/tkinter-builtin-informational?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)
[![OpenStreetMap](https://img.shields.io/badge/OpenStreetMap-tiles-7EBC6F?style=for-the-badge&logo=openstreetmap&logoColor=white)](https://www.openstreetmap.org/)
[![License](https://img.shields.io/badge/licence-MIT-D63384?style=for-the-badge)](LICENSE)

</div>

---

## 📋 Description

Application Python **Tkinter** intégrant une carte interactive basée sur **OpenStreetMap** via la bibliothèque `tkintermapview`.  
Centrée sur **Kairouan, Tunisie** avec les principaux sites touristiques marqués.

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| 🗺️ **Carte interactive** | Affichage OpenStreetMap, zoom, déplacement |
| 🔍 **Recherche de lieu** | Géocodage via Nominatim (OpenStreetMap API) |
| 📍 **Marqueurs** | 5 lieux de Kairouan préchargés + ajout manuel |
| 🛰️ **Types de carte** | OSM, Satellite ESRI, OpenTopoMap, CartoDB Dark |
| ➕ **Zoom** | Boutons + / − dans l'interface |
| 🗑️ **Gestion marqueurs** | Effacer, ajouter à la position courante |
| 📐 **Coordonnées** | Affichage lat/lon au clic sur la carte |

---

## 🗺️ Lieux préchargés — Kairouan

- 🕌 Grande Mosquée de Kairouan
- 🏘️ Médina de Kairouan
- 💧 Bassin des Aghlabides
- 🪣 Bir Barouta
- 🏛️ Musée de Kairouan

---

## 🚀 Installation & Lancement

```bash
# 1. Cloner
git clone https://github.com/bilel86/add_map-to-tkinter.git
cd add_map-to-tkinter

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer
python map_app.py
```

---

## 📦 Dépendances

| Package | Rôle |
|---|---|
| `tkintermapview` | Widget carte pour Tkinter |
| `requests` | Appels API Nominatim (recherche) |
| `pillow` | Rendu des tuiles de carte |

---

## 🖥️ Aperçu de l'interface

```
┌─────────────────────────────────────────────────────┐
│  🌹 Rose de Kairouan        Kairouan, Tunisie 🇹🇳  [+] [-] │
├──────────────┬──────────────────────────────────────┤
│  🔍 Recherche│                                      │
│  [__________]│                                      │
│              │         🗺️  CARTE INTERACTIVE        │
│  🗺️ Type carte│              OpenStreetMap           │
│  ○ OSM       │                                      │
│  ○ Satellite │       📍 Kairouan                    │
│  ○ Topo      │                                      │
│  ○ Dark      │                                      │
│              │                                      │
│  📍 Lieux    ├──────────────────────────────────────┤
│  [Mosquée]   │ Prêt     tkintermapview • OpenStreet │
│  [Médina ]   └──────────────────────────────────────┘
└──────────────┘
```

---

## 🛠️ Stack technique

- **Python** 3.10+
- **tkinter** — Interface graphique (natif Python)
- **tkintermapview** — Widget carte
- **requests** — Requêtes HTTP / géocodage
- **Nominatim API** — Recherche de lieux (gratuit, OpenStreetMap)

---

## 👤 Auteur

**Bilel Jaouadi** — [@bilel86](https://github.com/bilel86)  
Kairouan, Tunisie 🇹🇳

---

<div align="center">
  <sub>Fait avec ❤️ pour Kairouan 🌹</sub>
</div>
