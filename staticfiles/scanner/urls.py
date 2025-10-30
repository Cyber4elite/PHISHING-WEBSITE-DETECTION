from django.urls import path
from . import views

app_name = 'scanner'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_docs_view, name='about'),
    path('scan/', views.scan_view, name='scan'),
    path('result/', views.analyze_url_view, name='analyze'),
    path('report/<int:report_id>/pdf/', views.report_pdf_view, name='report_pdf'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('model-maintenance/', views.model_maintenance_view, name='model_maintenance'),
    path('threat-feed-monitor/', views.threat_feed_monitor_view, name='threat_feed_monitor'),
    path('retrain-model/', views.retrain_model_view, name='retrain_model'),
    path('export-model/', views.export_model_details_view, name='export_model'),
    
    # API endpoints for multiple models
    path('api/predict/ensemble/', views.predict_ensemble_api, name='predict_ensemble_api'),
    path('api/predict/model/<str:model_id>/', views.predict_with_model_api, name='predict_model_api'),
]
