from django.urls import path

from .views import IndexView, BlogDetailView, ArichiveView, TagView, TagDetailView, CategoryDetailView
from .feeds import BlogRssFeed

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('archive/', ArichiveView.as_view(), name='archive'),
    path('tags/', TagView.as_view(), name='tags'),
    path('tags/<slug:tag_name>/', TagDetailView.as_view(), name='tag_name'),
    path('categorys/<slug:category_name>/', CategoryDetailView.as_view(), name='category_name'),
    path('blog/<int:blog_id>/', BlogDetailView.as_view(),  name='blog'),
    path('rss/', BlogRssFeed(), name='rss'),
]

