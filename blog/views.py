import markdown
from django.shortcuts import render, get_object_or_404
from django.views import View
from pure_pagination import PageNotAnInteger, Paginator
from django.utils.html import strip_tags

from .models import Blog, Counts, Category, Tag


def wordcounts():
    all_counts = 0
    blogs = Blog.objects.all()
    for blog in blogs:
        all_counts += len(blog.content)
    return '%.1f' % (all_counts / 1000)


all_counts = wordcounts()


class IndexView(View):

    def get(self, request):
        all_blog = Blog.objects.all().order_by('-id')
        count_nums = Counts.objects.get(id=1)
        count_nums.visit_nums += 1
        count_nums.save()
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        visit_nums = count_nums.visit_nums

        for blog in all_blog:

            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            blog.content = strip_tags(md.convert(blog.content))[:160]

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blog, 6, request=request)
        all_blog = p.page(page)

        return render(request, 'index.html', {
            'all_blog': all_blog,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,
            'visit_nums': visit_nums,
            'all_counts': all_counts,
        })


class ArichiveView(View):

    def get(self, request):
        all_blog = Blog.objects.all().order_by('-create_time')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        visit_nums = count_nums.visit_nums
        p = Paginator(all_blog, 6, request=request)
        all_blog = p.page(page)

        return render(request, 'archive.html', {
            'all_blog': all_blog,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,
            'visit_nums': visit_nums,
            'all_counts': all_counts,
        })


class TagView(View):
    def get(self, request):
        all_tag = Tag.objects.all()
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        visit_nums = count_nums.visit_nums
        return render(request, 'tags.html', {
            'all_tag': all_tag,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,
            'visit_nums': visit_nums,
            'all_counts': all_counts,
        })


class TagDetailView(View):
    def get(self, request, tag_name):
        tag = get_object_or_404(Tag, name=tag_name)
        # tag = Tag.objects.filter(name=tag_name).first()
        tag_blogs = tag.blog_set.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        visit_nums = count_nums.visit_nums
        p = Paginator(tag_blogs, 6, request=request)
        tag_blogs = p.page(page)
        return render(request, 'tag-detail.html', {
            'tag_blogs': tag_blogs,
            'tag_name': tag_name,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,
            'visit_nums': visit_nums,
            'all_counts': all_counts,
        })


class CategoryDetailView(View):
    def get(self, request, category_name):
        # category = Category.objects.filter(name=category_name).first()
        category = get_object_or_404(Category, name=category_name)
        category_blogs = category.blog_set.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        visit_nums = count_nums.visit_nums
        p = Paginator(category_blogs, 5, request=request)
        category_blogs = p.page(page)
        return render(request, 'category-detail.html', {
            'category_blogs': category_blogs,
            'category_name': category_name,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,
            'visit_nums': visit_nums,
            'all_counts': all_counts,
        })


class BlogDetailView(View):

    def get(self, request, blog_id):

        # blog = Blog.objects.get(id=blog_id)
        blog = get_object_or_404(Blog, pk=blog_id)
        blog.click_nums += 1
        blog.save()
        md = markdown.Markdown(extensions=[
             'markdown.extensions.extra',
             'markdown.extensions.codehilite',
             'markdown.extensions.toc',
         ])

        blog.content = md.convert(blog.content)
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        visit_nums = count_nums.visit_nums

        has_prev = False
        has_next = False
        blog_prev = blog_next = None
        id_prev = id_next = int(blog_id)
        blog_id_max = Blog.objects.all().order_by('-id').first()
        id_max = blog_id_max.id
        while not has_prev and id_prev >= 1:
            blog_prev = Blog.objects.filter(id=id_prev - 1).first()
            if not blog_prev:
                id_prev -= 1
            else:
                has_prev = True

        while not has_next and id_next < id_max:
            blog_next = Blog.objects.filter(id=id_next + 1).first()
            if not blog_next:
                id_next += 1
            else:
                has_next = True

        return render(request, 'blog.html', {
            'blog': blog,
            'blog_prev': blog_prev,
            'blog_next': blog_next,
            'has_prev': has_prev,
            'has_next': has_next,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,
            'visit_nums': visit_nums,
            'all_counts': all_counts,
            'toc': md.toc,
        })


def page_not_found(request):
    return render(request, '404.html')


def page_errors(request):
    return render(request, '500.html')
