from django.test import TestCase
from django.contrib.auth.models import User
from document_processor.models import Document, DocumentType, ProcessingResult


class DocumentTypeModelTest(TestCase):
    def setUp(self):
        DocumentType.objects.create(name="Invoice", description="Invoice documents")

    def test_document_type_creation(self):
        invoice_type = DocumentType.objects.get(name="Invoice")
        self.assertEqual(invoice_type.description, "Invoice documents")
        self.assertEqual(str(invoice_type), "Invoice")


class DocumentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.doc_type = DocumentType.objects.create(name="Resume", description="Resume documents")
        self.document = Document.objects.create(
            title="Test Document",
            document_type=self.doc_type,
            user=self.user,
            description="A test document"
        )

    def test_document_creation(self):
        self.assertEqual(str(self.document), "Test Document")
        self.assertEqual(self.document.user, self.user)
        self.assertEqual(self.document.document_type, self.doc_type)
        self.assertEqual(self.document.status, "Uploaded")


class ProcessingResultModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.doc_type = DocumentType.objects.create(name="Report", description="Report documents")
        self.document = Document.objects.create(
            title="Test Report",
            document_type=self.doc_type,
            user=self.user
        )
        self.result = ProcessingResult.objects.create(
            document=self.document,
            extracted_text="Sample extracted text",
            processing_time=5.2
        )

    def test_processing_result_creation(self):
        self.assertEqual(self.result.document, self.document)
        self.assertEqual(self.result.extracted_text, "Sample extracted text")
        self.assertAlmostEqual(self.result.processing_time, 5.2)
        self.assertEqual(str(self.result), f"Processing Result for Test Report") 