# Frontend Development Plan

## Overview
Build a Nuxt 3 frontend application that displays financial ratio analysis in a clean, user-friendly interface matching the provided design.

## Technology Stack
- **Framework**: Nuxt 3
- **Language**: TypeScript
- **Styling**: Tailwind CSS (or similar utility-first CSS)
- **State Management**: Nuxt Composables
- **HTTP Client**: $fetch (built-in Nuxt)

## UI Design Reference
Based on the provided image, the interface includes:
- Navigation tabs: "Stock Analysis", "Batch Analysis" (NEW), "Stock Filter"
- Summary Table with columns: Metric, Value, Target, Status
- Metrics displayed: Gross Margin, ROIC, FCF Margin, Interest Coverage, P/E Ratio, Overall Score
- Status indicators: Green "Pass" ✓, Red "Fail" ✗, Blue "Info Only" ℹ
- Ticker input field at bottom
- "Analyze" button with icon
- Learning Opportunity section

## Step-by-Step Implementation

### Phase 1: Nuxt 3 Project Setup ✅ (Validation Required)

#### Step 1.1: Initialize Nuxt 3 Project
- [ ] Run `npx nuxi@latest init frontend` (or create manually)
- [ ] Verify Nuxt 3 installation
- [ ] Check Node.js version (18+)

#### Step 1.2: Install Dependencies
- [ ] Install Tailwind CSS: `npm install -D tailwindcss postcss autoprefixer`
- [ ] Initialize Tailwind: `npx tailwindcss init`
- [ ] Configure Tailwind in `nuxt.config.ts`
- [ ] Install additional packages if needed:
  - `@nuxtjs/color-mode` (optional, for dark mode)
  - `@vueuse/core` (optional, for utilities)

#### Step 1.3: Project Structure
- [ ] Create `pages/` directory
- [ ] Create `components/` directory
- [ ] Create `composables/` directory
- [ ] Create `types/` directory
- [ ] Create `assets/` directory (for styles, images)
- [ ] Create `.env` file for API URL

**Validation Checkpoint**: Verify Nuxt dev server runs, confirm structure

---

### Phase 2: Type Definitions ✅ (Validation Required)

#### Step 2.1: TypeScript Interfaces
- [ ] Create `types/stock.ts`
- [ ] Define interfaces:
  ```typescript
  interface SourceValue {
    source: string
    value: number | null
  }
  
  interface RatioResult {
    metric: string
    values: SourceValue[]
    consensus: number | null
    target: string
    status: 'Pass' | 'Fail' | 'Info Only'
  }
  
  interface AnalysisResponse {
    ticker: string
    ratios: RatioResult[]
    overall_score: number
    max_score: number
  }
  ```

**Validation Checkpoint**: Review type definitions, ensure they match backend schemas

---

### Phase 3: API Integration ✅ (Validation Required)

#### Step 3.1: API Client Composable
- [ ] Create `composables/useApi.ts`
- [ ] Implement `useApi()` composable:
  - Base URL from environment variable
  - `analyzeStock(ticker: string)` function
  - Error handling
  - Loading state management
- [ ] Add TypeScript types for API responses

#### Step 3.2: Stock Analysis Composable
- [ ] Create `composables/useStockAnalysis.ts`
- [ ] Implement `useStockAnalysis()` composable:
  - Reactive state for current ticker
  - Reactive state for analysis results
  - `fetchAnalysis(ticker: string)` function
  - `clearResults()` function
  - Computed properties for derived data

**Validation Checkpoint**: Test API connection, verify data fetching works

---

### Phase 4: UI Components ✅ (Validation Required)

#### Step 4.1: Status Badge Component
- [ ] Create `components/StatusBadge.vue`
- [ ] Props: `status: 'Pass' | 'Fail' | 'Info Only'`
- [ ] Display:
  - Green badge with checkmark for "Pass"
  - Red badge with X for "Fail"
  - Blue badge with info icon for "Info Only"
- [ ] Add Tailwind styling

#### Step 4.2: Metric Row Component
- [ ] Create `components/MetricRow.vue`
- [ ] Props: `ratio: RatioResult`
- [ ] Display:
  - Metric name
  - Value (formatted with % or decimal places)
  - Target threshold
  - Status badge
- [ ] Handle null/missing values gracefully
- [ ] Add hover effects

#### Step 4.3: Overall Score Component
- [ ] Create `components/OverallScore.vue`
- [ ] Props: `score: number, maxScore: number`
- [ ] Display score as "X/Y"
- [ ] Add visual indicator (color based on score)
- [ ] Show warning triangle if score is low

#### Step 4.4: Stock Input Component
- [ ] Create `components/StockInput.vue`
- [ ] Input field for ticker symbol
- [ ] "Analyze" button with icon
- [ ] Loading state during API call
- [ ] Error message display
- [ ] Form validation (non-empty, uppercase conversion)

#### Step 4.5: Summary Table Component
- [ ] Create `components/SummaryTable.vue`
- [ ] Props: `ratios: RatioResult[], overallScore: number, maxScore: number`
- [ ] Display table with columns:
  - Metric
  - Value (with formatting)
  - Target
  - Status
- [ ] Include Overall Score as last row
- [ ] Responsive design (mobile-friendly)
- [ ] Add table styling (borders, spacing, hover)

