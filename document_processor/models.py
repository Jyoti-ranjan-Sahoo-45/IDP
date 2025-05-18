import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import mimetypes

def document_upload_path(instance, filename):
    """Generate a unique file path for uploaded documents"""
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate filename based on timestamp and original filename
    filename = f"{timezone.now().strftime('%Y%m%d%H%M%S')}_{filename}"
    # Return the upload path
    return os.path.join('documents', filename)

class DocumentType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Document(models.Model):
    """Model for storing document metadata and processing results"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('fr', 'French'),
        ('es', 'Spanish'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
        ('ru', 'Russian'),
        ('zh', 'Chinese'),
        ('ja', 'Japanese'),
        ('ko', 'Korean'),
        ('ar', 'Arabic'),
        ('hi', 'Hindi'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=document_upload_path)
    file_type = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    
    # Processing results
    extracted_text = models.TextField(blank=True, null=True)
    processing_time = models.FloatField(null=True, blank=True)
    page_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Set file_type based on file extension if it's not set and file exists
        if not self.file_type and self.file:
            # Use mimetypes to determine file type
            file_name = self.file.name if hasattr(self.file, 'name') else None
            if file_name:
                self.file_type = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'
        
        super().save(*args, **kwargs)
    
    def get_file_extension(self):
        """Return the file extension of the uploaded document"""
        name, extension = os.path.splitext(self.file.name)
        return extension[1:] if extension else ""
    
    def delete(self, *args, **kwargs):
        """Override delete method to delete the file when the model instance is deleted"""
        # Delete the file from storage
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        # Call the parent delete method
        super(Document, self).delete(*args, **kwargs)

class ProcessingResult(models.Model):
    """
    Processing results for documents
    """
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='analysis_result')
    language = models.CharField(max_length=10, blank=True, null=True)
    sentiment_score = models.FloatField(default=0.0)
    keyword_summary = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Advanced GROQ analysis fields
    groq_analysis = models.TextField(blank=True, null=True)
    groq_insights = models.TextField(blank=True, null=True)
    model_used = models.CharField(max_length=50, blank=True, null=True)
    is_advanced = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Analysis for {self.document.title}"

class NamedEntity(models.Model):
    """
    Named entities extracted from documents
    """
    ENTITY_TYPES = [
        ('person', 'Person'),
        ('organization', 'Organization'),
        ('location', 'Location'),
        ('date', 'Date'),
        ('money', 'Money'),
        ('percentage', 'Percentage'),
        ('product', 'Product'),
        ('event', 'Event'),
        ('other', 'Other'),
    ]
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='entities')
    text = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES, default='other')
    confidence_score = models.FloatField(default=1.0)
    position_start = models.IntegerField(null=True, blank=True)
    position_end = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=20, default='spacy', choices=[('spacy', 'spaCy'), ('groq', 'GROQ')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.entity_type}: {self.text}"
