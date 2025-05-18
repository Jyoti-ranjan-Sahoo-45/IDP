# Intelligent Document Processing (IDP) System

A comprehensive web application for extracting, analyzing, and processing information from various document formats using OCR and NLP technologies.

## Features

- **Document Upload & Management**: Upload, view, and manage documents in various formats (PDF, images, text files)
- **OCR Processing**: Extract text from scanned documents, PDFs, and images
- **Entity Recognition**: Identify and extract named entities (people, organizations, locations, dates, etc.)
- **Sentiment Analysis**: Analyze the sentiment of document content
- **Keyword Extraction**: Identify important keywords and terms
- **User Management**: Secure authentication and user-specific document storage
- **Responsive UI**: Modern, mobile-friendly interface

## Technology Stack

- **Backend**: Python, Django
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: MySQL
- **OCR Engine**: Tesseract OCR
- **NLP**: spaCy, NLTK

## Installation

### Prerequisites

- Python 3.7+
- MySQL 8.0+
- Tesseract OCR 4.0+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**

```bash
git clone <repository-url>
cd idp-system
```

2. **Create and activate a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install required packages**

```bash
pip install -r requirements.txt
```

4. **Install additional dependencies**

```bash
# Download spaCy model
python -m spacy download en_core_web_sm

# Download NLTK data
python -m nltk.downloader punkt stopwords vader_lexicon
```

5. **Configure MySQL database**

Create a MySQL database named `idp` and configure the settings in `idp_system/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "idp",
        "USER": "your_mysql_username",
        "PASSWORD": "your_mysql_password",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

6. **Apply database migrations**

```bash
python manage.py migrate
```

7. **Create a superuser for admin access**

```bash
python manage.py createsuperuser
```

8. **Create required directories**

Ensure the following directories exist in the project:
- `media`: For storing uploaded files
- `static`: For static files
- `staticfiles`: For collected static files

```bash
mkdir -p media static staticfiles
```

9. **Run the development server**

```bash
python manage.py runserver
```

The application should now be running at http://127.0.0.1:8000/

## Usage

1. **Login or create an account**
   - Access the application at http://127.0.0.1:8000/
   - Log in using your credentials or use the admin account created earlier

2. **Upload a document**
   - Navigate to the "Upload" page
   - Fill in the document details and select a file
   - Click "Upload Document"

3. **Process the document**
   - Go to your document list
   - Click "Process" on the document you want to analyze
   - Wait for the processing to complete

4. **View results**
   - Once processing is complete, you can view:
     - Extracted text
     - Named entities
     - Sentiment analysis
     - Keywords and other insights

5. **Download or delete documents**
   - Use the available actions on the document detail page

## Directory Structure

```
idp_system/
├── idp_system/              # Project settings and configuration
│   ├── migrations/          # Database migrations
│   ├── models.py            # Data models
│   ├── views.py             # Views and request handlers
│   ├── forms.py             # Forms for data input
│   ├── utils/               # Utility functions
│   │   ├── ocr.py           # OCR processing utilities
│   │   ├── nlp.py           # NLP processing utilities
│   │   ├── document_processor.py # Main document processing logic
├── templates/               # HTML templates
│   ├── auth/                # Authentication templates
│   ├── document_processor/  # Application templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User-uploaded files
├── manage.py                # Django management script
├── requirements.txt         # Project dependencies
```

## Security Considerations

- File uploads are validated for type and size
- User authentication is required for all document operations
- Each user can only access their own documents
- All forms include CSRF protection
- File paths are sanitized to prevent path traversal attacks
- Sensitive configurations should be moved to environment variables in production

## Deployment Considerations

For production deployment:

1. **Set DEBUG = False** in settings.py
2. Configure a production-ready web server (Nginx, Apache)
3. Use a WSGI server (Gunicorn, uWSGI)
4. Set up proper SSL/TLS
5. Configure proper file permissions
6. Use environment variables for sensitive information
7. Set up regular database backups
8. Consider using a CDN for static files
9. Implement monitoring and logging

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [spaCy](https://spacy.io/)
- [NLTK](https://www.nltk.org/)
- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/) 