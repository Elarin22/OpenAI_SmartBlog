from django import forms
from .models import CustomUser
from blog.models import Post
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
import os

# 새로운 사용자 생성 폼
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg auth-input',
            'placeholder': '이메일을 입력하세요'
        }),
        label='이메일'
    )
    
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 사용자명 필드 커스터마이징
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg auth-input',
            'placeholder': '사용자명을 입력하세요'
        })
        
        # 비밀번호 필드 커스터마이징
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg auth-input',
            'placeholder': '비밀번호를 입력하세요'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg auth-input',
            'placeholder': '비밀번호를 다시 입력하세요'
        })
        
        # 라벨 설정
        self.fields['username'].label = '사용자명'
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# 사용자 회원가입 뷰
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # 회원가입 후 로그인 페이지로 리다이렉트
        return response

# 사용자 로그인 뷰
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    # 로그인 한 유저는 다시 로그인 페이지를 볼 필요없음.
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('post_list')
    
# 사용자 로그아웃 뷰
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('main')
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('main')
    
# 프로필 수정 폼
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '사용자명을 입력하세요'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '이메일을 입력하세요'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '자기소개를 입력하세요 (최대 500자)'
            })
        }
        labels = {
            'username': '사용자명',
            'email': '이메일',
            'bio': '자기소개'
        }


# 프로필 수정 뷰
class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('profile')
    success_message = "프로필이 성공적으로 수정되었습니다!"
    
    def get_object(self):
        return self.request.user


# 프로필 보기 뷰
class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        # URL에 user_id가 있으면 해당 사용자, 없으면 본인
        user_id = self.kwargs.get('user_id')
        if user_id:
            return get_object_or_404(CustomUser, id=user_id)
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        
        # 프로필 사용자가 작성한 게시글들
        context['user_posts'] = Post.objects.filter(author=profile_user).order_by('-created_at')[:5]
        
        # AI 사용 횟수 (본인 프로필일 때만)
        if profile_user == self.request.user:
            context['ai_usage_stats'] = {
                'total_usage': profile_user.ai_usage_count,
                'recent_posts': context['user_posts'].count()
            }
        else:
            context['ai_usage_stats'] = {
                'total_usage': 0,
                'recent_posts': context['user_posts'].count()
            }
        
        # 팔로우 관련 정보
        if self.request.user.is_authenticated:
            context['is_following'] = self.request.user.is_following(profile_user)
        else:
            context['is_following'] = False
        
        return context
    
# 비밀번호 변경 폼
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 폼 필드 스타일링
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': '현재 비밀번호를 입력하세요'
        })
        
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': '새 비밀번호를 입력하세요'
        })
        
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': '새 비밀번호를 다시 입력하세요'
        })
    
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        
        # 현재 비밀번호와 새 비밀번호가 같은지 확인
        if old_password and new_password1:
            # 현재 비밀번호가 맞는지 확인
            if self.user.check_password(old_password):
                # 현재 비밀번호와 새 비밀번호가 같은지 비교
                if old_password == new_password1:
                    raise ValidationError("새 비밀번호는 현재 비밀번호와 달라야 합니다.")
        
        return cleaned_data

# 비밀번호 변경 뷰
class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm  # 커스텀 폼 사용
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = "비밀번호가 성공적으로 변경되었습니다!"

@method_decorator([login_required, csrf_exempt], name='dispatch')

# 팔로우/언팔로우 토글 (AJAX)
class FollowToggleView(View):
    def post(self, request, user_id):
        try:
            target_user = get_object_or_404(CustomUser, id=user_id)
            
            # 자기 자신 팔로우 방지
            if request.user == target_user:
                return JsonResponse({
                    'success': False,
                    'error': '자기 자신을 팔로우할 수 없습니다.'
                })
            
            # 팔로우 토글
            is_following, follower_count = request.user.toggle_follow(target_user)
            
            return JsonResponse({
                'success': True,
                'is_following': is_following,
                'follower_count': follower_count,
                'message': '팔로우했습니다!' if is_following else '팔로우를 취소했습니다.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'오류가 발생했습니다: {str(e)}'
            })

# 팔로워 목록
class FollowerListView(DetailView):
    model = CustomUser
    template_name = 'accounts/follower_list.html'
    context_object_name = 'profile_user'
    pk_url_kwarg = 'user_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        followers = self.object.followers.all().order_by('-created_at')
        
        # 각 팔로워에 대해 현재 사용자가 팔로우하고 있는지 계산
        if self.request.user.is_authenticated:
            for follow in followers:
                follow.is_following = self.request.user.is_following(follow.follower)
        
        context['followers'] = followers
        return context

# 팔로잉 목록
class FollowingListView(DetailView):
    model = CustomUser
    template_name = 'accounts/following_list.html'
    context_object_name = 'profile_user'
    pk_url_kwarg = 'user_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following = self.object.following.all().order_by('-created_at')
        
        # 각 팔로잉에 대해 현재 사용자가 팔로우하고 있는지 계산
        if self.request.user.is_authenticated:
            for follow in following:
                follow.is_following = self.request.user.is_following(follow.following)
        
        context['following'] = following
        return context