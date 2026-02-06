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

- **Search API** (`GET https://api.ydc-index.io/search`) -- company news, tech stack research
- **Chat Completions** (`POST https://api.you.com/v1/chat/completions`) -- synthesises research into structured interview prep

## License

MIT
