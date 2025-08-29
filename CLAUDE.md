# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UC Investment Explorer - A web application that visualizes University of California investment data. The project consists of:
- Frontend: SvelteKit application for data visualization (hosted at http://ucinvestments.info/)
- Backend: Flask API server hosted on Heroku
- Data Processing: Python scripts for collecting, processing, and aggregating investment data

## Architecture

### Frontend (Webapp/)
- **Framework**: SvelteKit with TypeScript
- **Styling**: Tailwind CSS
- **Data Visualization**: D3.js
- **Main Components**:
  - `/src/routes/+page.svelte`: Main investment visualization interface
  - `/src/routes/about/+page.svelte`: About page
  - `/src/lib/`: Reusable components (loading, pie chart)
- **Deployment**: Vercel

### Backend (backend-server/)
- **Framework**: Flask with CORS support
- **Main Files**:
  - `main.py`: Flask API endpoints for serving investment data
  - `aggregator.py`: Investment data aggregation logic
- **API Base URL**: https://uc-investments-80f94956a47a.herokuapp.com

### Data Processing (Data-Collection/)
- **Helper-Functions/**: Python scripts for data transformation
  - `combine-investments.py`: Combines investment data from multiple sources
  - `convert-CSVs-JSON.py`: Converts CSV files to JSON format
  - `fund-re-weighting.py`: Adjusts fund weights
  - `whale-wisdom-convertor.py`: Converts data from Whale Wisdom format
  - `pdf-investment-cleaner.py`: Extracts data from PDF reports
- **Data Directories**:
  - `csv-files/`: Raw CSV data for individual funds
  - `json-outputs/`: Processed JSON files
  - `final-fund-holdings/`: Processed fund holdings data
  - `individual-fund-outputs/`: Investment data by fund type

## Commands

### Frontend Development (in Webapp/ directory)
```bash
cd Webapp
npm install              # Install dependencies
npm run dev              # Start development server
npm run build            # Build for production
npm run preview          # Preview production build
npm run check            # Type checking
npm run lint             # Check code formatting
npm run format           # Auto-format code
```

### Backend Development
```bash
pip install -r requirements.txt                    # Install Python dependencies
flask --app backend-server/main run               # Run Flask development server
gunicorn backend-server.main:app                  # Production server (as configured in Procfile)
```

### Data Processing
```bash
python Data-Collection/Helper-Functions/combine-investments.py     # Combine investment CSVs
python Data-Collection/Helper-Functions/convert-CSVs-JSON.py       # Convert CSVs to JSON
python backend-server/aggregator.py                                # Run data aggregation
```

## Key Data Flows

1. **Investment Data Collection**: Manual process (planned for automation)
   - UC releases investment reports
   - Data extracted and formatted into CSVs in `Data-Collection/csv-files/`
   - CSVs converted to JSON using helper scripts

2. **Data Aggregation**:
   - `aggregator.py` processes JSON files from `Data-Collection/json-outputs/`
   - Combines data with fund information from `final-datasets/listed_investments.csv`
   - Generates aggregated datasets in `final-datasets/`

3. **Frontend Data Fetching**:
   - SvelteKit app fetches data from Flask API endpoints
   - Main endpoint: `/listed-assets` returns processed investment data
   - Data visualization using D3.js pie charts

## Important Files

- `final-datasets/listed_investments.csv`: Master list of UC investments
- `final-datasets/full_investments_*.json`: Aggregated investment data with different configurations
- `Data-Collection/csv-files/`: Fund composition data in CSV format (format for contributions)

## Development Notes

- Frontend uses TypeScript - ensure type safety when modifying components
- API responses are CORS-enabled for cross-origin requests
- Investment data format in CSVs should match existing files in `Data-Collection/csv-files/`
- The project is transitioning to automated data collection (currently manual)