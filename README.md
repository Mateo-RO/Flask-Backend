# Project Manager API (Flask + MySQL)

This is the backend for my first-year project: a project management system built with Flask and MySQL. It handles users, projects, lists, and tasks with full CRUD operations, and supports integration with a React frontend via CORS.

## Technologies used:
- Python + Flask
- MySQL
- Flask-CORS
- Postman (testing)

## Endpoints Overview
- `/usuarios` → manage users  
- `/proyectos` → projects per user  
- `/listas` → lists per project  
- `/tareas` → tasks per list  
- `/listas/<id>/tareas` → tasks by list

## Run Locally
1. Create a MySQL database (you can name it however you want).
2. Set your DB credentials and name in the Python file.
3. Run the app:

```bash
python <your_filename>.py
