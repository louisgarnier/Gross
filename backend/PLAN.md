# Backend Development Plan

## Overview
Build a Python backend API that scrapes financial ratios from multiple sources and provides a unified REST API for the frontend.

## Technology Stack
- **Framework**: FastAPI (lightweight, fast, automatic docs)
- **Scraping**: BeautifulSoup4, Requests
- **Data Validation**: Pydantic
- **Testing**: pytest

## Step-by-Step Implementation

### Phase 1: Environment Setup ✅ (Validation Required)

#### Step 1.1: Create Virtual Environment
- [ ] Create Python virtual environment: `python -m venv venv`
- [ ] Activate virtual environment
- [ ] Verify Python version (3.9+)

#### Step 1.2: Install Dependencies
- [ ] Update `requirements.txt` with:
  ```
  fastapi>=0.104.0
  uvicorn>=0.24.0
  requests>=2.31.0
  beautifulsoup4>=4.12.0
  lxml>=4.9.0
  pydantic>=2.5.0
  pytest>=7.4.0
  pytest-asyncio>=0.21.0
  ```
- [ ] Run `pip install -r requirements.txt`
- [ ] Verify all packages installed

#### Step 1.3: Project Structure
- [ ] Create `backend/app/` directory
- [ ] Create `backend/app/scrapers/` directory
- [ ] Create `backend/app/services/` directory
- [ ] Create `backend/app/api/` directory
- [ ] Create `backend/app/models/` directory
- [ ] Create `backend/tests/` directory

**Validation Checkpoint**: Confirm directory structure matches PROJECT_STRUCTURE.md

---

### Phase 2: Base Scraper Infrastructure ✅ (Validation Required)

#### Step 2.1: Base Scraper Class
- [ ] Create `app/scrapers/base.py`
- [ ] Implement `BaseScraper` class with:
  - HTTP session management
  - `fetch_page(url)` method
  - `extract_number(text)` helper
  - `clean_ticker(ticker)` helper
  - Error handling and retries
- [ ] Add docstrings
- [ ] Write unit tests in `tests/test_scrapers.py`

**Validation Checkpoint**: Review base scraper code, approve before proceeding

---

### Phase 3: Individual Scraper Implementation ✅ (Validation Required)

#### Step 3.1: Finviz Scraper
- [ ] Create `app/scrapers/finviz.py`
- [ ] Implement `get_gross_margin(ticker)` method
- [ ] Implement `get_pe_ratio(ticker)` method
- [ ] Test with real ticker (e.g., AAPL)
- [ ] Handle edge cases (invalid ticker, missing data)

#### Step 3.2: Morningstar Scraper
- [ ] Create `app/scrapers/morningstar.py`
- [ ] Implement `get_gross_margin(ticker)` method
- [ ] Implement `get_roic(ticker)` method
- [ ] Implement `get_interest_coverage(ticker)` method
- [ ] Implement `get_pe_ratio(ticker)` method
- [ ] Handle exchange detection (NASDAQ, NYSE, etc.)
- [ ] Test with real ticker

#### Step 3.3: Yahoo Finance Scraper
- [ ] Create `app/scrapers/yahoo.py`
- [ ] Implement `get_interest_coverage(ticker)` method
  - Fetch Income Statement
  - Extract Operating Income
  - Extract Interest Expense
  - Calculate: Operating Income / Interest Expense
- [ ] Implement `get_pe_ratio(ticker)` method
- [ ] Test with real ticker

#### Step 3.4: QuickFS Scraper
- [ ] Create `app/scrapers/quickfs.py`
- [ ] Implement `get_roic(ticker)` method
- [ ] Implement `get_fcf_margin(ticker)` method
- [ ] Test with real ticker

#### Step 3.5: Koyfin Scraper
- [ ] Create `app/scrapers/koyfin.py`
- [ ] Implement `get_roic(ticker)` method
- [ ] Implement `get_fcf_margin(ticker)` method
- [ ] Implement `get_interest_coverage(ticker)` method
- [ ] Test with real ticker

#### Step 3.6: Macrotrends Scraper
- [ ] Create `app/scrapers/macrotrends.py`
- [ ] Implement `get_gross_margin(ticker)` method
- [ ] Implement `get_fcf_margin(ticker)` method
- [ ] Handle historical data tables
- [ ] Test with real ticker

**Validation Checkpoint**: Test each scraper individually, verify data extraction works

---

### Phase 4: Data Aggregation Service ✅ (Validation Required)

#### Step 4.1: Ratio Fetcher Service
- [ ] Create `app/services/ratio_fetcher.py`
- [ ] Implement `RatioFetcher` class
- [ ] Create method `fetch_gross_margin(ticker)` that:
  - Calls Finviz, Morningstar, Macrotrends
  - Returns list of values with source names
