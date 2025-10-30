"""
Test cases for scanner forms
"""
from django.test import TestCase
from scanner.forms import URLScanForm


class URLScanFormTest(TestCase):
    """Test cases for URLScanForm"""
    
    def test_valid_url(self):
        """Test form with valid URL"""
        form_data = {'url': 'https://example.com'}
        form = URLScanForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['url'], 'https://example.com')
    
    def test_valid_url_with_path(self):
        """Test form with valid URL containing path"""
        form_data = {'url': 'https://example.com/path/to/page'}
        form = URLScanForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['url'], 'https://example.com/path/to/page')
    
    def test_valid_url_with_query_params(self):
        """Test form with valid URL containing query parameters"""
        form_data = {'url': 'https://example.com/search?q=test&page=1'}
        form = URLScanForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['url'], 'https://example.com/search?q=test&page=1')
    
    def test_invalid_url_no_protocol(self):
        """Test form with URL missing protocol"""
        form_data = {'url': 'example.com'}
        form = URLScanForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('url', form.errors)
    
    def test_invalid_url_malformed(self):
        """Test form with malformed URL"""
        form_data = {'url': 'not-a-url'}
        form = URLScanForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('url', form.errors)
    
    def test_empty_url(self):
        """Test form with empty URL"""
        form_data = {'url': ''}
        form = URLScanForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('url', form.errors)
    
    def test_url_too_long(self):
        """Test form with URL exceeding max length"""
        long_url = 'https://example.com/' + 'a' * 500
        form_data = {'url': long_url}
        form = URLScanForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('url', form.errors)
    
    def test_http_url(self):
        """Test form with HTTP URL (should be valid)"""
        form_data = {'url': 'http://example.com'}
        form = URLScanForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['url'], 'http://example.com')
    
    def test_ftp_url(self):
        """Test form with FTP URL (should be valid)"""
        form_data = {'url': 'ftp://example.com/file.txt'}
        form = URLScanForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['url'], 'ftp://example.com/file.txt')
    
    def test_form_widget_attributes(self):
        """Test form widget attributes"""
        form = URLScanForm()
        
        url_field = form.fields['url']
        self.assertEqual(url_field.max_length, 500)
        self.assertTrue(url_field.required)
        
        # Check widget attributes
        widget_attrs = url_field.widget.attrs
        self.assertIn('class', widget_attrs)
        self.assertIn('placeholder', widget_attrs)
        self.assertIn('required', widget_attrs)
        self.assertEqual(widget_attrs['class'], 'form-control')
        self.assertEqual(widget_attrs['placeholder'], 'https://example.com')
    
    def test_form_label(self):
        """Test form field label"""
        form = URLScanForm()
        url_field = form.fields['url']
        
        self.assertEqual(url_field.label, 'Enter URL to scan')
    
    def test_form_clean_data(self):
        """Test form clean data method"""
        form_data = {'url': 'https://example.com'}
        form = URLScanForm(data=form_data)
        
        if form.is_valid():
            cleaned_data = form.clean()
            self.assertIn('url', cleaned_data)
            self.assertEqual(cleaned_data['url'], 'https://example.com')
    
    def test_multiple_validation_errors(self):
        """Test form with multiple validation errors"""
        form_data = {'url': ''}  # Empty URL
        form = URLScanForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('url', form.errors)
        self.assertTrue(len(form.errors) > 0)
    
    def test_form_rendering(self):
        """Test form rendering"""
        form = URLScanForm()
        form_html = str(form)
        
        # Check if form contains expected elements
        self.assertIn('form-control', form_html)
        self.assertIn('placeholder="https://example.com"', form_html)
        self.assertIn('required', form_html)
    
    def test_form_with_whitespace(self):
        """Test form with URL containing whitespace"""
        form_data = {'url': '  https://example.com  '}
        form = URLScanForm(data=form_data)
        
        # Django's URLField should handle whitespace
        if form.is_valid():
            self.assertEqual(form.cleaned_data['url'].strip(), 'https://example.com')
    
    def test_form_case_sensitivity(self):
        """Test form with different URL cases"""
        test_urls = [
            'https://EXAMPLE.COM',
            'https://Example.Com',
            'https://example.com'
        ]
        
        for url in test_urls:
            form_data = {'url': url}
            form = URLScanForm(data=form_data)
            self.assertTrue(form.is_valid(), f"URL {url} should be valid")
