# 📘 UserNotes Django Application

## 📜 Description

This is a UserNotes application created using Django REST Framework. It provides APIs for managing notes.

## 🚀 Setup Instructions

### Without Docker

#### 📋 Prerequisites
- Python 3.11
- pip (Python package manager)

#### 🔧 Steps
1. Clone the repository:
   ```bash
   git clone [repository_url]
   ```
2. Navigate to the project directory:
   ```bash
   cd [project_name]
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Unix or MacOS: `source venv/bin/activate`
5. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
6. Apply the migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Run the server:
   ```bash
   python manage.py runserver
   ```

### With Docker

#### 🐳 Prerequisites
- Docker
- Docker Compose

#### 🔧 Steps
1. Clone the repository:
   ```bash
   git clone [repository_url]
   ```
2. Navigate to the project directory:
   ```bash
   cd [project_name]
   ```
3. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```
4. To access the bash shell:
    ```bash
    docker-compose exec web bash
    ```

## 🌐 Accessing the Application

The application will be accessible at http://127.0.0.1:8000.

## 📚 Swagger API Documentation

To access the Swagger API documentation, visit http://127.0.0.1:8000/api/schema/swagger-ui/.

## 🧪 Running Tests

To run tests, execute the following command:

```bash
python manage.py test
```

## 🏗️ Creating Migrations

To create new migrations based on the changes you've made to your models:

```bash
python manage.py makemigrations
```

With docker
```bash
docker-compose exec web python manage.py makemigrations
```

To apply the migrations to the database:

```bash
python manage.py migrate
```
With docker:

```bash
docker-compose exec web python manage.py migrate
```
---

**Note**: Replace `[repository_url]` and `[project_name]` with the actual URL of your repository and the name of your project directory.
