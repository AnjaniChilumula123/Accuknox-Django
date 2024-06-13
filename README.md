# 📱 Social Networking API

A Django-based social networking API with functionalities for user registration, login, sending friend requests, accepting/rejecting friend requests, and searching for users.

Postman Collection for all API's : 
https://www.postman.com/technical-administrator-80202700/workspace/accuknox-django-problem/collection/33323466-9f8f62e7-8259-4c1b-8be1-3050392da856?action=share&creator=33323466 

## 🌟 Features

- 🔐 User Registration and Login
- 🔄 JWT Authentication for Secure Access
- 👫 Send, Accept, and Reject Friend Requests
- 🔍 Search for Users
- 🧑‍🤝‍🧑 List Friends

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Docker
- Docker Compose (optional, if you want to use it for easier management)
- Django 3.2+
- Django REST Framework
- Django REST Framework SimpleJWT
- MongoDB, Pymongo and Djongo (if using MongoDB as the database)

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/social-networking-api.git
   cd social-networking-api

2. Create Virtual Environment

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies

    ```sh
   pip install -r requirements.txt

![Screenshot 2024-06-11 192114](https://github.com/AnjaniChilumula123/Accuknox-Django/assets/93757236/ae9d39e3-c960-4c2d-993f-58bdfd2a7e0f)

use the token in the headers :

   ### Key : Authentication
   ### Value : 'Bearer [access token]'

Refresh token is used to refresh the access token, which expire for every 5 minutes
   ### 


## Using Docker

1. Build the Docker image:
   
    ```sh
    docker build -t my_django_app .

3. Run the Docker container:
    ```sh
    docker run --name my_django_app_container -p 8000:8000 my_django_app

4. Apply migrations:
    ```sh
    docker exec -it my_django_app_container python manage.py makemigrations
    docker exec -it my_django_app_container python manage.py migrate

5. Create a superuser:
   ```sh
   docker exec -it my_django_app_container python manage.py createsuperuser

6. Access the application:
   ```sh
    Open your browser and go to http://localhost:8000

