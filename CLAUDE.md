# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based web application for inventory management analysis and forecasting. The application analyzes historical inventory data and provides forecasts with purchase recommendations. It's designed for Russian-speaking users managing warehouse materials across multiple branches.

The application calculates key inventory metrics including turnover rates, seasonality, ABC-XYZ classification, safety stock levels, ROP (Reorder Point), Fill Rate, deficit analysis, dead stock detection, and opportunity costs from excess inventory.

**NEW (2025-10-19):** The application now includes comprehensive demand and inventory forecasting using 5 professional time series models (Naive, Moving Average, Exponential Smoothing, Holt-Winters, SARIMA) with automatic model selection. Users can either provide their own demand forecast or use automatic forecasting based on historical consumption data.

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
   - **TWO MODES:**
     - **Mode 1 (Classic):** User uploads Excel file with planned demand data
     - **Mode 2 (Auto - NEW):** Application automatically forecasts demand from historical consumption data
   - Forecasts starting balance using forecasting models (naive, moving_average, exponential_smoothing, holt_winters, sarima, auto)
   - Calculates ending balance = starting balance - planned demand
   - Computes purchase recommendations: max(0, future_demand + safety_stock - ending_balance)
   - Future demand = forward rolling sum of demand over 3 periods (FIXED: was backward)
   - Safety stock = planned_demand * user_defined_percentage
   - Returns analysis DataFrame and dynamic explanation text

### Module Structure

- **app.py** - Main Streamlit application entry point. Orchestrates the UI flow, file uploads, user inputs (column mapping, filters, safety stock %), and calls analysis modules. Handles session state management.

- **historical_analysis.py** - Core logic for historical inventory analysis. Key function: `analyze_historical_data()` which processes historical data and returns calculated metrics + explanations.

- **forecast_analysis.py** - Core logic for demand forecasting and purchase recommendations. Key functions:
  - `forecast_start_balance()` - Projects starting inventory using forecasting models (supports: naive, moving_average, exponential_smoothing, holt_winters, sarima, auto)
  - `auto_forecast_demand()` - Automatically forecasts future demand based on historical consumption data
  - `calculate_purchase_recommendations()` - Determines what to buy
  - `analyze_forecast_data()` - Main orchestrator for forecast analysis

- **forecasting_models.py** - Professional time series forecasting models (NEW):
  - `naive_forecast()` - Simple baseline: forecast = last value
  - `moving_average_forecast()` - Smoothed forecast over N periods
  - `exponential_smoothing_forecast()` - Adaptive smoothing with configurable alpha
  - `holt_winters_forecast()` - Triple exponential smoothing (level + trend + seasonality)
  - `sarima_forecast()` - Seasonal ARIMA for complex patterns
  - `auto_select_best_model()` - Automatically selects best model based on MAPE
  - `forecast_demand()` - Universal forecasting function supporting all models
  - `calculate_metrics()` - Computes MAPE, MAE, RMSE, Bias

- **visualization.py** - Plotly chart generation for inventory trends, seasonality patterns, and forecast visualizations.

- **utils.py** - Utility functions for Excel/CSV export, session state initialization, data filtering, and column selection UI components.

- **logging_config.py** - Application logging setup. Logs user actions to application.log file with timestamps. Includes password-protected log download feature.

- **data_processing.py** - Data manipulation utilities (note: appears to exist but not heavily used in main flow)

- **data_validation.py** - Input validation and consumption normalization logic:
  - `detect_consumption_convention()` - Detects if consumption is positive or negative format
  - `normalize_consumption()` - Normalizes consumption to positive values (supports AUTO/POSITIVE/NEGATIVE/ABS modes)
  - `print_consumption_analysis()` - Displays normalization results

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
- **Consumption column (optional but recommended)** - actual consumption/usage for accurate metrics and forecasting
  - Can be positive (consumption = positive number) or negative (consumption = negative number)
  - Application auto-detects format and normalizes using `data_validation.normalize_consumption()`

### Forecast Data Expected Columns (user-mapped):

**Option 1: User-provided forecast (classic mode)**
- Date column (datetime)
- Branch column (identifier)
- Material column (identifier)
- Planned demand column (numeric)

**Option 2: Auto-generated forecast (NEW)**
- No file needed - application generates forecast from historical consumption data
- User configures: forecast periods (1-24 months), model selection (auto/naive/ma/es/holt_winters/sarima)

## Important Implementation Notes

- All UI text is in Russian as the application targets Russian-speaking warehouse managers
- The application uses statsmodels for time series analysis (seasonal_decompose, ExponentialSmoothing, SARIMAX)
- Excel export uses xlsxwriter for in-memory file generation
- Logging is configured to use UTC+00:00 timezone
- The interest rate for opportunity cost calculation is user-configurable (default 5%)
- Safety stock percentage is user-configurable via slider (default 20%)
- Lead time for ROP calculation is user-configurable (default 30 days)
- **Consumption normalization:** Application automatically detects and normalizes positive/negative consumption formats
- **Forecasting models:** All models include fallback to simpler models on errors (e.g., SARIMA → Holt-Winters → Moving Average → Naive)

