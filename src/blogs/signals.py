import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

import logging

from django.urls import reverse
from .models import Post, Blog


@receiver(post_migrate)
def post_migrate_handler(sender, instance=None, created=False, **kwargs):
    User = get_user_model()

    if User.objects.filter(username='admin').count() == 0:
        print('run post_migrate_handler')

        User.objects.create_superuser(username='admin', password='admin', email='')

        admin = User(username='user1', email='user1@mail.ru')
        admin.set_password('user1')
        admin.save()

        some_user = User(username='user2', email='user2@mail.ru')
        some_user.set_password('user2')
        some_user.save()

        admin.subscriptions.create(blog=some_user.blog)


@receiver(post_save, sender=get_user_model())
def create_personal_blog_handler(sender, instance=None, created=False, **kwargs):
    if created:
        print('run create_personal_blog_handler')

        blog = Blog.objects.create(user=instance)

        Post \
            .objects \
            .create(blog=blog, title=instance.username + ' автоматический пост', text='') \
            .save()


@receiver(post_save, sender=Post)
def create_blog_post_handler(sender, instance=None, created=False, **kwargs):
    if created:

        url = os.environ.get('APP_URL') + reverse('blogs_post_url', kwargs={'post_id': instance.id})

        for subscription in instance.blog.subscriptions.all():
            if subscription.user.email:
                # need use async queue
                logging.error('sent to {} url {}'.format(subscription.user.email, url))
