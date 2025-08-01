# PostgreSQL
This is a basic Flask-based web application for creating, viewing, editing, and deleting notes, with support for tagging.

## Features

* **Create Notes**: Add new notes with a title, description, and associated tags.
* **View Notes**: Browse all notes on the homepage.
* **Edit Notes**: Modify existing notes, including their title, description, and tags.
* **Delete Notes**: Remove notes from the application.
* **Tagging**: Organize notes using tags.
* **View Notes by Tag**: See all notes associated with a specific tag.
* **Edit Tags**: Change the name of an existing tag.
* **Delete Tags**: Remove tags from the system.

## Setup Instructions

### 1. Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.9**: This application is built with Python.
* **PostgreSQL**: The application uses PostgreSQL as its database. Make sure it's installed and running.

### 2. Database Setup

Create a PostgreSQL database and a user for the application.

```sql
CREATE USER coe WITH PASSWORD 'CoEpasswd';
CREATE DATABASE coedb OWNER coe;
```
---

### 3\. Project Structure

Set up your project directory with the following structure:

```
your_project_folder/
├── .venv/ (your Python virtual environment)
├── requirements.txt
├── noteapp.py
├── forms.py
├── models.py
└── templates/
    ├── base.html
    ├── index.html
    ├── notes-create.html
    ├── notes-edit.html
    ├── tags-view.html
    └── tags-edit.html
```
### 4\. Virtual Environment & Dependencies

Navigate to your project folder in the terminal and set up a Python virtual environment:

```bash
python -m venv .venv
# On macOS/Linux
source .venv/bin/activate
# On Windows
.venv\Scripts\activate
```

Now, install the required Python packages:

```bash
pip install -r requirements.txt
```

## Troubleshooting

  * **`jinja2.exceptions.TemplateNotFound`**: This means Flask can't find one of your HTML template files. Make sure all `.html` files (e.g., `notes-edit.html`, `tags-edit.html`) are correctly placed inside the `templates` directory.
  * **`AttributeError: 'str' object has no attribute '_sa_instance_state'`**: This error usually occurs when you try to assign plain strings to a SQLAlchemy relationship field that expects model objects. The provided `noteapp.py` code has a fix for the `notes_edit` function that ensures `Tag` objects are used correctly.
  * **Database Connection Issues**: Double-check your `SQLALCHEMY_DATABASE_URI` in `noteapp.py`. Also, ensure your PostgreSQL server is running and the `coe` user has the necessary access to the `coedb` database.
  * **WTForms Validation Errors**: If your form isn't submitting correctly, check your terminal. The `print("error", form.errors)` line in your Flask app will output validation messages, helping you identify what's wrong with the form data.
