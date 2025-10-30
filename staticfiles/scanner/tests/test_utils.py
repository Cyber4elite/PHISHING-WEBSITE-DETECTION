"""
Test cases for scanner utilities
"""
from django.test import TestCase
from scanner.utils import extract_features, predict_phishing, rule_based_prediction
import numpy as np
import os
from django.conf import settings


class ExtractFeaturesTest(TestCase):
    """Test cases for feature extraction"""
    
    def test_extract_features_basic_url(self):
        """Test feature extraction for basic URL"""
        url = 'https://example.com'
        features = extract_features(url)
        
        # Check required features are present
        required_features = [
            'url_length', 'domain_length', 'path_length', 'query_length',
            'num_dots', 'num_hyphens', 'num_underscores', 'num_slashes',
            'num_question_marks', 'num_equals', 'num_ampersands', 'num_percent',
            'has_ip', 'has_shortener', 'has_suspicious_keywords',
            'subdomain_count', 'has_www', 'is_https', 'path_depth',
            'has_file_extension'
        ]
        
        for feature in required_features:
            self.assertIn(feature, features)
        
        # Check specific values
        self.assertEqual(features['url_length'], 19)
        self.assertEqual(features['domain_length'], 11)
        self.assertEqual(features['path_length'], 1)
        self.assertEqual(features['query_length'], 0)
        self.assertEqual(features['num_dots'], 1)
        self.assertEqual(features['is_https'], 1)
        self.assertEqual(features['has_ip'], 0)
        self.assertEqual(features['has_www'], 0)
    
    def test_extract_features_with_path(self):
        """Test feature extraction for URL with path"""
        url = 'https://example.com/path/to/page'
        features = extract_features(url)
        
        self.assertEqual(features['path_length'], 15)
        self.assertEqual(features['path_depth'], 2)
        self.assertEqual(features['num_slashes'], 4)
    
    def test_extract_features_with_query(self):
        """Test feature extraction for URL with query parameters"""
        url = 'https://example.com/search?q=test&page=1'
        features = extract_features(url)
        
        self.assertEqual(features['query_length'], 16)
        self.assertEqual(features['num_question_marks'], 1)
        self.assertEqual(features['num_equals'], 2)
        self.assertEqual(features['num_ampersands'], 1)
    
    def test_extract_features_ip_address(self):
        """Test feature extraction for IP address URL"""
        url = 'http://192.168.1.1'
        features = extract_features(url)
        
        self.assertEqual(features['has_ip'], 1)
        self.assertEqual(features['is_https'], 0)
    
    def test_extract_features_url_shortener(self):
        """Test feature extraction for URL shortener"""
        url = 'https://bit.ly/abc123'
        features = extract_features(url)
        
        self.assertEqual(features['has_shortener'], 1)
    
    def test_extract_features_suspicious_keywords(self):
        """Test feature extraction for suspicious keywords"""
        url = 'https://secure-bank-login.com'
        features = extract_features(url)
        
        self.assertEqual(features['has_suspicious_keywords'], 1)
    
    def test_extract_features_subdomain(self):
        """Test feature extraction for subdomain"""
        url = 'https://www.sub.example.com'
        features = extract_features(url)
        
        self.assertEqual(features['has_www'], 1)
        self.assertEqual(features['subdomain_count'], 1)
    
    def test_extract_features_file_extension(self):
        """Test feature extraction for file extension"""
        url = 'https://example.com/file.pdf'
        features = extract_features(url)
        
        self.assertEqual(features['has_file_extension'], 1)
    
    def test_extract_features_special_characters(self):
        """Test feature extraction for special characters"""
        url = 'https://example.com/path_with_underscores-and-hyphens'
        features = extract_features(url)
        
        self.assertEqual(features['num_underscores'], 1)
        self.assertEqual(features['num_hyphens'], 1)
    
    def test_extract_features_percent_encoding(self):
        """Test feature extraction for percent encoding"""
        url = 'https://example.com/path%20with%20spaces'
        features = extract_features(url)
        
        self.assertEqual(features['num_percent'], 2)
    
    def test_extract_features_empty_path(self):
        """Test feature extraction for URL with empty path"""
        url = 'https://example.com/'
        features = extract_features(url)
        
        self.assertEqual(features['path_length'], 1)  # Just the slash
        self.assertEqual(features['path_depth'], 0)
    
    def test_extract_features_complex_url(self):
        """Test feature extraction for complex URL"""
        url = 'https://www.sub.example.com:8080/path/to/file.html?param=value&other=123#fragment'
        features = extract_features(url)
        
        # Check various features
        self.assertGreater(features['url_length'], 50)
        self.assertEqual(features['has_www'], 1)
        self.assertEqual(features['subdomain_count'], 1)
        self.assertEqual(features['is_https'], 1)
        self.assertEqual(features['has_file_extension'], 1)
        self.assertGreater(features['path_depth'], 0)
        self.assertGreater(features['query_length'], 0)


