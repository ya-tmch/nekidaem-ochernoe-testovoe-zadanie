from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import RedirectView

from .views import *

# HTML form allow only POST and GET methods
urlpatterns = [

    path('feed', login_required(FeedView.as_view()), name='blogs_feed_url'),

    path('blogs/', include([

        path('', login_required(OtherUsersBlogsView.as_view()), name='blogs_other_users_blogs_url'),

        path('my', login_required(MyBlogView.as_view()), name='blogs_my_blog_url'),

        path('<int:blog_id>', login_required(BlogView.as_view()), name='blogs_blog_url'),

        # path('<int:blog_id>/post', login_required(BlogPostView.as_view()), name='blogs_blog_post_create_url'),

        path('<int:blog_id>/subscribe', login_required(BlogSubscribeView.as_view()), name='blogs_blog_subscript_url'),

        path('<int:blog_id>/unsubscribe', login_required(BlogUnsubscribeView.as_view()),
             name='blogs_blog_unsubscribe_url'),
    ])),

    path('post/', include([

        path('', login_required(BlogPostView.as_view()), name='blogs_post_create_url'),

        path('<int:post_id>', login_required(BlogPostView.as_view()), name='blogs_post_url'),

        path('<int:post_id>/read', login_required(BlogPostReadView.as_view()), name='blogs_post_read_url'),
    ])),

    path('', RedirectView.as_view(pattern_name='blogs_feed_url'))
]
