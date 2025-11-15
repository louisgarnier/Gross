# Project Structure

## Directory Layout

```
gross/
├── README.md                 # Project overview
├── PROJECT_STRUCTURE.md      # This file
├── GIT_WORKFLOW.md          # Version control guidelines
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
│
├── backend/                 # Python backend
│   ├── PLAN.md             # Backend development plan
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI/Flask application entry
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py   # API endpoints
│   │   ├── scrapers/       # Web scrapers for each source
│   │   │   ├── __init__.py
│   │   │   ├── base.py     # Base scraper class
│   │   │   ├── finviz.py
│   │   │   ├── morningstar.py
│   │   │   ├── yahoo.py
│   │   │   ├── quickfs.py
│   │   │   ├── koyfin.py
│   │   │   └── macrotrends.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ratio_fetcher.py  # Orchestrates scraping
│   │   │   └── validator.py      # Validates and compares data
│   │   └── models/
│   │       ├── __init__.py
│   │       └── schemas.py   # Pydantic models for API
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_scrapers.py
│   │   ├── test_api.py
│   │   └── test_services.py
│   ├── requirements.txt    # Backend-specific dependencies
│   └── .env.example        # Environment variables template
│
└── frontend/               # Nuxt 3 frontend
    ├── PLAN.md            # Frontend development plan
    ├── nuxt.config.ts     # Nuxt configuration
    ├── package.json      # Frontend dependencies
    ├── app.vue           # Root component
    ├── pages/
    │   ├── index.vue     # Stock Analysis page (main)
    │   ├── batch.vue     # Batch Analysis page
    │   └── filter.vue    # Stock Filter page
    ├── components/
    │   ├── StockInput.vue      # Ticker input component
    │   ├── SummaryTable.vue    # Main results table
    │   ├── MetricRow.vue       # Individual metric row
    │   ├── StatusBadge.vue     # Pass/Fail/Info badge
    │   └── OverallScore.vue    # Overall score display
    ├── composables/
    │   ├── useStockAnalysis.ts # Stock analysis logic
    │   └── useApi.ts           # API client
    ├── types/
    │   └── stock.ts            # TypeScript interfaces
    ├── tests/
    │   ├── components/
    │   └── composables/
    └── .env.example       # Frontend environment variables
```

## Key Files Description

### Backend
- `app/main.py`: FastAPI application initialization and middleware
- `app/api/routes.py`: REST API endpoints (GET /api/analyze/{ticker})
- `app/services/ratio_fetcher.py`: Coordinates scraping from all sources
- `app/services/validator.py`: Compares values across sources, calculates averages

### Frontend
- `pages/index.vue`: Main Stock Analysis page (matches the provided UI design)
- `components/SummaryTable.vue`: Displays the metric table with Value, Target, Status columns
- `composables/useStockAnalysis.ts`: Handles API calls and state management

## Environment Variables

### Backend (.env)
```
API_HOST=localhost
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

