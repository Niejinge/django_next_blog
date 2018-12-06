from django.contrib.syndication.views import Feed
from django.urls import reverse
from blog.models import Blog


class BlogRssFeed(Feed):

    title = "镍铬合金的博客小站"
    link = '/rss/'

    def items(self):
        return Blog.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('blog', args=[item.id, ])