**Validation Checkpoint**: Review each component, test individually

---

### Phase 5: Pages ✅ (Validation Required)

#### Step 5.1: Main Stock Analysis Page
- [ ] Create `pages/index.vue`
- [ ] Layout structure:
  - Navigation tabs at top
  - Summary Table in main area
  - Learning Opportunity section (optional)
  - Stock Input at bottom
- [ ] Integrate `useStockAnalysis` composable
- [ ] Display loading state while fetching
- [ ] Display error messages
- [ ] Handle empty state (before first analysis)
- [ ] Match design from provided image

#### Step 5.2: Navigation Tabs
- [ ] Add tab navigation component
- [ ] Tabs: "Stock Analysis" (active), "Batch Analysis", "Stock Filter"
- [ ] Routing: `/` (Stock Analysis), `/batch` (Batch Analysis), `/filter` (Stock Filter)
- [ ] Active tab highlighting

#### Step 5.3: Batch Analysis Page (Placeholder)
- [ ] Create `pages/batch.vue`
- [ ] Add "Coming Soon" or placeholder content
- [ ] Basic layout matching design

#### Step 5.4: Stock Filter Page (Placeholder)
- [ ] Create `pages/filter.vue`
- [ ] Add "Coming Soon" or placeholder content
- [ ] Basic layout matching design

**Validation Checkpoint**: Review page layouts, test navigation, verify UI matches design

---

### Phase 6: Styling & UX ✅ (Validation Required)

#### Step 6.1: Global Styles
- [ ] Configure Tailwind theme (colors, fonts)
- [ ] Create `assets/css/main.css` with base styles
- [ ] Add custom utility classes if needed
- [ ] Ensure consistent spacing and typography

#### Step 6.2: Responsive Design
- [ ] Test on mobile devices
- [ ] Adjust table layout for small screens
- [ ] Ensure input and buttons are touch-friendly
- [ ] Test on tablet sizes

#### Step 6.3: Loading States
- [ ] Add skeleton loaders for table
- [ ] Show spinner during API calls
- [ ] Disable input/button while loading

#### Step 6.4: Error Handling
- [ ] Display user-friendly error messages
- [ ] Handle network errors gracefully
- [ ] Show validation errors for invalid tickers
- [ ] Add retry functionality

#### Step 6.5: Animations & Transitions
- [ ] Add smooth transitions for table updates
- [ ] Add hover effects on interactive elements
- [ ] Add fade-in for results

**Validation Checkpoint**: Review complete UI, test all interactions

---

### Phase 7: Testing ✅ (Validation Required)

#### Step 7.1: Component Tests
- [ ] Write tests for StatusBadge component
- [ ] Write tests for MetricRow component
- [ ] Write tests for StockInput component
- [ ] Use Vitest (built into Nuxt 3)

#### Step 7.2: Composable Tests
- [ ] Test useApi composable
- [ ] Test useStockAnalysis composable
- [ ] Mock API responses

#### Step 7.3: Integration Tests
- [ ] Test full user flow: enter ticker → analyze → display results
- [ ] Test error scenarios
- [ ] Test with real API (if backend is ready)

**Validation Checkpoint**: All tests pass, review test coverage

---

### Phase 8: Optimization & Polish ✅ (Validation Required)

#### Step 8.1: Performance
- [ ] Optimize bundle size
- [ ] Add lazy loading for routes
- [ ] Optimize images/assets
- [ ] Check Lighthouse scores

#### Step 8.2: Accessibility
- [ ] Add ARIA labels
- [ ] Ensure keyboard navigation works
- [ ] Check color contrast
- [ ] Test with screen readers

#### Step 8.3: SEO (if needed)
- [ ] Add meta tags
- [ ] Add Open Graph tags
- [ ] Configure sitemap

**Validation Checkpoint**: Final review, approve for production

---

## Component Hierarchy

```
pages/index.vue
├── NavigationTabs (component)
├── SummaryTable (component)
│   ├── MetricRow (component) × 5
│   │   └── StatusBadge (component)
│   └── OverallScore (component)
└── StockInput (component)
```

## State Management Flow

1. User enters ticker in `StockInput`
2. `StockInput` emits event or calls `useStockAnalysis.fetchAnalysis()`
3. `useStockAnalysis` calls `useApi.analyzeStock()`
4. API returns data
5. `useStockAnalysis` updates reactive state
6. `SummaryTable` receives updated props and re-renders

## API Integration Details

### Endpoint
```
GET /api/analyze/{ticker}
```

### Response Format
```json
{
  "ticker": "AAPL",
  "ratios": [
    {
      "metric": "Gross Margin",
      "values": [
        {"source": "Finviz", "value": 91.51},
        {"source": "Morningstar", "value": 91.2},
        {"source": "Macrotrends", "value": 91.8}
      ],
      "consensus": 91.51,
      "target": ">60%",
      "status": "Pass"
    },
    // ... more ratios
  ],
  "overall_score": 2,
  "max_score": 4
}
```

## Styling Guidelines

- Use Tailwind utility classes
- Color scheme:
  - Pass: Green (#10B981 or similar)
  - Fail: Red (#EF4444 or similar)
  - Info: Blue (#3B82F6 or similar)
- Typography: Clean, readable fonts
- Spacing: Consistent padding/margins
- Borders: Subtle, light borders

