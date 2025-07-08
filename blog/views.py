from .models import Post, Comment, Tag
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import F, Q, Count
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json


# 메인 페이지
def main_view(request):
    return render(request, "main.html")


# 목록 페이지
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.select_related("author").prefetch_related("tags", "likes").annotate(likes_count = Count('likes'))

        # 검색 기능
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(content__icontains=search_query)
                | Q(tags__name__icontains=search_query)
            ).distinct()

        # 카테고리 필터
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)

        sort_by = self.request.GET.get("sort", "latest")  # 최신순
        
        if sort_by == "likes":
            # 좋아요 많은 순
            queryset = queryset.order_by("-likes_count", "-created_at")
        elif sort_by == "views":
            # 조회수 많은 순
            queryset = queryset.order_by("-views", "-created_at")
        elif sort_by == "oldest":
            # 오래된 순
            queryset = queryset.order_by("created_at")
        else:  # latest (기본값)
            # 최신순
            queryset = queryset.order_by("-created_at")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["selected_sort"] = self.request.GET.get("sort", "latest")
        context["categories"] = Post.CATEGORY_CHOICES
        context["sort_options"] = [
            ("latest", "최신순"),
            ("likes", "좋아요순"),
            ("views", "조회수순"),
            ("oldest", "오래된순"),
        ]
        
        # 각 포스트에 좋아요 정보 추가
        if self.request.user.is_authenticated:
            for post in context['posts']:
                post.user_liked = post.is_liked_by(self.request.user)
                post.like_count = post.get_like_count()
        else:
            for post in context['posts']:
                post.user_liked = False
                post.like_count = post.get_like_count()
        
        return context


# 게시물 상세 뷰
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        # 조회수 증가
        Post.objects.filter(pk=post.pk).update(views=F("views") + 1)
        post.refresh_from_db()
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        
        # 좋아요 관련 정보 추가
        if self.request.user.is_authenticated:
            context['is_liked'] = post.is_liked_by(self.request.user)
        else:
            context['is_liked'] = False
        
        context['like_count'] = post.get_like_count()
        
        return context


# 게시물 생성 뷰
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content", "category", "image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        
        # 폼이 유효하면 먼저 저장
        response = super().form_valid(form)
        
        # 태그 데이터 처리
        tags_data = self.request.POST.get('tags_data', '')
        if tags_data:
            try:
                tag_list = json.loads(tags_data)
                for tag_info in tag_list:
                    tag_name = tag_info.get('name', '').strip()
                    if tag_name:
                        tag = Tag.objects.get_or_create(name=tag_name)
                        self.object.tags.add(tag)
            except (json.JSONDecodeError, TypeError):
                pass  # 태그 데이터가 잘못된 경우 무시
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        return context


# 게시물 수정 뷰
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content", "category", "image"]

    def test_func(self):
        post = self.get_object()
        # 현재 로그인한 사용자 == 게시물 작성자 : True 일 때 수정가능
        return self.request.user == post.author

    def form_valid(self, form):
        # 폼이 유효하면 먼저 저장
        response = super().form_valid(form)
        
        # 기존 태그들 모두 제거
        self.object.tags.clear()
        
        # 새로운 태그 데이터 처리
        tags_data = self.request.POST.get('tags_data', '')
        if tags_data:
            try:
                tag_list = json.loads(tags_data)
                for tag_info in tag_list:
                    tag_name = tag_info.get('name', '').strip()
                    if tag_name:
                        tag = Tag.objects.get_or_create(name=tag_name)
                        self.object.tags.add(tag)
            except (json.JSONDecodeError, TypeError):
                pass  # 태그 데이터가 잘못된 경우 무시
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()  # 모든 태그 전달
        return context


# 게시물 삭제 뷰
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        # URL 파라미터로 이전 페이지 확인
        from_page = self.request.GET.get('from')
        
        if from_page == 'profile':
            return '/accounts/profile/'
        
        # 기본값 : 블로그 목록
        return reverse_lazy("post_list")


