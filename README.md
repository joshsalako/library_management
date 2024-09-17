# Library Management System

## 1. Project Overview

This Library Management System consists of two independent API services:

1. Frontend API: Handles user interactions like enrolling, listing books, and borrowing.
2. Admin API: Manages the book catalogue and user information.

The system is built using Django and Django Rest Framework, with separate databases for each service and inter-service communication via Redis.

## 2. System Architecture

- Frontend API: Django application with SQLite database
- Admin API: Django application with separate SQLite database
- Inter-service Communication: Redis pub/sub mechanism
- Deployment: Docker containers

## 3. API Endpoints

### Frontend API

- POST /api/frontend/users/enroll/: Enroll a new user
- GET /api/frontend/books/: List all available books
- GET /api/frontend/books/{id}/: Get a single book by ID
- GET /api/frontend/books/?publisher={publisher}: Filter books by publisher
- GET /api/frontend/books/?category={category}: Filter books by category
- POST /api/frontend/books/{id}/borrow/: Borrow a book

### Admin API

- POST /api/admin/books/: Add a new book
- DELETE /api/admin/books/{id}/: Remove a book
- GET /api/admin/users/: List all users
- GET /api/admin/users/{id}/borrowed_books/: List books borrowed by a user
- GET /api/admin/borrowings/unavailable_books/: List unavailable books

## 4. Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/joshsalako/library_management.git
   cd library_management
   ```

2. Install Docker and Docker Compose if not already installed.

3. Build the Docker images:
   ```
   docker-compose build
   ```

## 5. Running the Application

1. Start the services:
   ```
   docker-compose up
   ```

2. The services will be available at:
   - Frontend API: http://localhost:8000
   - Admin API: http://localhost:8001

## 6. Testing

Run the tests using:

```
docker-compose run frontend_api python manage.py test
docker-compose run admin_api python manage.py test
```

## 7. Docker Deployment

The application is containerized using Docker. The `docker-compose.yml` file defines the services:

- frontend_api
- admin_api
- redis
- subscriber

To deploy, ensure Docker and Docker Compose are installed on your server, then run:

```
docker-compose up -d
```

## 8. Inter-Service Communication

The Admin API publishes book updates to a Redis channel. The Frontend API subscribes to this channel and updates its database accordingly, ensuring consistency between the two services.

## 9. Future Improvements

- Implement authentication and authorization
- Add more comprehensive error handling and logging
- Implement a more robust database solution for production use
- Create a frontend client application
- Implement book return functionality
