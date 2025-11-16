# Execution Order - Master Plan

This document defines the sequential order of execution for all phases across backend and frontend development.

## Overview

**Strategy**: **Parallel Development with Iterative Testing** - Build backend API skeleton with mock data first, then develop frontend and backend scrapers in parallel. Each scraper can be tested immediately through the frontend interface as it's built. This allows for continuous validation and faster feedback loops.

## Execution Sequence

### 🟢 Phase 0: Project Initialization
**Status**: ✅ COMPLETED
- [x] Create documentation files (README, PLANS, etc.)
- [x] Define project structure
- [x] Establish Git workflow

**Next**: Initialize Git repository and clean up existing code

---

### 🔵 Phase 1: Foundation Setup (Backend + Frontend in Parallel) ✅
**Dependencies**: None  
**Duration**: ~3-4 validation cycles  
**Status**: ✅ COMPLETED

#### 1.1: Backend Environment Setup
- [x] Create virtual environment ✅
- [x] Install dependencies ✅
- [x] Create project directory structure ✅
- [x] Initialize Git repository (if not done) ✅

**Validation**: ✅ Directory structure matches PROJECT_STRUCTURE.md

#### 1.2: Frontend Environment Setup (Parallel with 1.1)
- [x] Initialize Nuxt 3 project ✅
- [x] Install dependencies (Tailwind, etc.) ✅
- [x] Create project directory structure ✅
- [x] Configure environment variables ✅

**Validation**: ✅ Both backend and frontend environments ready

#### 1.3: Base Scraper Infrastructure
- [x] Create `app/scrapers/base.py` ✅
- [x] Implement BaseScraper class ✅
- [ ] Write unit tests (optional for now)

**Validation**: ✅ Base scraper code reviewed and approved

---

### 🟢 Phase 2: API Contract & Mock Data (CRITICAL - Enables Parallel Dev)
**Dependencies**: Phase 1 complete  
**Duration**: ~2-3 validation cycles

**What we're doing:**
We're creating a "contract" between the backend and frontend - like a menu at a restaurant. The menu (API contract) tells the frontend exactly what data it will receive from the backend. We'll use fake data (mock data) first so the frontend can be built and tested before we have real scrapers working.

