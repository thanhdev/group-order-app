# Group Ordering Application

## Overview

This project is an application designed to facilitate group food and drink orders. Users can individually create their orders and then a designated member can host these orders by creating a group order. Once the group order is complete, each member's balance will be calculated based on the price of their individual orders and actual amount of the group order.

## Features

- **User Authentication**: Secure authentication using Auth0, supporting both regular accounts and social accounts (Google).
- **Order Management**: Users can create their own orders and join group orders.
- **Balance Calculation**: Automatic calculation of each member's balance based on their orders.

## Technology Stack

- **Backend Framework**: Django 4.2.13
- **API Framework**: Django REST Framework 3.15.1
- **Authentication**: Auth0
- **API Documentation**: drf-spectacular
- **Static File Handling**: WhiteNoise
- **Database**: PostgreSQL
- **Deployment**: Vercel

## Setup and Installation

### Prerequisites

- Python 3.8+
- Pipenv or virtualenv for managing dependencies
- PostgreSQL database

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/thanhdev/group-order-app
   cd group-order-app
   ```

2. **Set up a virtual environment**:

    Using virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory of your project and add the necessary environment variables:
   ```
   POSTGRES_DB=your_database_name
   POSTGRES_USER=your_database_user
   POSTGRES_PASSWORD=your_database_password
   POSTGRES_URL=your_postgresql_url
   AUTH0_CLIENT_ID=your_auth0_client_id
   AUTH0_CLIENT_SECRET=your_auth0_client_secret
   AUTH0_DOMAIN=your_auth0_domain
   DATABASE_URL=your_postgresql_database_url
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Deployment

The application is deployed on Vercel as serverless functions using the Python runtime, enabling continuous deployment. For deployment instructions, follow Vercel's documentation on deploying Python applications.

Link: https://group-order.vercel.app

## API Documentation

API documentation is provided using drf-spectacular. Once the server is running, you can access the documentation at `/api/schema/` for the schema and `/api/docs/` for the interactive documentation.

## Static Files and Frontend

WhiteNoise is used to serve static files and the frontend application. Ensure that your static files are collected and served correctly by running:
```bash
python manage.py collectstatic -c --noinput
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.
