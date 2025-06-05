# Tailwebs Teacher Portal

A web-based portal for teachers to manage their profiles, classes, and student information.

## Overview

The Tailwebs Teacher Portal is a Django-based web application that provides teachers with a centralized platform to manage their educational activities. The portal features user authentication, profile management, and a responsive interface built with Tailwind CSS.

## Features

- **User Authentication**: Secure login and registration system for teachers
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS
- **Profile Management**: Teachers can view and update their profile information
- **Modern UI**: Clean and intuitive user interface

## Technology Stack

- **Backend**: Django 3.2
- **Frontend**: HTML, JavaScript, Tailwind CSS
- **Database**: PostgreSQL (production), SQLite (development)
- **Deployment**: Docker, Render

## Installation

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- Git

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd teacher-portal
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up static files:
   ```bash
   python setup_static.py
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at http://localhost:8000

## Deployment

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t teacher-portal .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 teacher-portal
   ```

### Deploying to Render

This project is configured for deployment on Render. The `render.yaml` file contains the necessary configuration.

1. Push your code to a Git repository
2. Connect your repository to Render
3. Render will automatically deploy your application

## Project Structure

```
teacher-portal/
├── Teacher_portal/       # Main Django project directory
├── portal/               # Main application directory
├── static/               # Static files (CSS, JS, images)
├── staticfiles/          # Collected static files for production
├── Dockerfile            # Docker configuration
├── render.yaml           # Render deployment configuration
├── requirements.txt      # Python dependencies
└── setup_static.py       # Script to set up static directories
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

