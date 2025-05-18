"""
Utilities for document processing and text extraction
"""
import os
import PyPDF2
import docx
import time
import traceback
from django.conf import settings
from document_processor.models import Document, ProcessingResult, NamedEntity
from .ocr import extract_text_from_image
from .nlp import get_processor
from .groq_processor import get_groq_processor

def process_document(document_id, use_advanced=False):
    """
    Process document and extract information
    
    Args:
        document_id (int): Document ID
        use_advanced (bool): Whether to use advanced GROQ processing
        
    Returns:
        dict: Processing results
    """
    start_time = time.time()
    document = None
    
    try:
        # Get document from database
        document = Document.objects.get(id=document_id)
        
        # Update status to processing
        document.status = 'processing'
        document.save()
        
        # Extract text from document if not already done
        if not document.extracted_text:
            document.extracted_text = extract_text(document.file.path)
            document.save()
        
        # Get text for processing
        text = document.extracted_text
        
        if not text or len(text.strip()) < 10:
            raise ValueError("Insufficient text extracted from document. Please check the file format.")
        
        # Get document language or use default
        language = getattr(document, 'language', 'en')
        
        # Use NLP to process text
        nlp = get_processor(language=language)
        
        # Extract entities
        entities = nlp.extract_entities(text)
        
        # Extract keywords
        keywords = nlp.extract_keywords(text)
        
        # Analyze sentiment
        sentiment_score = nlp.analyze_sentiment(text)
        
        # Generate summary
        summary = nlp.summarize(text)
        
        # Advanced processing with GROQ if enabled
        groq_analysis = None
        groq_entities = None
        groq_insights = None
        
        if settings.ENABLE_ADVANCED_FEATURES:
            try:
                # Get GROQ processor
                groq = get_groq_processor(api_key=settings.GROQ_API_KEY)
                
                # Perform analysis with free model (or advanced if requested)
                groq_analysis = groq.analyze_document(text, advanced=use_advanced)
                
                # Extract entities with GROQ
                groq_entities = groq.extract_advanced_entities(text, advanced=use_advanced)
                
                # Generate insights with GROQ
                if use_advanced:
                    groq_insights = groq.generate_insights(text, advanced=True)
            except Exception as e:
                # Log error but continue with basic processing
                print(f"GROQ processing error: {str(e)}")
        
        # Get document language or use default
        document_language = getattr(document, 'language', 'en')
        
        # Save processing results
        result, created = ProcessingResult.objects.update_or_create(
            document=document,
            defaults={
                'summary': summary,
                'sentiment_score': sentiment_score,
                'keywords': ', '.join([kw[0] for kw in keywords]),
                'language': document_language,
                'groq_analysis': groq_analysis['analysis'] if groq_analysis else None,
                'groq_insights': groq_insights['insights'] if groq_insights else None,
                'model_used': groq_analysis['model_used'] if groq_analysis else None,
                'is_advanced': use_advanced,
            }
        )
        
        # Save entities
        document.entities.all().delete()  # Remove existing entities
        
        # Save standard NLP entities
        for entity in entities:
            NamedEntity.objects.create(
                document=document,
                text=entity['text'],
                entity_type=entity['entity_type'],
                confidence_score=entity['confidence_score'],
                position_start=entity['position_start'],
                position_end=entity['position_end'],
                source='spacy'
            )
        
        # Save GROQ entities if available
        if groq_entities and groq_entities.get('entities'):
            for entity in groq_entities['entities']:
                # Extract fields from GROQ entity format
                entity_text = entity.get('text', '')
                entity_type = entity.get('type', 'other').lower()
                
                # Skip if missing essential information
                if not entity_text:
                    continue
                
                NamedEntity.objects.create(
                    document=document,
                    text=entity_text,
                    entity_type=entity_type,
                    confidence_score=1.0,  # GROQ doesn't provide confidence scores
                    source='groq'
                )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        document.processing_time = processing_time
        
        # Update document status
        document.status = 'completed'
        document.save()
        
        # Return processing results
        return {
            'document_id': document.id,
            'status': 'success',
            'summary': summary,
            'sentiment_score': sentiment_score,
            'keywords': keywords,
            'entities_count': document.entities.count(),
            'advanced_processing': use_advanced,
            'groq_model': groq_analysis['model_used'] if groq_analysis else None,
            'processing_time': processing_time
        }
    
    except Exception as e:
        # Handle exceptions
        error_message = str(e)
        stack_trace = traceback.format_exc()
        print(f"Processing error: {error_message}")
        print(f"Stack trace: {stack_trace}")
        
        try:
            if document:
                # Get document language or use default
                document_language = getattr(document, 'language', 'en')
                
                # Create or update processing result with error information
                ProcessingResult.objects.update_or_create(
                    document=document,
                    defaults={
                        'summary': f"Processing failed: {error_message}",
                        'sentiment_score': 0.0,
                        'keywords': 'error, failed, processing',
                        'language': document_language,
                    }
                )
                
                # Update document status
                document.status = 'failed'
                document.save()
        except Exception as inner_e:
            print(f"Error updating document status: {str(inner_e)}")
        
        # Re-raise exception with detailed message
        raise Exception(f"Error processing document: {error_message}")

def extract_text(file_path):
    """
    Extract text from a document file
    
    Args:
        file_path (str): Path to the document file
        
    Returns:
        str: Extracted text
    """
    # Get file extension
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    # Extract text based on file type
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext in ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']:
        return extract_text_from_image(file_path)
    elif ext == '.txt':
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text
    """
    text = ""
    
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            
            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    return text

def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX file
    
    Args:
        file_path (str): Path to the DOCX file
        
    Returns:
        str: Extracted text
    """
    text = ""
    
    try:
        doc = docx.Document(file_path)
        
        # Extract text from paragraphs
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")
    
    return text

def extract_text_from_txt(file_path):
    """
    Extract text from a TXT file
    
    Args:
        file_path (str): Path to the TXT file
        
    Returns:
        str: Extracted text
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        # Try with a different encoding
        with open(file_path, 'r', encoding='latin-1') as f:
            text = f.read()
    except Exception as e:
        raise Exception(f"Error extracting text from TXT: {str(e)}")
    
    return text 