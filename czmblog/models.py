#coding:utf8
from django.db import models

# Create your models here.


class Tag(models.Model):
    """Tags"""
    tag_name = models.CharField(max_length=20, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    tag_count = models.IntegerField()  # 增加tag_count字段是为了方便在首页进行分类排行的排序

    def __unicode__(self):
        return self.tag_name

    class Meta:
        ordering = ['-tag_count']


class Author(models.Model):
    """Author"""
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return self.name

    # def __unicode__(self):
    #     return u'%s' % self.name  #TODO check the diff


class Blog(models.Model):
    """Blog"""
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    tags = models.ManyToManyField(Tag, blank=True)
    content = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    comment_count = models.IntegerField()  # 增加comment_count字段是为了方便在首页进行按照评论数量的排序

    def __unicode__(self):
        return u'%s %s %s' % (self.title, self.author, self.publish_time)

    def blog_comment_count(self):
        """
        计算每个blog有多少个comment
        :return:
        """
        comment_count = self.comments_set.count()
        self.comment_count = comment_count
        self.save()

    class Meta:
        ordering = ['-publish_time']


class Comments(models.Model):
    """Comments"""
    author = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    comment = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField()
    blog = models.ForeignKey(Blog)


class Feedback(models.Model):
    """
    feedback
    """
    name = models.CharField(max_length=20)
    email = models.EmailField()
    feedback_content = models.TextField()
    ip_address = models.IPAddressField()
