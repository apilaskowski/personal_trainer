# Personal Trainer — Hevy Smart Guidance

An intelligent, low-friction mobile dashboard connected to your **Hevy Pro** workout logs. It tracks muscle recovery and volume trends to answer one simple question before every session: **"What should I train today?"**

Hosted 100% read-only on GitHub Pages. Zero servers, zero host computer exposure, and zero maintenance.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph Cloud["1. External Data Source"]
        A["Hevy Pro API\n(api.hevyapp.com/v1/workouts)"]
    end

    subgraph CI["2. GitHub Actions Automation"]
        B["Scheduled Cron (Daily 5:00 UTC)"]
        C["Python Engine\n(HEVY_API_KEY)"]
        B --> C
        A --> C
        C --> D["48h Muscle Recovery Math"]
        C --> E["Rolling 7d/14d Volume Deficit"]
        D & E --> F["Build Static Site (public/data.json)"]
    end

    subgraph Hosting["3. Read-Only Hosting & Mobile UX"]
        F --> G["Deploy to GitHub Pages (gh-pages)"]
        G --> H["📱 Mobile PWA / Web App\n(Light Theme • Zero Login Friction)"]
    end
```

---

## 🧠 Core Engine & Logic Specification

### 1. Independent 48-Hour Muscle Recovery Model
* **No rigid workout splits**: You train on "vibes" and energy levels, but each muscle group tracks its own recovery clock.
* **Granular muscle tracking**:
  * **Lower Body**: Quads, Hamstrings, Glutes, Calves.
  * **Upper Body**: Chest, Back (Lats & Upper Back), Shoulders (Front/Side/Rear).
  * **Arms & Core**: Biceps, Triceps, Abs/Core.
* **Recovery States**:
  * 🟢 **Ready** ($\ge 48$ hours rested): Muscle has fully supercompensated and is primed for training.
  * 🟡 **Recovering** ($24 - 48$ hours rested): Intermediate recovery.
  * 🔴 **Resting** ($< 24$ hours rested): Recently trained; needs full rest.
* *Example scenario*: If you train Quads on Monday but skip Hamstrings, on Tuesday Hamstrings remain 🟢 **Ready**, while Quads go into 🔴 **Resting**.

### 2. Rolling Volume Windows (7 & 14 Days)
* Instead of resetting on arbitrary calendar Mondays, volume is evaluated on a **rolling 7-day window** (with a secondary 14-day window for long-term trend analysis).
* **Volume Deficit**:
  $$\text{Deficit} = \max(0, \text{Weekly Target Sets} - \text{Completed Sets in Last 7 Days})$$

### 3. "What to Train Today" Priority Algorithm
1. **Filter**: Identify all muscles currently in the 🟢 **Ready** state ($\ge 48$h rest).
2. **Sort**: Rank ready muscles by their **Volume Deficit** (highest deficit = highest priority).
3. **Recommend**: Output the top 2–4 priority muscles as **"Today's Focus"**.

---

## 🎨 UI/UX Design (Light Theme)

* **Design Aesthetic**: Minimalist, clean, high-contrast light theme (Apple Health & Linear inspired).
* **Palette**:
  * Background: Pure white & soft slate (`#f8fafc`).
  * Typography: Crisp deep navy/slate (`#0f172a`).
  * Badges: Vibrant green (`#10b981`), amber (`#f59e0b`), and blue accents.
* **Key Screen Sections**:
  1. **Top Recommendation Hero Card**: Clear headline (e.g. *"Today's Focus: Hamstrings, Back, Shoulders"*).
  2. **View Toggle**: Quick switch between **7-Day Rolling** and **14-Day View**.
  3. **Muscle Readiness & Goal Grid**: Individual cards showing last trained timestamp, recovery status, and set progress bar.
  4. **Recent Workouts Log**: Clean breakdown of recent Hevy sessions.

---

## 🗺️ Phased Implementation Roadmap

To ensure high code quality and clear review checkpoints, development is broken down into 5 focused steps:

- [x] **Step 1: Architecture & Design Specification** *(This PR)*  
  Document system architecture, recovery math, data models, and UI wireframes.
- [ ] **Step 2: Hevy API Client & Exercise Mapping**  
  Implement `src/hevy_client.py` with pagination, error handling, muscle taxonomy, and offline mock support.
- [ ] **Step 3: Recovery & Recommendation Engine**  
  Implement `src/analyzer.py` with unit tests for 48h recovery calculations and rolling set volume.
- [ ] **Step 4: Mobile-First Light Theme Web App**  
  Build `public/index.html`, `style.css`, and `app.js` with responsive layout and PWA support.
- [ ] **Step 5: GitHub Actions Daily Sync & GitHub Pages Deployment**  
  Configure `.github/workflows/sync-and-deploy.yml` with scheduled cron and automatic deployment.
