"""
NLP utilities for text processing, entity recognition, and analysis
"""
import re
import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
from django.conf import settings

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('vader_lexicon')

class NLPProcessor:
    """
    Utility class for text processing, entity recognition, and analysis
    """
    
    def __init__(self, language='en'):
        """
        Initialize NLP processor
        
        Args:
            language (str): Language code (default: 'en')
        """
        self.language = language
        self.nlp = spacy.load('en_core_web_sm')  # Load spaCy model
        self.stop_words = set(stopwords.words('english'))
        self.sia = SentimentIntensityAnalyzer()
    
    def extract_entities(self, text):
        """
        Extract named entities from text
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of entity dictionaries with entity text, type, etc.
        """
        entities = []
        doc = self.nlp(text)
        
        for ent in doc.ents:
            entity_type = self._map_entity_type(ent.label_)
            start_pos = ent.start_char
            end_pos = ent.end_char
            
            entities.append({
                'text': ent.text,
                'entity_type': entity_type,
                'confidence_score': 1.0,  # spaCy doesn't provide confidence scores by default
                'position_start': start_pos,
                'position_end': end_pos
            })
        
        return entities
    
    def _map_entity_type(self, spacy_entity_type):
        """Map spaCy entity types to our model's entity types"""
        entity_mapping = {
            'PERSON': 'person',
            'ORG': 'organization',
            'GPE': 'location',
            'LOC': 'location',
            'DATE': 'date',
            'TIME': 'date',
            'MONEY': 'money',
            'PERCENT': 'percentage'
        }
        
        return entity_mapping.get(spacy_entity_type, 'other')
    
    def extract_keywords(self, text, num_keywords=10):
        """
        Extract important keywords from text
        
        Args:
            text (str): Input text
            num_keywords (int): Number of keywords to extract
            
        Returns:
            list: List of keyword tuples (word, count)
        """
        # Clean and tokenize text
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        tokens = word_tokenize(text)
        
        # Remove stopwords and short words
        filtered_tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        # Count word frequencies
        word_counter = Counter(filtered_tokens)
        
        # Get the most common words
        return word_counter.most_common(num_keywords)
    
    def detect_language(self, text):
        """
        Detect the language of the text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Detected language code
        """
        # This is a simple implementation - in production, use a library like langdetect
        # For now, we just return the initialized language
        return self.language
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of the text
        
        Args:
            text (str): Input text
            
        Returns:
            float: Sentiment score (-1 to 1, where -1 is negative, 1 is positive)
        """
        sentiment = self.sia.polarity_scores(text)
        return sentiment['compound']  # Compound score from -1 to 1
    
    def summarize(self, text, num_sentences=3):
        """
        Generate a summary of the text
        
        Args:
            text (str): Input text
            num_sentences (int): Number of sentences for the summary
            
        Returns:
            str: Summarized text
        """
        # Simple extractive summarization using sentence importance
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        
        if len(sentences) <= num_sentences:
            return text
        
        # Get keywords to score sentences
        keywords = [kw[0] for kw in self.extract_keywords(text, 20)]
        
        # Score sentences based on keywords
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            score = sum(1 for kw in keywords if kw.lower() in sentence.lower())
            sentence_scores.append((i, score))
        
        # Sort by score and select top sentences
        top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:num_sentences]
        
        # Sort by original order
        top_sentences = sorted(top_sentences, key=lambda x: x[0])
        
        # Return the summary
        summary = ' '.join(sentences[i] for i, _ in top_sentences)
        return summary

def get_processor(language=None):
    """
    Factory function to get an NLP processor instance
    
    Args:
        language (str, optional): Language code
        
    Returns:
        NLPProcessor: Configured NLP processor instance
    """
    if language is None:
        language = 'en'
    
    return NLPProcessor(language=language) 