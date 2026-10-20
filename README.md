# Cosmic Origins Adventure

A fun choose-your-own-adventure science simulation covering 13.8 billion years of cosmic history — from the Big Bang to the formation of your own world. 

**Python · Streamlit · OpenAI-compatible LLM API (K2-Think-v2) · HTML5 Canvas · SVG · pytest**

<!-- Add once deployed: **[Live demo](https://your-app.streamlit.app)** -->
<!-- Add a screenshot or GIF: ![Cosmic Origins demo](docs/demo.gif) -->

**Highlights**
- A physics-based world model: energy-balance surface temperature, star-specific habitable zones, and a habitability score built from water, atmosphere, magnetic field, geology, and impact history.
- 5 journey types × 8 cosmic stages, each with a procedurally drawn canvas animation and an SVG cross-section of the final world.
- LLM-generated world names, lore, and stories, with prompt and output-parsing logic that strips the model's visible reasoning, plus offline fallback text so the app works without an API key.
- Unit tests covering the physics and scoring model.

---

## What It Does

You pick a **journey type** (the kind of world you want to build), then make choices at **8 cosmic stages**. Each choice steers your world's evolution and affects its final habitability score. At the end, an AI (K2-Think-v2) names your world, writes its lore, describes its conditions, and generates a speculative story about what life — or the absence of it — might look like there.

---

## Journey Types

| Journey | What You're Building |
|---|---|
| Rocky Planet | A dense, silicate world like Earth or Mars |
| Gas Giant | A massive hydrogen/helium world like Jupiter |
| Icy Moon | A frozen moon with a subsurface ocean like Europa |
| Earth-like World | A blue world optimized for life |
| Star System | An entire multi-planet system |

---

## The 8 Cosmic Stages

| Stage | Concept Covered |
|---|---|
| 1. The Big Bang | Expansion of space, no center, uniform origin |
| 2. Big Bang Nucleosynthesis | H and He formation, temperature-driven particle physics |
| 3. First Stars (Pop III) | Metal-free stars, explosive deaths, first heavy elements |
| 4. Supernovae & Heavy Elements | Carbon, oxygen, iron forged and scattered |
| 5. Galaxy Formation | Dark matter scaffolding, disk vs. elliptical galaxies |
| 6. Solar Nebula | Angular momentum, frost line, rocky vs. icy material |
| 7. Planet Accretion | Runaway growth, differentiation, core formation |
| 8. Planetary Evolution | Atmosphere, oceans, magnetic field, plate tectonics |

At each stage you read a narrative written from the perspective of a particle or atom in your journey, see an animated canvas visualization, view the causal chain of events, and make a choice that affects your world's outcome.

---

## Inputs

| Input | What It Does |
|---|---|
| **Journey type** (home screen) | Sets the category of world you are building |
| **Stage choices** (one per stage) | Steers physical properties — distance, composition, evolution path |

The number of planets generated (for the Star System journey) depends on user choices at the accretion stage, not a fixed number.

---

## Outputs & Result Page

When all 8 stages are complete, the result page shows:

| Section | Content |
|---|---|
| **World name + lore** | K2-generated unique name and 2–3 sentence origin story |
| **Habitability label + score** | 0–100 score with label (Uninhabitable → Life Confirmed) |
| **Cross-section SVG** | Layered diagram: core, mantle, crust, atmosphere |
| **Properties** | Star type, distance, temperature, water, atmosphere, magnetic field |
| **AI description** | K2 narrative of the world's conditions |
| **Factor breakdown** | Bar chart of each habitability factor and its point contribution |
| **Cosmic Story** | Speculative K2 scenario — what could happen on this world |

---

## AI Usage

K2-Think-v2 is used **only on the result page** for three tasks:

1. **World naming** — generates a unique planet name and 2-sentence lore
2. **Result narrative** — describes the world's conditions
3. **Cosmic Story** — speculative scenario based on the world's real properties

Stage narrations (the "you are a hydrogen atom…" text at each stage) are pre-written static text, not AI-generated, to ensure instant load and scientific accuracy.

---

## Habitability Score

Computed from the world's physical properties at the end of stage 8 (rocky and Earth-like journeys; capped at 0–100):

| Factor | Points |
|---|---|
| Temperature in liquid-water range (−20 to 65 °C; partial credit −60 to 100 °C) | up to +30 |
| Water (ice → abundant) | up to +25 |
| Atmosphere (thin or thick best; runaway greenhouse penalised) | up to +20 |
| Magnetic field | up to +15 |
| Geological activity | up to +15 |
| Impact history (calm +5, heavy −15) | −15 to +5 |
| Large stabilising moon | +5 |

Gas giants, icy moons, and star systems use their own scoring (moon systems, tidal heating, star stability, etc.) — see `cosmic_origins/simulation.py`. An Earth-like world reaches **"Life Confirmed"** only if it matches Earth on every key property simultaneously.

---

## Setup & Running

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Add your API key to .env.local — without it, the app uses built-in fallback text
#    K2_API_KEY=your-key-here
#    K2_MODEL=MBZUAI-IFM/K2-Think-v2

# 4. Run
streamlit run app.py
```

The app opens at `http://localhost:8501`.

### Running tests

```bash
pip install -r requirements-dev.txt
pytest
```

---

## File Structure

```
cosmic-origins-simulator/
├── app.py                  # Streamlit entry point: UI, routing, result page
├── cosmic_origins/
│   ├── simulation.py       # World model: temperature, habitable zones, habitability scoring
│   ├── story.py            # Journeys, stage definitions, pre-written narratives, choices
│   ├── visuals.py          # HTML5 canvas animations and SVG cross-section diagrams
│   └── ai.py               # K2-Think-v2 calls, reasoning-stripping parser, fallbacks
├── tests/
│   └── test_simulation.py  # Physics and scoring tests
├── requirements.txt
├── requirements-dev.txt
└── .env.local              # API key (not committed)
```
