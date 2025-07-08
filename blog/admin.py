from django.contrib import admin
from .models import Post, Comment, Tag, AIUsageLog


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "category",
        "views",
        "is_ai_assisted",
        "created_at",
    ]
    list_filter = ["category", "is_ai_assisted", "created_at"]
    search_fields = ["title", "content"]
    filter_horizontal = ["tags"]
    readonly_fields = ["views", "created_at", "updated_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "content_preview", "created_at"]
    list_filter = ["created_at"]

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "내용 미리보기"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(AIUsageLog)
class AIUsageLogAdmin(admin.ModelAdmin):
    list_display = ["user", "feature_type", "tokens_used", "created_at"]
    list_filter = ["feature_type", "created_at"]
    readonly_fields = ["created_at"]
