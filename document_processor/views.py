"""
Views for document processing application
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.conf import settings

from .models import Document, DocumentType, ProcessingResult, NamedEntity
from .forms import DocumentUploadForm
from .utils.document_processor import process_document

def index(request):
    """Home page view"""
    return render(request, 'document_processor/index.html')

def about(request):
    """About page view"""
    return render(request, 'document_processor/about.html')

@login_required
def document_list(request):
    """View for listing user's documents"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Get documents for the current user
    documents = Document.objects.filter(uploaded_by=request.user)
    
    # Apply search filter if provided
    if search_query:
        documents = documents.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Apply status filter if provided
    if status_filter and status_filter != 'all':
        documents = documents.filter(status=status_filter)
    
    # Paginate results
    paginator = Paginator(documents, 10)  # 10 documents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Document.STATUS_CHOICES,
    }
    
    return render(request, 'document_processor/document_list.html', context)

@login_required
def document_upload(request):
    """View for uploading documents"""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            document = form.save()
            
            # Redirect to document detail page
            messages.success(request, f"Document '{document.title}' uploaded successfully.")
            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentUploadForm(user=request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'document_processor/document_upload.html', context)

@login_required
def document_detail(request, pk):
    """View for displaying document details"""
    document = get_object_or_404(Document, pk=pk, uploaded_by=request.user)
    
    # Get document entities
    spacy_entities = document.entities.filter(source='spacy')
    groq_entities = document.entities.filter(source='groq')
    
    # Get document analysis
    try:
        analysis = document.analysis_result
    except ProcessingResult.DoesNotExist:
        analysis = None
    
    context = {
        'document': document,
        'spacy_entities': spacy_entities,
        'groq_entities': groq_entities,
        'analysis': analysis,
        'enable_advanced': settings.ENABLE_ADVANCED_FEATURES,
    }
    
    return render(request, 'document_processor/document_detail.html', context)

@login_required
def document_process(request, pk):
    """View for processing a document"""
    document = get_object_or_404(Document, pk=pk, uploaded_by=request.user)
    
    if request.method == 'POST':
        try:
            # Check if advanced processing is requested
            use_advanced = request.POST.get('use_advanced', False) == 'on'
            
            # Process document
            result = process_document(document.id, use_advanced=use_advanced)
            
            # Redirect to document detail page
            messages.success(request, "Document processed successfully.")
            return redirect('document_detail', pk=document.pk)
        except Exception as e:
            messages.error(request, f"Error processing document: {str(e)}")
            return redirect('document_detail', pk=document.pk)
    
    context = {
        'document': document,
        'enable_advanced': settings.ENABLE_ADVANCED_FEATURES,
        'advanced_models': settings.AI_FEATURES['ADVANCED_MODELS'],
        'free_models': settings.AI_FEATURES['FREE_MODELS'],
    }
    
    return render(request, 'document_processor/document_process.html', context)

@login_required
def document_delete(request, pk):
    """View for deleting a document"""
    document = get_object_or_404(Document, pk=pk, uploaded_by=request.user)
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, f"Document '{document.title}' deleted successfully.")
        return redirect('document_list')
    
    context = {
        'document': document,
    }
    
    return render(request, 'document_processor/document_delete.html', context)

@csrf_exempt
@login_required
def document_process_api(request, pk):
    """API view for processing a document asynchronously"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        document = get_object_or_404(Document, pk=pk, uploaded_by=request.user)
        
        # Get advanced processing option
        data = json.loads(request.body)
        use_advanced = data.get('use_advanced', False)
        
        # Start processing
        result = process_document(document.id, use_advanced=use_advanced)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Document processed successfully',
            'result': result,
            'advanced_used': use_advanced
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
def document_download(request, pk):
    """View for downloading document text"""
    document = get_object_or_404(Document, pk=pk, uploaded_by=request.user)
    
    # Create text file
    response = HttpResponse(document.extracted_text, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{document.title}_extracted_text.txt"'
    
    return response
