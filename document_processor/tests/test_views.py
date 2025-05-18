from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from document_processor.models import Document, DocumentType


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_view_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'document_processor/home.html')


class AboutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.about_url = reverse('about')

    def test_about_view_GET(self):
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'document_processor/about.html')


class DocumentListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.list_url = reverse('document_list')
        
        # Create test documents
        self.doc_type = DocumentType.objects.create(name="Test Type")
        Document.objects.create(title="Test Doc 1", user=self.user, document_type=self.doc_type)
        Document.objects.create(title="Test Doc 2", user=self.user, document_type=self.doc_type)
        
    def test_document_list_redirect_if_not_logged_in(self):
        response = self.client.get(self.list_url)
        self.assertRedirects(response, f'/login/?next={self.list_url}')
        
    def test_document_list_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'document_processor/document_list.html')
        self.assertEqual(len(response.context['documents']), 2)


class DocumentDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.doc_type = DocumentType.objects.create(name="Test Type")
        self.document = Document.objects.create(
            title="Test Document",
            user=self.user,
            document_type=self.doc_type,
            description="A test document"
        )
        self.detail_url = reverse('document_detail', args=[self.document.id])
        
    def test_document_detail_redirect_if_not_logged_in(self):
        response = self.client.get(self.detail_url)
        self.assertRedirects(response, f'/login/?next={self.detail_url}')
        
    def test_document_detail_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'document_processor/document_detail.html')
        self.assertEqual(response.context['document'], self.document) 