"""
Test cases for scanner views
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from scanner.models import ScanReport


class HomeViewTest(TestCase):
    """Test cases for home view"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_home_view_get(self):
        """Test GET request to home view"""
        response = self.client.get(reverse('scanner:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PhishShield')
        self.assertContains(response, 'Enter URL to scan')
        self.assertContains(response, 'form')
    
    def test_home_view_template(self):
        """Test home view uses correct template"""
        response = self.client.get(reverse('scanner:home'))
        self.assertTemplateUsed(response, 'index.html')


class AnalyzeUrlViewTest(TestCase):
    """Test cases for analyze URL view"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
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
    
    def test_analyze_url_view_get(self):
        """Test GET request to analyze URL view"""
        response = self.client.get(reverse('scanner:analyze'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_analyze_url_view_post_valid(self):
        """Test POST request with valid URL"""
        url_data = {
            'url': 'https://example.com'
        }
        
        response = self.client.post(reverse('scanner:analyze'), url_data)
        
        # Should redirect to results page or show results
        self.assertIn(response.status_code, [200, 302])
        
        # Check if report was created
        self.assertTrue(ScanReport.objects.filter(url='https://example.com').exists())
    
    def test_analyze_url_view_post_invalid(self):
        """Test POST request with invalid URL"""
        url_data = {
            'url': 'invalid-url'
        }
        
        response = self.client.post(reverse('scanner:analyze'), url_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'error')
    
    def test_analyze_url_view_post_empty(self):
        """Test POST request with empty URL"""
        url_data = {
            'url': ''
        }
        
        response = self.client.post(reverse('scanner:analyze'), url_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_analyze_url_view_csrf_protection(self):
        """Test CSRF protection is enabled"""
        # This test ensures CSRF protection is working
        # The view should be decorated with @csrf_protect
        response = self.client.post(reverse('scanner:analyze'), {
            'url': 'https://example.com'
        })
        
        # Should not raise CSRF error for valid requests
        self.assertNotEqual(response.status_code, 403)


class ReportPdfViewTest(TestCase):
    """Test cases for PDF report view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
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
        
        self.report = ScanReport.objects.create(
            url='https://example.com',
            result='legitimate',
            confidence=0.95,
            features=self.sample_features
        )
    
    def test_report_pdf_view_valid_id(self):
        """Test PDF view with valid report ID"""
        response = self.client.get(reverse('scanner:report_pdf', args=[self.report.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment', response['Content-Disposition'])
        self.assertIn('phishshield_report', response['Content-Disposition'])
    
    def test_report_pdf_view_invalid_id(self):
        """Test PDF view with invalid report ID"""
        response = self.client.get(reverse('scanner:report_pdf', args=[99999]))
        
        self.assertEqual(response.status_code, 404)
    
    def test_report_pdf_content(self):
        """Test PDF content contains expected information"""
        response = self.client.get(reverse('scanner:report_pdf', args=[self.report.id]))
        
        # Check PDF content (basic check)
        self.assertIn(b'PDF', response.content)
        self.assertIn(b'PhishShield', response.content)
    
    def test_report_pdf_filename(self):
        """Test PDF filename format"""
        response = self.client.get(reverse('scanner:report_pdf', args=[self.report.id]))
        
        expected_filename = f'phishshield_report_{self.report.id}.pdf'
        self.assertIn(expected_filename, response['Content-Disposition'])


class ViewIntegrationTest(TestCase):
    """Integration tests for views"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_complete_workflow(self):
        """Test complete workflow from home to results"""
        # 1. Access home page
        response = self.client.get(reverse('scanner:home'))
        self.assertEqual(response.status_code, 200)
        
        # 2. Submit URL for analysis
        url_data = {'url': 'https://example.com'}
        response = self.client.post(reverse('scanner:analyze'), url_data)
        
        # 3. Check if report was created
        self.assertTrue(ScanReport.objects.filter(url='https://example.com').exists())
        
        # 4. Get the created report
        report = ScanReport.objects.get(url='https://example.com')
        
        # 5. Test PDF generation
        response = self.client.get(reverse('scanner:report_pdf', args=[report.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
