# Gross - Financial Ratio Analysis Tool

A full-stack application for analyzing public company financial ratios by comparing data from multiple free financial data sources.

## Project Overview

This application allows users to:
- Enter a stock ticker symbol
- Fetch 5 key financial ratios from 3 independent sources each
- Compare values across sources to verify data accuracy
- Display results in a clean, tabular format with pass/fail status indicators
- View overall score based on target thresholds

## Architecture

### Backend (Python)
- **Purpose**: Scrape financial data from multiple sources and provide REST API
- **Technology**: Python 3.x, FastAPI (or Flask), BeautifulSoup, Requests
- **Location**: `/backend`

### Frontend (Nuxt 3)
- **Purpose**: User interface for stock analysis
- **Technology**: Nuxt 3, Vue 3, TypeScript
- **Location**: `/frontend`

## Financial Ratios Analyzed

1. **Gross Margin** - (Revenue - COGS) / Revenue
2. **ROIC** - Return on Invested Capital
3. **FCF Margin** - Free Cash Flow / Revenue
4. **Interest Coverage** - EBIT / Interest Expense
5. **P/E Ratio** - Price to Earnings Ratio

## Data Sources (3 per ratio)

### Gross Margin
- Finviz
- Morningstar
- Macrotrends

### ROIC
- QuickFS
- Morningstar
- Koyfin

### FCF Margin
- QuickFS
- Koyfin
- Macrotrends

### Interest Coverage
- Morningstar
- Koyfin
- Yahoo Finance

### P/E Ratio
- Finviz
- Yahoo Finance
- Morningstar

## Development Workflow

1. **Documentation First**: All implementation steps are documented in MD files
2. **Step-by-Step Validation**: Each step is validated before proceeding
3. **Testing**: Tests are written and run after each feature
4. **Version Control**: Changes are committed and pushed to GitHub after validation

## Getting Started

See individual plan files:
- `backend/PLAN.md` - Backend development steps
- `frontend/PLAN.md` - Frontend development steps
- `GIT_WORKFLOW.md` - Version control process
- `PROJECT_STRUCTURE.md` - Detailed directory layout

## Repository

GitHub: https://github.com/louisgarnier/Gross.git