- [ ] Create similar methods for:
  - `fetch_roic(ticker)`
  - `fetch_fcf_margin(ticker)`
  - `fetch_interest_coverage(ticker)`
  - `fetch_pe_ratio(ticker)`
- [ ] Implement parallel fetching (asyncio) for speed
- [ ] Add timeout handling

#### Step 4.2: Data Validator Service
- [ ] Create `app/services/validator.py`
- [ ] Implement `Validator` class
- [ ] Create `compare_sources(values, sources)` method:
  - Calculate average of all values
  - Calculate standard deviation
  - Flag outliers (>2 standard deviations)
  - Return consensus value (median or average)
- [ ] Create `validate_ratio(ratio_name, value, target)` method:
  - Compare value against target threshold
  - Return pass/fail status
- [ ] Define target thresholds:
  - Gross Margin: >60%
  - ROIC: >10-12%
  - FCF Margin: >20%
  - Interest Coverage: ≥3-4x
  - P/E Ratio: Info only (no pass/fail)

**Validation Checkpoint**: Test aggregation and validation logic with sample data

---

### Phase 5: API Layer ✅ (Validation Required)

#### Step 5.1: Data Models
- [ ] Create `app/models/schemas.py`
- [ ] Define Pydantic models:
  ```python
  class SourceValue(BaseModel):
      source: str
      value: float | None
  
  class RatioResult(BaseModel):
      metric: str
      values: List[SourceValue]
      consensus: float | None
      target: str
      status: str  # "Pass", "Fail", "Info Only"
  
  class AnalysisResponse(BaseModel):
      ticker: str
      ratios: List[RatioResult]
      overall_score: int
      max_score: int
  ```

#### Step 5.2: API Routes
- [ ] Create `app/api/routes.py`
- [ ] Implement `GET /api/analyze/{ticker}` endpoint:
  - Accept ticker parameter
  - Call RatioFetcher for all ratios
  - Call Validator for each ratio
  - Calculate overall score (count of passes)
  - Return AnalysisResponse
- [ ] Add error handling (invalid ticker, network errors)
- [ ] Add request validation
- [ ] Add response caching (optional, for performance)

#### Step 5.3: FastAPI Application
- [ ] Create `app/main.py`
- [ ] Initialize FastAPI app
- [ ] Configure CORS (allow frontend origin)
- [ ] Include API routes
- [ ] Add health check endpoint: `GET /health`
- [ ] Add API documentation (auto-generated by FastAPI)

**Validation Checkpoint**: Test API endpoints with Postman/curl, verify JSON responses

---

### Phase 6: Testing ✅ (Validation Required)

#### Step 6.1: Unit Tests
- [ ] Write tests for each scraper in `tests/test_scrapers.py`
- [ ] Write tests for services in `tests/test_services.py`
- [ ] Write tests for API endpoints in `tests/test_api.py`
- [ ] Achieve >80% code coverage

#### Step 6.2: Integration Tests
- [ ] Test full flow: ticker → API → scrapers → response
- [ ] Test error scenarios (invalid ticker, network failure)
- [ ] Test with multiple real tickers (AAPL, MSFT, GOOGL)

**Validation Checkpoint**: All tests pass, review test coverage

---

### Phase 7: Documentation & Deployment Prep ✅ (Validation Required)

#### Step 7.1: Documentation
- [ ] Add docstrings to all functions/classes
- [ ] Create `backend/README.md` with setup instructions
- [ ] Document API endpoints

#### Step 7.2: Environment Configuration
- [ ] Create `.env.example` file
- [ ] Document required environment variables
- [ ] Add `.env` to `.gitignore`

**Validation Checkpoint**: Review documentation, approve for Git commit

---

## Testing Strategy

### Manual Testing Checklist
- [ ] Test each scraper with valid ticker (AAPL)
- [ ] Test each scraper with invalid ticker
- [ ] Test API endpoint with valid ticker
- [ ] Test API endpoint with invalid ticker
- [ ] Verify CORS works with frontend
- [ ] Check API response format matches frontend expectations

### Automated Testing
- [ ] Unit tests for all scrapers
- [ ] Unit tests for services
- [ ] Integration tests for API
- [ ] Mock external HTTP requests in tests

## Error Handling

- Network timeouts: Return partial data if some sources fail
- Invalid ticker: Return 404 with error message
- Missing data: Return None for that source, continue with others
- Rate limiting: Implement exponential backoff

## Performance Considerations

- Use asyncio for parallel scraping
- Implement request caching (optional)
- Set reasonable timeouts (10 seconds per source)
- Return partial results if some sources are slow

