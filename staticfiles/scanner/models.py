from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q, Count, Avg
from django.contrib.auth.models import User


class ScanReportManager(models.Manager):
    def recent(self, days=7):
        """Get recent scans within specified days"""
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(timestamp__gte=cutoff)
    
    def phishing(self):
        """Get phishing reports"""
        return self.filter(result='phishing')
    
    def legitimate(self):
        """Get legitimate reports"""
        return self.filter(result='legitimate')
    
    def high_confidence(self, threshold=0.8):
        """Get high confidence reports"""
        return self.filter(confidence__gte=threshold)
    
    def low_confidence(self, threshold=0.5):
        """Get low confidence reports"""
        return self.filter(confidence__lt=threshold)
    
    def by_domain(self, domain):
        """Get reports by domain"""
        return self.filter(url__icontains=domain)
    
    def statistics(self):
        """Get scan statistics"""
        return self.aggregate(
            total_scans=Count('id'),
            phishing_count=Count('id', filter=Q(result='phishing')),
            legitimate_count=Count('id', filter=Q(result='legitimate')),
            avg_confidence=Avg('confidence')
        )


class ScanReport(models.Model):
    PHISHING = 'phishing'
    LEGITIMATE = 'legitimate'
    RESULT_CHOICES = [
        (PHISHING, 'Phishing'),
        (LEGITIMATE, 'Legitimate'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.URLField(max_length=500, db_index=True)
    result = models.CharField(
        max_length=20, 
        choices=RESULT_CHOICES,
        db_index=True
    )
    confidence = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        db_index=True
    )
    features = models.JSONField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    
    objects = ScanReportManager()
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['result']),
            models.Index(fields=['confidence']),
            models.Index(fields=['url', 'timestamp']),
            models.Index(fields=['result', 'confidence']),
        ]
        verbose_name = 'Scan Report'
        verbose_name_plural = 'Scan Reports'
    
    def __str__(self):
        return f"Scan Report for {self.url} - {self.result}"
    
    @property
    def is_phishing(self):
        return self.result == self.PHISHING
    
    @property
    def is_legitimate(self):
        return self.result == self.LEGITIMATE
    
    @property
    def confidence_percentage(self):
        return round(self.confidence * 100, 2)


class UserActivity(models.Model):
    """Track user activity for admin monitoring"""
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('scan', 'URL Scan'),
        ('signup', 'User Registration'),
        ('profile_view', 'Profile View'),
        ('password_changed', 'Password Changed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} at {self.timestamp}"