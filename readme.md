# 📊 STATYX — Sports Intelligence & Referral Network Analytics Platform

> **Full-stack sports betting analytics + referral graph intelligence platform** — combining multi-sport player props research, real-time odds ingestion, graph-theoretic network modelling, Expected Value (+EV) scoring, and multi-provider OAuth authentication into a single unified research surface.

[![Django](https://img.shields.io/badge/Django-5.1.7-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.15.2-ff1709?style=flat-square)](https://www.django-rest-framework.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Vite](https://img.shields.io/badge/Vite-5.x-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev)
[![Render](https://img.shields.io/badge/Deployed-Render.com-46E3B7?style=flat-square)](https://render.com)

---

## 🔗 Quick Links

| Resource | URL |
|---|---|
| 🌐 Live Platform | [statyx.io](https://statyx.io) |
| 🎬 Demo Video | [Google Drive](https://drive.google.com/file/d/1MM9s7fH6XkBgMpIbQMhxkwRXxrmdAb6m/view?usp=sharing) |
| ⚛️ Frontend Repo | [github.com/vk93102/statyx-frontend](https://github.com/vk93102/statyx-frontend) |
| 🐍 Backend Repo | [github.com/vk93102/statyx-Backend](https://github.com/vk93102/statyx-Backend) |

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [System Architecture](#️-system-architecture)
- [Tech Stack](#-tech-stack)
- [Backend — Django Apps Deep Dive](#-backend--django-apps-deep-dive)
- [Frontend — React / TypeScript Architecture](#️-frontend--react--typescript-architecture)
- [Authentication System](#-authentication-system)
- [Graph Analytics Engine](#-graph-analytics-engine)
- [Sports Props & EV Modelling](#-sports-props--ev-modelling)
- [API Design](#-api-design)
- [Database Schema](#️-database-schema)
- [Deployment — Render.com](#-deployment--rendercom)
- [Environment Variables](#-environment-variables)
- [Local Development Setup](#-local-development-setup)

---

## 🌐 Project Overview

Statyx is a dual-purpose intelligence platform built for the **Mercor Challenge** and deployed live at [statyx.io](https://statyx.io). It solves two distinct but architecturally unified problems:

**1. Referral Network Graph Analytics** — A graph-theoretic engine that models user referral networks as directed acyclic graphs (DAGs), computes BFS-based network reach, identifies key influencers via greedy submodular maximisation, simulates growth scenarios with discrete-time modelling, and determines minimum viable bonus thresholds via binary search optimisation.

**2. Multi-Sport Props Intelligence** — An NBA, NFL, and Soccer player props research hub aggregating real-time fixture data, computing historical hit-rates with exponential recency decay, grading matchup quality against defensive efficiency rankings, and surfacing positive Expected Value (+EV) prop bets by comparing model probability estimates against sportsbook implied probability.

The system is architected as a **decoupled monorepo** — a Django 5.1 REST API backend (deployed on Render.com) serving a Vite-bundled React 18 / TypeScript SPA frontend over CORS-permissioned HTTPS.

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                             USER LAYER                                        │
│                                                                               │
│                    Browser Client — statyx.io                                 │
│               Vite SPA · React 18 · TypeScript · Redux Toolkit               │
└─────────────────────────────┬────────────────────────────────────────────────┘
                               │  HTTPS + CORS (django-cors-headers)
┌─────────────────────────────▼────────────────────────────────────────────────┐
│                   FRONTEND LAYER  (React / TypeScript SPA)                    │
│                                                                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────────────┐   │
│  │   AUTH VIEWS     │  │  NETWORK DASH    │  │    SPORTS PROPS UI      │   │
│  │                  │  │                  │  │                         │   │
│  │  SignIn/SignUp   │  │  Graph Topology  │  │  NBA · NFL · Soccer     │   │
│  │  OTP Verify     │  │  Influencers     │  │  Fixture List           │   │
│  │  LinkedIn OAuth │  │  Growth Sim      │  │  Odds Tables            │   │
│  │  Google OAuth   │  │  Bonus Optim.    │  │  EV Badges              │   │
│  │  Framer Motion  │  │  Recharts Charts │  │  RTK Query cache        │   │
│  └──────────────────┘  └──────────────────┘  └─────────────────────────┘   │
│                                                                               │
│     Redux Toolkit · RTK Query · React Router v6 · Tailwind · Lucide React   │
└─────────────────────────────┬────────────────────────────────────────────────┘
                               │  REST API  (JSON over HTTPS)
┌─────────────────────────────▼────────────────────────────────────────────────┐
│                  API GATEWAY — Django REST Framework                           │
│                                                                               │
│    django-cors-headers  │  DRF Serializers  │  Session Auth  │  URLconf      │
└──────┬──────────────────┬─────────────────┬──────────────────┬───────────────┘
       │                  │                 │                  │
┌──────▼───────┐  ┌───────▼──────┐  ┌──────▼───────┐  ┌──────▼────────────┐
│authentication│  │    NBA/      │  │NFA_Football/ │  │   create_set/     │
│              │  │              │  │              │  │                   │
│ Twilio OTP  │  │ Fixture ingest│  │ NFL + Soccer │  │ Referral graph    │
│ LinkedIn    │  │ Player props  │  │ Player stats │  │ BFS reach calc    │
│ Google OAuth│  │ DRF ViewSets │  │ Matchup grade│  │ Influencer rank   │
│ Sessions    │  │ Hit-rate calc │  │ Prop registry│  │ Growth simulation │
│ Pillow img  │  │ EV scoring   │  │ BETA module  │  │ Bonus optimise    │
│             │  │ requests HTTP│  │              │  │ Cycle detection   │
└──────┬───────┘  └───────┬──────┘  └──────┬───────┘  └──────┬────────────┘
       └──────────────────┴─────────────────┴─────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────────────────┐
│                              DATA LAYER                                        │
│                                                                               │
│  ┌─────────────────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │     PostgreSQL 15        │  │  External APIs   │  │  Render.com Infra │  │
│  │                         │  │                  │  │                   │  │
│  │  users                  │  │  Sports Data     │  │  Gunicorn WSGI    │  │
│  │  nba_fixtures           │  │  Odds Providers  │  │  WhiteNoise       │  │
│  │  nba_player_props       │  │  Twilio Verify   │  │  render.yaml IaC  │  │
│  │  network_nodes          │  │  LinkedIn API    │  │  Managed Postgres │  │
│  │  network_edges          │  │  Google JWKS     │  │  python-decouple  │  │
│  │  dj-database-url conn.  │  │  requests 2.31   │  │  dj-database-url  │  │
│  └─────────────────────────┘  └──────────────────┘  └───────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Architecture Philosophy

Statyx uses a **thick client, thin server** pattern for sports modules — real-time prop data is fetched and rendered client-side to eliminate server-side latency — while the **graph analytics engine** runs as a hybrid: lightweight BFS/DFS computations execute in the browser (via `utils/graphAlgorithms.js`) while heavier persistence and batch computations live in the Django `create_set` app.

The Django backend is a single **Gunicorn-served WSGI process** on Render.com, keeping infrastructure minimal while WhiteNoise handles compressed static asset delivery without a separate Nginx layer.

---

## 🛠 Tech Stack

### Backend — Python / Django

| Package | Version | Role |
|---|---|---|
| **Django** | 5.1.7 | Core framework — ORM, URLconf, admin, middleware, migration engine, CSRF/XSS protection |
| **djangorestframework** | 3.15.2 | REST API — ModelSerializers, ViewSets, DRF router, session auth, browsable API |
| **django-cors-headers** | 4.4.0 | CORS middleware — injects `Access-Control-Allow-Origin` headers for the decoupled SPA |
| **psycopg2-binary** | ≥ 2.9.7 | PostgreSQL adapter — CPython driver bridging Django ORM to PostgreSQL 15 |
| **twilio** | 9.0.4 | Twilio Verify SDK — SMS OTP dispatch, code lifecycle, fraud detection |
| **python-decouple** | 3.8 | 12-Factor env management — reads `.env` in dev, OS environment in production |
| **dj-database-url** | 2.1.0 | Parses `DATABASE_URL` connection string into Django `DATABASES` dict |
| **gunicorn** | 21.2.0 | Production WSGI HTTP server — multi-process worker pool |
| **whitenoise** | 6.6.0 | Static file serving — Brotli/GZip compression, immutable cache headers, no Nginx needed |
| **requests** | 2.31.0 | HTTP client — server-side calls to sports data APIs, odds providers, Twilio REST |
| **Pillow** | 11.0.0 | Imaging library — avatar upload processing, resize and format conversion |

### Frontend — React / TypeScript

| Package | Version | Role |
|---|---|---|
| **React** | 18 | Concurrent-mode component framework — Suspense, strict mode, concurrent rendering |
| **TypeScript** | 5.x | Strict type safety across all API response models and component props |
| **Vite** | 5.x + SWC | ESM-native build tool — sub-100ms HMR, tree-shaken production bundles |
| **Redux Toolkit** | latest | Normalised global state — `createSlice`, `createAsyncThunk`, immer reducers |
| **RTK Query** | (bundled) | Server state — cache invalidation, request deduplication, background refetch |
| **React Router** | v6 | Nested SPA routing — `/nba-props`, `/nfl-props`, `/analytics`, `/auth` |
| **Recharts** | 2.x | React charting — Bar, Line, Pie charts for hit-rates and network metrics |
| **Framer Motion** | latest | Spring physics animations — staggered reveals, page transitions, skeleton loaders |
| **Tailwind CSS** | 3.x | Utility-first CSS — responsive grid, glassmorphism, dark-mode tokens |
| **Lucide React** | 0.383.0 | SVG icon library — consistent iconography across nav, badges, and actions |

### Infrastructure & Third-Party Services

| Service | Purpose |
|---|---|
| **Render.com** | Backend hosting — Web Service + Managed PostgreSQL, `render.yaml` IaC, auto-deploy on Git push |
| **Twilio Verify** | Phone OTP auth — SMS dispatch, code verification scoped by `TWILIO_VERIFY_SERVICE_SID` |
| **LinkedIn OAuth 2.0** | Professional identity — PKCE flow, callback at `/auth/linkedin/callback.html` |
| **Google OAuth 2.0 / OpenID** | Consumer identity — ID token (JWT) verified against Google JWKS endpoint |
| **PostgreSQL 15** | Primary datastore — managed by Render, connected via `dj-database-url` |

---

## 🐍 Backend — Django Apps Deep Dive

The backend is a Django 5.1 monolith structured into **four domain-specific apps**, each self-contained with its own `models.py`, `serializers.py`, `views.py`, and `urls.py`.

```
statyx-Backend/
├── authentication/       # Identity, OTP, OAuth token exchange
├── NBA/                  # NBA fixtures, player props, hit-rate computation
├── NFA_Football/         # NFL + Soccer props module (BETA)
├── create_set/           # Referral network graph engine
├── tests/                # Unit + integration tests
├── check_db_integrity.py # Pre-start schema integrity gate
├── render.yaml           # Render.com IaC deployment manifest
├── requirements.txt      # Dev dependencies
├── requirements_prod.txt # Production dependencies
├── runtime.txt           # Python version pin for Render.com
└── .env.example          # Environment variable template
```

---

### `authentication/` — Identity & Multi-Provider Auth

Handles all user identity concerns across three independent authentication pathways:

**Twilio OTP Flow:**
- `POST /api/auth/send-otp/` — Calls `twilio.verify.v2.services.verifications.create(to=phone, channel="sms")` via the Twilio SDK
- `POST /api/auth/verify-otp/` — Calls `twilio.verify.v2.services.verification_checks.create(to=phone, code=otp)`, returns `approved` or `pending`, creates Django session on approval

**LinkedIn OAuth 2.0 (PKCE):**
- Frontend redirects to `https://www.linkedin.com/oauth/v2/authorization` with `client_id`, `redirect_uri`, `scope=openid profile email`
- Callback handler POSTs auth code to Django → Django exchanges for access token → fetches profile from `/v2/me` → upserts user → session created

**Google OAuth 2.0 / OpenID Connect:**
- Frontend initiates Google Sign-In popup → Google returns ID token (JWT)
- Token POSTed to Django → Backend verifies signature against Google JWKS endpoint → `sub` claim used as stable identity → user upserted → Django session issued

**Avatar Upload:**
- `POST /api/auth/avatar/` — Multipart upload, Pillow resizes to 256×256 PNG, saves to `MEDIA_ROOT`, path stored in `users.avatar`

---

### `NBA/` — NBA Fixtures, Props & Analytics

Manages the complete NBA props data lifecycle:

- **Fixture Ingestion** — `requests.get()` to sports data provider, normalises into `NBAFixture` Django models
- **Player Props** — `NBAPlayerProp` model per player/fixture/prop type with `line`, `over_odds`, `under_odds`, `ev_score`
- **DRF ViewSets** — `NBAFixtureViewSet` with `?date=YYYY-MM-DD` filter, `NBAPlayerPropsViewSet` nested under fixture
- **Hit-Rate Computation** — `hit_rate_l5`, `hit_rate_l10`, `hit_rate_season` returned in serializer from historical `NBAGameStat` records
- **EV Scoring** — `ev_score = P_model × odds_decimal - 1` computed on `to_representation()`

---

### `NFA_Football/` — NFL & Soccer Props (BETA)

Parallel architecture to the NBA module:

- Sport-specific Django models for `Fixture`, `Player`, `PlayerProp`, `GameStat`
- Prop type registry: Passing (yards, TDs, completions), Rushing (yards, attempts), Receiving (targets, receptions, yards)
- **Matchup Grading** — Composite grade (A+ → F) from opponent defensive rank percentile + last-10 trend + pace adjustment
- BETA status flagged via `"is_beta": true` field in API responses

---

### `create_set/` — Referral Network Graph Engine

The most algorithmically complex module — implements a full directed graph engine backed by Django ORM:

- `NetworkNode` model — wraps a user with `join_date` and `referral_code`
- `NetworkEdge` model — directed edge `(from_node, to_node)` with `UNIQUE(from_node, to_node)` preventing duplicates
- `POST /api/network/add-referral/` — Runs DFS cycle detection before inserting edge
- `GET /api/network/reach/{user_id}/` — BFS from node returning subtree size
- `GET /api/network/influencers/` — Greedy k-selection by unique reach
- `POST /api/network/simulate/` — Discrete-time growth simulation
- `POST /api/network/optimise-bonus/` — Binary search for minimum viable bonus
- `GET /api/network/centrality/` — Flow centrality scores via all-pairs shortest path

---

### `check_db_integrity.py` — Pre-Start Schema Gate

Runs before Gunicorn starts as part of the Render.com build command. Validates that all expected Django app tables exist and have correct column counts — prevents starting with a broken migration state.

---

### `render.yaml` — Infrastructure as Code

```yaml
services:
  - type: web
    name: statyx-backend
    runtime: python
    buildCommand: |
      pip install -r requirements_prod.txt
      python manage.py collectstatic --no-input
      python manage.py migrate
      python check_db_integrity.py
    startCommand: gunicorn neosharx.wsgi:application
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: statyx-postgres
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "False"

databases:
  - name: statyx-postgres
    plan: free
```

---

## ⚛️ Frontend — React / TypeScript Architecture

```
statyx-frontend/
├── src/
│   ├── App.jsx                    # Root component — React Router outlet
│   ├── main.jsx                   # Vite entry — Redux Provider mount
│   ├── components/
│   │   ├── auth/
│   │   │   ├── SignIn.tsx          # Email/password + OAuth entry
│   │   │   ├── SignUp.tsx          # Registration + phone OTP trigger
│   │   │   ├── OTPVerify.tsx       # 6-digit Twilio OTP form
│   │   │   └── OAuthCallback.tsx   # LinkedIn / Google redirect handler
│   │   ├── dashboard/
│   │   │   ├── Overview.tsx        # Network KPI cards (Framer counter anims)
│   │   │   ├── Influencers.tsx     # Ranked influencer table + flow centrality
│   │   │   ├── Simulation.tsx      # Growth sim controls + Recharts Line chart
│   │   │   └── Optimization.tsx    # Bonus optimisation + bar charts
│   │   ├── sports/
│   │   │   ├── NBAProps.tsx        # NBA fixture list + prop cards
│   │   │   ├── NFLProps.tsx        # NFL fixture list + prop cards
│   │   │   └── SoccerProps.tsx     # Soccer fixture list + prop cards
│   │   └── shared/
│   │       ├── PropCard.tsx        # Reusable player prop card
│   │       ├── OddsTable.tsx       # Multi-book odds comparison
│   │       └── EVBadge.tsx         # +EV classification badge
│   ├── utils/
│   │   ├── graphAlgorithms.js      # BFS, DFS, centrality, simulation, binary search
│   │   ├── evCalculator.ts         # EV% from odds + model probability
│   │   └── formatters.ts           # Date, odds, percentage formatters
│   └── assets/
├── public/
├── vite.config.js
├── tsconfig.json
├── eslint.config.js
└── package.json
```

### State Management

```
Redux Store
├── authSlice         — user session, OAuth tokens, loading flags
├── fixturesSlice     — NBA/NFL/Soccer fixture lists keyed by sport+date
├── propsSlice        — player prop data per fixture, EV scores
└── networkSlice      — graph state, influencer rankings, simulation results

RTK Query Endpoints
├── fixturesApi       — GET /api/nba/fixtures/?date=   (5 min cache TTL)
├── propsApi          — GET /api/nba/fixtures/{id}/props/
├── networkApi        — GET /api/network/influencers/
└── authApi           — POST /api/auth/send-otp/ | verify-otp/
```

### Algorithm Complexity — `utils/graphAlgorithms.js`

| Algorithm | Function | Time | Space |
|---|---|---|---|
| Add Referral + Cycle Detection | `addReferral()` | O(V) DFS | O(V) |
| Total Referral Count — BFS | `getReachBFS()` | O(V + E) | O(V) |
| Top Referrers — All Users | `getTopReferrers()` | O(V × (V + E)) | O(V) |
| Unique Reach — Greedy Selection | `greedyInfluencers()` | O(k × V²) | O(V) |
| Flow Centrality — All-pairs SP | `flowCentrality()` | O(V³) | O(V²) |
| Growth Simulation — Discrete-time | `simulateGrowth()` | O(days × referrers) | O(days) |
| Target Days — Binary Search | `binarySearchTarget()` | O(log(days) × sim) | O(1) |
| Bonus Optimisation — Binary Search | `optimiseBonus()` | O(log(range) × sim) | O(1) |

---

## 🔐 Authentication System

Three independent auth pathways all converging to `django.contrib.auth.login(request, user)`:

### Path 1 — Twilio SMS OTP

```
1. POST /api/auth/send-otp/  { phone: "+91XXXXXXXXXX" }
         │
         ▼
   twilio.verify.v2.services(SID).verifications.create(to=phone, channel="sms")
         │
         ▼  SMS dispatched to user
         │
2. POST /api/auth/verify-otp/  { phone, code }
         │
         ▼
   twilio.verify.v2.services(SID).verification_checks.create(to=phone, code=code)
         │
   status == "approved"  →  Django session created  →  200 OK
   status == "pending"   →  401 Unauthorized
```

### Path 2 — LinkedIn OAuth 2.0 (PKCE)

```
1. Frontend → https://www.linkedin.com/oauth/v2/authorization
              ?client_id=LINKEDIN_CLIENT_ID
              &redirect_uri=http://localhost:8001/auth/linkedin/callback.html
              &scope=openid profile email
              &response_type=code

2. LinkedIn → callback.html?code=AUTH_CODE

3. Frontend → POST /api/auth/linkedin/  { code }

4. Django → POST https://www.linkedin.com/oauth/v2/accessToken  (code exchange)
          → GET  https://api.linkedin.com/v2/me                 (profile fetch)
          → Upsert user on linkedin_id
          → django.contrib.auth.login() → session cookie issued
```

### Path 3 — Google OAuth 2.0 / OpenID Connect

```
1. Google Sign-In popup → ID token (JWT) returned to browser

2. Frontend → POST /api/auth/google/  { id_token }

3. Django → GET https://www.googleapis.com/oauth2/v3/certs  (JWKS fetch)
          → Verify JWT: signature + exp + aud claims
          → Extract sub (stable Google user ID)
          → Upsert user on google_sub
          → Session issued
```

---

## 🔢 Graph Analytics Engine

### BFS Network Reach

```python
def get_reach_bfs(root, adjacency_list):
    visited = set()
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for child in adjacency_list[node]:
            if child not in visited:
                visited.add(child)
                queue.append(child)
    return len(visited) - 1   # exclude root itself
    # Time: O(V + E)  |  Space: O(V)
```

### Greedy Influencer Maximisation

```python
def greedy_influencers(k, all_users, reach_fn):
    selected, covered = [], set()
    for _ in range(k):
        best = max(
            (u for u in all_users if u not in selected),
            key=lambda u: len(reach_fn(u) - covered)
        )
        covered |= reach_fn(best)
        selected.append(best)
    return selected
    # Approximation guarantee: (1 - 1/e) ≈ 63% of optimal
    # Time: O(k × V²)
```

### DFS Cycle Detection (before edge insertion)

```python
def has_cycle_after_insert(from_node, to_node, adj):
    # If DFS from to_node can reach from_node, adding edge creates cycle
    visited, stack = set(), [to_node]
    while stack:
        node = stack.pop()
        if node == from_node:
            return True          # cycle detected — reject insert
        if node not in visited:
            visited.add(node)
            stack.extend(adj.get(node, []))
    return False
    # Time: O(V)
```

### Binary Search — Minimum Viable Bonus

```python
def optimise_bonus(target_users, days, simulate_fn):
    lo, hi = 0, MAX_BONUS
    while lo < hi:
        mid = (lo + hi) // 2
        if simulate_fn(bonus=mid, days=days).users >= target_users:
            hi = mid
        else:
            lo = mid + 1
    return lo   # minimum bonus achieving target in D days
    # Time: O(log(MAX_BONUS) × simulation_cost)
```

---

## 📈 Sports Props & EV Modelling

### Expected Value Formula

```
EV% = P_model × odds_decimal - 1

Positive odds (+150):
  P_implied    = 100 / (150 + 100) = 40.0%
  odds_decimal = 2.50

Negative odds (-120):
  P_implied    = 120 / (120 + 100) = 54.5%
  odds_decimal = 1.833

No-vig probability (two-sided market):
  P_novig_over = P_implied_over / (P_implied_over + P_implied_under)
```

### Hit Rate Computation

```
Raw Hit Rate:
  HR_raw = count(games where stat >= line) / total_games

Recency-Weighted (exponential decay, λ = 0.85):
  HR_weighted = Σ (λ^i × indicator(stat_i >= line)) / Σ λ^i

Opponent-Adjusted Hit Rate (OAHR):
  OAHR = HR_weighted × (1 + α × (DefRank_percentile - 0.5))
  α = 0.35 (NBA pts) | 0.28 (NFL passing yds) | 0.22 (Soccer shots)
```

### EV Classification

| EV% | Classification | UI |
|---|---|---|
| > +8% | Strong +EV | 🟢 Green — surfaced first |
| +4% to +8% | Moderate +EV | 🟡 Yellow |
| +1% to +4% | Marginal +EV | ⚪ Grey |
| -1% to +1% | Breakeven | — neutral |
| < -1% | Negative EV | 🔴 Hidden from EV filter |

### Matchup Grading (A+ → F)

```
Composite Score =
    0.50 × season_defensive_rank_percentile
  + 0.30 × last_10_games_defensive_trend
  + 0.10 × pace_adjustment_factor
  + 0.10 × injury_adjusted_rank_delta

Grade mapping:
  0.85–1.00 → A+    0.70–0.85 → A
  0.55–0.70 → B+    0.40–0.55 → B
  0.25–0.40 → C     0.10–0.25 → D
  0.00–0.10 → F
```

---

## 🔌 API Design

All endpoints served by DRF ViewSets, routed via `DefaultRouter`, protected where required by Django session authentication, and CORS-gated by `django-cors-headers`.

```
# ── Authentication ────────────────────────────────────────────────
POST   /api/auth/send-otp/             Twilio — dispatch SMS OTP
POST   /api/auth/verify-otp/           Twilio — confirm code → create session
GET    /auth/linkedin/callback.html    LinkedIn OAuth2 redirect handler
GET    /auth/google/callback.html      Google OAuth2 redirect handler
POST   /api/auth/google/               ID token verification + session
POST   /api/auth/logout/               Session invalidation
GET    /api/auth/me/                   Authenticated user profile
POST   /api/auth/avatar/               Pillow image upload + resize to 256×256

# ── NBA Props ─────────────────────────────────────────────────────
GET    /api/nba/fixtures/?date=YYYY-MM-DD     Day fixture list
GET    /api/nba/fixtures/{id}/props/          All props for a fixture
GET    /api/nba/players/{id}/splits/          Historical hit-rate splits (L5/L10/season)
GET    /api/nba/players/{id}/gamelog/         Raw game log with stat values

# ── NFL / Football (BETA) ─────────────────────────────────────────
GET    /api/football/fixtures/?date=YYYY-MM-DD
GET    /api/football/fixtures/{id}/props/
GET    /api/football/players/{id}/splits/

# ── Referral Network Graph ────────────────────────────────────────
POST   /api/network/add-referral/       Add edge (DFS cycle check first)
GET    /api/network/reach/{user_id}/    BFS subtree reach count
GET    /api/network/influencers/        Top-k influencers (greedy selection)
POST   /api/network/simulate/           Discrete-time growth simulation
POST   /api/network/optimise-bonus/     Binary search — minimum viable bonus
GET    /api/network/centrality/         Flow centrality scores O(V³)
```

---

## 🗄️ Database Schema

PostgreSQL 15 managed by Render.com, connected via `dj-database-url`, migrated by Django ORM.

```sql
-- ── AUTH DOMAIN ───────────────────────────────────────────────────
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone           VARCHAR(20)   UNIQUE,
    email           VARCHAR(254)  UNIQUE,
    linkedin_id     VARCHAR(50)   UNIQUE,
    google_sub      VARCHAR(100)  UNIQUE,
    display_name    VARCHAR(150),
    avatar          TEXT,                    -- Pillow-processed file path
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ── NBA DOMAIN ────────────────────────────────────────────────────
CREATE TABLE nba_fixtures (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_id     VARCHAR(50)   UNIQUE,
    home_team       VARCHAR(100),
    away_team       VARCHAR(100),
    game_date       DATE NOT NULL,
    status          VARCHAR(30)   DEFAULT 'scheduled'
);

CREATE TABLE nba_player_props (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fixture_id      UUID REFERENCES nba_fixtures(id) ON DELETE CASCADE,
    player_name     VARCHAR(150),
    team            VARCHAR(100),
    prop_type       VARCHAR(50),    -- 'points','assists','rebounds','3pm'
    line            NUMERIC(6,1),
    over_odds       SMALLINT,       -- American odds
    under_odds      SMALLINT,
    ev_score        NUMERIC(6,3),   -- computed EV%
    hit_rate_l5     NUMERIC(5,3),
    hit_rate_l10    NUMERIC(5,3),
    hit_rate_season NUMERIC(5,3),
    matchup_grade   CHAR(2),        -- 'A+','B','F' etc.
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- ── REFERRAL GRAPH DOMAIN ─────────────────────────────────────────
CREATE TABLE network_nodes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    join_date       DATE,
    referral_code   VARCHAR(20) UNIQUE
);

CREATE TABLE network_edges (        -- directed: referrer → referee
    id              BIGSERIAL PRIMARY KEY,
    from_node       UUID REFERENCES network_nodes(id),
    to_node         UUID REFERENCES network_nodes(id),
    created_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(from_node, to_node)      -- prevent duplicate referrals
);

-- ── INDEXES ───────────────────────────────────────────────────────
CREATE INDEX idx_edges_from      ON network_edges(from_node);  -- BFS hot path
CREATE INDEX idx_edges_to        ON network_edges(to_node);    -- reverse lookup
CREATE INDEX idx_props_fixture   ON nba_player_props(fixture_id);
CREATE INDEX idx_props_ev        ON nba_player_props(ev_score DESC);
CREATE INDEX idx_fixtures_date   ON nba_fixtures(game_date);
```

---

## 🚀 Deployment — Render.com

### Production Stack

```
Cloudflare (DNS + DDoS + SSL termination)
    │
    ├── statyx.io  (Frontend SPA)
    │   └── Vite build → dist/ → Static hosting (Vercel / Cloudflare Pages)
    │
    └── api backend (Django)
        └── Render.com Web Service
            ├── Gunicorn WSGI (multi-worker)
            ├── WhiteNoise (Brotli/GZip static files)
            └── Render Managed PostgreSQL 15
                └── Connected via DATABASE_URL
```

### Build & Deploy Flow

```bash
# Render.com auto-executes on every push to main:

pip install -r requirements_prod.txt
python manage.py collectstatic --no-input   # WhiteNoise compression
python manage.py migrate                     # Django ORM migrations
python check_db_integrity.py                 # schema gate before serving
gunicorn neosharx.wsgi:application           # start WSGI server
```

### Frontend Build

```bash
git clone https://github.com/vk93102/statyx-frontend.git
cd statyx-frontend
npm install
npm run build     # → dist/ (ES modules, tree-shaken, Brotli-ready)
# Deploy dist/ to Vercel / Cloudflare Pages / Render Static Site
```

---

## 🔐 Environment Variables

Copy `.env.example` from the [backend repo](https://github.com/vk93102/statyx-Backend/blob/main/.env.example) and fill in:

```env
# Django Core
SECRET_KEY=your-super-secret-key-50-chars-minimum-random-string
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/statyx_db

# CORS
CORS_ALLOWED_ORIGINS=https://statyx.io,https://www.statyx.io
CORS_ALLOW_ALL_ORIGINS=False

# Twilio SMS OTP
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_VERIFY_SERVICE_SID=VAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# LinkedIn OAuth 2.0
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8001/auth/linkedin/callback.html

# Google OAuth 2.0 / OpenID
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8001/auth/google/callback.html
```

---

## 💻 Local Development Setup

### Backend

```bash
# Clone
git clone https://github.com/vk93102/statyx-Backend.git
cd statyx-Backend

# Virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your credentials

# Migrate + validate
python manage.py migrate
python check_db_integrity.py

# Run
python manage.py runserver 8000
```

### Frontend

```bash
# Clone
git clone https://github.com/vk93102/statyx-frontend.git
cd statyx-frontend

# Install
npm install

# Point to local backend
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Dev server (Vite HMR)
npm run dev              # → http://localhost:5173

# Production build + type check
npm run build
npm run typecheck
```

---

## 📁 Full Repository Structure

```
statyx-Backend/                       statyx-frontend/
├── authentication/                   ├── src/
│   ├── models.py                     │   ├── App.jsx
│   ├── views.py                      │   ├── main.jsx
│   ├── serializers.py                │   ├── components/
│   └── urls.py                       │   │   ├── auth/
├── NBA/                              │   │   ├── dashboard/
│   ├── models.py                     │   │   ├── sports/
│   ├── views.py                      │   │   └── shared/
│   ├── serializers.py                │   └── utils/
│   └── urls.py                       │       ├── graphAlgorithms.js
├── NFA_Football/                     │       ├── evCalculator.ts
│   ├── models.py                     │       └── formatters.ts
│   ├── views.py                      ├── public/
│   ├── serializers.py                ├── vite.config.js
│   └── urls.py                       ├── tsconfig.json
├── create_set/                       ├── eslint.config.js
│   ├── models.py                     └── package.json
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── tests/
├── check_db_integrity.py
├── render.yaml
├── requirements.txt
├── requirements_prod.txt
├── runtime.txt
└── .env.example
```

---

## 🤝 Contributing

1. Fork the repo — [frontend](https://github.com/vk93102/statyx-frontend) | [backend](https://github.com/vk93102/statyx-Backend)
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Backend: `python manage.py test` must pass
4. Frontend: `npm run typecheck` and ESLint must pass with zero errors
5. Commits: Conventional Commits format (`feat:`, `fix:`, `perf:`, `chore:`)
6. Open a Pull Request with a clear description

---

## 📜 License

© Statyx. All rights reserved.

---

<p align="center">
  <strong>Statyx</strong> · Django 5.1 + DRF 3.15 + React 18 + TypeScript 5 + Vite 5 + PostgreSQL 15<br/>
  Twilio Verify · LinkedIn OAuth2 · Google OAuth2 · Deployed on Render.com<br/><br/>
  <a href="https://statyx.io">statyx.io</a> ·
  <a href="https://github.com/vk93102/statyx-frontend">Frontend Repo</a> ·
  <a href="https://github.com/vk93102/statyx-Backend">Backend Repo</a> ·
  <a href="https://drive.google.com/file/d/1MM9s7fH6XkBgMpIbQMhxkwRXxrmdAb6m/view?usp=sharing">Demo Video</a>
</p>