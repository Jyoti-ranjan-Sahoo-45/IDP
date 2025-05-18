"""
OCR utilities for extracting text from images and PDFs
"""
import os
import time
import tempfile
import pytesseract
from PIL import Image
import pdf2image
from django.conf import settings

class OCRProcessor:
    """
    Utility class for extracting text from images and PDFs using Tesseract OCR
    """
    
    def __init__(self, language='eng'):
        """
        Initialize OCR processor
        
        Args:
            language (str): Language code for OCR (default: 'eng')
        """
        self.language = language
        
        # Set Tesseract path from settings
        tesseract_path = getattr(settings, 'TESSERACT_PATH', None)
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
    def process_image(self, image_path):
        """
        Extract text from an image file
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            tuple: (extracted_text, processing_time)
        """
        start_time = time.time()
        
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Extract text
            text = pytesseract.image_to_string(image, lang=self.language)
            
            processing_time = time.time() - start_time
            return text, processing_time
        except Exception as e:
            processing_time = time.time() - start_time
            raise Exception(f"OCR processing error: {str(e)}")
    
    def process_pdf(self, pdf_path):
        """
        Extract text from a PDF file
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            tuple: (extracted_text, processing_time, page_count)
        """
        start_time = time.time()
        
        try:
            # Create temp directory for PDF images
            with tempfile.TemporaryDirectory() as temp_dir:
                # Convert PDF to images
                images = pdf2image.convert_from_path(
                    pdf_path,
                    output_folder=temp_dir,
                    fmt='jpeg',
                    thread_count=os.cpu_count()
                )
                
                page_count = len(images)
                full_text = []
                
                # Process each page
                for i, image in enumerate(images):
                    text = pytesseract.image_to_string(image, lang=self.language)
                    full_text.append(f"--- Page {i+1} ---\n{text}\n")
                
                processing_time = time.time() - start_time
                return '\n'.join(full_text), processing_time, page_count
        except Exception as e:
            processing_time = time.time() - start_time
            raise Exception(f"PDF OCR processing error: {str(e)}")

def extract_text_from_image(image_path, language=None):
    """
    Extract text from an image file
    
    Args:
        image_path (str): Path to the image file
        language (str, optional): Language code for OCR
        
    Returns:
        str: Extracted text
    """
    if language is None:
        language = getattr(settings, 'OCR_LANGUAGE', 'eng')
    
    # Set Tesseract path from settings
    tesseract_path = getattr(settings, 'TESSERACT_PATH', None)
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Extract text
        text = pytesseract.image_to_string(image, lang=language)
        
        return text
    except Exception as e:
        raise Exception(f"OCR processing error: {str(e)}")

def get_processor(language=None):
    """
    Factory function to get an OCR processor instance
    
    Args:
        language (str, optional): Language code for OCR
        
    Returns:
        OCRProcessor: Configured OCR processor instance
    """
    if language is None:
        language = getattr(settings, 'OCR_LANGUAGE', 'eng')
    
    return OCRProcessor(language=language) 