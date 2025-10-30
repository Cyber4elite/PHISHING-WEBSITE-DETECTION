"""
Test cases for scanner models
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from scanner.models import ScanReport


class ScanReportModelTest(TestCase):
    """Test cases for ScanReport model"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_features = {
            'url_length': 19,
            'domain_length': 11,
            'path_length': 1,
            'query_length': 0,
            'num_dots': 1,
            'num_hyphens': 0,
            'num_underscores': 0,
            'num_slashes': 2,
            'num_question_marks': 0,
            'num_equals': 0,
            'num_ampersands': 0,
            'num_percent': 0,
            'has_ip': 0,
            'has_shortener': 0,
            'has_suspicious_keywords': 0,
            'subdomain_count': 0,
            'has_www': 0,
            'is_https': 1,
            'path_depth': 0,
            'has_file_extension': 0
        }
    
    def test_scan_report_creation(self):
        """Test creating a scan report"""
        report = ScanReport.objects.create(
            url='https://example.com',
            result='legitimate',
            confidence=0.95,
            features=self.sample_features
        )
        
        self.assertEqual(report.url, 'https://example.com')
        self.assertEqual(report.result, 'legitimate')
        self.assertEqual(report.confidence, 0.95)
        self.assertEqual(report.features, self.sample_features)
        self.assertIsNotNone(report.timestamp)
    
    def test_scan_report_str_representation(self):
        """Test string representation of scan report"""
        report = ScanReport.objects.create(
            url='https://example.com',
            result='phishing',
            confidence=0.85,
            features=self.sample_features
        )
        
        expected = 'Scan Report for https://example.com - phishing'
        self.assertEqual(str(report), expected)
    
    def test_confidence_validation(self):
        """Test confidence field validation"""
        # Test valid confidence values
        report = ScanReport.objects.create(
            url='https://example.com',
            result='legitimate',
            confidence=0.5,
            features=self.sample_features
        )
        self.assertEqual(report.confidence, 0.5)
        
        # Test edge cases
        report.confidence = 0.0
        report.full_clean()
        
        report.confidence = 1.0
        report.full_clean()
    
    def test_confidence_percentage_property(self):
        """Test confidence percentage property"""
        report = ScanReport.objects.create(
            url='https://example.com',
            result='legitimate',
            confidence=0.75,
            features=self.sample_features
        )
        
        self.assertEqual(report.confidence_percentage, 75.0)
    
    def test_is_phishing_property(self):
        """Test is_phishing property"""
        # Test phishing result
        phishing_report = ScanReport.objects.create(
            url='https://phishing.com',
            result='phishing',
            confidence=0.9,
            features=self.sample_features
        )
        self.assertTrue(phishing_report.is_phishing)
        
        # Test legitimate result
        legitimate_report = ScanReport.objects.create(
            url='https://example.com',
            result='legitimate',
            confidence=0.9,
            features=self.sample_features
        )
        self.assertFalse(legitimate_report.is_phishing)
    
    def test_is_legitimate_property(self):
        """Test is_legitimate property"""
        # Test legitimate result
        legitimate_report = ScanReport.objects.create(
            url='https://example.com',
            result='legitimate',
            confidence=0.9,
            features=self.sample_features
        )
        self.assertTrue(legitimate_report.is_legitimate)
        
        # Test phishing result
        phishing_report = ScanReport.objects.create(
            url='https://phishing.com',
            result='phishing',
            confidence=0.9,
            features=self.sample_features
        )
        self.assertFalse(phishing_report.is_legitimate)
    
    def test_model_ordering(self):
        """Test model ordering by timestamp"""
        # Create reports with different timestamps
        report1 = ScanReport.objects.create(
            url='https://example1.com',
            result='legitimate',
            confidence=0.9,
            features=self.sample_features
        )
        
        report2 = ScanReport.objects.create(
            url='https://example2.com',
            result='phishing',
            confidence=0.8,
            features=self.sample_features
        )
        
        reports = ScanReport.objects.all()
        self.assertEqual(reports[0], report2)  # Most recent first
        self.assertEqual(reports[1], report1)


class ScanReportManagerTest(TestCase):
    """Test cases for ScanReportManager"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_features = {
            'url_length': 19,
            'domain_length': 11,
            'path_length': 1,
            'query_length': 0,
            'num_dots': 1,
            'num_hyphens': 0,
            'num_underscores': 0,
            'num_slashes': 2,
            'num_question_marks': 0,
            'num_equals': 0,
            'num_ampersands': 0,
            'num_percent': 0,
            'has_ip': 0,
            'has_shortener': 0,
            'has_suspicious_keywords': 0,
            'subdomain_count': 0,
            'has_www': 0,
            'is_https': 1,
            'path_depth': 0,
            'has_file_extension': 0
        }
        
        # Create test reports
        self.phishing_report = ScanReport.objects.create(
            url='https://phishing.com',
            result='phishing',
            confidence=0.9,
            features=self.sample_features
        )
        
        self.legitimate_report = ScanReport.objects.create(
            url='https://example.com',
            result='legitimate',
            confidence=0.95,
            features=self.sample_features
        )
    
    def test_phishing_filter(self):
        """Test phishing filter"""
        phishing_reports = ScanReport.objects.phishing()
        self.assertEqual(phishing_reports.count(), 1)
        self.assertEqual(phishing_reports.first(), self.phishing_report)
    
    def test_legitimate_filter(self):
        """Test legitimate filter"""
        legitimate_reports = ScanReport.objects.legitimate()
        self.assertEqual(legitimate_reports.count(), 1)
        self.assertEqual(legitimate_reports.first(), self.legitimate_report)
    
    def test_high_confidence_filter(self):
        """Test high confidence filter"""
        high_confidence_reports = ScanReport.objects.high_confidence(0.8)
        self.assertEqual(high_confidence_reports.count(), 2)
        
        high_confidence_reports = ScanReport.objects.high_confidence(0.95)
        self.assertEqual(high_confidence_reports.count(), 1)
    
    def test_low_confidence_filter(self):
        """Test low confidence filter"""
        low_confidence_reports = ScanReport.objects.low_confidence(0.5)
        self.assertEqual(low_confidence_reports.count(), 0)
        
        low_confidence_reports = ScanReport.objects.low_confidence(0.98)
        self.assertEqual(low_confidence_reports.count(), 2)
    
    def test_by_domain_filter(self):
        """Test by domain filter"""
        domain_reports = ScanReport.objects.by_domain('example.com')
        self.assertEqual(domain_reports.count(), 1)
        self.assertEqual(domain_reports.first(), self.legitimate_report)
    
    def test_statistics(self):
        """Test statistics aggregation"""
        stats = ScanReport.objects.statistics()
        
        self.assertEqual(stats['total_scans'], 2)
        self.assertEqual(stats['phishing_count'], 1)
        self.assertEqual(stats['legitimate_count'], 1)
        self.assertAlmostEqual(stats['avg_confidence'], 0.925, places=2)
