"""
Forms for document upload and processing
"""
from django import forms
from .models import Document, DocumentType

class DocumentUploadForm(forms.ModelForm):
    """
    Form for uploading documents
    """
    
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'description', 'file', 'language']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'language': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if field_name != 'language':  # Skip language field as it already has form-select class
                field.widget.attrs['class'] = 'form-control'
        
        # Set document_type choices
        if DocumentType.objects.count() == 0:
            # Create default document types if none exist
            document_types = [
                {'name': 'Invoice', 'description': 'Financial invoices for billing purposes'},
                {'name': 'Resume/CV', 'description': 'Professional resumes and CVs'},
                {'name': 'Contract', 'description': 'Legal agreements and contracts'},
                {'name': 'Report', 'description': 'Business or technical reports'},
                {'name': 'Form', 'description': 'Structured forms and applications'},
                {'name': 'Other', 'description': 'Other document types'},
            ]
            
            for doc_type in document_types:
                DocumentType.objects.create(
                    name=doc_type['name'],
                    description=doc_type['description']
                )
                
        # Add help text for language field
        self.fields['language'].help_text = "Select the primary language of the document"
    
    def clean_file(self):
        """Validate the uploaded file"""
        file = self.cleaned_data.get('file')
        
        if file:
            # Check file extension
            ext = file.name.split('.')[-1].lower()
            allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'txt', 'doc', 'docx']
            
            if ext not in allowed_extensions:
                raise forms.ValidationError(
                    f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
                )
            
            # Check file size (10 MB limit)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be less than 10 MB")
        
        return file
    
    def save(self, commit=True):
        """Override save method to set uploaded_by and file_type"""
        instance = super().save(commit=False)
        
        # Set uploaded_by to the current user
        if self.user:
            instance.uploaded_by = self.user
        
        # Set file_type based on file extension
        if instance.file:
            ext = instance.file.name.split('.')[-1].lower()
            mime_types = {
                'pdf': 'application/pdf',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'txt': 'text/plain',
                'doc': 'application/msword',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            }
            instance.file_type = mime_types.get(ext, 'application/octet-stream')
        
        if commit:
            instance.save()
        
        return instance 