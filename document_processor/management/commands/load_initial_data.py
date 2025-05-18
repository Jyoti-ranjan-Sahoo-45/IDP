from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from document_processor.models import DocumentType


class Command(BaseCommand):
    help = 'Load initial data for the IDP project'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading initial data...')
        
        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        
        # Create document types
        document_types = [
            {'name': 'Invoice', 'description': 'Financial invoices for billing purposes'},
            {'name': 'Resume/CV', 'description': 'Professional resumes and CVs'},
            {'name': 'Contract', 'description': 'Legal agreements and contracts'},
            {'name': 'Report', 'description': 'Business or technical reports'},
            {'name': 'Form', 'description': 'Structured forms and applications'},
            {'name': 'Other', 'description': 'Other document types'},
        ]
        
        for doc_type in document_types:
            DocumentType.objects.get_or_create(
                name=doc_type['name'],
                defaults={'description': doc_type['description']}
            )
        
        self.stdout.write(self.style.SUCCESS('Document types created'))
        
        # Create user groups
        groups = {
            'Analysts': 'Can process and view documents',
            'Managers': 'Can manage documents and users',
            'Viewers': 'Can only view documents',
        }
        
        for group_name, description in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Created group: {group_name}')
        
        # Set up permissions
        content_type = ContentType.objects.get_for_model(User)
        
        self.stdout.write(self.style.SUCCESS('Initial data loading completed')) 