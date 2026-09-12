# VERIFY GH

**Check it. Match it. Trust the information.**

VERIFY GH is a consumer product verification and regulatory reporting platform for Ghana. It allows consumers to compare regulated-product information against available registry records through a deterministic, rule-based verification system.

## Features

- **Product Verification**: Compare product information against registry records
- **Four Verification Statuses**: MATCH, PARTIAL_MATCH, DOES_NOT_MATCH, NOT_FOUND
- **Field-by-Field Comparison**: See exactly which fields match or differ
- **Inconsistency Reporting**: Submit reports to regulators when discrepancies are found
- **Regulator Dashboard**: Secure dashboard for reviewing and managing reports
- **Mobile-First PWA**: Progressive Web App for mobile accessibility
- **Demo Dataset**: Controlled demonstration data for hackathon/testing

## Technology Stack

### Backend
- Python 3.12+
- FastAPI
- SQLAlchemy (with SQLite for development, PostgreSQL ready for production)
- JWT Authentication
- Pydantic for validation

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript
- PWA with Service Worker

## Project Structure

```
verify-gh/
├── frontend/           # Consumer PWA
│   ├── css/          # Stylesheets
│   ├── js/           # JavaScript modules
│   ├── assets/       # Icons and images
│   ├── index.html    # Home page
│   ├── verify.html   # Verification page
│   ├── search.html   # Search page
│   ├── report.html   # Report page
│   ├── login.html    # Regulator login
│   ├── dashboard.html # Regulator dashboard
│   ├── reports.html  # Reports list
│   ├── help.html     # Help page
│   ├── manifest.json # PWA manifest
│   └── service-worker.js # Service worker
│
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── main.py   # Application entry point
│   │   ├── config.py # Configuration
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── routes/   # API routes
│   │   ├── services/ # Business logic
│   │   ├── database/ # Database connection
│   │   ├── auth/     # Authentication
│   │   └── utils/    # Utilities
│   ├── requirements.txt
│   ├── seed_data.py  # Demo data seeding
│   └── .env.example  # Environment variables
│
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create environment file:
```bash
cp .env.example .env
```

6. Seed the database with demo data:
```bash
python seed_data.py
```

This will create:
- Demo registry products (including test scenarios for MATCH, DOES_NOT_MATCH, NOT_FOUND)
- Demo regulator account: `regulator@verifygh.demo` / `demo123`
- Demo admin account: `admin@verifygh.demo` / `demo123`

7. Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Start a simple HTTP server:

**Python 3:**
```bash
python -m http.server 8080
```

The frontend will be available at `http://localhost:8080`

## Demo Scenarios

### Demo 1 - MATCH
- **Input**: Registration: `GH-DEMO-001`, Manufacturer: `Demo Pharma Ltd`
- **Expected**: MATCH
- **Purpose**: Demonstrates successful verification

### Demo 2 - DOES NOT MATCH
- **Input**: Registration: `GH-DEMO-001`, Manufacturer: `Wrong Manufacturer Ltd`
- **Expected**: DOES NOT MATCH
- **Purpose**: Demonstrates manufacturer mismatch detection

### Demo 3 - NOT FOUND
- **Input**: Registration: `GH-NOT-FOUND-999`
- **Expected**: NOT FOUND
- **Purpose**: Demonstrates handling of non-existent registry records

### Demo 4 - REPORT
- **Flow**: After a mismatch, submit an inconsistency report
- **Expected**: Report created successfully with report ID
- **Purpose**: Demonstrates reporting workflow

### Demo 5 - REGULATOR DASHBOARD
- **Login**: `regulator@verifygh.demo` / `ChangeMe123!`
- **Flow**: View dashboard, review reports, update status
- **Expected**: Dashboard loads with statistics and recent reports
- **Purpose**: Demonstrates regulator functionality

## API Endpoints

### Products
- `GET /products/search` - Search products by name, registration number, or manufacturer
- `GET /products/{id}` - Get product by ID
- `POST /products` - Create product (admin only)

### Verifications
- `POST /verifications` - Create verification
- `GET /verifications/{id}` - Get verification by ID

### Reports
- `POST /reports` - Create report
- `GET /reports` - List reports (regulator/admin only)
- `GET /reports/{id}` - Get report by ID (regulator/admin only)
- `PATCH /reports/{id}` - Update report status (regulator/admin only)

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `GET /auth/me` - Get current user

### Dashboard
- `GET /dashboard/summary` - Get dashboard summary (regulator/admin only)
- `GET /dashboard/recent-reports` - Get recent reports (regulator/admin only)

## Verification Statuses

### MATCH
All submitted fields match the available registry record.

### PARTIAL_MATCH
Some fields match, but others require attention or were not provided.

### DOES_NOT_MATCH
One or more important fields differ from the available registry record.

### NOT_FOUND
No corresponding record was found in the available registry dataset. This does not prove that the product is fake.

## Important Notes

- **Demo Data**: This prototype uses controlled demonstration data and is not a live official registry.
- **No Authenticity Claims**: VERIFY GH does not determine that a product is fake or genuine. It compares information and reports the comparison result.
- **Consumer Reports**: A consumer report is an observation, not a confirmed regulatory conclusion.
- **Privacy**: Only necessary information is collected. Location is collected at town/district/region level.

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Role-based access control (consumer, retailer, regulator, admin)
- Input validation and sanitization
- CORS configuration

## Development

### Running Tests
```bash
cd backend
pytest
```

### Database Schema
The database schema is defined in `backend/app/models/`. For production, PostgreSQL is recommended. SQLite is used for local development.

### Adding New Products
Edit `backend/seed_data.py` and add products to the `demo_products` list, then run:
```bash
python seed_data.py
```

## License

Proprietary - VERIFY GH Project

## Support

For issues or questions, please refer to the Help page in the application or contact the development team.
