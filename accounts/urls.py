from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # 프로필 관련 URL
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='user_profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),

    # 팔로우 관련 URL
    path('follow/<int:user_id>/', views.FollowToggleView.as_view(), name='follow_toggle'),
    path('followers/<int:user_id>/', views.FollowerListView.as_view(), name='follower_list'),
    path('following/<int:user_id>/', views.FollowingListView.as_view(), name='following_list'),
]