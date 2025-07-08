from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # 자기소개 등 서식 파일
    bio = models.TextField(max_length=500, blank=True)
    # user마다 ai 사용횟수 / default 0번
    ai_usage_count = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    # 팔로워 수 반환
    def get_follower_count(self):
        return self.followers.count()

    # 팔로잉 수 반환
    def get_following_count(self):
        return self.following.count()

    # 특정 사용자를 팔로우하고 있는지 확인
    def is_following(self, user):
        if user == self:
            return False
        return self.following.filter(following=user).exists()

    # 팔로우 토글 (팔로우/언팔로우)
    def toggle_follow(self, user):
        if user == self or not user:
            return False, 0

        follow, created = Follow.objects.get_or_create(follower=self, following=user)
        if not created:
            # 이미 팔로우한 경우 -> 언팔로우
            follow.delete()
            return False, user.get_follower_count()
        else:
            # 새로 팔로우
            return True, user.get_follower_count()


# 사용자 팔로우 모델
class Follow(models.Model):
    # 팔로우 하는 사람
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="following"
    )
    # 팔로우 받는 사람
    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 중복 팔로우 방지
        unique_together = ("follower", "following")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    def save(self, *args, **kwargs):
        # 자기 자신을 팔로우하는 것 방지
        if self.follower == self.following:
            raise ValueError("사용자는 자기 자신을 팔로우할 수 없습니다.")
        super().save(*args, **kwargs)
