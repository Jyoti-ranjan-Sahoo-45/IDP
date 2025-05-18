from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from document_processor.forms import DocumentUploadForm
from document_processor.models import DocumentType


class DocumentUploadFormTest(TestCase):
    def setUp(self):
        self.doc_type = DocumentType.objects.create(name="Report", description="Report documents")
        
        # Create a test file for upload
        self.test_file = SimpleUploadedFile(
            "test_doc.pdf",
            b"file_content",
            content_type="application/pdf"
        )
    
    def test_form_valid_data(self):
        form_data = {
            'title': 'Test Document',
            'document_type': self.doc_type.id,
            'description': 'This is a test document'
        }
        form_files = {
            'file': self.test_file
        }
        
        form = DocumentUploadForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())
    
    def test_form_missing_title(self):
        form_data = {
            'document_type': self.doc_type.id,
            'description': 'This is a test document'
        }
        form_files = {
            'file': self.test_file
        }
        
        form = DocumentUploadForm(data=form_data, files=form_files)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_form_missing_file(self):
        form_data = {
            'title': 'Test Document',
            'document_type': self.doc_type.id,
            'description': 'This is a test document'
        }
        
        form = DocumentUploadForm(data=form_data, files={})
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)
    
    def test_form_invalid_file_type(self):
        invalid_file = SimpleUploadedFile(
            "test_doc.exe",
            b"file_content",
            content_type="application/octet-stream"
        )
        
        form_data = {
            'title': 'Test Document',
            'document_type': self.doc_type.id,
            'description': 'This is a test document'
        }
        form_files = {
            'file': invalid_file
        }
        
        form = DocumentUploadForm(data=form_data, files=form_files)
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors) 