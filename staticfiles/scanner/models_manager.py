"""
Multi-Model Manager for PhishShield
Handles multiple AI models for ensemble prediction
"""

import numpy as np
import os
import joblib
from django.conf import settings
from .utils import extract_features, rule_based_prediction


class ModelManager:
    """Manages multiple models for ensemble prediction"""
    
    def __init__(self):
        self.models_config = settings.PHISHSHIELD_SETTINGS.get('MODELS', {})
        self.enabled_models = self._get_enabled_models()
    
    def _get_enabled_models(self):
        """Get list of enabled models"""
        enabled = []
        for model_id, config in self.models_config.items():
            if config.get('enabled', False):
                enabled.append((model_id, config))
        return enabled
    
    def predict_with_model(self, url, model_id, model_config):
        """Predict using a specific model"""
        try:
            features = extract_features(url)
            feature_vector = self._prepare_feature_vector(features)
            
            if model_config['type'] == 'q_learning':
                return self._predict_q_learning(feature_vector, model_config['path'])
            elif model_config['type'] == 'rule_based':
                return self._predict_rule_based(features)
            elif model_config['type'] == 'sklearn':
                return self._predict_sklearn(feature_vector, model_config['path'], model_config.get('feature_count', 20))
            elif model_config['type'] == 'experimental':
                return self._predict_experimental(feature_vector, model_config['path'])
            else:
                # Unknown model type, fallback to rule-based
                return self._predict_rule_based(features)
                
        except Exception as e:
            print(f"Error with model {model_id}: {e}")
            features = extract_features(url)
            return self._predict_rule_based(features)
    
    def _prepare_feature_vector(self, features):
        """Convert features to numpy array"""
        return np.array([
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
    
    def _predict_q_learning(self, feature_vector, model_path):
        """Q-Learning model prediction"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        try:
            model_weights = np.load(model_path, allow_pickle=True)
            
            # Handle different model structures
            if model_weights.shape == (2074, 2):
                # This appears to be a Q-table or different structure
                # Use rule-based fallback for now
                # Extract features from the feature vector for rule-based prediction
                features = {
                    'url_length': feature_vector[0, 0],
                    'domain_length': feature_vector[0, 1],
                    'path_length': feature_vector[0, 2],
                    'query_length': feature_vector[0, 3],
                    'num_dots': feature_vector[0, 4],
                    'num_hyphens': feature_vector[0, 5],
                    'num_underscores': feature_vector[0, 6],
                    'num_slashes': feature_vector[0, 7],
                    'has_ip': feature_vector[0, 12],
                    'has_shortener': feature_vector[0, 13],
                    'has_suspicious_keywords': feature_vector[0, 14],
                    'subdomain_count': feature_vector[0, 15],
                    'has_www': feature_vector[0, 16],
                    'is_https': feature_vector[0, 17],
                    'path_depth': feature_vector[0, 18],
                    'has_file_extension': feature_vector[0, 19]
                }
                prediction, confidence = rule_based_prediction(features)
                return {
                    'prediction': prediction,
                    'confidence': confidence,
                    'model_type': 'q_learning_fallback'
                }
            elif model_weights.size == 221:
                # Original neural network structure
                w1 = model_weights[:200].reshape(20, 10)
                b1 = model_weights[200:210]
                w2 = model_weights[210:220].reshape(10, 1)
                b2 = model_weights[220:221]
                
                z1 = np.dot(feature_vector, w1) + b1
                a1 = np.maximum(0, z1)  # ReLU
                z2 = np.dot(a1, w2) + b2
                prediction_prob = 1 / (1 + np.exp(-z2))  # Sigmoid
                
                prediction = 'phishing' if prediction_prob[0][0] > 0.5 else 'legitimate'
                confidence = float(prediction_prob[0][0]) if prediction == 'phishing' else float(1 - prediction_prob[0][0])
                
                return {
                    'prediction': prediction,
                    'confidence': confidence,
                    'model_type': 'q_learning'
                }
            else:
                # Unknown structure, use rule-based fallback
                prediction, confidence = rule_based_prediction({})
                return {
                    'prediction': prediction,
                    'confidence': confidence,
                    'model_type': 'q_learning_fallback'
                }
                
        except Exception as e:
            print(f"Error with Q-Learning model: {e}")
            # Fallback to rule-based
            prediction, confidence = rule_based_prediction({})
            return {
                'prediction': prediction,
                'confidence': confidence,
                'model_type': 'q_learning_fallback'
            }
    
    def _predict_rule_based(self, features):
        """Rule-based prediction"""
        prediction, confidence = rule_based_prediction(features)
        return {
            'prediction': prediction,
            'confidence': confidence,
            'model_type': 'rule_based'
        }
    
    def _predict_sklearn(self, feature_vector, model_path, feature_count):
        """Scikit-learn model prediction"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        try:
            # Load the scikit-learn model
            model = joblib.load(model_path)
            
            # Select features based on the model's expected input
            if feature_count == 4:
                # Use only the first 4 most important features for your models
                selected_features = feature_vector[:, [0, 1, 2, 3]]  # url_length, domain_length, path_length, query_length
            else:
                # Use all features if model expects more
                selected_features = feature_vector
            
            # Make prediction
            prediction_proba = model.predict_proba(selected_features)[0]
            
            # Get class labels
            if hasattr(model, 'classes_'):
                classes = model.classes_
                # Assuming classes are [0, 1] where 0=legitimate, 1=phishing
                if len(classes) == 2:
                    phishing_prob = prediction_proba[1] if classes[1] == 1 else prediction_proba[0]
                    prediction = 'phishing' if phishing_prob > 0.5 else 'legitimate'
                    confidence = float(phishing_prob) if prediction == 'phishing' else float(1 - phishing_prob)
                else:
                    # Fallback if class structure is different
                    prediction = 'phishing' if prediction_proba[1] > 0.5 else 'legitimate'
                    confidence = float(max(prediction_proba))
            else:
                # Fallback prediction
                prediction = 'phishing' if prediction_proba[1] > 0.5 else 'legitimate'
                confidence = float(max(prediction_proba))
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'model_type': 'sklearn'
            }
            
        except Exception as e:
            print(f"Error loading sklearn model: {e}")
            raise e
    
    def _predict_experimental(self, feature_vector, model_path):
        """Experimental model prediction (placeholder)"""
        # This is where you'd implement your experimental model
        # For now, it's a placeholder that returns random results
        import random
        prediction = 'phishing' if random.random() > 0.5 else 'legitimate'
        confidence = random.uniform(0.6, 0.9)
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'model_type': 'experimental'
        }
    
    def ensemble_predict(self, url):
        """Ensemble prediction using multiple models"""
        predictions = []
        model_results = {}
        
        for model_id, model_config in self.enabled_models:
            result = self.predict_with_model(url, model_id, model_config)
            model_results[model_id] = result
            predictions.append({
                'prediction': result['prediction'],
                'confidence': result['confidence'],
                'weight': model_config['weight']
            })
        
        # Weighted ensemble prediction
        phishing_score = 0.0
        legitimate_score = 0.0
        total_weight = 0.0
        
        for pred in predictions:
            weight = pred['weight']
            total_weight += weight
            
            if pred['prediction'] == 'phishing':
                phishing_score += pred['confidence'] * weight
            else:
                legitimate_score += pred['confidence'] * weight
        
        if total_weight == 0:
            # Fallback if no weights
            final_prediction = 'legitimate'
            final_confidence = 0.5
        else:
            # Normalize scores
            phishing_score /= total_weight
            legitimate_score /= total_weight
            
            if phishing_score > legitimate_score:
                final_prediction = 'phishing'
                final_confidence = phishing_score
            else:
                final_prediction = 'legitimate'
                final_confidence = legitimate_score
        
        return {
            'prediction': final_prediction,
            'confidence': final_confidence,
            'model_results': model_results,
            'ensemble_type': 'weighted_average',
            'models_used': [model_id for model_id, _ in self.enabled_models]
        }


# Global model manager instance
model_manager = ModelManager()


def predict_phishing_ensemble(url):
    """
    Enhanced prediction function using multiple models
    """
    return model_manager.ensemble_predict(url)


def predict_phishing_single_model(url, model_id='primary'):
    """
    Predict using a single specific model
    """
    model_config = settings.PHISHSHIELD_SETTINGS.get('MODELS', {}).get(model_id)
    if not model_config:
        raise ValueError(f"Model '{model_id}' not found in configuration")
    
    return model_manager.predict_with_model(url, model_id, model_config)
