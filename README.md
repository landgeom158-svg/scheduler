# 🐱 Cat — Premium iOS Dark Interactive Scheduler

Cat is a state-of-the-art, high-fidelity scheduling SaaS platform dashboard designed with a **Premium iOS Dark** aesthetic. It showcases a modern calendar client booking flow, live dashboard analytics, drag-and-drop simulated scheduler, and flexible meeting-type creators.

Built entirely using **Vanilla HTML, CSS, and modern ES6 JavaScript Modules**, this project highlights how rich visual interactions, micro-animations, glassmorphic UI elements, and glowing neon accents can create a top-tier user experience without heavy framework overhead.

---

## ✨ Features & Modules

### 1. 📊 SaaS Analytics Hub
- **Dynamic Charting**: Gradient charts (Line chart and Donut breakdown) drawn dynamically on HTML5 Canvas.
- **KPI Metrics**: Glancing KPIs (Active Links, Scheduled Meetings, Booking Rate, Completion Score) with micro-pulsing indicators.
- **Activity Feed**: Interactive notification ticker showing real-time booking actions.

### 2. 📅 Interactive Weekly Scheduler
- **Custom Grid**: Custom-built 12-hour weekly calendar view.
- **Interactive Slots**: Click-to-create meeting slot interface.
- **Drag-and-Drop & Resizing Sim**: Drag slots or adjust duration dynamically.
- **Timezone Selector**: Real-time timezone shifts adjusting scheduler indexes.

### 3. ⚙️ Meeting Link Builder
- **Meeting Configurations**: Create, modify, or delete custom scheduling pages (e.g., "15m Catchup", "30m Demo", "60m Deep Dive").
- **Dynamic Customizer**: Choose locations (Google Meet, Zoom, Phone, In-person), descriptions, custom card glow accents, and durations.

### 4. 🔗 Booking Simulator (Client Flow)
- **Live Simulator**: A side-by-side split screen showing exactly what the client sees when accessing your Cat link.
- **Booking Steps**:
  1. Select a meeting type.
  2. Date picking (interactive calendar calendar widgets).
  3. Time slot selection (smart filters checking for conflicts).
  4. Client details form (Name, Email, Notes).
  5. Booking confirmation with sleek micro-animations.

---

## 🎨 Design System & Visuals

- **Theme**: Premium Dark (Obsidian Black, Deep Slate, with Indigo & Purple glow accents).
- **Glassmorphism**: Backdrop blur filters, 1px border highlights, and subtle background linear gradients simulating light catching the edges of card elements.
- **Animations**: CSS custom timing curves, spring effects, active click physics, and fade-in router transits.
- **Typography**: "Outfit" (Headings) & "Plus Jakarta Sans" (Body) imported via Google Fonts.
- **Icons**: Lucide Icons loaded via CDN.

---

## 🚀 How to Run Locally

Since this app uses native ES6 JavaScript modules, it needs to be served using a local development server to avoid CORS issues with `file://` protocols.

### Option 1: Using Node (npx)
Simply run the following command in this directory:
```bash
npx serve .
```

### Option 2: Live Server (VS Code Extension)
Right-click on `index.html` and select **"Open with Live Server"**.

### Option 3: Python HTTP Server
Run this from your terminal:
```bash
python -m http.server 8000
```
Then navigate to `http://localhost:8000`.

---

## 📂 Project Structure

```text
chronosflow/
├── index.html        # Main template containing layout grid and router containers
├── styles.css        # Modular CSS custom properties, glass effects, animations
├── README.md         # This repository guide
└── js/
    ├── app.js        # Bootstrapper & router controller
    ├── state.js      # Global reactive state store
    ├── dashboard.js  # Analytics, charts, and activity feeds
    ├── calendar.js   # Interactive calendar grid renderer
    ├── booking.js    # Client-facing scheduling flow simulator
    └── meetingTypes.js # CRUD meeting template builder
```