class RuleBasedPredictionTest(TestCase):
    """Test cases for rule-based prediction fallback"""
    
    def test_rule_based_prediction_legitimate(self):
        """Test rule-based prediction for legitimate URL"""
        features = {
            'has_ip': 0,
            'has_shortener': 0,
            'has_suspicious_keywords': 0,
            'url_length': 20,
            'num_dots': 1,
            'subdomain_count': 0,
            'is_https': 1
        }
        
        prediction, confidence = rule_based_prediction(features)
        
        self.assertEqual(prediction, 'legitimate')
        self.assertLess(confidence, 0.5)
    
    def test_rule_based_prediction_phishing(self):
        """Test rule-based prediction for phishing URL"""
        features = {
            'has_ip': 1,  # +0.3
            'has_shortener': 1,  # +0.2
            'has_suspicious_keywords': 1,  # +0.2
            'url_length': 150,  # +0.1
            'num_dots': 5,  # +0.1
            'subdomain_count': 3,  # +0.1
            'is_https': 0  # +0.1
        }
        
        prediction, confidence = rule_based_prediction(features)
        
        self.assertEqual(prediction, 'phishing')
        self.assertGreater(confidence, 0.5)
    
    def test_rule_based_prediction_edge_case(self):
        """Test rule-based prediction for edge case"""
        features = {
            'has_ip': 0,
            'has_shortener': 0,
            'has_suspicious_keywords': 0,
            'url_length': 50,
            'num_dots': 2,
            'subdomain_count': 1,
            'is_https': 1
        }
        
        prediction, confidence = rule_based_prediction(features)
        
        # Should be legitimate with low confidence
        self.assertEqual(prediction, 'legitimate')
        self.assertLess(confidence, 0.5)
    
    def test_rule_based_prediction_confidence_calculation(self):
        """Test confidence calculation in rule-based prediction"""
        features = {
            'has_ip': 1,  # +0.3
            'has_shortener': 0,
            'has_suspicious_keywords': 0,
            'url_length': 50,
            'num_dots': 1,
            'subdomain_count': 0,
            'is_https': 1
        }
        
        prediction, confidence = rule_based_prediction(features)
        
        # Score should be 0.3, so phishing with 0.3 confidence
        self.assertEqual(prediction, 'phishing')
        self.assertAlmostEqual(confidence, 0.3, places=1)


class PredictPhishingTest(TestCase):
    """Test cases for main prediction function"""
    
    def test_predict_phishing_basic(self):
        """Test basic prediction functionality"""
        url = 'https://example.com'
        result = predict_phishing(url)
        
        # Check result structure
        self.assertIn('prediction', result)
        self.assertIn('confidence', result)
        self.assertIn('features', result)
        
        # Check prediction values
        self.assertIn(result['prediction'], ['phishing', 'legitimate'])
        self.assertIsInstance(result['confidence'], float)
        self.assertGreaterEqual(result['confidence'], 0.0)
        self.assertLessEqual(result['confidence'], 1.0)
        
        # Check features
        self.assertIsInstance(result['features'], dict)
        self.assertGreater(len(result['features']), 0)
    
    def test_predict_phishing_with_model(self):
        """Test prediction with model file present"""
        # This test assumes model.npy exists
        url = 'https://example.com'
        result = predict_phishing(url)
        
        # Should return valid result regardless of model presence
        self.assertIn('prediction', result)
        self.assertIn('confidence', result)
        self.assertIn('features', result)
    
    def test_predict_phishing_without_model(self):
        """Test prediction without model file"""
        # Temporarily rename model file if it exists
        model_path = os.path.join(settings.BASE_DIR, 'scanner', 'model.npy')
        backup_path = model_path + '.backup'
        
        if os.path.exists(model_path):
            os.rename(model_path, backup_path)
        
        try:
            url = 'https://example.com'
            result = predict_phishing(url)
            
            # Should fall back to rule-based prediction
            self.assertIn('prediction', result)
            self.assertIn('confidence', result)
            self.assertIn('features', result)
            
        finally:
            # Restore model file if it existed
            if os.path.exists(backup_path):
                os.rename(backup_path, model_path)
    
    def test_predict_phishing_error_handling(self):
        """Test prediction error handling"""
        # Test with invalid URL that might cause errors
        url = 'not-a-valid-url'
        result = predict_phishing(url)
        
        # Should handle error gracefully
        self.assertIn('prediction', result)
        self.assertIn('confidence', result)
        self.assertIn('features', result)
    
    def test_predict_phishing_different_urls(self):
        """Test prediction with different types of URLs"""
        test_urls = [
            'https://example.com',
            'http://192.168.1.1',
            'https://bit.ly/abc123',
            'https://secure-bank-login.com',
            'https://www.sub.example.com/path/file.html?param=value'
        ]
        
        for url in test_urls:
            result = predict_phishing(url)
            
            # Each result should be valid
            self.assertIn('prediction', result)
            self.assertIn('confidence', result)
            self.assertIn('features', result)
            self.assertIn(result['prediction'], ['phishing', 'legitimate'])
            self.assertGreaterEqual(result['confidence'], 0.0)
            self.assertLessEqual(result['confidence'], 1.0)
    
    def test_predict_phishing_feature_consistency(self):
        """Test that features are consistent between calls"""
        url = 'https://example.com'
        result1 = predict_phishing(url)
        result2 = predict_phishing(url)
        
        # Features should be identical
        self.assertEqual(result1['features'], result2['features'])
        
        # Predictions should be identical (deterministic)
        self.assertEqual(result1['prediction'], result2['prediction'])
        self.assertEqual(result1['confidence'], result2['confidence'])
