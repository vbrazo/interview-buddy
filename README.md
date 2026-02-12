# Interview Buddy

AI-powered interview preparation tool that transforms job descriptions into comprehensive, citation-backed research reports. Paste a job description, and get real-time company intelligence, technology deep-dives, interview focus areas, and practice questions -- all backed by live web research via the You.com APIs.

## Tech Stack

| Layer    | Technology                                             |
| -------- | ------------------------------------------------------ |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui    |
| Backend  | Python 3.11+, FastAPI, uvicorn                         |
| APIs     | You.com Search API, You.com Express Agent (Agents API) |

## Quick Start

### 1. Clone and install frontend dependencies

```bash
cd interview-buddy
npm install
```

### 2. Set up the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and add your You.com API key
```

### 4. Run both servers

In one terminal -- backend:

```bash
cd interview-buddy/backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

In another terminal -- frontend:

```bash
cd interview-buddy
npm run dev
```

Open **http://localhost:8080** and paste a job description to get started.

## How It Works

1. **Paste a job description** into the input textarea.
2. The backend **extracts metadata** (company name, role title, key technologies).
3. **You.com Search API** is called to research the company and each technology.
4. **You.com Express Agent** synthesises all research into a structured report.
5. The frontend streams progress in real-time via **Server-Sent Events**.
6. You get a full interview prep report you can save, copy, or export as Markdown.

## Project Structure

The backend follows an **MVC-style layout**: models, views, controllers, with services (orchestration + integrations), helpers (parsers, prompts, SSE), and repositories (data access).

```
interview-buddy/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # App factory, middleware, lifespan
│   │   ├── config.py            # Centralised settings (env vars)
│   │   ├── controllers/         # HTTP handlers (MVC Controller)
│   │   │   ├── routes.py        # Assembles API router under /api
│   │   │   ├── health.py        # GET /health
│   │   │   ├── history.py       # History CRUD
│   │   │   └── prepare.py       # POST /prepare
│   │   ├── views/               # Response shaping (MVC View)
│   │   │   ├── health.py
│   │   │   ├── history.py
│   │   │   └── prepare.py
│   │   ├── models/               # Pydantic models (MVC Model)
│   │   │   ├── __init__.py      # Re-exports all models
│   │   │   ├── requests.py      # PrepareRequest
│   │   │   ├── job_metadata.py
│   │   │   ├── search.py        # SearchHit
│   │   │   └── analysis.py      # AnalysisResult, SavedAnalysis, etc.
│   │   ├── services/            # Orchestration and external APIs
│   │   │   ├── pipeline.py      # Analysis pipeline orchestrator
│   │   │   └── you_client.py    # You.com API client (Search + Express Agent)
│   │   ├── helpers/             # Parsers, prompts, SSE formatting
│   │   │   ├── job_parser.py    # Job description metadata extractor
│   │   │   ├── prompts.py       # LLM prompt templates
│   │   │   └── sse.py           # SSE event formatting
│   │   └── repositories/        # Data access
│   │       └── history_store.py # In-memory store for /api/history
│   ├── requirements.txt
│   └── .env.example
├── src/
│   ├── components/          # React UI components
│   ├── hooks/
│   │   ├── useAnalysis.ts   # SSE streaming hook
│   │   └── useSavedAnalyses.ts
│   ├── pages/               # Route pages
│   ├── types/analysis.ts    # Shared TypeScript types
│   └── data/mockData.ts     # Example data for demos
├── index.html
├── vite.config.ts
├── tailwind.config.ts
└── package.json
```

## API Endpoints

| Method | Path             | Description                                                |
| ------ | ---------------- | ---------------------------------------------------------- |
| POST   | `/api/prepare`   | Accepts `{ jobDescription }`, returns SSE stream           |
| GET    | `/api/health`    | Health check                                               |
| GET    | `/api/history`   | List all saved analyses (newest first)                     |
| POST   | `/api/history`   | Save an analysis (`{ jobDescription, results }`)           |
| GET    | `/api/history/{id}` | Get one saved analysis by id                            |
| DELETE | `/api/history/{id}` | Delete a saved analysis                                |

