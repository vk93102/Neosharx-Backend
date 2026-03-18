# 📊 Statyx

> **Advanced Sports Betting Analytics & Player Props Research Platform** — Consolidating multi-sport statistical modelling, real-time odds ingestion, matchup grading, and positive expected value (+EV) identification for NFL, NBA, MLB, and Soccer into a single unified research interface.

[![Live Platform](https://img.shields.io/badge/Live-statyx.io-brightgreen?style=flat-square)](https://statyx.io)
[![Sports](https://img.shields.io/badge/Sports-NFL%20%7C%20NBA%20%7C%20MLB%20%7C%20Soccer-blue?style=flat-square)](#)
[![Status](https://img.shields.io/badge/Football-BETA-orange?style=flat-square)](#)
[![Auth](https://img.shields.io/badge/Auth-Sign%20In%20%2F%20Sign%20Up-lightgrey?style=flat-square)](https://statyx.io/sign-up)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Core Value Proposition](#-core-value-proposition)
- [Platform Architecture](#️-platform-architecture)
- [Tech Stack](#-tech-stack)
- [Sports Data Ingestion Pipeline](#-sports-data-ingestion-pipeline)
- [Props Analytics Engine](#-props-analytics-engine)
- [Expected Value (+EV) Modelling](#-expected-value-ev-modelling)
- [Matchup Grading System](#-matchup-grading-system)
- [Odds Aggregation Layer](#-odds-aggregation-layer)
- [Sport-Specific Modules](#-sport-specific-modules)
- [Analytics Dashboard](#-analytics-dashboard)
- [Real-Time Data Architecture](#-real-time-data-architecture)
- [Database Schema](#-database-schema)
- [API Design](#-api-design)
- [Authentication & Subscription](#-authentication--subscription)
- [Affiliate System](#-affiliate-system)
- [Performance & Scalability](#-performance--scalability)
- [Directory Structure](#-directory-structure)
- [Setup & Local Development](#-setup--local-development)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)

---

## 🌐 Project Overview

Statyx is a **full-stack sports betting intelligence platform** designed around a single thesis: serious bettors should not have to context-switch across five separate research tools — box score aggregators, odds comparison engines, historical trend databases, matchup graders, and projection models — when a unified analytical surface can serve all of these simultaneously.

The platform's core offering is **player props research** — the fastest-growing and most inefficiently priced segment of the sports betting market. While sportsbooks deploy sophisticated quant teams to set game lines with sub-0.5% margin error, player prop markets remain structurally mispriced due to the combinatorial explosion of prop types per game, giving edge-aware bettors meaningful +EV opportunities that Statyx is specifically architected to surface.

### Market Context

The US sports betting market crossed **$13B in annual handle** as of 2025, with player props representing the highest-margin, highest-variance segment. Statyx targets the analytically-oriented bettor segment who demands statistical rigour — hit-rate tracking, sample-size-adjusted historical splits, opponent defensive ranking percentiles, and multi-book line comparison — rather than surface-level pick recommendations.

---

## 🎯 Core Value Proposition

| Problem | Statyx Solution |
|---|---|
| Props research requires 5+ separate sites | Unified multi-sport props research hub |
| No single platform covers NFL + NBA + Soccer + MLB | All four sports in one interface |
| Sportsbook lines are opaque | Multi-book odds aggregation with line movement tracking |
| Historical trends buried in raw box scores | Pre-computed rolling splits, opponent-adjusted hit rates |
| No way to identify +EV props efficiently | Expected Value engine surfacing mispriced lines |
| Matchup context missing from prop analysis | Integrated matchup grading against positional defensive rankings |

---

## 🏗️ Platform Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER (SPA)                               │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │  Sport Modules   │  │  Props Research  │  │  Analytics Dashboard │  │
│  │  NFL / NBA /     │  │  Engine UI       │  │  Hit rates, trends,  │  │
│  │  MLB / Soccer /  │  │  - Fixture list  │  │  ROI tracking,       │  │
│  │  Football (BETA) │  │  - Player cards  │  │  leaderboard views   │  │
│  └──────────────────┘  │  - Odds tables   │  └──────────────────────┘  │
│                         │  - Trend charts  │                             │
│  ┌──────────────────┐  └──────────────────┘  ┌──────────────────────┐  │
│  │  Auth Layer      │                         │  Pricing / Affiliate │  │
│  │  Sign In/Up      │  ┌──────────────────┐  │  Subscription mgmt   │  │
│  │  JWT sessions    │  │  Real-Time Feed  │  │  Affiliate dashboard │  │
│  └──────────────────┘  │  WebSocket/SSE   │  └──────────────────────┘  │
│                         │  Live odds,      │                             │
│                         │  game status     │                             │
│                         └──────────────────┘                             │
└──────────────────────────────┬──────────────────────────────────────────┘
                                │ REST + WebSocket
┌──────────────────────────────▼──────────────────────────────────────────┐
│                         API GATEWAY LAYER                                │
│                                                                          │
│   Rate Limiting  │  JWT Auth Middleware  │  Request Routing  │  CORS    │
└──────────────────────────────┬──────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────────┐   ┌──────────────────────┐
│  Props API    │   │  Analytics API    │   │  User / Auth API     │
│  Service      │   │  Service          │   │  Service             │
│               │   │                   │   │                      │
│  - Fixtures   │   │  - Hit rates      │   │  - Registration      │
│  - Player     │   │  - Trend splits   │   │  - JWT issuance      │
│    props      │   │  - EV scoring     │   │  - Subscription      │
│  - Odds feed  │   │  - Matchup grades │   │  - Affiliate mgmt    │
└───────┬───────┘   └─────────┬─────────┘   └──────────┬───────────┘
        │                     │                          │
        └─────────────────────┼──────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                       │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ PostgreSQL   │  │    Redis     │  │  TimescaleDB │  │  S3 / CDN  │ │
│  │ (core data)  │  │  (cache +   │  │  (time-series│  │  (static + │ │
│  │              │  │   sessions)  │  │   odds + PBP)│  │   exports) │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────┐
│                    EXTERNAL DATA INGESTION LAYER                         │
│                                                                          │
│  Sports Data APIs     │  Odds APIs              │  Injury / Lineup      │
│  (SportsDataIO,       │  (OddsAPI, TheOdds,     │  Feeds (FantasyLabs,  │
│   StatMuse,           │   DraftKings odds,       │   Rotowire,           │
│   ESPN Stats)         │   BetMGM odds)           │   ESPN injuries)      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

### Frontend

| Layer | Technology | Rationale |
|---|---|---|
| Framework | React 18 + TypeScript | Component-driven SPA with strict typing across all data models |
| State Management | Redux Toolkit + RTK Query | Normalized server state cache; auto-deduplication of concurrent requests |
| Routing | React Router v6 | Sport-scoped nested routes (`/nba-props`, `/nfl-props`, etc.) |
| Real-Time | WebSocket / Server-Sent Events | Live odds updates and game status without polling |
| Data Viz | Recharts + D3.js | Hit-rate trend charts, line movement graphs, EV distribution plots |
| Styling | Tailwind CSS + CSS Modules | Utility-first base with scoped overrides for data-dense tables |
| Build | Vite 5 | Sub-second HMR; tree-shaken ESM bundles per sport module |

### Backend

| Layer | Technology | Rationale |
|---|---|---|
| API Framework | Node.js + Express / FastAPI (Python) | Hybrid: TypeScript Express for client-facing API; Python FastAPI for analytics compute |
| Auth | JWT (access + refresh tokens) + bcrypt | Stateless, horizontally scalable auth |
| ORM | Prisma (Node) / SQLAlchemy (Python) | Type-safe queries across PostgreSQL |
| Task Queue | Celery + Redis | Scheduled odds ingestion, stat computation jobs |
| WebSocket | Socket.io | Real-time odds broadcast to subscribed clients |
| Cache | Redis 7 | Hot-path fixture lists, computed EV scores (TTL-keyed by game start) |
| Time-Series | TimescaleDB (PostgreSQL extension) | Hypertable storage for odds movement history, play-by-play event streams |

---

## 🔄 Sports Data Ingestion Pipeline

The ingestion pipeline is the backbone of Statyx — a multi-source, fault-tolerant ETL system that continuously hydrates the analytical data store with player statistics, odds, injury reports, and lineup intelligence.

### Pipeline Architecture

```
External Sources
      │
      ├── Sports Stats APIs  (polling: per-5-min during live games)
      ├── Odds APIs          (polling: per-30-sec during live windows)
      ├── Injury Feed        (polling: per-10-min)
      └── Lineup Feed        (polling: per-15-min pre-game)
      │
      ▼
┌─────────────────────────────────────────────┐
│            INGESTION WORKERS (Celery)        │
│                                              │
│  ┌──────────────┐   ┌──────────────────┐   │
│  │ StatFetcher  │   │  OddsFetcher     │   │
│  │              │   │                  │   │
│  │ - Normalize  │   │ - Multi-book     │   │
│  │   schema     │   │   dedup          │   │
│  │ - Validate   │   │ - Timestamp      │   │
│  │   types      │   │   each line move │   │
│  │ - Upsert DB  │   │ - Detect CLV     │   │
│  └──────────────┘   └──────────────────┘   │
│                                              │
│  ┌──────────────┐   ┌──────────────────┐   │
│  │ InjuryParser │   │  LineupScraper   │   │
│  │              │   │                  │   │
│  │ - Status     │   │ - Starter lists  │   │
│  │   change     │   │ - Minutes proj.  │   │
│  │   detection  │   │ - Usage rate est │   │
│  └──────────────┘   └──────────────────┘   │
└────────────────────────┬────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │ Normalization &  │
              │ Schema Validation│
              │ Layer            │
              │ (Pydantic models)│
              └────────┬─────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
   PostgreSQL (core)          TimescaleDB
   player_stats,              odds_history,
   fixtures, teams,           play_by_play,
   props_lines                clv_snapshots
```

### Ingestion Data Contracts (Pydantic)

```python
class PlayerStatLine(BaseModel):
    player_id: str
    game_id: str
    sport: Literal["nfl", "nba", "mlb", "soccer"]
    stat_type: str                   # "points", "assists", "rushing_yards", etc.
    value: float
    game_date: date
    opponent_team_id: str
    home_away: Literal["home", "away"]
    minutes_played: Optional[float]
    usage_rate: Optional[float]      # NBA: possessions used %
    snap_count: Optional[int]        # NFL: offensive snaps

class OddsSnapshot(BaseModel):
    prop_id: str
    sportsbook: str
    line: float                      # The over/under number
    over_odds: int                   # American odds
    under_odds: int
    captured_at: datetime
    is_opening_line: bool
    juice: float                     # Computed: vig percentage
```

---

## 🧮 Props Analytics Engine

The Props Analytics Engine is a multi-factor scoring system that, for every player prop available on a given game day, computes:

1. **Hit Rate** — Historical frequency of a player exceeding a given threshold
2. **Opponent-Adjusted Hit Rate** — Hit rate weighted against defensive rank at the relevant statistical position
3. **Recency Weight** — Exponential decay of older game logs to emphasize recent form
4. **Matchup Grade** — Composite grade of the opponent's defensive efficiency against this stat category
5. **EV Score** — Expected Value against the book's implied probability

### Hit Rate Computation

```
For a prop: Player X to score 20+ points

Raw Hit Rate:
  HR_raw = count(games where points >= 20) / total_games

Recency-Weighted Hit Rate:
  HR_weighted = Σ (w_i × indicator(points_i >= line)) / Σ w_i

  where w_i = λ^(rank of game, most recent = rank 0)
  λ = 0.85 (decay factor, configurable per sport)

Sample-Size Adjusted Hit Rate (Wilson Score Interval):
  Provides 95% CI: (HR ± 1.96 × sqrt(HR(1-HR)/n))
  Displayed to users with confidence band shading
```

### Opponent-Adjusted Hit Rate (OAHR)

```
OAHR = HR_weighted × (1 + α × (DefRank_percentile - 0.5))

Where:
  DefRank_percentile = opponent's percentile rank in defending
                       this stat category (0=best defense, 1=worst)
  α = sport-specific sensitivity coefficient
      NBA points: α = 0.35
      NFL passing yards: α = 0.28
      Soccer shots on target: α = 0.22
```

### Split Filters

Users can filter historical hit rates by granular splits:

| Split Category | Examples |
|---|---|
| Recency | Last 5 / 10 / 20 games, current season |
| Venue | Home only / Away only |
| Opponent | Specific team, division, conference |
| Rest | 0 days rest, 1+ days rest, back-to-back |
| Game context | Favourite / Underdog, High total / Low total |
| Usage | High usage games (>28% USG%), standard usage |

---

## 📈 Expected Value (+EV) Modelling

**Expected Value** is the core metric that separates serious bettors from recreational ones. Statyx computes EV for every prop line by comparing the model's probability estimate against the sportsbook's implied probability.

### EV Formula

```
EV = (P_model × Payout_win) - ((1 - P_model) × Stake)

Expressed as a percentage:
EV% = (P_model × (odds_decimal - 1)) - (1 - P_model)

Simplified:
EV% = P_model × odds_decimal - 1

Where P_model comes from the Props Analytics Engine's OAHR output,
adjusted for injury status, lineup uncertainty, and usage projection.
```

### Implied Probability Extraction

```
For American odds:

Positive odds (+150):
  P_implied = 100 / (odds + 100) = 100/250 = 40%

Negative odds (-120):
  P_implied = |odds| / (|odds| + 100) = 120/220 = 54.5%

Vig-removed "no-vig" probability (two-sided market):
  P_novig_over = P_implied_over / (P_implied_over + P_implied_under)
```

### EV Threshold Classification

| EV% | Classification | UI Indicator |
|---|---|---|
| > +8% | Strong +EV | 🟢 Green badge |
| +4% to +8% | Moderate +EV | 🟡 Yellow badge |
| +1% to +4% | Marginal +EV | ⚪ Grey badge |
| -1% to +1% | Breakeven | — |
| < -1% | Negative EV | 🔴 (hidden from EV filter) |

### Sharp Money Signals (CLV Tracking)

**Closing Line Value (CLV)** is tracked by snapshotting odds at multiple timestamps from open to close, detecting directional line movement that indicates sharp (professional) money:

```
CLV = odds_close - odds_open   (in American odds points)

Strong sharp signal:
  - Line moves 10+ points against public percentage
  - Public betting ≥60% on one side, line moves opposite
  → "Reverse Line Movement" flag surfaced in UI
```

---

## 🏆 Matchup Grading System

Every player prop in Statyx is contextualised with a **Matchup Grade** — a composite score (A+ through F) evaluating how favourable the opposing defence is for the specific statistical category being bet.

### Grade Computation

```
Grade inputs:
1. Opponent's season-long defensive rank (per stat category)
   e.g., "Opponent ranks 28th in points allowed to SGs"

2. Opponent's last-10-game defensive trend
   (improving vs degrading vs stable)

3. Opponent's pace adjustment
   (high-pace teams inflate counting stats; normalised)

4. Injury-adjusted defensive ranking
   (if key defender is out, rank adjusted upward)

Composite Score = 0.50 × season_rank_pctile
               + 0.30 × last10_rank_pctile
               + 0.10 × pace_adj_factor
               + 0.10 × injury_adj_factor

Grade mapping:
  0.85–1.00 → A+ (elite matchup)
  0.70–0.85 → A
  0.55–0.70 → B+
  0.40–0.55 → B
  0.25–0.40 → C
  0.10–0.25 → D
  0.00–0.10 → F (brutal matchup)
```

---

## 💹 Odds Aggregation Layer

Statyx aggregates odds from multiple sportsbooks in real time, giving users a **consensus line** and the ability to shop for the best price on each side.

### Multi-Book Ingestion

```
Books monitored (configurable per region):
  - DraftKings
  - FanDuel
  - BetMGM
  - Caesars
  - PointsBet
  - ESPN Bet
  - Hard Rock Bet

For each prop line, Statyx stores:
  - Opening line per book
  - Current line per book
  - Timestamps of all line moves
  - Over/under vig per book
  - Best available over (highest implied probability removed)
  - Best available under
```

### Consensus Line (Sharp Number)

The **consensus line** (also called the "sharp number" or "market number") is computed as the vig-adjusted weighted average across books, with higher weight given to sharp-money books:

```python
BOOK_WEIGHTS = {
    "pinnacle":    1.0,   # sharpest book (reference)
    "draftkings":  0.8,
    "fanduel":     0.8,
    "betmgm":      0.6,
    "caesars":     0.6,
}

consensus_line = Σ (weight_b × novig_line_b) / Σ weight_b
```

---

## 🏈🏀⚽⚾ Sport-Specific Modules

### NFL Module

**Prop Categories:**
- Passing: Yards, TDs, Completions, Attempts, Interceptions, Longest Completion
- Rushing: Yards, Attempts, TDs, Longest Rush, Carries
- Receiving: Receptions, Yards, TDs, Targets, Longest Reception
- Kicking: FG Made, Points Scored, Longest FG

**NFL-Specific Analytics:**
- **Air Yards Share** — receiving yards opportunity weighted by air yards (better than target share for WRs)
- **Route Participation Rate** — % of team routes run (differentiates scheme usage from injury)
- **Snap Count Trend** — rolling 4-game snap count for injury/usage momentum
- **DVOA-Adjusted Matchup** — opponent's defensive efficiency using Football Outsiders DVOA methodology

### NBA Module

**Prop Categories:**
- Points, Rebounds, Assists, 3PM, Steals, Blocks
- Combo props: Pts+Reb, Pts+Ast, Pts+Reb+Ast, Reb+Ast, Stk (Stocks: Stl+Blk)

**NBA-Specific Analytics:**
- **Usage Rate Context** — prop lines contextualised against player's usage rate variability
- **Pace-Adjusted Stats** — all per-game stats normalised to 100 possessions for cross-matchup comparability
- **On/Off Splits** — performance delta when specific teammates are in/out of the lineup
- **Rest & Schedule** — back-to-back flags, days-rest splits (0/1/2+), load management probability

### MLB Module (In Development)

**Prop Categories:**
- Hitting: Hits, RBIs, Runs, HRs, Stolen Bases, Strikeouts (batter)
- Pitching: Strikeouts (pitcher), Earned Runs, Outs Recorded, Hits Allowed

**MLB-Specific Analytics:**
- **Statcast Data Integration** — xBA, xSLG, barrel rate, exit velocity, launch angle for batter vs pitcher matchups
- **Platoon Splits** — LHP vs RHP performance differentials (L/R split hit rates)
- **Park Factor Adjustment** — normalisation for ballpark effects on counting stats
- **Pitcher Handedness & Stuff+** — quality-of-pitch metrics contextualised against batter's swing tendencies

### Soccer Module

**Prop Categories:**
- Shots, Shots on Target, Goals, Assists, Key Passes
- Match result props, Both Teams to Score, Over/Under totals
- Player Cards: Yellow/Red card props

**Soccer-Specific Analytics:**
- **xG (Expected Goals)** — shot quality metric for both teams; used to grade over/under totals
- **xA (Expected Assists)** — chance creation volume adjusted for shot quality
- **Progressive Passes / Carries** — ball progression metrics for midfielder prop analysis
- **Defensive Line Height** — opponent defensive shape contextualised for through-ball / behind-defence shot opportunities

### Football BETA (American College Football / International)

Currently in BETA with limited prop markets. Full analytics suite planned for next major release.

---

## 📊 Analytics Dashboard

The Analytics module provides users with **self-performance tracking** — connecting their prop research decisions to outcomes:

### User Bet Tracker

```typescript
interface BetRecord {
  propId: string;
  playerName: string;
  sport: Sport;
  propType: string;
  line: number;
  side: "over" | "under";
  sportsbook: string;
  oddsAmerican: number;
  stake: number;
  evAtTime: number;           // EV% when bet was placed
  matchupGradeAtTime: string; // Grade at time of bet
  result: "win" | "loss" | "push" | "pending";
  clv: number | null;         // CLV achieved (open vs close)
  placedAt: datetime;
  settledAt: datetime | null;
}
```

### Dashboard Metrics

| Metric | Computation |
|---|---|
| ROI % | `(net_profit / total_staked) × 100` |
| Win Rate | `wins / (wins + losses)` |
| Average CLV | Mean CLV across settled bets (quality-of-bet metric) |
| EV Accuracy | Correlation between EV% at placement and actual outcomes |
| Yield by Sport | Per-sport ROI breakdown |
| Yield by Prop Type | Points vs assists vs rebounds ROI breakdown |
| Closing Line Value Rate | % of bets where closing line was more favourable than bet line |

---

## ⚡ Real-Time Data Architecture

### WebSocket Event Model

```
Server → Client events:

"odds_update" — {propId, book, newLine, newOverOdds, newUnderOdds, timestamp}
"game_status"  — {gameId, status, period, clock, score}
"injury_alert" — {playerId, name, status, sport, timestamp}
"lineup_lock"  — {gameId, sport, confirmedStarters}
"ev_recalc"    — {propId, newEV, triggerReason}

Client → Server events:
"subscribe_game"   — {gameId} — join game-specific room
"unsubscribe_game" — {gameId}
"subscribe_player" — {playerId} — get real-time updates for a specific player
```

### Real-Time Odds Update Flow

```
OddsAPI webhook / polling
         │
         ▼
   OddsIngestionWorker
         │
         ▼
   Detect line change (vs last stored snapshot)
         │
   ┌─────┴─────┐
   │           │
   ▼           ▼
TimescaleDB  Redis pub/sub
(persist)    (broadcast)
                │
                ▼
        Socket.io server
                │
                ▼
        All subscribed clients
        receive "odds_update" event
        → React state update
        → Re-render odds cell
        → Trigger EV recalculation
```

---

## 🗄️ Database Schema

```sql
-- ============================================================
-- CORE ENTITIES
-- ============================================================

CREATE TABLE sports (
    id          SERIAL PRIMARY KEY,
    slug        VARCHAR(20) UNIQUE NOT NULL,  -- 'nfl', 'nba', 'mlb', 'soccer'
    name        VARCHAR(50) NOT NULL,
    is_active   BOOLEAN DEFAULT TRUE,
    season      VARCHAR(10)                   -- '2024-25', '2025'
);

CREATE TABLE teams (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sport_id        INTEGER REFERENCES sports(id),
    external_id     VARCHAR(50),              -- API provider's team ID
    name            VARCHAR(100) NOT NULL,
    abbreviation    VARCHAR(10) NOT NULL,
    city            VARCHAR(100),
    conference      VARCHAR(50),
    division        VARCHAR(50)
);

CREATE TABLE players (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sport_id        INTEGER REFERENCES sports(id),
    team_id         UUID REFERENCES teams(id),
    external_id     VARCHAR(50) UNIQUE,
    full_name       VARCHAR(150) NOT NULL,
    position        VARCHAR(20),
    jersey_number   SMALLINT,
    status          VARCHAR(30) DEFAULT 'active',  -- 'active', 'injured', 'suspended'
    injury_detail   TEXT,
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE fixtures (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sport_id        INTEGER REFERENCES sports(id),
    external_id     VARCHAR(50) UNIQUE,
    home_team_id    UUID REFERENCES teams(id),
    away_team_id    UUID REFERENCES teams(id),
    game_date       DATE NOT NULL,
    game_time       TIME,
    timezone        VARCHAR(50) DEFAULT 'America/New_York',
    status          VARCHAR(30) DEFAULT 'scheduled',
    home_score      SMALLINT,
    away_score      SMALLINT,
    period          SMALLINT,
    clock           VARCHAR(10)
);

-- ============================================================
-- PROPS & ODDS
-- ============================================================

CREATE TABLE prop_types (
    id          SERIAL PRIMARY KEY,
    sport_id    INTEGER REFERENCES sports(id),
    slug        VARCHAR(50) NOT NULL,         -- 'points', 'rushing_yards', 'shots_on_target'
    label       VARCHAR(100) NOT NULL,
    unit        VARCHAR(20),                  -- 'yards', 'points', 'goals'
    UNIQUE(sport_id, slug)
);

CREATE TABLE player_props (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fixture_id      UUID REFERENCES fixtures(id),
    player_id       UUID REFERENCES players(id),
    prop_type_id    INTEGER REFERENCES prop_types(id),
    line            NUMERIC(6,1) NOT NULL,    -- The over/under threshold
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- TimescaleDB hypertable for odds history
CREATE TABLE odds_snapshots (
    prop_id         UUID REFERENCES player_props(id),
    sportsbook      VARCHAR(50) NOT NULL,
    line            NUMERIC(6,1),
    over_odds       SMALLINT,                 -- American odds
    under_odds      SMALLINT,
    vig             NUMERIC(5,4),             -- Computed juice
    is_opening      BOOLEAN DEFAULT FALSE,
    captured_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

SELECT create_hypertable('odds_snapshots', 'captured_at');
CREATE INDEX ON odds_snapshots (prop_id, captured_at DESC);

-- ============================================================
-- STATISTICS
-- ============================================================

CREATE TABLE player_game_stats (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID REFERENCES players(id),
    fixture_id      UUID REFERENCES fixtures(id),
    prop_type_id    INTEGER REFERENCES prop_types(id),
    value           NUMERIC(8,2) NOT NULL,
    minutes_played  NUMERIC(5,2),
    usage_rate      NUMERIC(5,3),             -- NBA usage %
    snap_count      SMALLINT,                 -- NFL snaps
    target_share    NUMERIC(5,3),             -- NFL/NBA opportunity metric
    created_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(player_id, fixture_id, prop_type_id)
);

-- Pre-computed rolling splits (refreshed by Celery jobs)
CREATE TABLE player_splits (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id       UUID REFERENCES players(id),
    prop_type_id    INTEGER REFERENCES prop_types(id),
    window          VARCHAR(20) NOT NULL,     -- 'L5', 'L10', 'L20', 'season'
    split_key       VARCHAR(50),             -- 'home', 'away', 'vs_ATL', 'b2b'
    sample_size     SMALLINT,
    hit_rate        NUMERIC(5,3),            -- Against line at time of computation
    avg_value       NUMERIC(8,2),
    oahr            NUMERIC(5,3),            -- Opponent-adjusted hit rate
    ev_score        NUMERIC(6,3),
    matchup_grade   CHAR(2),                 -- 'A+', 'B', 'F', etc.
    computed_at     TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- USERS & SUBSCRIPTIONS
-- ============================================================

CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(254) UNIQUE NOT NULL,
    password_hash   TEXT NOT NULL,
    display_name    VARCHAR(100),
    plan            VARCHAR(20) DEFAULT 'free',  -- 'free', 'pro', 'elite'
    plan_expires_at TIMESTAMP,
    affiliate_code  VARCHAR(20) UNIQUE,
    referred_by     UUID REFERENCES users(id),
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE bet_records (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    prop_id         UUID REFERENCES player_props(id),
    side            VARCHAR(5) NOT NULL CHECK (side IN ('over', 'under')),
    sportsbook      VARCHAR(50),
    odds_american   SMALLINT,
    stake           NUMERIC(10,2),
    ev_at_placement NUMERIC(6,3),
    grade_at_placement CHAR(2),
    result          VARCHAR(10) CHECK (result IN ('win','loss','push','pending')),
    clv             SMALLINT,                  -- CLV in odds points
    placed_at       TIMESTAMP DEFAULT NOW(),
    settled_at      TIMESTAMP
);
```

---

## 🔌 API Design

### REST Endpoints

```
GET    /api/v1/fixtures/:sport?date=YYYY-MM-DD
       Returns all fixtures for a sport on a given date with game status

GET    /api/v1/fixtures/:fixtureId/props
       Returns all player props for a fixture with current odds (all books)
       Query params: ?propType=points&minEV=4&minGrade=B

GET    /api/v1/players/:playerId/splits
       Returns pre-computed splits for all prop types
       Query params: ?window=L10&split=home&line=22.5

GET    /api/v1/players/:playerId/gamelog
       Returns raw game log with stats and computed hit indicators
       Query params: ?propType=points&seasons=2024-25,2023-24

GET    /api/v1/props/:propId/odds
       Returns full odds history for a prop across all books
       Includes opening line, current line, line movement timeline

GET    /api/v1/analytics/leaderboard
       Returns top +EV props across all sports for the day
       Query params: ?sport=nba&minEV=5&maxProps=20

POST   /api/v1/bets
       Log a bet record (requires auth)
       Body: {propId, side, sportsbook, oddsAmerican, stake}

GET    /api/v1/bets/me
       Returns authenticated user's bet history with performance metrics

GET    /api/v1/affiliate/stats
       Returns affiliate referral stats and earnings (requires auth)
```

### Response Shape (Player Props)

```typescript
interface PropResponse {
  id: string;
  player: {
    id: string;
    name: string;
    team: string;
    position: string;
    injuryStatus: string | null;
  };
  propType: string;
  line: number;
  matchupGrade: string;
  splits: {
    L5: SplitStats;
    L10: SplitStats;
    L20: SplitStats;
    season: SplitStats;
  };
  odds: {
    [sportsbook: string]: {
      overOdds: number;
      underOdds: number;
      vig: number;
    };
  };
  bestOver: { book: string; odds: number };
  bestUnder: { book: string; odds: number };
  consensusLine: number;
  evOver: number;     // EV% for over side
  evUnder: number;    // EV% for under side
  sharpSignal: "rlm_over" | "rlm_under" | null;
}

interface SplitStats {
  sampleSize: number;
  hitRate: number;
  oahr: number;
  avgValue: number;
  confidenceLow: number;  // Wilson CI lower bound
  confidenceHigh: number;
}
```

---

## 🔐 Authentication & Subscription

### Auth Flow

```
1. POST /api/v1/auth/register   → create user, send verification email
2. POST /api/v1/auth/verify     → verify email token
3. POST /api/v1/auth/login      → return {accessToken (15min), refreshToken (7d)}
4. POST /api/v1/auth/refresh    → rotate refresh token, issue new access token
5. POST /api/v1/auth/logout     → invalidate refresh token (Redis blacklist)
```

### Access Control by Plan

| Feature | Free | Pro | Elite |
|---|---|---|---|
| Fixture list (today) | ✅ | ✅ | ✅ |
| Hit rates (L5, season) | ✅ | ✅ | ✅ |
| Full split filters | ❌ | ✅ | ✅ |
| EV scoring | ❌ | ✅ | ✅ |
| Matchup grades | ❌ | ✅ | ✅ |
| Odds comparison (all books) | ❌ | ✅ | ✅ |
| CLV tracking | ❌ | ❌ | ✅ |
| Bet tracker + analytics | ❌ | ✅ | ✅ |
| API access | ❌ | ❌ | ✅ |
| Historical data (2+ seasons) | ❌ | 1 season | 3 seasons |

---

## 🤝 Affiliate System

Statyx operates an affiliate programme (visible in the main navigation as "Affiliate") with:

- **Unique referral codes** per user — encoded UUID slug assigned on sign-up
- **Conversion tracking** — referral code stored on referred user's account at registration
- **Commission model** — percentage of referred user's first subscription payment
- **Affiliate dashboard** — click-throughs, conversion rate, total earnings, payout history

```typescript
// Referral attribution middleware
function attributeReferral(req: Request, res: Response, next: NextFunction) {
  const refCode = req.query.ref as string;
  if (refCode) {
    res.cookie('statyx_ref', refCode, {
      maxAge: 30 * 24 * 60 * 60 * 1000, // 30-day attribution window
      httpOnly: true,
      secure: true,
      sameSite: 'lax'
    });
  }
  next();
}
```

---

## ⚡ Performance & Scalability

### Caching Strategy

| Data Type | Cache Key Pattern | TTL | Invalidation Trigger |
|---|---|---|---|
| Fixture list | `fixtures:{sport}:{date}` | 5 min | New fixture ingested |
| Player splits | `splits:{playerId}:{propType}:{window}` | 30 min | New stat line ingested |
| EV scores | `ev:{propId}` | 2 min | Odds update received |
| Matchup grades | `grade:{playerId}:{fixtureId}:{propType}` | 60 min | Lineup lock event |
| Odds (current) | `odds:{propId}` | 30 sec during live window | Any odds update |

### Database Query Optimisation

```sql
-- Covering index for the hot-path split query
CREATE INDEX CONCURRENTLY idx_splits_lookup
ON player_splits (player_id, prop_type_id, window, computed_at DESC)
INCLUDE (hit_rate, oahr, ev_score, matchup_grade, sample_size);

-- Partial index for active props only
CREATE INDEX idx_active_props
ON player_props (fixture_id, player_id, prop_type_id)
WHERE is_active = TRUE;

-- TimescaleDB: compress chunks older than 7 days
SELECT add_compression_policy('odds_snapshots',
    INTERVAL '7 days');
```

### Horizontal Scaling Plan

```
Load Balancer (Nginx / Cloudflare)
    │
    ├── API Server Pool (2–8 instances, auto-scale)
    │   └── Stateless: only reads from Redis + DB
    │
    ├── WebSocket Server Pool (sticky sessions via Nginx)
    │   └── Redis pub/sub bridges socket clusters
    │
    └── Worker Pool (Celery, 4–16 workers)
        ├── High-priority queue: odds ingestion
        ├── Medium-priority queue: stat ingestion
        └── Low-priority queue: split recomputation
```

---

## 📁 Directory Structure

```
statyx/
├── apps/
│   ├── api/                    # Express/FastAPI backend
│   │   ├── routes/
│   │   │   ├── fixtures.ts
│   │   │   ├── props.ts
│   │   │   ├── analytics.ts
│   │   │   └── auth.ts
│   │   ├── services/
│   │   │   ├── PropsAnalyticsEngine.ts
│   │   │   ├── EVCalculator.ts
│   │   │   ├── MatchupGrader.ts
│   │   │   └── OddsAggregator.ts
│   │   ├── middleware/
│   │   │   ├── auth.ts
│   │   │   ├── rateLimit.ts
│   │   │   └── planGuard.ts
│   │   └── websocket/
│   │       ├── OddsRoom.ts
│   │       └── GameRoom.ts
│   │
│   ├── workers/               # Celery / background jobs (Python)
│   │   ├── ingestion/
│   │   │   ├── stats_fetcher.py
│   │   │   ├── odds_fetcher.py
│   │   │   ├── injury_parser.py
│   │   │   └── lineup_scraper.py
│   │   ├── compute/
│   │   │   ├── split_computer.py
│   │   │   ├── ev_scorer.py
│   │   │   └── matchup_grader.py
│   │   └── tasks.py
│   │
│   └── web/                   # React frontend
│       ├── src/
│       │   ├── modules/
│       │   │   ├── nba/
│       │   │   ├── nfl/
│       │   │   ├── mlb/
│       │   │   ├── soccer/
│       │   │   └── football/
│       │   ├── components/
│       │   │   ├── PropCard/
│       │   │   ├── OddsTable/
│       │   │   ├── TrendChart/
│       │   │   ├── MatchupBadge/
│       │   │   └── EVIndicator/
│       │   ├── store/
│       │   │   ├── propsSlice.ts
│       │   │   ├── fixturesSlice.ts
│       │   │   └── authSlice.ts
│       │   └── hooks/
│       │       ├── useRealTimeOdds.ts
│       │       ├── usePlayerSplits.ts
│       │       └── useEVFilter.ts
│       └── vite.config.ts
│
├── db/
│   ├── migrations/
│   └── seeds/
├── docker-compose.yml
├── docker-compose.prod.yml
└── .env.example
```

---

## 🚀 Setup & Local Development

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 15+ with TimescaleDB extension
- Redis 7+
- Docker + Docker Compose (recommended)

### Quick Start (Docker)

```bash
git clone https://github.com/yourorg/statyx.git
cd statyx

cp .env.example .env
# Configure API keys, DB credentials

docker-compose up --build
# Web: http://localhost:5173
# API: http://localhost:3000
# Workers: background (Celery)
```

### Manual Setup

```bash
# Backend API
cd apps/api
npm install
npm run db:migrate
npm run dev

# Workers (Python)
cd apps/workers
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt --break-system-packages
celery -A tasks worker --loglevel=info -Q high_priority,medium_priority,low_priority

# Frontend
cd apps/web
npm install
npm run dev
```

### Seed Development Data

```bash
# Seed fixtures, teams, players
npm run db:seed --sport=nba --date=today

# Run initial split computation
python apps/workers/compute/split_computer.py --sport=nba --full-refresh
```

---

## 🔐 Environment Variables

```env
# ── Database ──────────────────────────────────
DATABASE_URL=postgresql://statyx:password@localhost:5432/statyx
TIMESCALE_URL=postgresql://statyx:password@localhost:5432/statyx

# ── Redis ─────────────────────────────────────
REDIS_URL=redis://localhost:6379/0
REDIS_PUBSUB_URL=redis://localhost:6379/1

# ── Auth ──────────────────────────────────────
JWT_ACCESS_SECRET=your-access-secret-here
JWT_REFRESH_SECRET=your-refresh-secret-here
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# ── Sports Data APIs ──────────────────────────
SPORTSDATA_IO_API_KEY=your-key
ODDS_API_KEY=your-key
ROTOWIRE_API_KEY=your-key

# ── Stripe (subscriptions) ────────────────────
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRO_PRICE_ID=price_...
STRIPE_ELITE_PRICE_ID=price_...

# ── Email ─────────────────────────────────────
SENDGRID_API_KEY=SG...
FROM_EMAIL=noreply@statyx.io

# ── App ───────────────────────────────────────
NODE_ENV=production
PORT=3000
FRONTEND_URL=https://statyx.io
CORS_ORIGINS=https://statyx.io,https://www.statyx.io
```

---

## 🌍 Deployment

### Production Stack

```
Cloudflare (DNS + CDN + DDoS)
    │
    ├── statyx.io → Vercel / Cloudflare Pages (React SPA)
    │
    └── api.statyx.io → Load Balancer
            │
            ├── API Servers (2–4× Node, EC2/Railway)
            ├── WebSocket Servers (2× sticky sessions)
            └── Worker Servers (2–4× Celery, EC2)
                    │
                    ├── RDS PostgreSQL + TimescaleDB
                    ├── ElastiCache Redis
                    └── S3 (exports, backups)
```

### Deployment Commands

```bash
# Frontend deploy (Vercel)
vercel --prod

# Backend (Docker)
docker build -t statyx-api -f apps/api/Dockerfile .
docker push registry/statyx-api:latest
kubectl rollout restart deployment/statyx-api

# DB migrations in production
npm run db:migrate --env=production

# Worker restart
celery -A tasks control shutdown
celery -A tasks worker -D --loglevel=warning
```

---

## 📜 License

© Statyx. All rights reserved.

---

<p align="center">
  <strong>Statyx</strong> — Why juggle 5 sites when 1 can do all of your props research.
</p>