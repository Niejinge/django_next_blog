from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(verbose_name="文章类别", max_length=20)
    number = models.IntegerField(verbose_name="分类数目", default=0)

    class Meta:
        verbose_name = "文章类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name="文章标签", max_length=20)
    number = models.IntegerField(verbose_name="标签数目", default=0)

    class Meta:
        verbose_name = "博客标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(verbose_name="文章标题", max_length=100)
    content = models.TextField(verbose_name="正文", default="")
    create_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    modify_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    click_nums = models.IntegerField(verbose_name="点击量", default=0)
    category = models.ForeignKey(Category, verbose_name="文章类别", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name="文章标签")

    class Meta:
        verbose_name = "我的文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Counts(models.Model):
    blog_nums = models.IntegerField(verbose_name="博客数目", default=0)
    category_nums = models.IntegerField(verbose_name="分类数目", default=0)
    tag_nums = models.IntegerField(verbose_name="标签数目", default=0)
    visit_nums = models.IntegerField(verbose_name="网站访问量", default=0)

    class Meta:
        verbose_name = "统计数目"
        verbose_name_plural = verbose_name


