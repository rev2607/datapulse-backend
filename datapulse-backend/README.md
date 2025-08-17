# DataPulse Backend

A FastAPI-based backend service for CSV data analysis and exploration.

## Features

- **CSV Upload & Analysis**: Upload CSV files and get instant analysis results
- **Health Check**: Simple health endpoint to verify service status
- **Data Insights**: Schema inference, comprehensive statistics, missing values analysis, and data health scoring
- **Fast & Lightweight**: Built with FastAPI for high performance

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd datapulse-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Docker

```bash
# Build the image
docker build -t datapulse-backend .

# Run the container
docker run -p 8000:8000 datapulse-backend
```

## API Endpoints

### Health Check
- **GET** `/` - Returns service status

### File Upload & Analysis
- **POST** `/upload` - Upload a CSV file for analysis
  - **Request**: Form data with CSV file
  - **Response**: Analysis results including schema, summary statistics, missing values, and data health score

## Example Usage

### Using curl
```bash
curl -X POST "http://localhost:8000/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_data.csv"
```

### Using Python requests
```python
import requests

with open('your_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload',
        files={'file': f}
    )
    results = response.json()
    print(results)
```

## Response Format

```json
{
  "schema": {
    "name": "object",
    "age": "int64",
    "city": "object",
    "salary": "float64",
    "department": "object"
  },
  "summary": {
    "name": {
      "count": 100,
      "unique": 100,
      "top": "John Doe",
      "freq": 1
    },
    "age": {
      "count": 98.0,
      "mean": 35.2,
      "std": 8.5,
      "min": 22.0,
      "25%": 28.0,
      "50%": 35.0,
      "75%": 42.0,
      "max": 65.0
    },
    "salary": {
      "count": 99.0,
      "mean": 75000.0,
      "std": 15000.0,
      "min": 45000.0,
      "25%": 65000.0,
      "50%": 75000.0,
      "75%": 85000.0,
      "max": 120000.0
    }
  },
  "missing": {
    "name": 0,
    "age": 2,
    "city": 0,
    "salary": 1,
    "department": 0
  },
  "health_score": 97.0
}
```

## Project Structure

```
datapulse-backend/
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── schemas.py       # Pydantic models (for future use)
│   └── utils.py         # Data analysis utilities
├── tests/
│   └── test_utils.py    # Unit tests
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black app/
isort app/
```

### Linting
```bash
flake8 app/
mypy app/
```

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Uvicorn**: ASGI server for running FastAPI
- **Python-multipart**: File upload support
- **Scipy**: Scientific computing
- **Scikit-learn**: Machine learning utilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub or contact the development team.