**Why this is important:**
- Frontend and backend can work in parallel (frontend doesn't wait for scrapers)
- We can test the UI immediately with sample data
- When we build scrapers later, we just swap mock data for real data
- Everything stays organized and predictable

**IMPORTANT - What to Expect:**
- ✅ API structure is complete (all 5 ratios, all 3 sources per ratio)
- ✅ Some mock values (PLTR has Finviz Gross Margin and P/E)
- ⚠️ **Most values are NULL** - This is EXPECTED and CORRECT for Phase 2
- ⚠️ **Real scrapers come in Phase 4** - That's when we'll fill in all the null values
- ⚠️ **Phase 2 goal**: Test that the API structure works, not that all data is present

---

#### 2.1: Define API Contract (Backend)
**What:** Create a "data structure definition" - like a blueprint that says "the API will return data in this exact format"

**Why:** So frontend knows what to expect. Like a contract: "I promise to give you data that looks like this"

**Steps:**
- [x] Create `app/models/schemas.py` - This file defines the data structure ✅
- [x] Define Pydantic models for API responses - Pydantic is like a validator that ensures data matches the structure ✅
- [x] Document exact response format - Write down what the response will look like ✅
- [x] Create sample mock data matching the schema - Create fake data that matches our structure (for PLTR and NVDA) ✅

**Example:** The API will return:
```json
{
  "ticker": "PLTR",
  "ratios": [
    {
      "metric": "Gross Margin",
      "values": [{"source": "Finviz", "value": 80.81}, ...],
      "consensus": 80.81,
      "target": ">60%",
      "status": "Pass"
    }
  ],
  "overall_score": 2,
  "max_score": 4
}
```

**Validation**: ⏳ **PENDING USER VALIDATION** - User confirmed Finviz values match (80.81%, 406.95)

**IMPORTANT - About Null Values:**
- Most source values are `null` - This is EXPECTED for Phase 2
- We only have mock data for Finviz (PLTR Gross Margin and P/E)
- Other sources (Morningstar, Macrotrends, QuickFS, Koyfin, Yahoo) will be `null` until Phase 4
- **This is correct** - Phase 2 is about API structure, not complete data

**Validation Steps:**
1. [x] Open https://finviz.com/quote.ashx?t=PLTR - ✅ **DONE**
2. [x] Check Gross Margin value on Finviz - ✅ **80.81%**
3. [x] Compare with mock data (80.81%) - ✅ **MATCHES**
4. [x] Check P/E Ratio value on Finviz - ✅ **406.95**
5. [x] Compare with mock data (406.95) - ✅ **MATCHES**
6. [x] If match: ✅ Verified | If not: Update mock_data.py - ✅ **VERIFIED**
7. [x] **Verify**: Null values for other sources are expected and OK - ✅ **CONFIRMED**

---

#### 2.2: API Skeleton with Mock Data (Backend)
**What:** Create the actual API server that the frontend will call. For now, it returns fake data (mock data) instead of scraping real websites.

**Why:** 
- Frontend can start working immediately (doesn't need real scrapers yet)
- We can test the connection between frontend and backend
- When scrapers are ready, we just swap mock data for real data

**Steps:**
- [x] Create `app/main.py` (FastAPI app) - This starts the web server ✅
- [x] Create `app/api/routes.py` - This defines the API endpoints (like `/api/analyze/PLTR`) ✅
- [x] Implement `GET /api/analyze/{ticker}` endpoint - When frontend calls this, it gets data back ✅
- [x] Return mock data matching the schema - Return our fake data in the correct format ✅
- [x] Configure CORS for frontend - Allow frontend (running on port 3001) to talk to backend (port 8000) ✅
- [x] Add health check endpoint - A simple endpoint to test if backend is running ✅

**Example:** When frontend calls `http://localhost:8000/api/analyze/PLTR`, backend returns mock PLTR data

**Validation**: ✅ **VALIDATED** - All API endpoints tested and working

**Required Tests (USER TESTED):**
1. [x] Health check works: http://localhost:8000/api/health - ✅ **PASSED**
2. [x] PLTR API works: http://localhost:8000/api/analyze/PLTR - ✅ **PASSED**
3. [x] NVDA API works: http://localhost:8000/api/analyze/NVDA - ✅ **PASSED**
4. [x] MSFT API works: http://localhost:8000/api/analyze/MSFT (returns structure) - ✅ **PASSED**
5. [x] Run automated test: `cd backend && python3 test_phase2_api.py` - ✅ **ALL 5 TESTS PASSED**
6. [x] All tests pass before proceeding - ✅ **VALIDATED**

**To Test:**
1. Start backend: `cd backend && source venv/bin/activate && uvicorn app.main:app --reload`
2. Run test: `python3 test_phase2_api.py` (in backend directory)
3. Or test manually: Open http://localhost:8000/api/analyze/PLTR in browser
4. Test other stocks: http://localhost:8000/api/analyze/MSFT (returns structure with None values - expected until scrapers built)

---

#### 2.3: Frontend Type Definitions (Parallel with 2.1)
**What:** Create TypeScript "types" that match the backend data structure. Like creating a template that says "this is what the data will look like"

**Why:** 
- TypeScript can check if we're using the data correctly
- Prevents bugs (like trying to access a field that doesn't exist)
- Makes code easier to understand

**Steps:**
- [x] Create `types/stock.ts` - File that defines the data types ✅
- [x] Define TypeScript interfaces matching API contract - Create types that match what backend promises to send ✅
- [x] Verify types match backend schemas - Make sure frontend and backend agree on data structure ✅

**Example:** Define that `AnalysisResponse` has `ticker: string`, `ratios: RatioResult[]`, etc.

**Validation**: ✅ **VALIDATED** - Types match backend schemas

**Validation Steps (VERIFIED):**
1. [x] Compare `frontend/types/stock.ts` with `backend/app/models/schemas.py` - ✅ **DONE**
2. [x] Verify all fields match - ✅ **ALL MATCH**
3. [x] Verify types are correct (string, number, null, etc.) - ✅ **COMPATIBLE**
4. [x] If match: ✅ Verified | If not: Fix types - ✅ **VERIFIED**

---

#### 2.4: Frontend API Integration (Parallel with 2.2)
**What:** Create code in the frontend that can call the backend API and handle the response.

**Why:** 
- Frontend needs a way to request data from backend
- Need to handle loading states, errors, etc.
- This connects the UI to the backend

**Steps:**
- [x] Create `composables/useApi.ts` - A reusable function to make API calls ✅
- [x] Implement API client functions - Functions like `analyzeStock(ticker)` that call the backend ✅
- [x] Connect to backend API (with mock data) - Test that frontend can talk to backend ✅
- [x] Create `composables/useStockAnalysis.ts` - Manages the state (what ticker is selected, what data we have, etc.) ✅
- [ ] Test API calls with mock data - Verify frontend can fetch and display the mock data ⏳

**Example:** When user clicks "PLTR" button, frontend calls backend API, gets mock PLTR data, displays it in the table

**Validation**: ✅ **VALIDATED** - Frontend-backend connection tested and working

**Required Tests (USER TESTED):**
1. [x] Backend running on port 8000 - ✅ **RUNNING**
2. [x] Frontend running on port 3001 - ✅ **RUNNING**
3. [x] Open http://localhost:3001 - ✅ **ACCESSIBLE**
4. [x] Check browser console (F12) for errors - ✅ **NO ERRORS**
5. [x] No CORS errors in browser console - ✅ **NO CORS ERRORS**
6. [x] Frontend can make API calls - ✅ **TESTED** (Health check ✅, NVDA API ✅)
7. [x] API calls return correct data structure - ✅ **VERIFIED** (JSON structure correct)
8. [x] All tests pass before proceeding - ✅ **VALIDATED**

**To Test:**
1. Start backend (port 8000)
2. Start frontend: `cd frontend && npm run dev` (runs on port 3001)
3. Open http://localhost:3001
4. Test API connection (will need UI components from Phase 3)

---

### 🟡 Phase 3: UI Components (Frontend - Can Start Immediately)
**Dependencies**: Phase 2.3 and 2.4 complete (types + API integration)  
**Duration**: ~5-6 validation cycles

**Note**: These can be built and tested with mock data while scrapers are being developed.

1. **StatusBadge Component**
   - [x] Create component ✅
   - [x] Add styling (Pass/Fail/Info Only) ✅
   - [x] Test with mock data ✅ **USER CONFIRMED** (Pass ✓, Fail ✗, Info Only ℹ)

2. **OverallScore Component**
   - [x] Create component ✅
   - [x] Add styling and indicators ✅
   - [x] Test with mock data ✅ **USER CONFIRMED** (1/4 with warning ⚠)

3. **StockInput Component**
   - [x] Create component ✅
   - [x] Add form validation ✅
   - [x] Add loading states ✅
   - [x] Test user interaction ✅ **USER CONFIRMED** (PLTR input works)

4. **MetricRow Component**
   - [x] Create component ✅
   - [x] Integrate StatusBadge ✅
   - [x] Add formatting for values ✅
   - [x] Test with mock data ✅ **USER CONFIRMED** (Values formatted correctly: 80.81%, 406.95)

5. **SummaryTable Component**
   - [x] Create component ✅
   - [x] Integrate MetricRow ✅
   - [x] Add table styling ✅
   - [x] Test with full mock dataset ✅ **USER CONFIRMED** (All 5 metrics displayed)

6. **Main Stock Analysis Page**
   - [x] Create `pages/index.vue` ✅
   - [x] Integrate all components ✅
   - [x] Connect to useStockAnalysis composable ✅
   - [x] Add loading and error states ✅
   - [x] Match UI design ✅ **USER CONFIRMED** (Navigation, table, input all working)

**Validation**: ✅ **VALIDATED** - All components working correctly with mock data, UI matches design

---

### 🔴 Phase 4: Iterative Scraper Development (Test Each API Call & Verify Data)
**Dependencies**: Phase 2.2 complete (API skeleton ready)  
**Duration**: ~6-8 validation cycles (one per scraper)

**Strategy**: 
1. Build one scraper at a time
2. **TEST API CALL** - Verify scraper returns data
3. **VERIFY AGAINST SOURCE WEBSITE** - Compare scraper value with actual website
4. **ONLY IF VERIFIED** - Integrate into API
5. Test through frontend

#### 4.1: Finviz Scraper - Gross Margin (Start Here)
- [x] Create `app/scrapers/finviz.py` ✅
- [x] Implement `get_gross_margin(ticker)` method ✅
- [x] **TEST API CALL**: Test scraper with PLTR → Get value ✅ (80.81%)
- [x] **TEST API CALL**: Test scraper with NVDA → Get value ✅ (69.85%)
- [x] **VERIFY SOURCE**: Open https://finviz.com/quote.ashx?t=PLTR → Check Gross Margin ✅ **USER CONFIRMED** (80.81%)
- [x] **VERIFY SOURCE**: Open https://finviz.com/quote.ashx?t=NVDA → Check Gross Margin ✅ **USER CONFIRMED** (69.85%)
- [x] **COMPARE**: Does scraper value match website? ✅ **VERIFIED**
- [x] If match: ✅ Verified, proceed to integrate ✅
- [x] **ONLY AFTER VERIFICATION**: Integrate into API ✅
- [x] Test through frontend ✅ **USER CONFIRMED** (Frontend displays real Finviz data)

**Validation**: ✅ **COMPLETE** - Scraper verified, integrated, and tested through frontend. Real data displaying correctly.

#### 4.2: Finviz Scraper - P/E Ratio
- [x] Implement `get_pe_ratio(ticker)` method in finviz.py ✅ (Already implemented)
- [x] **TEST API CALL**: Test scraper with PLTR → Get value ✅ (406.95)
- [x] **TEST API CALL**: Test scraper with NVDA → Get value ✅ (54.13)
- [x] **VERIFY SOURCE**: Open https://finviz.com/quote.ashx?t=PLTR → Check P/E Ratio ✅ **USER CONFIRMED** (406.95)
- [x] **VERIFY SOURCE**: Open https://finviz.com/quote.ashx?t=NVDA → Check P/E Ratio ✅ **USER CONFIRMED** (54.13)
- [x] **COMPARE**: Does scraper value match website? ✅ **VERIFIED**
- [x] If match: ✅ Verified, proceed to integrate ✅
- [x] **ONLY AFTER VERIFICATION**: Integrate into API ✅ (Already integrated in ratio_fetcher)
- [x] Test through frontend ✅ **USER CONFIRMED**

**Validation**: ✅ **COMPLETE** - Scraper verified, integrated, and tested through frontend. Real data displaying correctly.

#### 4.3: Yahoo Finance Scraper - Interest Coverage
- [x] Create `app/scrapers/yahoo.py` ✅ (Using yfinance library)
- [x] Implement `get_interest_coverage(ticker)` method ✅ (Using **ANNUAL** data for consistency)
- [x] **TEST API CALL**: Test scraper with PLTR → Get value ✅ (None - no debt, expected)
- [x] **TEST API CALL**: Test scraper with NVDA → Get value ✅ (~341x using Annual data)
- [x] **POLICY CHANGE**: Changed from TTM to Annual for consistency with other sources ✅
- [x] **VERIFY SOURCE**: Open https://finance.yahoo.com/quote/NVDA/financials → Check EBIT Annual and Interest Expense Annual ✅ **USER VERIFIED**
- [x] **COMPARE**: Does scraper value match website? ✅ **YES** - Using Annual data matches Yahoo Finance
- [x] **ONLY AFTER VERIFICATION**: Integrate into API ✅ (Already integrated in ratio_fetcher)
- [ ] Test through frontend ⏳

**Validation**: ✅ **COMPLETE** - Scraper uses **ANNUAL** data (not TTM) for consistency with Finviz and other sources. Verified by user. See `DATA_PERIOD_POLICY.md` for details.

#### 4.4: Yahoo Finance Scraper - P/E Ratio
- [x] Implement `get_pe_ratio(ticker)` method in yahoo.py ✅ (Using trailingPE)
- [x] **TEST API CALL**: Test scraper with PLTR → Get value ✅
- [x] **TEST API CALL**: Test scraper with NVDA → Get value ✅ (54.03, expected ~54.18)
- [x] **VERIFY SOURCE**: Open https://finance.yahoo.com/quote/NVDA → Check Trailing P/E ✅ **VERIFIED**
- [x] **COMPARE**: Does scraper value match website? ✅ **YES** - 54.03 matches 54.18 on Yahoo Finance
- [x] **NOTE**: P/E Ratio uses trailingPE (TTM-based) as this is industry standard for P/E ratios
- [x] **ONLY AFTER VERIFICATION**: Integrate into API ✅ (Already integrated in ratio_fetcher)
- [ ] Test through frontend ⏳

**Validation**: ✅ **COMPLETE** - Scraper uses trailingPE (TTM-based) which is standard for P/E ratios. Other ratios use Annual data (see `DATA_PERIOD_POLICY.md`).

#### 4.5: Macrotrends Scraper - Gross Margin
- [ ] Create `app/scrapers/macrotrends.py`
- [ ] Implement `get_gross_margin(ticker)` method
- [ ] **TEST API CALL**: Test scraper with PLTR → Get value
- [ ] **VERIFY SOURCE**: Open https://www.macrotrends.net/stocks/charts/PLTR/palantir/gross-margin → Check Gross Margin
- [ ] **COMPARE**: Does scraper value match website?
- [ ] If match: ✅ Verified, proceed to integrate
- [ ] If no match: ❌ Fix scraper, re-test
- [ ] Repeat verification with NVDA
- [ ] **ONLY AFTER VERIFICATION**: Integrate into API
- [ ] Test through frontend

**Validation**: Macrotrends Gross Margin verified against source website

#### 4.6: Macrotrends Scraper - FCF Margin
- [ ] Implement `get_fcf_margin(ticker)` method in macrotrends.py
- [ ] **TEST API CALL**: Test scraper with PLTR → Get value
- [ ] **VERIFY SOURCE**: Open https://www.macrotrends.net/stocks/charts/PLTR/palantir/free-cash-flow-margin → Check FCF Margin
- [ ] **COMPARE**: Does scraper value match website?
- [ ] If match: ✅ Verified, proceed to integrate
- [ ] If no match: ❌ Fix scraper, re-test
- [ ] Repeat verification with NVDA
- [ ] **ONLY AFTER VERIFICATION**: Integrate into API
- [ ] Test through frontend

**Validation**: Macrotrends FCF Margin verified against source website

#### 4.7: QuickFS Scraper - ROIC
- [ ] Create `app/scrapers/quickfs.py`
- [ ] Implement `get_roic(ticker)` method
- [ ] **TEST API CALL**: Test scraper with PLTR → Get value
- [ ] **VERIFY SOURCE**: Open https://quickfs.net/company/PLTR → Check ROIC
- [ ] **COMPARE**: Does scraper value match website?
- [ ] If match: ✅ Verified, proceed to integrate
- [ ] If no match: ❌ Fix scraper, re-test
- [ ] Repeat verification with NVDA
- [ ] **ONLY AFTER VERIFICATION**: Integrate into API
- [ ] Test through frontend

**Validation**: QuickFS ROIC verified against source website

#### 4.8: QuickFS Scraper - FCF Margin
- [ ] Implement `get_fcf_margin(ticker)` method in quickfs.py
- [ ] **TEST API CALL**: Test scraper with PLTR → Get value
- [ ] **VERIFY SOURCE**: Open https://quickfs.net/company/PLTR → Check FCF Margin
- [ ] **COMPARE**: Does scraper value match website?
- [ ] If match: ✅ Verified, proceed to integrate
- [ ] If no match: ❌ Fix scraper, re-test
- [ ] Repeat verification with NVDA
- [ ] **ONLY AFTER VERIFICATION**: Integrate into API
- [ ] Test through frontend

**Validation**: QuickFS FCF Margin verified against source website

#### 4.9: Koyfin Scraper - ROIC
- [ ] Create `app/scrapers/koyfin.py`
- [ ] Implement `get_roic(ticker)` method
- [ ] **TEST API CALL**: Test scraper with PLTR → Get value
- [ ] **VERIFY SOURCE**: Open https://app.koyfin.com/company/PLTR/overview → Check ROIC
- [ ] **COMPARE**: Does scraper value match website?
- [ ] If match: ✅ Verified, proceed to integrate
- [ ] If no match: ❌ Fix scraper, re-test
- [ ] Repeat verification with NVDA
- [ ] **ONLY AFTER VERIFICATION**: Integrate into API
- [ ] Test through frontend

**Validation**: Koyfin ROIC verified against source website

#### 4.10: Koyfin Scraper - FCF Margin
- [ ] Implement `get_fcf_margin(ticker)` method in koyfin.py
- [ ] **TEST API CALL**: Test scraper with PLTR → Get value
- [ ] **VERIFY SOURCE**: Open https://app.koyfin.com/company/PLTR/overview → Check FCF Margin
- [ ] **COMPARE**: Does scraper value match website?
- [ ] If match: ✅ Verified, proceed to integrate
- [ ] If no match: ❌ Fix scraper, re-test
- [ ] Repeat verification with NVDA
- [ ] **ONLY AFTER VERIFICATION**: Integrate into API
- [ ] Test through frontend

**Validation**: Koyfin FCF Margin verified against source website

#### 4.11: Koyfin Scraper - Interest Coverage
- [ ] Implement `get_interest_coverage(ticker)` method in koyfin.py
- [ ] **TEST API CALL**: Test scraper with PLTR → Get value
- [ ] **VERIFY SOURCE**: Open https://app.koyfin.com/company/PLTR/financials → Check Interest Coverage
- [ ] **COMPARE**: Does scraper value match website?
- [ ] If match: ✅ Verified, proceed to integrate
- [ ] If no match: ❌ Fix scraper, re-test
- [ ] Repeat verification with NVDA
- [ ] **ONLY AFTER VERIFICATION**: Integrate into API
- [ ] Test through frontend

**Validation**: Koyfin Interest Coverage verified against source website

#### 4.12: Morningstar Scraper - Gross Margin
- [ ] Create `app/scrapers/morningstar.py`
- [ ] Implement `get_gross_margin(ticker)` method
- [ ] **TEST API CALL**: Test scraper with PLTR → Get value
- [ ] **VERIFY SOURCE**: Open https://www.morningstar.com/stocks/xnas/PLTR/quote → Check Gross Margin
- [ ] **COMPARE**: Does scraper value match website?
- [ ] If match: ✅ Verified, proceed to integrate
- [ ] If no match: ❌ Fix scraper, re-test
- [ ] Repeat verification with NVDA
- [ ] **ONLY AFTER VERIFICATION**: Integrate into API
- [ ] Test through frontend

**Validation**: Morningstar Gross Margin verified against source website

#### 4.13: Morningstar Scraper - ROIC
- [ ] Implement `get_roic(ticker)` method in morningstar.py
- [ ] **TEST API CALL**: Test scraper with PLTR → Get value
- [ ] **VERIFY SOURCE**: Open https://www.morningstar.com/stocks/xnas/PLTR/quote → Key Ratios → ROIC
- [ ] **COMPARE**: Does scraper value match website?
- [ ] If match: ✅ Verified, proceed to integrate
- [ ] If no match: ❌ Fix scraper, re-test
- [ ] Repeat verification with NVDA
- [ ] **ONLY AFTER VERIFICATION**: Integrate into API
- [ ] Test through frontend

**Validation**: Morningstar ROIC verified against source website

#### 4.14: Morningstar Scraper - Interest Coverage
- [ ] Implement `get_interest_coverage(ticker)` method in morningstar.py
- [ ] **TEST API CALL**: Test scraper with PLTR → Get value
- [ ] **VERIFY SOURCE**: Open https://www.morningstar.com/stocks/xnas/PLTR/quote → Key Ratios → Interest Coverage
- [ ] **COMPARE**: Does scraper value match website?
- [ ] If match: ✅ Verified, proceed to integrate
- [ ] If no match: ❌ Fix scraper, re-test
- [ ] Repeat verification with NVDA
- [ ] **ONLY AFTER VERIFICATION**: Integrate into API
- [ ] Test through frontend

**Validation**: Morningstar Interest Coverage verified against source website

#### 4.15: Morningstar Scraper - P/E Ratio
- [ ] Implement `get_pe_ratio(ticker)` method in morningstar.py
- [ ] **TEST API CALL**: Test scraper with PLTR → Get value
- [ ] **VERIFY SOURCE**: Open https://www.morningstar.com/stocks/xnas/PLTR/quote → Valuation → P/E Ratio
- [ ] **COMPARE**: Does scraper value match website?
- [ ] If match: ✅ Verified, proceed to integrate
- [ ] If no match: ❌ Fix scraper, re-test
- [ ] Repeat verification with NVDA
- [ ] **ONLY AFTER VERIFICATION**: Integrate into API
- [ ] Test through frontend

**Validation**: Morningstar P/E Ratio verified against source website, all sources working

---

### 🟢 Phase 5: Data Aggregation & Validation Services
**Dependencies**: Phase 4 complete (all scrapers working)  
**Duration**: ~2-3 validation cycles

#### 5.1: Ratio Fetcher Service (Enhance Existing)
- [ ] Enhance `app/services/ratio_fetcher.py`
- [ ] Implement parallel fetching from all 3 sources per ratio
- [ ] Add timeout handling
- [ ] Add error handling for failed sources
- [ ] **TEST THROUGH FRONTEND** - Verify all 3 sources show in UI

**Validation**: All 3 sources per ratio fetch correctly, display in frontend

#### 5.2: Data Validator Service
- [ ] Create `app/services/validator.py`
- [ ] Implement source comparison logic (average, median, outliers)
- [ ] Implement pass/fail validation against targets
- [ ] Define target thresholds:
  - Gross Margin: >60%
  - ROIC: >10-12%
  - FCF Margin: >20%
  - Interest Coverage: ≥3-4x
  - P/E Ratio: Info only
- [ ] Calculate overall score
- [ ] Update API to use validator
- [ ] **TEST THROUGH FRONTEND** - Verify pass/fail statuses and overall score

**Validation**: Validation logic works, status badges show correctly in frontend

---

### 🟣 Phase 6: Frontend Polish & Additional Features
**Dependencies**: Phase 5 complete  
**Duration**: ~3-4 validation cycles

#### 6.1: Navigation & Additional Pages
- [ ] Add navigation tabs component
- [ ] Create `pages/batch.vue` (placeholder for now)
- [ ] Create `pages/filter.vue` (placeholder for now)
- [ ] Test routing

#### 6.2: Enhanced UX
- [ ] Add loading skeletons
- [ ] Improve error messages
- [ ] Add animations/transitions
- [ ] Responsive design testing
- [ ] Accessibility improvements

#### 6.3: Display Source Comparison
- [ ] Show all 3 source values in UI (maybe tooltip or expandable row)
- [ ] Highlight consensus value
- [ ] Show if sources disagree significantly

**Validation**: UI polished, all features work, user experience validated

---

### 🔵 Phase 7: Testing & Documentation
**Dependencies**: Phase 6 complete  
**Duration**: ~3-4 validation cycles

#### 7.1: Backend Testing
- [ ] Write unit tests for all scrapers
- [ ] Write unit tests for services
- [ ] Write integration tests for API
- [ ] Achieve >80% code coverage

#### 7.2: Frontend Testing
- [ ] Write component tests
- [ ] Write composable tests
- [ ] Write integration tests
- [ ] Mock API responses in tests

#### 7.3: End-to-End Testing
- [ ] Test complete flow with multiple tickers
- [ ] Test error scenarios
- [ ] Performance testing
- [ ] Cross-browser testing

#### 7.4: Documentation
- [ ] Add docstrings to all functions
- [ ] Create `backend/README.md`
- [ ] Create `frontend/README.md`
- [ ] Document API endpoints
- [ ] Create `.env.example` files

**Validation**: All tests pass, documentation complete

---

### 🟡 Phase 8: Final Integration & Deployment Prep
**Dependencies**: Phase 7 complete  
**Duration**: ~2-3 validation cycles

#### 8.1: Final Bug Fixes
- [ ] Fix any remaining issues
- [ ] Optimize performance
- [ ] Security review

#### 8.2: Production Readiness
- [ ] Environment configuration
- [ ] Error logging setup
- [ ] Final documentation review

#### 8.3: Git Finalization
- [ ] Final commit
- [ ] Tag release
- [ ] Push to GitHub

**Validation**: Application ready for deployment

---

## Quick Reference: New Parallel Development Path

```
Phase 0 (Init) ✅
  ↓
Phase 1 (Both Backend + Frontend Setup in Parallel)
  ↓
Phase 2 (API Contract + Mock Data + Frontend Integration)
  ├─→ Backend: API skeleton with mocks
  └─→ Frontend: Types + API client + Components
  ↓
Phase 3 (Frontend UI Components - works with mocks)
  ↓
Phase 4 (Iterative Scraper Development)
  ├─→ Build Scraper 1 → Integrate → Test in Frontend ✅
  ├─→ Build Scraper 2 → Integrate → Test in Frontend ✅
  ├─→ Build Scraper 3 → Integrate → Test in Frontend ✅
  └─→ ... (each scraper tested immediately)
  ↓
Phase 5 (Services & Validation - test in frontend)
  ↓
Phase 6 (Frontend Polish)
  ↓
Phase 7 (Testing & Documentation)
  ↓
Phase 8 (Final Integration & Deploy)
```

## Key Benefits of This Approach

✅ **Immediate Feedback**: Each scraper tested through frontend as it's built  
✅ **Parallel Development**: Frontend and backend evolve together  
✅ **Continuous Validation**: User can validate each scraper individually  
✅ **Faster Iteration**: Issues caught early, not at the end  
✅ **Better UX Testing**: Real UI testing from day one  

## Validation Checkpoints Summary

- ✅ After each phase completion
- ✅ **After each scraper implementation** (test through frontend)
- ✅ After API contract definition
- ✅ After frontend components built
- ✅ After services integration
- ✅ After full stack integration

## Estimated Timeline

- **Phase 1-2**: ~5-7 validation cycles (foundation + API contract)
- **Phase 3**: ~5-6 validation cycles (frontend UI with mocks)
- **Phase 4**: ~6-8 validation cycles (scrapers, tested iteratively)
- **Phase 5-6**: ~5-7 validation cycles (services + polish)
- **Phase 7-8**: ~5-7 validation cycles (testing + deploy)
- **Total**: ~26-35 validation cycles

*Note: Timeline is more efficient due to parallel development and iterative testing*

