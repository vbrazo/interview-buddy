# Interview Buddy

AI-powered interview preparation tool that transforms job descriptions into comprehensive, citation-backed research reports. Paste a job description, and get real-time company intelligence, technology deep-dives, interview focus areas, and practice questions -- all backed by live web research via the You.com APIs.

## Tech Stack

| Layer    | Technology                                          |
| -------- | --------------------------------------------------- |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui |
| Backend  | Python 3.11+, FastAPI, uvicorn                      |
| APIs     | You.com Search API, You.com Chat Completions        |

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
4. **You.com Chat Completions** synthesises all research into a structured report.
5. The frontend streams progress in real-time via **Server-Sent Events**.
6. You get a full interview prep report you can save, copy, or export as Markdown.

## Project Structure

```
interview-buddy/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # App factory, middleware, lifespan
│   │   ├── config.py        # Centralised settings (env vars)
│   │   ├── models.py        # Pydantic request/response models
│   │   ├── routes.py        # API route handlers
│   │   ├── pipeline.py      # Analysis pipeline orchestrator
│   │   ├── you_client.py    # You.com API client (Search + Chat)
│   │   ├── job_parser.py    # Job description metadata extractor
│   │   ├── prompts.py       # LLM prompt templates
│   │   └── sse.py           # SSE event formatting helpers
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

| Method | Path           | Description                                      |
| ------ | -------------- | ------------------------------------------------ |
| POST   | `/api/prepare` | Accepts `{ jobDescription }`, returns SSE stream |
| GET    | `/api/health`  | Health check                                     |

## You.com API Usage

The backend uses the [documented You.com APIs](https://documentation.you.com/):

- **Search** — Tries `GET https://ydc-index.io/v1/search` (query, count). If that returns 403, it falls back to the legacy `GET https://api.ydc-index.io/search` (query, num_web_results). Both use the `X-API-Key` header.
- **Synthesis** — `POST https://chat-api.you.com/smart` (Smart API, legacy) with `X-API-Key` and body `{ query, chat_id, instructions }` to produce the structured interview prep JSON.

Get a free API key at [you.com/platform](https://you.com/platform). For Smart API access, you may need to contact [api@you.com](mailto:api@you.com) if you see 403 on the `/smart` endpoint.

### Troubleshooting 403 / 404

- **403 on Search** — Ensure your key is from [you.com/platform](https://you.com/platform). The app will automatically retry with the legacy search URL. You can force the legacy endpoint by setting `YOU_SEARCH_URL=https://api.ydc-index.io/search` in `.env` (and the client will use `num_web_results` for that URL).
- **404 on synthesis** — The app uses the Smart API at `chat-api.you.com/smart`, not `api.you.com/v1/chat/completions`. If you still see 404, check that your key has Smart/Research access or email [api@you.com](mailto:api@you.com).

## License

MIT
