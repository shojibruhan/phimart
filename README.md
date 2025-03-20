# PhiMart API Documentation

## Introduction

PhiMart is a RESTful API built using Django REST Framework (DRF) for an e-commerce platform. It provides endpoints for managing products, categories, orders, and shopping carts. JWT authentication is implemented using djoser, and API documentation is generated using drf-yasg (Swagger).

## Features

* **Product Management:** Create, read, update, and delete products.
* **Category Management:** Create, read, update, and delete product categories.
* **Order Management:** Place orders, view order history.
* **Cart Management:** Add, remove, and view items in the shopping cart.
* **JWT Authentication:** Secure API access using JSON Web Tokens (JWT).
* **Swagger Documentation:** Interactive API documentation for easy testing and exploration.

## Technologies Used

* **Django:** Python web framework.
* **Django REST Framework (DRF):** Toolkit for building Web APIs.
* **djoser:** REST implementation of Django authentication system.
* **drf-yasg:** Swagger/OpenAPI 2.0 and 3.0 spec generator for DRF.
* **JWT (JSON Web Tokens):** For authentication.

## Getting Started

### Prerequisites

* Python (3.7+)
* pip
* Virtual environment (recommended)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <https://github.com/shojibruhan/phimart>
    cd PhiMart
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

### API Documentation

* Access the Swagger UI at `http://127.0.0.1:8000/swagger/` (or the appropriate address if you're using a different port or host).
* Access the ReDoc documentation at `http://127.0.0.1:8000/redoc/`.

### API Endpoints

#### Authentication

| Method | Endpoint              | Description              | Authentication |
| :----- | :-------------------- | :----------------------- | :------------- |
| POST   | `/auth/users/`        | Register a new user      | None           |
| POST   | `/auth/jwt/create/`   | Obtain a JWT token       | None           |
| POST   | `/auth/jwt/refresh/`  | Refresh a JWT token      | None           |

#### Products

| Method | Endpoint            | Description                  | Authentication |
| :----- | :------------------ | :--------------------------- | :------------- |
| GET    | `/products/`        | List all products            | Optional       |
| POST   | `/products/`        | Create a new product         | Admin Required |
| GET    | `/products/{id}/`    | Retrieve a specific product  | Optional       |
| PUT    | `/products/{id}/`    | Update a product             | Admin Required |
| DELETE | `/products/{id}/`   | Delete a product             | Admin Required |

#### Categories

| Method | Endpoint             | Description                   | Authentication |
| :----- | :------------------- | :---------------------------- | :------------- |
| GET    | `/categories/`       | List all categories           | Optional       |
| POST   | `/categories/`       | Create a new category         | Admin Required |
| GET    | `/categories/{id}/`   | Retrieve a specific category  | Optional       |
| PUT    | `/categories/{id}/`   | Update a category             | Admin Required |
| DELETE | `/categories/{id}/`  | Delete a category             | Admin Required |

#### Orders

| Method | Endpoint          | Description                 | Authentication |
| :----- | :---------------- | :-------------------------- | :------------- |
| POST   | `/orders/`        | Create a new order          | User Required  |
| GET    | `/orders/`        | List user's orders          | User Required  |
| GET    | `/orders/{id}/`    | Retrieve a specific order   | User Required  |

#### Carts

| Method | Endpoint           | Description                 | Authentication |
| :----- | :----------------- | :-------------------------- | :------------- |
| GET    | `/carts/`          | Retrieve the user's cart    | User Required  |
| POST   | `/carts/add/`      | Add an item to the cart     | User Required  |
| POST   | `/carts/remove/`   | Remove an item from the cart| User Required  |
| POST   | `/carts/clear/`    | Clear the cart              | User Required  |

### Authentication

* All endpoints requiring authentication use JWT tokens.
* Include the `Authorization: Bearer <token>` header in your requests.

### Example Usage (using `curl`)

#### Obtaining a JWT token

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}' [http://127.0.0.1:8000/auth/jwt/create/](http://127.0.0.1:8000/auth/jwt/create/)