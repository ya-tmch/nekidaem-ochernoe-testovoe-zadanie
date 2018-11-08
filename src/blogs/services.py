from django.db.models import Exists, OuterRef

from .models import Blog, Post


def get_other_users_blogs(user):
    return Blog \
        .objects \
        .exclude(user=user) \
        .annotate(subscribed=Exists(user.subscriptions.filter(blog=OuterRef('id'))))


def get_user_feed_posts(user):
    return Post \
        .objects \
        .filter(blog__in=user.subscriptions.values('blog_id')) \
        .annotate(read=Exists(user.read_posts.filter(post=OuterRef('id')))) \
        .order_by('-create_datetime')


def subscribe_to_blog(user, blog_id):
    if user.subscriptions.filter(blog_id=blog_id).count() == 0:
        user.subscriptions.create(blog=Blog.objects.get(pk=blog_id))


def unsubscribe_from_blog(user, blog_id):
    user.subscriptions.filter(blog=blog_id).delete()
    user.read_posts.filter().delete()


def mark_post_read(user, post_id):
    if user.read_posts.filter(post_id=post_id).count() == 0:
        user.read_posts.create(post_id=post_id)
