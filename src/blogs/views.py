from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from .forms import PostForm
from .services import *
from .models import *


class FeedView(TemplateView):
    template_name = 'feed.html'

    def get(self, request, *args, **kwargs):
        posts = get_user_feed_posts(request.user)
        return self.render_to_response({'posts': posts})


class OtherUsersBlogsView(TemplateView):
    template_name = 'blogs.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'blogs': get_other_users_blogs(request.user)})


class BlogView(TemplateView):
    template_name = 'blog.html'

    def send_blog(self, request, blog):
        is_my_blog = blog.user_id == request.user.id
        return self.render_to_response({'blog': blog, 'is_my_blog': is_my_blog})

    def get(self, request, *args, **kwargs):
        return self.send_blog(request, get_object_or_404(Blog, pk=kwargs['blog_id']))


class MyBlogView(BlogView):

    def get(self, request, *args, **kwargs):
        return self.send_blog(request, request.user.blog)


class BlogSubscribeView(TemplateView):

    def post(self, request, *args, **kwargs):
        subscribe_to_blog(request.user, kwargs['blog_id'])
        return redirect('blogs_other_users_blogs_url')


class BlogUnsubscribeView(TemplateView):

    def post(self, request, *args, **kwargs):
        unsubscribe_from_blog(request.user, kwargs['blog_id'])
        return redirect('blogs_other_users_blogs_url')


class BlogPostView(TemplateView):
    template_name = 'blog_post.html'

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_id'])

        # not good solution
        mark_post_read(request.user, kwargs['post_id'])

        return self.render_to_response({'post': post})

    def post(self, request, *args, **kwargs):
        form_with_data = PostForm(request.POST)

        if form_with_data.is_valid():
            request.user.blog.posts.create(title=request.POST['title'], text=request.POST['text'])
        else:
            raise ValidationError(form_with_data.errors)

        return redirect('blogs_my_blog_url')


class BlogPostReadView(TemplateView):
    def post(self, request, *args, **kwargs):
        mark_post_read(request.user, kwargs['post_id'])
        return redirect('blogs_feed_url')
