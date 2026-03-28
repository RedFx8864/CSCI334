# CSCI334

ParkingManagment

Setup Instructions:

1. Clone repository and open directory with Pipfile.lock in vscode (or other IDE)
2. Run virtual env with 'pipenv shell' (make sure pipenv is installed (pip install pipenv))
3. Install dependencies with 'pipenv install'
4. Generate django secret key with 'python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"' and copy it
5. Navigate to ParkingProject where manage.py is, and create .env file.
6. Add line 'SECRET_KEY=your-generated-secret-key'
7. Apply migrations with 'python manage.py migrate'
8. Create superuser with 'python manage.py createsuperuser' (for django's built in admin access through localhost:port/admin)
9. Run server with 'python manage.py runserver <port number, or leave blank for 8000>'
10. Development server should be running at 'localhost:port' (port: 8000 or ur input port number)
