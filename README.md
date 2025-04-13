# Restaurant Booking Service

A FastAPI-based service for managing restaurant table bookings, with PostgreSQL database support.

## Features

- Table management (CRUD operations)
- Reservation management (CRUD operations)
- Async database operations
- Automatic database migrations

## Tech Stack

- **API Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Containerization**: Docker

## API Endpoints

### Tables Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tables` | GET | Get all available tables |
| `/tables` | POST | Create a new table |
| `/tables/{table_id}` | DELETE | Delete a specific table |

### Reservations Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reservations` | GET | Get all reservations |
| `/reservations` | POST | Create a new reservation |
| `/reservations/{reservation_id}` | DELETE | Cancel a specific reservation |

## Request/Response Examples

### Create a Table (POST /tables)
```json
{
  "name": Luxury,
  "location": Behind fireplac,
  "seats": 4
}

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.12

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/restaurant-booking-service.git
   cd restaurant-booking-service
