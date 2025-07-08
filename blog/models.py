from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


# 해시태그 데이터 저장 모델
class Tag(models.Model):
    # 태그 이름은 고유해야함 : unique = True
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# 게시물 데이터 구조 정의 모델
class Post(models.Model):
    CATEGORY_CHOICES = [
        ("tech", "기술"),
        ("life", "일상"),
        ("review", "리뷰"),
        ("etc", "기타"),
    ]
    title = models.CharField(max_length=200)  # 제목
    content = models.TextField()  # 내용
    summary = models.TextField(blank=True, help_text="AI 생성 요약")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="etc")
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    is_ai_assisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 최신순(내림차순)으로 게시물 목록 정렬 기준
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    # 대표 URL 반환 메서드
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    # 좋아요 수 반환
    def get_like_count(self):
        return self.likes.count()
    
    # 특정 사용자가 좋아요 했는지 확인
    def is_liked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False
    
    # 좋아요 토글 (좋아요/취소)
    def toggle_like(self, user):
        if not user.is_authenticated:
            return False, 0
        
        like, created = Like.objects.get_or_create(user=user, post=self)
        if not created:
            # 이미 좋아요한 경우 -> 취소
            like.delete()
            return False, self.get_like_count()
        else:
            # 새로 좋아요
            return True, self.get_like_count()

# 댓글 데이터 정의 모델(대댓글 포함)
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 대댓글 기능
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 오래된순(오름차순)으로 댓글/리뷰 정렬기준
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username} : {self.content[:50]}'
    
# AI 사용횟수 정의 모델
class AIUsageLog(models.Model):
    FEATURE_CHOICES = [
        ('autocomplete', '자동완성'),
        ('title_suggest', '제목추천'),
        ('tag_suggest', '태그추천'),
        ('summary', '요약'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feature_type = models.CharField(max_length=20, choices=FEATURE_CHOICES)
    tokens_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 사용자명 - 기능유형
        return f'{self.user.username} - {self.feature_type}'
    
# 게시글 좋아요 모델
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # 한 사용자가 같은 게시글에 중복 좋아요 방지
        unique_together = ('user', 'post')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'