## Testing

### Automated Tests

**Forecasting Models:**
```bash
python test_forecasting_models.py
```
Tests all 5 forecasting models on real data, compares accuracy, validates auto-selection.

**Historical Analysis:**
```bash
python -m pytest test_historical_analysis.py -v
```
12 unit tests for historical analysis functions.

**Forecast Analysis:**
```bash
python -m pytest test_forecast_analysis.py -v
```
12 unit tests for forecast analysis functions.

### Manual Testing

When making changes, manually verify:
1. File upload functionality works for both historical and forecast data
2. Column mapping correctly identifies data
3. Filtering by material/branch/date produces expected subsets
4. Calculations match the formulas in the explanation text
5. Excel/CSV downloads contain correct data
6. Charts render properly with filtered data
7. Automatic forecasting generates reasonable predictions
8. Model selection works correctly (AUTO mode)

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

When adding new forecasting models:
1. Add model function in `forecasting_models.py` (e.g., `prophet_forecast()`)
2. Update `auto_select_best_model()` to include new model in comparison
3. Add model to `forecast_demand()` switch statement
4. Update model descriptions in `get_model_description()`
5. Test with `test_forecasting_models.py`
6. Update FORECASTING_MODELS_GUIDE.md documentation

When modifying forecasting behavior:
1. For demand forecasting: Update `auto_forecast_demand()` in forecast_analysis.py
2. For balance forecasting: Update `forecast_start_balance()` in forecast_analysis.py
3. Ensure fallback to simple models (naive/moving_average) on errors
4. Test with real datasets using `test_forecasting_models.py`

## Dependencies

Key libraries:
- streamlit >= 1.38.0 - Web UI framework
- pandas >= 1.5.3 - Data manipulation
- numpy >= 1.26.4 - Numerical operations
- plotly >= 5.14.1 - Interactive charts
- statsmodels >= 0.13.5 - Time series analysis (seasonal_decompose, ExponentialSmoothing, SARIMAX for forecasting models)
- scipy >= 1.13.1 - Linear regression for trend analysis
- openpyxl >= 3.1.2 - Excel file reading
- xlsxwriter >= 3.1.2 - Excel file writing

## Additional Documentation

**Error Reports and Fixes:**
- **ERRORS_FOUND.md** - Documents 3 critical calculation errors found and fixed
- **FIXES_SUMMARY.md** - Summary of all corrections made to the application
- **FINAL_REPORT.md** - Comprehensive assessment of application quality (8/10 → 9/10)

**Feature Guides:**
- **CONSUMPTION_CONVENTION_GUIDE.md** - How consumption sign normalization works (positive vs negative)
- **FORECASTING_MODELS_GUIDE.md** - Complete guide to forecasting models (600+ lines)
- **FORECASTING_INTEGRATION_REPORT.md** - Technical report on forecasting system integration

**Analysis Scripts:**
- **analyze_calculations.py** - Detected calculation errors in historical analysis
- **analyze_forecast.py** - Detected errors in forecast rolling sum
- **analyze_forecasting_models.py** - Analysis of forecasting capabilities (before integration)
- **business_logic_review.py** - Business logic review and recommendations

**Testing Scripts:**
- **test_forecasting_models.py** - Comprehensive tests for all 5 forecasting models
- **test_historical_analysis.py** - 12 unit tests for historical analysis
- **test_forecast_analysis.py** - 12 unit tests for forecast analysis
- **test_consumption_conventions.py** - Tests for consumption normalization

## Key Improvements Made

1. **Fixed 3 critical calculation errors:**
   - ERROR #1: Average consumption calculation (negative values)
   - ERROR #2: Rolling sum direction (backward instead of forward)
   - ERROR #3: Exponential Smoothing overwriting planned demand

2. **Added 5 new inventory metrics:**
   - Turnover in days
   - Reorder Point (ROP) with lead time
   - Deficit periods analysis
   - Fill Rate calculation
   - Dead stock detection

3. **Implemented consumption normalization:**
   - Automatic detection of positive vs negative consumption conventions
   - AUTO/POSITIVE/NEGATIVE/ABS modes
   - Balance validation

4. **Integrated professional forecasting:**
   - 5 time series models (Naive, MA, ES, Holt-Winters, SARIMA)
   - Automatic model selection (AUTO mode)
   - Quality metrics (MAPE, MAE, RMSE, Bias)
   - Two modes: user-provided forecast OR automatic forecasting
