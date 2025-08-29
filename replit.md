# Overview

Biryani Club is a full-featured restaurant ordering and delivery application built with Flask. The application provides a complete online food ordering experience with features including menu browsing, cart management, user authentication, order processing, admin controls, and UPI payment integration. The system supports both registered users and guest checkout, with role-based access control for customers, delivery personnel, and administrators.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses a responsive web interface built with Bootstrap 5 and modern CSS. The frontend is implemented using Jinja2 templating with Flask, featuring a mobile-first design approach. The interface includes progressive web app (PWA) capabilities with service worker support for offline functionality and app-like user experience.

## Backend Architecture
The system follows a traditional MVC pattern using Flask as the web framework. The application is structured with separate modules for models, routes, and utilities to maintain clean separation of concerns. The backend handles user authentication, session management, order processing, and administrative functions.

## Data Storage Solutions
The application uses SQLAlchemy ORM with support for both SQLite (development) and PostgreSQL (production). The database schema includes entities for users, menu items, cart items, orders, order items, promotions, and store settings. The system supports automatic table creation and migration handling.

## Authentication and Authorization
User authentication is implemented using Werkzeug's password hashing with session-based login management. The system includes role-based access control with three user types: customers, delivery personnel, and administrators. Protected routes use decorators to enforce authentication and authorization requirements.

## Payment Integration
The application integrates UPI payment processing with QR code generation for seamless mobile payments. Payment status tracking is implemented to monitor transaction completion and order fulfillment workflow.

## Order Management System
The platform includes comprehensive order management with status tracking (pending, confirmed, preparing, out for delivery, delivered, cancelled). The system supports both guest and registered user ordering, with automatic cart management and order history tracking.

# External Dependencies

## Web Framework and Core Libraries
- Flask 3.1.1+ for web application framework
- Flask-SQLAlchemy 3.1.1+ for database ORM
- SQLAlchemy 2.0.43+ for database operations
- Werkzeug 3.1.3+ for security utilities and WSGI support

## Database Support
- PostgreSQL support via psycopg2-binary 2.9.10+
- SQLite for development and testing environments
- Database connection pooling and health check features

## Frontend Dependencies
- Bootstrap 5.3.0 for responsive UI framework
- Font Awesome 6.0.0 for iconography
- Google Fonts (Poppins) for typography
- Bootstrap Icons for additional icon support

## Payment Processing
- QRCode library with PIL support for UPI payment QR code generation
- Base64 encoding for image embedding in HTML templates

## Development and Deployment
- Gunicorn 23.0.0+ for production WSGI server
- Email-validator 2.2.0+ for input validation
- Environment variable configuration for deployment flexibility

## PWA Features
- Service worker for offline functionality and caching
- Web app manifest for progressive web app capabilities
- Mobile-optimized interface with app-like experience

## Security Features
- ProxyFix middleware for handling reverse proxy headers
- Session management with configurable timeout
- Password hashing and secure authentication
- CSRF protection through form validation