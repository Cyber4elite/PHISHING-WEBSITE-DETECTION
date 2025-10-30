import numpy as np
import re
from urllib.parse import urlparse
import os
from django.conf import settings


def extract_features(url):
    """
    Extract features from URL for phishing detection
    """
    features = {}
    
    # Add scheme if missing to ensure proper parsing
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    # Parse URL
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path
    query = parsed.query
    
    # Basic URL features
    features['url_length'] = len(url)
    features['domain_length'] = len(domain)
    features['path_length'] = len(path)
    features['query_length'] = len(query)
    
    # Count special characters
    features['num_dots'] = url.count('.')
    features['num_hyphens'] = url.count('-')
    features['num_underscores'] = url.count('_')
    features['num_slashes'] = url.count('/')
    features['num_question_marks'] = url.count('?')
    features['num_equals'] = url.count('=')
    features['num_ampersands'] = url.count('&')
    features['num_percent'] = url.count('%')
    
    # Check for suspicious patterns
    features['has_ip'] = 1 if re.match(r'^\d+\.\d+\.\d+\.\d+', domain) else 0
    features['has_shortener'] = 1 if any(shortener in domain for shortener in 
                                       ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly']) else 0
    features['has_suspicious_keywords'] = 1 if any(keyword in url.lower() for keyword in 
                                                 ['secure', 'account', 'update', 'verify', 'confirm', 'login']) else 0
    
    # Domain analysis
    features['subdomain_count'] = len(domain.split('.')) - 2 if '.' in domain else 0
    features['has_www'] = 1 if domain.startswith('www.') else 0
    
    # Protocol
    features['is_https'] = 1 if parsed.scheme == 'https' else 0
    
    # Path analysis
    features['path_depth'] = len([p for p in path.split('/') if p])
    features['has_file_extension'] = 1 if '.' in path.split('/')[-1] else 0
    
    # Store original URL in lowercase for pattern matching
    features['url_lower'] = url.lower()
    
    return features


def predict_phishing(url):
    """
    Predict if URL is phishing using Q-learning model
    Returns: dict with 'prediction', 'confidence', 'features'
    """
    try:
        # Extract features
        features = extract_features(url)
        
        # Convert features to numpy array for model prediction
        feature_vector = np.array([
            features['url_length'],
            features['domain_length'],
            features['path_length'],
            features['query_length'],
            features['num_dots'],
            features['num_hyphens'],
            features['num_underscores'],
            features['num_slashes'],
            features['num_question_marks'],
            features['num_equals'],
            features['num_ampersands'],
            features['num_percent'],
            features['has_ip'],
            features['has_shortener'],
            features['has_suspicious_keywords'],
            features['subdomain_count'],
            features['has_www'],
            features['is_https'],
            features['path_depth'],
            features['has_file_extension']
        ]).reshape(1, -1)
        
        # Load the pre-trained Q-learning model
        model_path = os.path.join(settings.BASE_DIR, 'scanner', 'model.npy')
        
        if os.path.exists(model_path):
            # Load the model weights
            model_weights = np.load(model_path, allow_pickle=True)
            
            # Simple neural network forward pass (assuming 2-layer network)
            # Layer 1: 20 -> 10
            w1 = model_weights[:200].reshape(20, 10)  # 20 features -> 10 hidden
            b1 = model_weights[200:210]  # 10 biases
            # Layer 2: 10 -> 1
            w2 = model_weights[210:220].reshape(10, 1)  # 10 hidden -> 1 output
            b2 = model_weights[220:221]  # 1 bias
            
            # Forward pass
            z1 = np.dot(feature_vector, w1) + b1
            a1 = np.maximum(0, z1)  # ReLU activation
            z2 = np.dot(a1, w2) + b2
            prediction_prob = 1 / (1 + np.exp(-z2))  # Sigmoid activation
            
            # Convert to binary prediction
            prediction = 'phishing' if prediction_prob[0][0] > 0.5 else 'legitimate'
            confidence = float(prediction_prob[0][0]) if prediction == 'phishing' else float(1 - prediction_prob[0][0])
            
        else:
            # Fallback to rule-based prediction if model not found
            prediction, confidence = rule_based_prediction(features)
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'features': features
        }
        
    except Exception as e:
        # Fallback to rule-based prediction on error
        features = extract_features(url)
        prediction, confidence = rule_based_prediction(features)
        return {
            'prediction': prediction,
            'confidence': confidence,
            'features': features
        }


def rule_based_prediction(features):
    """
    Enhanced rule-based prediction with more sophisticated phishing detection
    """
    score = 0
    
    # High-risk indicators
    if features['has_ip']:
        score += 0.4
    if features['has_shortener']:
        score += 0.3
    
    # Medium-risk indicators
    if features['has_suspicious_keywords']:
        score += 0.25
    if features['url_length'] > 80:  # Lowered threshold
        score += 0.15
    if features['num_dots'] > 2:  # Lowered threshold
        score += 0.15
    if features['subdomain_count'] > 1:  # Lowered threshold
        score += 0.15
    if not features['is_https']:
        score += 0.15
    
    # Additional phishing patterns
    if features['path_depth'] > 4:  # Deep paths often indicate phishing
        score += 0.2
    if features['num_hyphens'] > 2:  # Multiple hyphens suspicious
        score += 0.1
    if features['num_underscores'] > 1:  # Multiple underscores suspicious
        score += 0.1
    if features['domain_length'] > 30:  # Very long domains suspicious
        score += 0.1
    if features['has_file_extension'] and features['path_depth'] > 3:  # File in deep path
        score += 0.15
    
    # Special patterns for email/mail services (common phishing targets)
    url_lower = features.get('url_lower', '')
    if any(pattern in url_lower for pattern in ['zimbra', 'exchange', 'owa', 'webmail', 'mail']):
        score += 0.2
    
    prediction = 'phishing' if score > 0.4 else 'legitimate'  # Lowered threshold
    confidence = min(score, 1.0) if prediction == 'phishing' else min(1.0 - score, 1.0)
    
    return prediction, confidence