# 댓글 작성 뷰
@method_decorator([login_required, csrf_exempt], name='dispatch')
class CommentCreateView(View):
    def post(self, request, post_id):
        try:
            post = get_object_or_404(Post, pk=post_id)
            data = json.loads(request.body)
            
            content = data.get('content', '').strip()
            parent_id = data.get('parent_id')
            
            if not content:
                return JsonResponse({
                    'success': False,
                    'error': '댓글 내용을 입력해주세요.'
                })
            
            # 대댓글인 경우 부모 댓글 확인
            parent_comment = None
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id, post=post)
                except Comment.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': '부모 댓글을 찾을 수 없습니다.'
                    })
            
            # 댓글 생성
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
                parent=parent_comment
            )
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.author.username,
                    'created_at': comment.created_at.strftime('%Y년 %m월 %d일 %H:%M'),
                    'parent_id': comment.parent.id if comment.parent else None,
                    'is_author': True,  # 작성자이므로 삭제 버튼 표시
                    'can_delete': True
                },
                'message': '댓글이 작성되었습니다!'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': '잘못된 요청 형식입니다.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'댓글 작성 중 오류가 발생했습니다: {str(e)}'
            })


# 댓글 삭제 뷰
@method_decorator([login_required, csrf_exempt], name='dispatch')
class CommentDeleteView(View):
    def post(self, request, comment_id):
        try:
            comment = get_object_or_404(Comment, pk=comment_id)
            
            # 작성자 또는 게시글 작성자만 삭제 가능
            if request.user != comment.author and request.user != comment.post.author:
                return JsonResponse({
                    'success': False,
                    'error': '댓글을 삭제할 권한이 없습니다.'
                })
            
            comment_id = comment.id
            comment.delete()
            
            return JsonResponse({
                'success': True,
                'comment_id': comment_id,
                'message': '댓글이 삭제되었습니다.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'댓글 삭제 중 오류가 발생했습니다: {str(e)}'
            })


# 댓글 목록 조회 뷰
class CommentListView(View):
    def get(self, request, post_id):
        try:
            post = get_object_or_404(Post, pk=post_id)
            comments = Comment.objects.filter(post=post).select_related('author', 'parent').order_by('created_at')
            
            comments_data = []
            for comment in comments:
                comments_data.append({
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.author.username,
                    'created_at': comment.created_at.strftime('%Y년 %m월 %d일 %H:%M'),
                    'parent_id': comment.parent.id if comment.parent else None,
                    'is_author': request.user == comment.author if request.user.is_authenticated else False,
                    'can_delete': (
                        request.user == comment.author or 
                        request.user == comment.post.author
                    ) if request.user.is_authenticated else False
                })
            
            return JsonResponse({
                'success': True,
                'comments': comments_data,
                'total_count': len(comments_data)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'댓글을 불러오는 중 오류가 발생했습니다: {str(e)}'
            })


# 댓글 수정 뷰
@method_decorator([login_required, csrf_exempt], name='dispatch')
class CommentUpdateView(View):
    def post(self, request, comment_id):
        try:
            comment = get_object_or_404(Comment, pk=comment_id)
            
            # 작성자만 수정 가능
            if request.user != comment.author:
                return JsonResponse({
                    'success': False,
                    'error': '댓글을 수정할 권한이 없습니다.'
                })
            
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            
            if not content:
                return JsonResponse({
                    'success': False,
                    'error': '댓글 내용을 입력해주세요.'
                })
            
            comment.content = content
            comment.save()
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.author.username,
                    'created_at': comment.created_at.strftime('%Y년 %m월 %d일 %H:%M'),
                    'parent_id': comment.parent.id if comment.parent else None,
                },
                'message': '댓글이 수정되었습니다!'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': '잘못된 요청 형식입니다.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'댓글 수정 중 오류가 발생했습니다: {str(e)}'
            })
        
# 좋아요/좋아요 취소 토글 (AJAX)
@method_decorator([login_required, csrf_exempt], name='dispatch')
class LikeToggleView(View):
    
    def post(self, request, post_id):
        try:
            post = get_object_or_404(Post, pk=post_id)
            
            # 좋아요 토글
            is_liked, like_count = post.toggle_like(request.user)
            
            return JsonResponse({
                'success': True,
                'is_liked': is_liked,
                'like_count': like_count,
                'message': '좋아요를 눌렀습니다!' if is_liked else '좋아요를 취소했습니다.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'오류가 발생했습니다: {str(e)}'
            })