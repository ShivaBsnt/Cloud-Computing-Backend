# Cloud Computing Backend

Short description of the project.

## Requirements

- Python 3.x
- Django
- Django REST Framework

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <project-folder>
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser (optional):

```bash
python manage.py createsuperuser
```

## Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```
http://127.0.0.1:8000/
```

## Running Tests

```bash
python manage.py test
```

## License

This project is licensed under the MIT License.