Here is a comprehensive summary of the design language developed and refined throughout our session. You can copy and save this section for future reference or reuse in prompt instructions.

---

## 🎨 FocusLink 2026 Material UI — Design Language Specification

### 1. Core Philosophy & Theme

* **Theme Concept:** Light, 2026-styled Material UI Dashboard. Clean, energetic, and colorful while maintaining high-density operational visual hierarchy.
* **Device Identity:** The IoT device is always branded as **"FocusLink Hardware"** powered by ESP32 microcontrollers and Blynk IoT sync.
* **Gamification Archetype:** 6-Tier Butterfly Metamorphosis System ($1\text{ Minute Focused} = 10\text{ XP}$).
1. **Egg** ($0\text{ XP}$)
2. **Larva** ($5,000\text{ XP}$)
3. **Caterpillar** ($20,000\text{ XP}$)
4. **Chrysalis** ($40,000\text{ XP}$)
5. **Butterfly** ($100,000\text{ XP}$)
6. **Golden Butterfly** ($200,000\text{ XP}$)



---

### 2. Color Palette & Enterprise Accents

All colors are solid material tones (strict avoidance of loud background gradients):

| Role | Color Name | Hex Code | Usage |
| --- | --- | --- | --- |
| **Primary Accent** | Enterprise Blue | `#2563eb` | Main brand elements, active states, icons |
| **Deep Base** | Deep Indigo | `#1e1b4b` | Featured dark cards, contrast headers, identity blocks |
| **Electric Accent** | Electric Sky Blue | `#38bdf8` | Live telemetry highlights, dark card borders, badges |
| **App Background** | Soft Slate Slate | `#f8fafc` | Page background |
| **Surface/Card** | Pure White | `#ffffff` | Content containers, structured split-view cards |
| **Text Primary** | Dark Slate | `#0f172a` | Main headings and bold numeric data |
| **Text Secondary** | Muted Grey | `#64748b` | Subtitles, labels, and secondary indicators |
| **Success / Clean** | Emerald Green | `#16a34a` / `#dcfce7` | Completed sessions, online status, clean runs |
| **Danger / Abort** | Crimson Red | `#dc2626` / `#fee2e2` | Aborted sessions, offline warnings, cut runs |
| **Interactive Glow** | Indigo Glow | `#6366f1` / `#eef2ff` | Top Navigation bar pill-style hover/active tabs |

---

### 3. Typography & Icons

* **Font Family:** `Google Sans`, `-apple-system`, `BlinkMacSystemFont`, `sans-serif` (loaded directly via Google Fonts).
* **Font Weights:**
* **900 (`fw-black`):** Large numeric data counters, hero titles.
* **700 (`fw-bold`):** Card titles, navigation tabs, section headers.
* **500/600 (`fw-medium` / `font-semibold`):** Micro-labels, badge text.


* **Monospace Font:** Used for hardware device IDs, raw timestamps, and UTC tags.
* **Icons:** Bootstrap Icons (`bi-*`) paired alongside every metric, status indicator, or action button for visual cues.

---

### 4. Layout Architecture & Screen Real-Estate

* **Container Width:** Strictly **80% screen real-estate** (`width: 80% !important; max-width: 80% !important; margin: 0 auto;`), sharp and centered for desktop viewports.
* **Top Navigation Bar:**
* Positioned **sticky-top** with a glassmorphism effect (`background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px);`).
* **Left Side:** FocusLink Logo + App Links (`Dashboard`, `Device Status`, `Timeline Archive`).
* **Right Side:** Red-tinted Logout Button (`.btn-logout-custom`).


* **Card Design Pattern:** Clean split-view card grid (`.row.g-4` / `.row.g-3`).
* 16px corner radiuses (`.rounded-4`).
* Crisp, light subtle borders (`border: 1px solid #e2e8f0`).
* Subtle elevation shadows (`.shadow-sm`).



---

### 5. UI/UX Rules & Code Principles

1. **Bootstrap-First Inline Styling:** Page-specific styling uses inline CSS to prevent template clashes and eliminate external CSS bundle overhead.
2. **Interactive Telemetry Elements:**

* Live status spinners and pulsing badges for live hardware state.
* Meaningful action buttons (e.g., *"Fetch Live Stream"*, *"Refresh Telemetry"*, *"Refresh Archive"*).
* Smooth Chart.js visual gauges (doughnut charts) for completion/abortion ratios.

3. **Data Humanization:** Raw UTC timestamps are parsed into clean date/time formats alongside micro-badges for readability.