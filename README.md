# Robert Ruidisch — Portfolio Website

Signal Processing & Machine Learning Engineer — Open Source Contributions Portfolio.

## 🚀 Deployment auf GitHub Pages

### 1. Repository erstellen

Erstelle ein Repository auf GitHub mit dem Namen **`robrui.github.io`** (privat oder öffentlich).

### 2. Dateien pushen

```bash
# Repository klonen
git clone https://github.com/robrui/robrui.github.io.git
cd robrui.github.io

# Website-Dateien kopieren
cp /pfad/zu/index.html .
cp /pfad/zu/contributions.json .

# Pushen
git add .
git commit -m "Initial portfolio website"
git push origin main
```

### 3. GitHub Pages aktivieren

1. Gehe zu den Repository-Einstellungen (Settings)
2. Links: **Pages**
3. Source: **Deploy from a branch**
4. Branch: `main`, Ordner: `/ (root)`
5. Speichern

Nach ~2 Minuten ist die Website live unter **https://robrui.github.io**

### 4. Eigene Domain (optional)

- Unter Settings → Pages → Custom domain eintragen
- CNAME/DNS-Eintrag beim Domain-Provider setzen

## 📁 Dateien

| Datei | Beschreibung |
|-------|-------------|
| `index.html` | **Single-File-Website** — Enthält HTML, CSS und JS |
| `contributions.json` | Datenquelle (Kopie, für Debugging/API) |
| `README.md` | Diese Datei |

## 🧩 Features

- **Single Page App** — Kein Framework, keine Dependencies
- **Dark Theme** — Modernes Dev-Portfolio mit Blau-Akzent
- **Learning Curve** — Visuelle Lernprogression von Beginner → Advanced
- **Live PR Status** — GitHub API fetch() für OPEN/MERGED/CLOSED Badges
- **Skills Radar** — Canvas-basierte Visualisierung der Kompetenzen
- **Blog Posts** — Expandierbare Markdown-Blog-Artikel zu jedem PR
- **Responsive** — Desktop, Tablet, Mobile
- **Kein Build System** — Einfach `index.html` öffnen

## 🔧 Lokal testen

Einfach `index.html` im Browser öffnen — geht sofort, kein Server nötig.

Für die Live-PR-Status-Funktion muss die Seite über `http://` oder `https://` geöffnet sein (nicht `file://`), da die GitHub API CORS erfordert. Am einfachsten:

```bash
python3 -m http.server 8000
# Öffne http://localhost:8000
```
