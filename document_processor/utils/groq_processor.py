"""
GROQ API integration for advanced NLP processing
"""
import os
import requests
from typing import Dict, List, Optional, Any, Union
import json

class GroqProcessor:
    """
    Processor class for GROQ API integration
    """
    
    def __init__(self, api_key=None):
        """
        Initialize GROQ processor
        
        Args:
            api_key (str, optional): GROQ API key
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ API key is required. Set it in environment or pass as parameter.")
        
        self.base_url = "https://api.groq.com/openai/v1"
        self.models = {
            "free": "llama3-8b-8192",  # Free tier model
            "advanced": [
                "llama3-70b-8192",
                "mixtral-8x7b-32768",
                "gemma-7b-it"
            ]
        }
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make request to GROQ API
        
        Args:
            endpoint: API endpoint
            data: Request data
            
        Returns:
            dict: API response
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{self.base_url}/{endpoint}",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        
        return response.json()
    
    def analyze_document(self, text: str, advanced: bool = False) -> Dict[str, Any]:
        """
        Perform advanced document analysis
        
        Args:
            text: Document text to analyze
            advanced: Whether to use advanced models
            
        Returns:
            dict: Analysis results
        """
        model = self.models["advanced"][0] if advanced else self.models["free"]
        
        prompt = f"""
        Analyze the following document text and provide a comprehensive analysis including:
        1. A concise summary (max 100 words)
        2. Main themes/topics
        3. Key entities (people, organizations, locations, dates)
        4. The overall sentiment (positive, neutral, negative)
        5. Important facts extracted from the document
        
        Text:
        {text[:4000]}  # Limiting text size for API constraints
        """
        
        response = self._make_request("chat/completions", {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an AI assistant that specializes in document analysis."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        })
        
        # Parse the response
        analysis_text = response["choices"][0]["message"]["content"]
        
        # Structure the response
        return {
            "model_used": model,
            "is_advanced": advanced,
            "analysis": analysis_text,
            "usage": response.get("usage", {})
        }
    
    def extract_advanced_entities(self, text: str, advanced: bool = False) -> Dict[str, Any]:
        """
        Extract entities with advanced capabilities
        
        Args:
            text: Document text
            advanced: Whether to use advanced models
            
        Returns:
            dict: Extracted entities
        """
        model = self.models["advanced"][0] if advanced else self.models["free"]
        
        prompt = f"""
        Extract all named entities from the following text. For each entity, provide:
        1. The entity text
        2. Entity type (person, organization, location, date, event, product, etc.)
        3. A brief description of the entity if possible
        
        Format the response as a JSON object with an "entities" array.
        
        Text:
        {text[:4000]}
        """
        
        response = self._make_request("chat/completions", {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an AI assistant that specializes in named entity recognition."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        })
        
        # Parse the response
        entity_text = response["choices"][0]["message"]["content"]
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            json_start = entity_text.find('{')
            json_end = entity_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                entity_json = json.loads(entity_text[json_start:json_end])
                entities = entity_json.get("entities", [])
            else:
                entities = []
                
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw text
            entities = []
        
        return {
            "model_used": model,
            "is_advanced": advanced,
            "entities": entities,
            "raw_response": entity_text,
            "usage": response.get("usage", {})
        }
    
    def generate_insights(self, text: str, advanced: bool = False) -> Dict[str, Any]:
        """
        Generate insights from document text
        
        Args:
            text: Document text
            advanced: Whether to use advanced models
            
        Returns:
            dict: Generated insights
        """
        model = self.models["advanced"][0] if advanced else self.models["free"]
        
        prompt = f"""
        Generate valuable insights from the following document text. Include:
        1. Unexpected connections or patterns
        2. Important implications
        3. Potential action items
        4. Questions that should be explored further
        
        Text:
        {text[:4000]}
        """
        
        response = self._make_request("chat/completions", {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an AI assistant that specializes in analyzing documents and generating valuable insights."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5
        })
        
        # Parse the response
        insights_text = response["choices"][0]["message"]["content"]
        
        return {
            "model_used": model,
            "is_advanced": advanced,
            "insights": insights_text,
            "usage": response.get("usage", {})
        }

def get_groq_processor(api_key=None):
    """
    Factory function to get a GROQ processor instance
    
    Args:
        api_key (str, optional): GROQ API key
        
    Returns:
        GroqProcessor: Configured GROQ processor instance
    """
    return GroqProcessor(api_key=api_key) 