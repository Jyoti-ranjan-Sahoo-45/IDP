# Intelligent Document Processing (IDP) System

## About

The IDP System is a comprehensive document management and analysis platform designed to extract meaningful information from various document formats. It combines traditional OCR techniques with advanced AI-powered recognition technologies to provide accurate text extraction from both printed and handwritten documents.

### Core Capabilities

- **Hybrid Recognition Engine**: Combines local processing with cloud-based OCR for superior accuracy
- **Offline & Online Processing**: Functions fully offline with enhanced results when internet-connected
- **Self-Learning System**: Continuously improves by tracking recognition performance metrics
- **Multi-Service Architecture**: Automatically routes requests to the most effective OCR service
- **Fallback Mechanisms**: Ensures consistent operation even when services are unavailable

The system leverages multiple free OCR APIs without requiring API keys, making it accessible while providing enterprise-grade recognition capabilities.

## Features

- **Document Upload & Management**: Upload, view, and manage documents in various formats (PDF, images, text files)
- **OCR Processing**: Extract text from scanned documents, PDFs, and images
- **Handwriting Recognition**: Extract text from handwritten documents using OpenCV and Tesseract
- **Online OCR Enhancement**: Improve recognition accuracy using free cloud OCR services
- **Entity Recognition**: Identify and extract named entities (people, organizations, locations, dates, etc.)
- **Sentiment Analysis**: Analyze the sentiment of document content
- **Keyword Extraction**: Identify important keywords and terms
- **Signature Detection**: Detect and verify signatures within documents
- **Admin Interface**: Comprehensive admin dashboard for managing documents and processing results
- **User Management**: Secure authentication and user-specific document storage
- **Responsive UI**: Modern, mobile-friendly interface

## Technology Stack

- **Backend**: Python, Django
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development), MySQL (production)
- **OCR Engine**: Tesseract OCR
- **Computer Vision**: OpenCV
- **NLP**: spaCy, NLTK
- **Scripts**: PowerShell and Batch scripts for Windows environments

## Installation

### Prerequisites

- Python 3.7+
- Tesseract OCR 4.0+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**

```bash
git clone <repository-url>
cd idp-project
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

4. **Install Tesseract OCR**

Using the provided installation helper:

```bash
# Windows CMD
install_tesseract.bat

# PowerShell
powershell -ExecutionPolicy Bypass -File .\install_tesseract.ps1
```

Or manually download and install from: https://github.com/UB-Mannheim/tesseract/wiki

5. **Apply database migrations**

```bash
python manage.py migrate
```

6. **Create a superuser for admin access**

```bash
python manage.py createsuperuser
```

7. **Create required directories**

Ensure the following directories exist in the project:
- `media`: For storing uploaded files
- `static`: For static files
- `handwriting_ai/data`: For storing handwriting recognition training data

```bash
mkdir -p media static handwriting_ai/data
```

8. **Run the development server**

Using the provided server script:

```bash
# Windows CMD
run_server.bat

