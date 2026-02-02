# Django Polls Tutorial - Advanced Edition

A production-ready Django REST API application built as an extended version of the official Django tutorial. This project demonstrates a polling application with advanced features including role-based access control (RBAC), attribute-based access control (ABAC), audit logging, and comprehensive security policies.

## 📑 Table of Contents

- [🚀 Features](#-features)
- [📋 Prerequisites](#-prerequisites)
- [🛠️ Installation](#️-installation)
- [🚦 Running the Application](#-running-the-application)
- [📚 API Endpoints](#-api-endpoints)
  - [Authentication](#authentication)
  - [Questions](#questions)
  - [Choices (Voting)](#choices-voting)
  - [Admin Panel](#admin-panel)
- [🏗️ Project Structure](#️-project-structure)
- [🔑 Key Architecture Patterns](#-key-architecture-patterns)
  - [Domain-Driven Design](#domain-driven-design)
  - [Security Design](#security-design)
  - [Transaction Safety](#transaction-safety)
- [🧪 Testing](#-testing)
- [🛠️ Makefile Commands](#️-makefile-commands)
- [🔒 Security Configuration](#-security-configuration)
  - [JWT Authentication](#jwt-authentication)
  - [Rate Limiting](#rate-limiting)
  - [CORS Configuration](#cors-configuration)
- [🌐 Frontend Integration](#-frontend-integration)
- [📝 Models](#-models)
  - [Question](#question)
  - [Choice](#choice)
- [🔐 Permissions & Roles](#-permissions--roles)
  - [Roles](#roles)
  - [Permission Classes](#permission-classes)
- [📊 Audit Logging](#-audit-logging)
- [🚧 Development Setup](#-development-setup)
- [🐛 Known Issues](#-known-issues)
- [📄 License](#-license)
- [🤝 Contributing](#-contributing)
- [📚 Resources](#-resources)

## 🚀 Features

- **RESTful API**: Built with Django REST Framework
- **Voting System**: Create questions and vote on multiple choice options
- **Advanced Security**:
  - Role-Based Access Control (RBAC)
  - Attribute-Based Access Control (ABAC)
  - Audit logging for all voting actions
  - JWT Authentication
- **Permissions**:
  - Voter role for voting on polls
  - Moderator role for administrative actions
- **API Throttling**: Rate limiting to prevent abuse
- **CORS Support**: Configured for local development with React/Vue frontends

## 📋 Prerequisites

- Python 3.10+
- Virtual environment (venv)
- SQLite (default database)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd djangotutorial
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source ./venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install Django djangorestframework djangorestframework-simplejwt django-cors-headers django-extensions
   ```

4. **Run migrations**:
   ```bash
   make migrate
   # Or manually:
   # ./venv/bin/python manage.py makemigrations
   # ./venv/bin/python manage.py migrate
   ```

5. **Create a superuser** (optional but recommended):
   ```bash
   ./venv/bin/python manage.py createsuperuser
   ```

## 🚦 Running the Application

### Start the development server:
```bash
make dev-backend
# Or manually:
# ./venv/bin/python manage.py runserver --noreload
```

The API will be available at `http://localhost:8000/`

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/token/` - Obtain JWT access and refresh tokens
- `POST /api/v1/auth/token/refresh/` - Refresh an expired access token

### Questions
- `GET /api/v1/questions/` - List all questions with total votes
- `GET /api/v1/questions/{id}/` - Retrieve a specific question
- `POST /api/v1/questions/` - Create a new question (admin only)
- `PUT /api/v1/questions/{id}/` - Update a question (admin only)
- `DELETE /api/v1/questions/{id}/` - Delete a question (admin only)

### Choices (Voting)
- `POST /api/v1/choices/{id}/vote/` - Vote on a choice (requires Voter role)
- `POST /api/v1/choices/{id}/un_vote/` - Remove a vote (requires Moderator role)

### Admin Panel
- `GET /admin/` - Django admin interface

## 🏗️ Project Structure

```
djangotutorial/
├── mysite/                  # Main project configuration
│   ├── settings.py         # Django settings with REST framework & security config
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI configuration
├── polls/                   # Polls application
│   ├── models.py           # Question and Choice models
│   ├── views.py            # ViewSets for API endpoints
│   ├── serializers.py      # DRF serializers
│   ├── admin.py            # Admin panel configuration
│   ├── permissions/        # Permission classes (RBAC & ABAC)
│   │   ├── permissions.py  # IsVoter, IsModerator
│   │   ├── rbac.py         # Role-based access control
│   │   └── abac.py         # Attribute-based access control
│   ├── security/           # Security infrastructure
│   │   ├── actions.py      # Action definitions for audit logging
│   │   ├── audit.py        # Audit logging functionality
│   │   ├── roles.py        # Role definitions
│   │   └── policy/         # Policy enforcement
│   ├── services/           # Business logic layer
│   │   └── voting.py       # Vote/unvote service functions
│   ├── domain/             # Domain-specific logic
│   │   └── voting/         # Voting domain logic
│   ├── urls/               # URL routing
│   │   └── v1.py          # API v1 routes
│   └── tests/              # Test suite
│       └── test_voting_service.py
├── Makefile                # Development commands
├── manage.py               # Django management script
├── db.sqlite3              # SQLite database
└── README.md               # This file
```

## 🔑 Key Architecture Patterns

### Domain-Driven Design
The application separates concerns into layers:
- **Views**: Handle HTTP requests/responses
- **Services**: Contain business logic (e.g., `vote()`, `unvote()`)
- **Models**: Define data structure
- **Permissions**: Enforce access control
- **Domain**: Core domain logic and contracts

### Security Design
1. **RBAC (Role-Based Access Control)**: Users are assigned roles (Voter, Moderator)
2. **ABAC (Attribute-Based Access Control)**: Fine-grained permissions based on context
3. **Audit Logging**: All voting actions are logged with user, action, resource, and decision
4. **Policy Enforcement**: Centralized policy decisions before executing business logic

### Transaction Safety
All vote operations use database transactions to ensure atomicity and prevent race conditions.

## 🧪 Testing

Run the test suite:
```bash
make test-polls
# Or manually:
# ./venv/bin/python manage.py test polls.tests
```

## 🛠️ Makefile Commands

- `make migrate` - Run database migrations
- `make dev-backend` - Start development server
- `make graph` - Generate polls app model diagram
- `make graph-full` - Generate full project model diagram
- `make test-polls` - Run polls app tests

## 🔒 Security Configuration

### JWT Authentication
The application uses JWT (JSON Web Tokens) for authentication. Configure token settings in `settings.py`.

### Rate Limiting
Anonymous users are limited to 10 requests per minute to prevent API abuse.

### CORS Configuration
CORS is enabled for:
- `http://localhost:3000` (React default)
- `http://localhost:5173` (Vite default)

## 🌐 Frontend Integration

This API is designed to work with modern frontend frameworks. Example CORS origins are configured for:
- React (port 3000)
- Vue/Vite (port 5173)

## 📝 Models

### Question
- `question_text`: CharField (max 200 characters)
- `pub_date`: DateTimeField (publication date)

### Choice
- `question`: ForeignKey to Question
- `choice_text`: CharField (max 200 characters)
- `votes`: IntegerField (default: 0)

## 🔐 Permissions & Roles

### Roles
- **Voter**: Can vote on poll choices
- **Moderator**: Can remove votes and perform admin actions

### Permission Classes
- `IsVoter`: Requires user to have Voter role
- `IsModerator`: Requires user to have Moderator role
- `CanVote`: ABAC permission that evaluates voting context

## 📊 Audit Logging

All voting actions are logged with the following format:
```
[AUDIT] user=<user_id> action=<action> resource=<resource> allowed=<true/false> reason=<reason>
```

Logs are written to the console and can be configured to write to files in production.

## 🚧 Development Setup

### Generate Database Schema Diagrams
```bash
make graph        # Polls app only
make graph-full   # All apps including Django built-ins
```

### Access Django Admin
1. Create a superuser: `./venv/bin/python manage.py createsuperuser`
2. Navigate to `http://localhost:8000/admin/`
3. Log in with your superuser credentials

## 🐛 Known Issues

- Line 19 in `Makefile` has a typo: `$(PHTHON)` should be `$(PYTHON)`

## 📄 License

This project is for educational purposes based on the Django official tutorial.

## 🤝 Contributing

This is a learning project. Feel free to fork and experiment!

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Original Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
