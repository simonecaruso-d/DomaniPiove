# DomaniPiove

DomaniPiove is an end-to-end weather intelligence product built to answer one concrete user question:

"Can I plan quality time outside in the next days, with confidence?"

Instead of showing a single forecast source, the app compares multiple providers, weights their reliability, and translates weather signals into actionable decisions for real people.

---

## Why this project matters

### User value
- Reduces uncertainty in daily planning (work, travel, events, leisure).
- Converts raw weather metrics into decision-ready guidance ("can I go out?" + why).
- Improves trust by exposing forecast accuracy, not only forecast values.

### Business value
- Demonstrates how to build a data product that combines ingestion, quality, analytics, and UX.
- Can be adapted for verticals where weather impacts operations: mobility, tourism, events, retail footfall, field services.
- Shows a practical foundation for monetizable features: premium city coverage, alerts, API, white-label dashboards.

---

## What I built

### 1) Multi-provider weather data pipeline
- Fetches forecasts from Open-Meteo, Met Norway, Visual Crossing, Bright Sky.
- Fetches historical actuals (Open-Meteo Archive) to evaluate prediction quality.
- Normalizes records and writes to Supabase with robust retry logic.
- Implements SCD-like update behavior for forecast history.

### 2) Accuracy engine
- Computes MAE and MAPE across meteorological metrics.
- Buckets forecast lead time into day spans: 1, 2, 3, 5, 7, 10, 15 days.
- Produces provider-level and day-span-level reliability tables used by the app.

### 3) Interactive Streamlit product
- **Home**: storytelling, geographic coverage map, visual context.
- **Previsioni**: advanced filters, weighted forecast chart, "Posso uscire?" score table, AI concierge for suggestions.
- **Accuratezza**: radar comparison and best/worst provider summaries.

### 4) Operational automation
- GitHub Actions schedules morning data refresh and evening accuracy refresh.
- Timezone-aware gates (Europe/Rome) to run at business-relevant local times.

### 5) Product analytics instrumentation
- Added visit/page tracking to Supabase (`visit_start`, `page_view`).
- Enables usage monitoring and conversion/funnel analysis for product decisions.

---

## Technical highlights

- **Architecture**: modular Python codebase (`weather`, `accuracy`, `db`, `app`, `configuration`).
- **Data layer**: Supabase Postgres + typed table contracts in SQL DDL.
- **Resilience**: retry + exponential backoff on external/API/DB operations.
- **Performance**: cached reads, concurrent table loading, paginated reads/writes.
- **UX engineering**: custom Streamlit layout, dynamic visual components, clear interaction flow.
- **AI integration**: OpenRouter-backed assistant embedded in a real user journey.

---