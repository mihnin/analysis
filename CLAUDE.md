# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based web application for inventory management analysis and forecasting. The application analyzes historical inventory data and provides forecasts with purchase recommendations. It's designed for Russian-speaking users managing warehouse materials across multiple branches.

The application calculates key inventory metrics including turnover rates, seasonality, ABC-XYZ classification, safety stock levels, and opportunity costs from excess inventory.

## Running the Application

```bash
# Activate conda environment
conda activate analysis

# Run the Streamlit application
streamlit run app.py
```

The application will open in a web browser at `http://localhost:8501`

## Development Setup

```bash
# Create and activate conda environment
conda create --name analysis python=3.12 -y
conda activate analysis

# Install dependencies
pip install -r requirements.txt
```

## Architecture

### Application Flow

The application follows a two-phase analysis workflow:

1. **Historical Data Analysis** (historical_analysis.py)
   - User uploads Excel file with historical inventory data
   - Data is grouped by material and branch
   - Calculates metrics: growth rate, average usage, turnover, seasonality (using seasonal_decompose), trend (linear regression), ABC-XYZ classification
   - Identifies excess inventory and calculates opportunity cost
   - Returns results DataFrame and dynamic explanation text

2. **Forecast Analysis** (forecast_analysis.py)
   - User uploads Excel file with planned demand data
   - Forecasts starting balance using Exponential Smoothing (statsmodels.tsa.holtwinters)
   - Calculates ending balance = starting balance - planned demand
   - Computes purchase recommendations: max(0, future_demand + safety_stock - ending_balance)
   - Future demand = rolling sum of demand over 3 periods
   - Safety stock = planned_demand * user_defined_percentage
   - Returns analysis DataFrame and dynamic explanation text

### Module Structure

- **app.py** - Main Streamlit application entry point. Orchestrates the UI flow, file uploads, user inputs (column mapping, filters, safety stock %), and calls analysis modules. Handles session state management.

- **historical_analysis.py** - Core logic for historical inventory analysis. Key function: `analyze_historical_data()` which processes historical data and returns calculated metrics + explanations.

- **forecast_analysis.py** - Core logic for demand forecasting and purchase recommendations. Key functions:
  - `forecast_start_balance()` - Projects starting inventory from historical data
  - `calculate_purchase_recommendations()` - Determines what to buy
  - `analyze_forecast_data()` - Main orchestrator for forecast analysis

- **visualization.py** - Plotly chart generation for inventory trends, seasonality patterns, and forecast visualizations.

- **utils.py** - Utility functions for Excel/CSV export, session state initialization, data filtering, and column selection UI components.

- **logging_config.py** - Application logging setup. Logs user actions to application.log file with timestamps. Includes password-protected log download feature.

- **data_processing.py** - Data manipulation utilities (note: appears to exist but not heavily used in main flow)

- **data_validation.py** - Input validation logic (if present)

### Key Technical Patterns

**Data Processing Pipeline:**
- User uploads Excel → pandas DataFrame → user maps columns → filter by material/branch/date → analyze → display results + explanations

**Dynamic Explanations:**
The `get_explanation()` functions in both analysis modules generate Russian-language explanations dynamically based on the first row of results. These explanations include formulas, business context, and actionable recommendations.

**ABC-XYZ Classification:**
- ABC classes based on average usage thresholds (A>100, B>50, C<=50 units/month)
- XYZ classes based on coefficient of variation (X<0.1, Y<0.3, Z>=0.3)

**Session State Usage:**
Streamlit session_state stores uploaded DataFrames (historical_df, forecast_df) to persist data across widget interactions without re-uploading.

## Data Schema

### Historical Data Expected Columns (user-mapped):
- Date column (datetime)
- Branch column (identifier)
- Material column (identifier)
- Start quantity column (numeric)
- End quantity column (numeric)
- End cost column (numeric) - used for opportunity cost calculation

### Forecast Data Expected Columns (user-mapped):
- Date column (datetime)
- Branch column (identifier)
- Material column (identifier)
- Planned demand column (numeric)

## Important Implementation Notes

- All UI text is in Russian as the application targets Russian-speaking warehouse managers
- The application uses statsmodels for time series analysis (seasonal_decompose, ExponentialSmoothing)
- Excel export uses xlsxwriter for in-memory file generation
- Logging is configured to use UTC+00:00 timezone
- The interest rate for opportunity cost calculation is user-configurable (default 5%)
- Safety stock percentage is user-configurable via slider (default 20%)

## Testing

There are no automated tests in this repository. When making changes, manually verify:
1. File upload functionality works for both historical and forecast data
2. Column mapping correctly identifies data
3. Filtering by material/branch/date produces expected subsets
4. Calculations match the formulas in the explanation text
5. Excel/CSV downloads contain correct data
6. Charts render properly with filtered data

## Common Development Tasks

When adding new metrics to historical analysis:
1. Add calculation logic in `historical_analysis.py` → `analyze_historical_data()`
2. Include the metric in the results dictionary
3. Add explanation text in `get_explanation()` function
4. Update README.md to document the new metric

When modifying forecast logic:
1. Update calculations in `forecast_analysis.py` → `calculate_purchase_recommendations()`
2. Ensure explanation text in `get_explanation()` reflects changes
3. Verify visualization.py charts display new data if needed

When adding new chart types:
1. Create function in `visualization.py` using plotly
2. Call from app.py after analysis completes
3. Use `st.plotly_chart()` to render

## Dependencies

Key libraries:
- streamlit >= 1.38.0 - Web UI framework
- pandas >= 1.5.3 - Data manipulation
- numpy >= 1.26.4 - Numerical operations
- plotly >= 5.14.1 - Interactive charts
- statsmodels >= 0.13.5 - Time series analysis (seasonal_decompose, ExponentialSmoothing)
- scipy >= 1.13.1 - Linear regression for trend analysis
- openpyxl >= 3.1.2 - Excel file reading
- xlsxwriter >= 3.1.2 - Excel file writing