# PowerShell
powershell -ExecutionPolicy Bypass -File .\run_server.ps1
```

Or directly with Django:

```bash
python manage.py runserver
```

The application should now be running at http://127.0.0.1:8000/

## Usage

1. **Login or create an account**
   - Access the application at http://127.0.0.1:8000/
   - Log in using your credentials or use the admin account created earlier
   - Access the admin interface at http://127.0.0.1:8000/admin/

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
     - Extracted text (including handwritten text if applicable)
     - Named entities
     - Sentiment analysis
     - Keywords and other insights
     - Detected signatures

5. **Download or delete documents**
   - Use the available actions on the document detail page

## Project Structure

```
idp_project/
├── idp_project/              # Project settings and configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
├── document_processor/       # Main application
│   ├── migrations/           # Database migrations
│   ├── models.py             # Data models for documents and processing results
│   ├── views.py              # Views and request handlers
│   ├── admin.py              # Admin interface configuration
│   ├── urls.py               # App URL configuration
│   ├── document_processing.py# Document processing logic
│   ├── templates/            # App-specific templates
├── handwriting_ai/           # Handwriting recognition module
│   ├── models/               # AI model implementations
│   │   ├── opencv_recognition.py  # OpenCV-based handwriting recognizer
│   ├── data/                 # Training data and parameters
│   ├── train_recognition.py  # Training and optimization scripts
├── templates/                # HTML templates
├── static/                   # Static files (CSS, JS, images)
├── media/                    # User-uploaded files
├── samples/                  # Sample documents for testing
├── manage.py                 # Django management script
├── requirements.txt          # Project dependencies
├── run_server.bat            # Batch script to run the server (Windows CMD)
├── run_server.ps1            # PowerShell script to run the server
├── install_tesseract.bat     # Batch script to install Tesseract (Windows CMD)
├── install_tesseract.ps1     # PowerShell script to install Tesseract
├── train_handwriting.bat     # Batch script to train handwriting recognition
└── README.md                 # Project documentation
```

## Admin Interface

The administrative interface provides comprehensive management capabilities:

1. **Document Types Management**
   - Create and manage different document categories
   - Configure processing options for each type

2. **Documents Management**
   - View and filter all uploaded documents
   - Check document status and processing results
   - Trigger manual processing

3. **Processing Results Management**
   - Review extracted text, entities, and sentiment analysis
   - Verify handwriting recognition results

4. **Named Entities Viewing**
   - Browse all extracted entities by type
   - Filter by confidence score and document

5. **Signature Management**
   - View detected signatures
   - Verify signature authenticity
   - Compare signatures across documents

## Helper Scripts

### Windows CMD Scripts

1. **run_server.bat**
   - Checks for Tesseract OCR installation
   - Verifies required Python packages
   - Applies database migrations
   - Starts the Django development server

2. **install_tesseract.bat**
   - Checks if Tesseract is already installed
   - Provides download and installation instructions
   - Tests Tesseract functionality

3. **train_handwriting.bat**
   - Guides through the handwriting recognition model training
   - Collects training data and runs optimization

### PowerShell Scripts

1. **run_server.ps1**
   - Enhanced version of run_server.bat with better error handling
   - Color-coded output for improved readability
   - Same functionality as the batch version

2. **install_tesseract.ps1**
   - PowerShell version of the Tesseract installation helper
   - Interactive prompts with improved user experience

## Training the Handwriting Recognition Model

The system includes a handwriting recognition module that can be trained to improve accuracy for specific handwriting styles or document types. Follow these detailed steps to train the model:

### Prerequisites

- Make sure Tesseract OCR is properly installed (see Installation section)
- Prepare sample handwriting images for training
- Ensure you have the correct transcriptions for each sample image

### Option 1: Using the Command Line Interface

1. **Collect Training Data**

   ```bash
   # Windows
   python handwriting_ai/train_recognition.py --collect
   
   # PowerShell
   python .\handwriting_ai\train_recognition.py --collect
   ```

   This interactive process will:
   - Prompt you to provide paths to sample handwriting images
   - Ask for the ground truth text for each image
   - Store the training data in the `handwriting_ai/data` directory

2. **Optimize Recognition Parameters**

   ```bash
   # Windows
   python handwriting_ai/train_recognition.py --optimize
   
   # PowerShell
   python .\handwriting_ai\train_recognition.py --optimize
   ```

   During this step, the system will:
   - Load your training samples
   - Run through different parameter combinations for image preprocessing
   - Test Tesseract OCR with various segmentation modes
   - Find the optimal parameters that maximize text recognition accuracy
   - Save these parameters to `handwriting_ai/data/optimal_params.json`

3. **Test the Optimized Parameters**

   ```bash
   # Windows
   python handwriting_ai/train_recognition.py --test
   
   # PowerShell
   python .\handwriting_ai\train_recognition.py --test
   ```

   This will:
   - Prompt you to provide a test image path
   - Apply the optimized parameters to the test image
   - Show the recognition results
   - Display a comparison of results with and without optimization

### Option 2: Using the PowerShell Script

For Windows users, a convenience script is provided:

1. **Run the Training Script**

   ```powershell
   # From your project root
   powershell -ExecutionPolicy Bypass -File .\train_handwriting.ps1
   ```

   This script will:
   - Check if Tesseract is installed
   - Guide you through the entire training process
   - Provide a user-friendly interface for each step

### Training Parameters Explained

The optimization process tunes the following parameters:

1. **CLAHE Clip Limit**: Controls contrast enhancement (values 1.0-4.0)
2. **Adaptive Threshold Block Size**: Affects text segmentation (values 7-15, odd numbers only)
3. **Adaptive Threshold C**: Fine-tunes thresholding sensitivity (values 1-5)
4. **Morphological Kernel Size**: Controls cleanup operations (values 1-3)
5. **Denoising Strength**: Reduces image noise (values 5-15)
6. **Tesseract PSM Mode**: Page segmentation mode (values 3, 6, 7, 8, or 13)

### Understanding the Results

After optimization, the system generates:

1. **Parameter File**: `handwriting_ai/data/optimal_params.json` containing the best parameter values
2. **Performance Report**: Shows recognition accuracy before and after optimization
3. **Visualization**: (When using `--test`) Displays each preprocessing step's effect on the image

### Tips for Better Results

1. **Use diverse samples** representing the handwriting styles you expect to process
2. **Provide accurate ground truth** text for each training image
3. **Use 10-15 samples minimum** for better parameter generalization
4. **Include challenging cases** like different pen colors, paper backgrounds, etc.
5. **Re-train periodically** as you collect more document samples

### Applying Trained Parameters

Once trained, the system will automatically use the optimized parameters for all handwriting recognition tasks. The document processing pipeline will:

1. Check for optimized parameters when initializing the recognizer
2. Apply these parameters during document processing
3. Use default parameters only if no optimized parameters are found

## OpenCV Handwriting Recognition

The handwriting recognition system uses a combination of computer vision techniques and OCR:

1. **Preprocessing Pipeline**:
   - Grayscale conversion
   - CLAHE contrast enhancement
   - Adaptive thresholding
   - Morphological operations
   - Denoising

2. **Text Line Segmentation**:
   - Horizontal projection profiling
   - Line boundary detection
   - Line image extraction

3. **OCR Enhancement**:
   - Image resizing
   - Unsharp masking
   - Otsu's thresholding

4. **Text Recognition**:
   - Tesseract OCR processing
   - Post-processing and text cleanup

5. **Result Visualization**:
   - Processing step visualization
   - Before/after comparison

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

## Upcoming Features

The IDP System is actively being developed with the following enhancements planned:

1. **Enhanced Online Learning**: Improved algorithms for automatically selecting the best OCR service based on document type
2. **Document Classification**: Automatic categorization of documents based on content and layout
3. **Custom OCR Service Integration**: Framework for easily adding additional OCR services
4. **Batch Processing API**: RESTful API for processing multiple documents programmatically
5. **Performance Optimization**: Improved caching and parallel processing for faster results
6. **Advanced Analytics Dashboard**: Visual insights into document processing metrics and recognition quality

## Contributing

Contributions to the IDP System are welcome! Here's how you can contribute:

1. **Report Bugs**: Open an issue describing the bug and steps to reproduce it
2. **Suggest Features**: Open an issue describing the feature and its potential benefits
3. **Submit Pull Requests**: Fork the repository, make changes, and submit a pull request
4. **Improve Documentation**: Help improve or translate the documentation
5. **Share Test Data**: Contribute sample documents for testing recognition accuracy

When contributing code, please follow these guidelines:
- Follow the existing code style and conventions
- Add appropriate tests for new functionality
- Update documentation to reflect changes
- Ensure all tests pass before submitting pull requests

For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [OpenCV](https://opencv.org/)
- [spaCy](https://spacy.io/)
- [NLTK](https://www.nltk.org/)
- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)

# Online OCR Integration

The system includes an advanced internet-based OCR capability that enhances handwriting recognition by leveraging multiple online services. This hybrid approach delivers superior accuracy while maintaining resilience through intelligent fallback mechanisms.

## How It Works

1. **Multi-Stage Processing**: 
   - Document images are first processed locally using OpenCV and Tesseract
   - If online services are available, the system sends the same image to selected cloud OCR services
   - Results are compared and the most complete/accurate text is selected

2. **Service Orchestration**:
   - The system automatically tries services in order of reliability
   - If any service fails or times out, it seamlessly falls back to alternatives
   - Response caching prevents redundant processing of identical images

3. **Learning & Adaptation**:
   - Each recognition operation is recorded with performance metrics
   - The system tracks which services perform best for different document types
   - This data can be analyzed to further optimize recognition parameters

## Free OCR Services

The system uses free OCR APIs that do not require API keys:

1. **Free OCR API** - Uses OCR.space's free tier with a public API key
   - Good general-purpose OCR with reasonable rate limits
   - Handles both printed and basic handwritten text

2. **EasyOCR API** - A free online API for OCR with good handwriting recognition  
   - Specialized in multi-language document processing
   - Particularly effective for mixed content documents

3. **Hugging Face** - Uses Microsoft's TrOCR model, specialized for handwritten text
   - State-of-the-art deep learning model for handwriting
   - Excellent for cursive and challenging handwriting styles

## Benefits

- **Improved Accuracy**: Online services often achieve 15-30% better recognition rates for handwritten text
- **Resilience**: System continues functioning when offline or when services are unavailable
- **Cost Efficiency**: Uses free tiers of OCR services without requiring paid subscriptions
- **Privacy Aware**: Can be configured to use only local processing for sensitive documents
- **Learning System**: Gets better over time by tracking service performance

## Configuration

The online OCR is enabled by default. You can configure it in your `.env` file:

```
# Online OCR settings
USE_ONLINE_OCR=True
OCR_SERVICE=free_ocr_api  # Options: free_ocr_api, easy_ocr_api, hugging_face
OCR_LEARNING_ENABLED=True
```

## Test Script

You can test the online OCR functionality using the included test script:

```
python test_online_recognition.py --image samples/test_handwriting.jpg --service free_ocr_api
```

Use the `--service all` option to test all available services. 
