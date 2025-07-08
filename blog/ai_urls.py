from django.urls import path
from . import ai_views

app_name = 'ai'

urlpatterns = [
    path('suggest-title/', ai_views.TitleSuggestionView.as_view(), name='suggest_title'),
    path('complete-content/', ai_views.ContentCompletionView.as_view(), name='complete_content'),
    path('suggest-tags/', ai_views.TagSuggestionView.as_view(), name='suggest_tags'),
    path('generate-summary/', ai_views.SummaryGenerationView.as_view(), name='generate_summary'),
    path('usage-stats/', ai_views.ai_usage_stats, name='usage_stats'),
]