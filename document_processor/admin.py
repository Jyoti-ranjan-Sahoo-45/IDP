from django.contrib import admin
from .models import Document, DocumentType, ProcessingResult, NamedEntity

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'file_type', 'uploaded_at', 'status', 'uploaded_by')
    list_filter = ('status', 'document_type', 'uploaded_at')
    search_fields = ('title', 'description')
    readonly_fields = ('file_type', 'uploaded_at', 'updated_at', 'processing_time', 'page_count')

@admin.register(ProcessingResult)
class ProcessingResultAdmin(admin.ModelAdmin):
    list_display = ('document', 'language', 'sentiment_score', 'created_at')
    list_filter = ('language', 'created_at')
    search_fields = ('document__title',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(NamedEntity)
class NamedEntityAdmin(admin.ModelAdmin):
    list_display = ('text', 'entity_type', 'document', 'confidence_score', 'source')
    list_filter = ('entity_type', 'confidence_score', 'source')
    search_fields = ('text', 'document__title')
