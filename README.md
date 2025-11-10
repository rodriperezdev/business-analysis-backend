# Business Analytics API

A scalable FastAPI application for business metrics analysis, benchmarking, and insights generation.

## Features

- **Financial Metrics Calculation**: Automatically calculates key business metrics (margins, profitability, customer economics)
- **Industry Benchmarking**: Compares your metrics against industry standards
- **Actionable Insights**: Generates prioritized recommendations based on your data
- **Scenario Analysis**: What-if analysis to model the impact of changes
- **RESTful API**: Clean, well-documented API endpoints
- **Type Safety**: Full type hints and Pydantic validation

## Project Structure

```
business-analysis-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── business_metrics.py
│   │   ├── scenario.py
│   │   └── responses.py
│   ├── routers/              # API route handlers
│   │   ├── __init__.py
│   │   ├── analysis.py
│   │   ├── scenario.py
│   │   └── benchmarks.py
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   ├── metrics_calculator.py
│   │   ├── benchmark_service.py
│   │   └── insight_service.py
│   └── utils/                # Utilities
│       ├── __init__.py
│       └── logging.py
├── main.py                   # Application entry point
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Create Virtual Environment

```bash
python -m venv BusinessAnalyticsEnv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
BusinessAnalyticsEnv\Scripts\activate
```

**Linux/Mac:**
```bash
source BusinessAnalyticsEnv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**⚠️ Troubleshooting Installation Issues:**

If you encounter Rust compilation errors (especially on Python 3.14), you have two options:

**Option 1: Install Rust (Recommended)**
1. Download and install Rust from https://rustup.rs/
2. Restart your terminal/command prompt
3. Run `pip install -r requirements.txt` again

**Option 2: Use Python 3.11 or 3.12**
Python 3.11 and 3.12 have more pre-built wheels available:
```bash
# Create a new virtual environment with Python 3.11 or 3.12
python3.11 -m venv BusinessAnalyticsEnv
# or
python3.12 -m venv BusinessAnalyticsEnv
```

### 4. Configure Environment (Optional)

Copy `.env.example` to `.env` and adjust settings:

```bash
cp .env.example .env
```

Default settings work for local development.

### 5. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8004`

## API Endpoints

### Root
- `GET /` - API information and status

### Analysis
- `POST /analyze` - Main analysis endpoint
  - Calculates metrics, benchmarks, and insights
  - Request body: `BusinessMetrics`
  - Response: `AnalysisResponse`

### Scenario Analysis
- `POST /scenario` - What-if scenario analysis
  - Applies percentage changes to metrics
  - Request body: `ScenarioInput`
  - Response: `ScenarioResponse`

### Benchmarks
- `GET /benchmarks/{industry}` - Get industry benchmarks
  - Path parameter: `industry` (saas, ecommerce, retail, manufacturing, services)
  - Response: `BenchmarkResponse`

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8004/docs`
- ReDoc: `http://localhost:8004/redoc`

## Usage Examples

### Basic Analysis

```python
import requests

url = "http://localhost:8004/analyze"
data = {
    "revenue": 100000.0,
    "cogs": 30000.0,
    "operating_expenses": 40000.0,
    "sales_marketing_expense": 15000.0,
    "new_customers": 50,
    "total_customers": 500,
    "churned_customers": 10,
    "cash_balance": 200000.0,
    "monthly_burn": 35000.0,
    "industry": "saas",
    "time_period_months": 1
}

response = requests.post(url, json=data)
result = response.json()
```

### Scenario Analysis

```python
url = "http://localhost:8004/scenario"
data = {
    "base_metrics": {
        "revenue": 100000.0,
        "cogs": 30000.0,
        "operating_expenses": 40000.0,
        "sales_marketing_expense": 15000.0,
        "industry": "saas",
        "time_period_months": 1
    },
    "changes": {
        "revenue": 15,      # +15%
        "cogs": -10         # -10%
    }
}

response = requests.post(url, json=data)
result = response.json()
```

## Supported Industries

- **SaaS**: Software as a Service
- **E-commerce**: Online retail
- **Retail**: Physical retail
- **Manufacturing**: Production/manufacturing
- **Services**: Service-based businesses

## Architecture

The application follows a clean architecture pattern:

- **Models**: Data validation and serialization (Pydantic)
- **Routers**: HTTP request handling and routing
- **Services**: Business logic and calculations
- **Utils**: Shared utilities (logging, helpers)
- **Config**: Centralized configuration management

This structure makes it easy to:
- Add new endpoints
- Extend calculations
- Add new industries
- Modify business logic
- Test individual components

## Extending the API

### Adding a New Metric

1. Add calculation in `app/services/metrics_calculator.py`
2. Update response models if needed
3. Add benchmark data in `app/services/benchmark_service.py` (if applicable)

### Adding a New Industry

1. Add industry type to `IndustryType` enum in `app/models/business_metrics.py`
2. Add benchmark data in `BENCHMARKS` dict in `app/services/benchmark_service.py`

### Adding a New Endpoint

1. Create router file in `app/routers/`
2. Import and include in `app/main.py`
3. Add business logic in `app/services/` if needed

## Development

### Running in Development Mode

Set `RELOAD=true` in `.env` or modify `main.py`:

```python
uvicorn.run(app, host=settings.host, port=settings.port, reload=True)
```

### Logging

Logging is configured in `app/utils/logging.py`. Set `LOG_LEVEL` in `.env`:
- `DEBUG`: Detailed debug information
- `INFO`: General information (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages only

## License

MIT

