import os
import json
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

# Global model and tokenizer variables
model = None
tokenizer = None

def load_model():
    """Load the trained T5 model for summarization"""
    global model, tokenizer
    if model is None or tokenizer is None:
        # Path to the checkpoint directory in models folder
        checkpoint_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'checkpoint-1878')
        
        if not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"Model checkpoint not found at {checkpoint_path}")
        
        print(f"Loading T5 model from {checkpoint_path}")
        
        # Load tokenizer and model
        tokenizer = T5Tokenizer.from_pretrained(checkpoint_path)
        model = T5ForConditionalGeneration.from_pretrained(checkpoint_path)
        
        # Set model to evaluation mode
        model.eval()
        
        print("T5 model loaded successfully")
    
    return model, tokenizer

def preprocess_text(text, max_length=512):
    """Preprocess text for T5 summarization"""
    # Clean and prepare text
    text = text.strip()
    
    # Truncate if too long
    if len(text) > max_length * 4:  # Rough estimate of tokens
        text = text[:max_length * 4]
    
    return text

def generate_summary(text, max_length=200, min_length=30, num_beams=8):
    """Generate summary using the T5 model"""
    model, tokenizer = load_model()
    
    # Preprocess text
    processed_text = preprocess_text(text)
    
    # Add summarization prefix
    input_text = f"summarize: {processed_text}"
    
    # Tokenize input
    inputs = tokenizer.encode(
        input_text,
        max_length=512,
        truncation=True,
        padding=True,
        return_tensors="pt"
    )
    
    # Generate summary
    with torch.no_grad():
        summary_ids = model.generate(
            inputs,
            max_length=max_length,
            min_length=min_length,
            num_beams=num_beams,
            early_stopping=True,
            no_repeat_ngram_size=3,
            length_penalty=2.0
        )
    
    # Decode summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary

@api_view(['POST'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def summarize_article(request):
    """Summarize article text using T5 model"""
    try:
        # Get text from request
        if request.content_type == 'application/json':
            text = request.data.get('text', '')
        else:
            # Handle form data
            text = request.data.get('text', '')
        
        if not text:
            return Response(
                {'error': 'No text provided for summarization'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get optional parameters
        max_length = int(request.data.get('max_length', 200))
        min_length = int(request.data.get('min_length', 30))
        num_beams = int(request.data.get('num_beams', 8))
        
        # Validate parameters
        if max_length < min_length:
            max_length = min_length + 50
        
        # Generate summary
        summary = generate_summary(
            text=text,
            max_length=max_length,
            min_length=min_length,
            num_beams=num_beams
        )
        
        # Calculate summary statistics
        original_length = len(text.split())
        summary_length = len(summary.split())
        compression_ratio = round((1 - summary_length / original_length) * 100, 2) if original_length > 0 else 0
        
        response_data = {
            'summary': summary,
            'original_length': original_length,
            'summary_length': summary_length,
            'compression_ratio': compression_ratio,
            'parameters': {
                'max_length': max_length,
                'min_length': min_length,
                'num_beams': num_beams
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except FileNotFoundError as e:
        return Response(
            {'error': f'Model not found: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {'error': f'Error generating summary: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    try:
        # Try to load model to check if it's available
        load_model()
        return Response({
            'status': 'healthy',
            'model_loaded': True
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'model_loaded': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
