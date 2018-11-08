from django.contrib.auth import get_user_model
from django.db import models


class Blog(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='blog')


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_datetime = models.DateTimeField(auto_now_add=True)


class UserSubscription(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='subscriptions')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        unique_together = ('user', 'blog')


class UserReadPosts(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='read_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')
