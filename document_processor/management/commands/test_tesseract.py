import subprocess
import pytesseract
from PIL import Image
import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Test Tesseract OCR installation'

    def handle(self, *args, **kwargs):
        self.stdout.write('Testing Tesseract OCR installation...')
        
        # Get tesseract path from settings
        tesseract_path = getattr(settings, 'TESSERACT_PATH', None)
        
        self.stdout.write(f"Tesseract path in settings: {tesseract_path}")
        
        # Check if the path exists
        if tesseract_path and os.path.exists(tesseract_path):
            self.stdout.write(self.style.SUCCESS(f"✓ Tesseract executable found at: {tesseract_path}"))
        else:
            self.stdout.write(self.style.ERROR(f"✗ Tesseract executable not found at: {tesseract_path}"))
        
        # Set tesseract command path for pytesseract
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Test pytesseract is working
        try:
            # Get tesseract version
            version = pytesseract.get_tesseract_version()
            self.stdout.write(self.style.SUCCESS(f"✓ Tesseract version: {version}"))
            
            # Get available languages
            langs = pytesseract.get_languages()
            self.stdout.write(self.style.SUCCESS(f"✓ Available languages: {', '.join(langs)}"))
            
            self.stdout.write(self.style.SUCCESS("Tesseract OCR is correctly installed and configured!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error testing Tesseract: {str(e)}"))
            self.stdout.write(self.style.WARNING(
                "Please check that Tesseract is correctly installed and the path is properly set in settings.py or .env file."
            ))
            
            # Suggest troubleshooting steps
            self.stdout.write("\nTroubleshooting steps:")
            self.stdout.write("1. Make sure Tesseract OCR is installed")
            self.stdout.write("2. Check that the path in settings.py or .env file matches your installation location")
            self.stdout.write("   Current path: " + (tesseract_path or "Not set"))
            self.stdout.write("3. Try running Tesseract directly from the command line:")
            self.stdout.write("   > tesseract --version") 