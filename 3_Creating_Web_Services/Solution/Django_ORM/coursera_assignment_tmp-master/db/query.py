# query.py

from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC

from db.models import User, Blog, Topic


def create():
    u1 = User.objects.create(first_name='u1', last_name='u1')
    u2 = User.objects.create(first_name='u2', last_name='u2')
    u3 = User.objects.create(first_name='u3', last_name='u3')

    b1 = Blog.objects.create(title='blog1', author=u1)
    b2 = Blog.objects.create(title='blog2', author=u1)

    b1.subscribers.add(u1, u2)
    b2.subscribers.add(u2)

    t1 = Topic.objects.create(title='topic1', blog=b1, author=u1)
    t2 = Topic.objects.create(
        title='topic2_content', blog=b1, author=u3,
        created=datetime(year=2017, month=1, day=1, tzinfo=UTC)
    )

    t1.likes.add(u1, u2, u3)


def edit_all():
    User.objects.all().update(first_name='uu1')


def edit_u1_u2():
    User.objects.filter(
        Q(first_name='u1') | Q(first_name='u2')
    ).update(first_name='uu1')


def delete_u1():
    User.objects.filter(first_name='u1').delete()


def unsubscribe_u2_from_blogs():
    Blog.subscribers.through.objects.filter(user__first_name='u2').delete()


def get_topic_created_grated():
    return Topic.objects.filter(created__gt=datetime(year=2018, month=1, day=1,
                                                     tzinfo=UTC))


def get_topic_title_ended():
    return Topic.objects.filter(title__endswith='content')


def get_user_with_limit():
    return User.objects.all().order_by('-id')[:2]


def get_topic_count():
    return Blog.objects.annotate(
        topic_count=Count('topic')).order_by('topic_count')


def get_avg_topic_count():
    return Blog.objects.annotate(topic_count=Count('topic')).aggregate(
        avg=Avg('topic_count')
    )


def get_blog_that_have_more_than_one_topic():
    return Blog.objects.annotate(
        topic_count=Count('topic')).filter(topic_count__gt=1)


def get_topic_by_u1():
    return Topic.objects.filter(author__first_name='u1')


def get_user_that_dont_have_blog():
    return User.objects.filter(blog__isnull=True).order_by('pk')


def get_topic_that_like_all_users():
    count = User.objects.count()
    return Topic.objects.annotate(like=Count('likes')).filter(like=count)


def get_topic_that_dont_have_like():
    return Topic.objects.filter(likes__isnull=True)
