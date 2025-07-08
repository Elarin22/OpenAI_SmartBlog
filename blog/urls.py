from django.urls import path
from . import views
from . import ai_views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("write/", views.PostCreateView.as_view(), name="post_create"),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path("<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    
    # 댓글 관련 URL
    path('comment/<int:post_id>/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:comment_id>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:post_id>/', views.CommentListView.as_view(), name='comment_list'),

    # 좋아요 관련 URL
    path('like/<int:post_id>/', views.LikeToggleView.as_view(), name='like_toggle'),

    # AI 관련 URL
    path('ai/suggest-title/', ai_views.TitleSuggestionView.as_view(), name='ai_suggest_title'),
    path('ai/complete-content/', ai_views.ContentCompletionView.as_view(), name='ai_complete_content'),
    path('ai/suggest-tags/', ai_views.TagSuggestionView.as_view(), name='ai_suggest_tags'),
    path('ai/generate-summary/', ai_views.SummaryGenerationView.as_view(), name='ai_generate_summary'),
    path('ai/usage-stats/', ai_views.ai_usage_stats, name='ai_usage_stats'),
]