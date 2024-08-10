from django.db.models import Count
from django.utils import timezone as tz

from .models import Post


def get_posts_queryset(
        manager=Post.objects,
        is_filtered=True,
        is_annotated=True,
):
    queryset = manager.select_related(
        'author',
        'category',
        'location',
    )
    if is_filtered:
        queryset = queryset.filter(
            pub_date__lt=tz.now(),
            is_published=True,
            category__is_published=True
        )
    if is_annotated:
        queryset = queryset.annotate(comment_count=Count('comments')
                                     ).order_by('-pub_date')

    return queryset