History is stored in memory on the backend (no persistence across restarts unless you replace the store with a database). The frontend uses these endpoints when available and falls back to localStorage when the API is unavailable.

When deployed as a full-stack app (e.g. Heroku), the same server also serves the frontend: static assets at `/assets/*`, root-level files (e.g. favicon, `robots.txt`), and `index.html` for all other paths (SPA routing). API routes remain under `/api/*`.

## Backend testing

From the `backend` directory with your venv activated:

```bash
cd backend
source .venv/bin/activate   # if not already
pytest
```

Run only unit or integration tests:

```bash
pytest tests/unit -v
pytest tests/integration -v
```

Tests use mocks for the You.com API; no real API key is needed in CI (a dummy key is set in `tests/conftest.py`).

## You.com API Usage

The backend uses the [documented You.com APIs](https://documentation.you.com/):

- **Search** — Tries `GET https://ydc-index.io/v1/search` (query, count). If that returns 403, it falls back to the legacy `GET https://api.ydc-index.io/search` (query, num_web_results). Both use the `X-API-Key` header.
- **Synthesis** — `POST https://api.you.com/v1/agents/runs` (Express Agent) with `Authorization: Bearer <key>` and body `{ agent: "express", input, stream: false }` to produce the structured interview prep JSON.

Get a free API key at [you.com/platform](https://you.com/platform).

### Troubleshooting 403 / 404

- **403 on Search** — Ensure your key is from [you.com/platform](https://you.com/platform). The app will automatically retry with the legacy search URL. You can force the legacy endpoint by setting `YOU_SEARCH_URL=https://api.ydc-index.io/search` in `.env` (and the client will use `num_web_results` for that URL).
- **404 on synthesis** — The app uses the Express Agent at `api.you.com/v1/agents/runs`. If you see 404 or 403, check that your key has access to the Agents API or contact [api@you.com](mailto:api@you.com).

## Heroku Deployment (Full-Stack)

This app is configured to deploy as a full-stack application on Heroku, serving both the React frontend and FastAPI backend from a single dyno.

### Prerequisites

1. Heroku CLI installed
2. Heroku account
3. Git repository

### Setup Steps

1. **Create a Heroku app** (if you haven't already):
   ```bash
   heroku create your-app-name
   ```

2. **Set buildpacks** (Node.js first, then Python):
   ```bash
   heroku buildpacks:add heroku/nodejs --index 1
   heroku buildpacks:add heroku/python --index 2
   ```
   
   Or use the `.buildpacks` file (already included) - Heroku will read it automatically.

3. **Set environment variables** (from your `backend/.env`):
   ```bash
   heroku config:set YOU_API_KEY=your_api_key_here
   # Add any other env vars you need (YOU_SEARCH_URL, etc.)
   ```

4. **Important: Enable dev dependencies for build**:
   ```bash
   heroku config:set NPM_CONFIG_PRODUCTION=false
   ```
   This ensures Vite and other build tools (in devDependencies) are installed during the build.

5. **Deploy**:
   ```bash
   git push heroku main
   # or
   git push heroku master
   ```

### How It Works

- **Build phase**: Node.js buildpack installs dependencies and runs `npm run build` (via `heroku-postbuild` script), creating the `dist/` folder
- **Python phase**: Python buildpack installs backend dependencies from `requirements.txt`
- **Runtime**: FastAPI serves:
  - API routes at `/api/*`
  - Static frontend files from `dist/`
  - `index.html` for all other routes (SPA routing)

### Troubleshooting

- **Build fails with "vite: command not found"**: Make sure `NPM_CONFIG_PRODUCTION=false` is set
- **Frontend not loading**: Check that `dist/` was created during build (check build logs)
- **API routes return 404**: Ensure your routes are prefixed with `/api/` in the frontend code

## License

MIT
