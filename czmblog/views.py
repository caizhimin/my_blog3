#coding:utf8
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from czmblog.models import Blog, Tag, Author, Comments, Feedback
from czmblog.form import CzmBlogForm, TagForm
import random
# Create your views here.


def index(request):
    """
    首页的一些显示功能
    :param request:
    :return:
    """
    tags = Tag.objects.all()
    for tag in tags:  # 计算每个tag对应的blogs数量并保存再 tag_count字段
        tag_count = tag.blog_set.count()
        tag.tag_count = tag_count
        tag.save()
    first_five_tags = tags[0:5]
    blogs = Blog.objects.all()
    latest_blogs_by_publish_date = blogs[0:5]
    # random_five_blogs = []
    # for i in xrange(5):
    #     random_five_blogs.append(random.choice(Blogs))
    #random_five_blogs = [random.choice(Blogs) for i in xrange(5)]
    random_five_blogs = blogs.order_by('?')[0:5]  # 随机生成5个blog,等同于上面的for循环和列表解析
    return render_to_response('index.html', {'last_blogs_by_publish_date': latest_blogs_by_publish_date,
                              'first_five_tags': first_five_tags, 'random_five_blogs': random_five_blogs})


def czm_blog_list(request):
    """
    返回blog全部列表及搜索blog功能
    :param request:
    :return:
    """
    czmblogs = Blog.objects.all()
    for czmblog in czmblogs:
        czmblog.blog_comment_count()  # 调用了类的实例方法计算blog的comment数
    czmblogs_order_by_comment_count = czmblogs.order_by('-comment_count')
    random_eight_czmblogs = czmblogs.order_by('?')[0:8]
    tags = Tag.objects.all()
    search_blogs = []
    search_result = False
    if request.GET.get('search', None):  # 如果能找到搜索内容，则执行下面
        search_content = request.GET.get('search', None)
        for czmblog in czmblogs:
            if search_content in czmblog.content:
                search_blogs.append(czmblog)
                search_result = True
        search_blogs_count = len(search_blogs)  # 计算出搜索到的blog数量
        print search_blogs_count
        return render_to_response('czm_blog_list.html',
                                  {'czmblogs': czmblogs,
                                   'czmblogs_order_by_comment_count': czmblogs_order_by_comment_count,
                                   'random_eight_czmblogs': random_eight_czmblogs,
                                   'search_blogs': search_blogs, 'search_result': search_result,
                                   'search_blogs_count': search_blogs_count, 'tags': tags})
    else:  # 未能找到搜索内容，则执行下面
        search_result = True
        return render_to_response('czm_blog_list.html',
                                  {'czmblogs': czmblogs,
                                   'czmblogs_order_by_comment_count': czmblogs_order_by_comment_count,
                                   'random_eight_czmblogs': random_eight_czmblogs,
                                   'search_result': search_result, 'tags': tags})


def czm_blog_show(request, blog_id):
    """
    显示单个blog
    :param request:
    :param blog_id:
    :return:
    """
    czmblogs = Blog.objects.all()
    for czmblog in czmblogs:
        czmblog.blog_comment_count()  # 调用了类的实例方法计算blog的comment数
    czmblogs_order_by_comment_count = czmblogs.order_by('-comment_count')
    random_eight_czmblogs = czmblogs.order_by('?')[0:8]
    tags = Tag.objects.all()
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist:
        raise Http404
    if blog.comments_set:
        comment_count = blog.comments_set.count()
        comments = blog.comments_set.all()
    if blog.tags.all():
        blog_tags = blog.tags.all()
    return render_to_response('czm_blog_show.html', {'blog': blog,
                                                     'comment_count': comment_count,
                                                     'czmblogs_order_by_comment_count': czmblogs_order_by_comment_count,
                                                     'random_eight_czmblogs': random_eight_czmblogs,
                                                     'comments': comments, 'blog_tags': blog_tags, 'tags': tags},
                              context_instance=RequestContext(request))


def filter_czm_blog_by_tag(request, tag_id):
    """
    根据一个tag来反向查询blogs
    :param request:
    :param tag_id:
    :return:
    """
    tags = Tag.objects.all()
    tag = Tag.objects.get(pk=tag_id)
    blogs = tag.blog_set.all()   # 通过tag反向查询对应的blogs
    czmblogs = Blog.objects.all()
    for czmblog in czmblogs:
        czmblog.blog_comment_count()  # 调用了类的实例方法计算blog的comment数
    czmblogs_order_by_comment_count = czmblogs.order_by('-comment_count')
    random_eight_czmblogs = czmblogs.order_by('?')[0:8]
    return render_to_response('czm_blog_filter_by_tag.html', {'blogs': blogs,
                                                              'czmblogs_order_by_comment_count':
                                                               czmblogs_order_by_comment_count,
                                                              'random_eight_czmblogs': random_eight_czmblogs,
                                                              'tags': tags})


def czm_blog_add(request):
    """
    1.当GET的时候，返回表单页面
    2.当POST的时候，清理数据，增加不存在的标签，将标签加入到blog中，重定向至最新增加的单个blog页面
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = CzmBlogForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data  # 清理POST过来的数据
            title = cd['title']
            content = cd['content']
            cdtag = tag.cleaned_data
            tag_name = cdtag['tag_name']
            for tag_list in tag_name.split():  # split方法将去除字符串中的空格并转化成列表, 'aaaa bbbb'=====>['aaaa','bbbb']
                Tag.objects.get_or_create(tag_name=tag_list.strip())  # 查找或者增加tag
            author = Author.objects.get(pk=1)
            blog = Blog(title=title, author_id=author.id, content=content)  # 默认设置了author为第一个author
            blog.save()
            for tag_list in tag_name.split():
                blog.tags.add(Tag.objects.get(tag_name=tag_list.strip()))  # 增加Blog的多个tag（多对多字段增加）
                blog.save()
            blog_id = Blog.objects.order_by('-publish_time')[0].id
            return HttpResponseRedirect('/czmblog/czm_blog/%s' % blog_id)
        else:
            return render_to_response('czm_blog_add.html', {'form': form, 'tag': tag},
                                      context_instance=RequestContext(request))  # 不增加context_instance会引发CSRF 403错误

    if request.method == 'GET':
        form = CzmBlogForm()  # 用于生成form表单
        tag = TagForm()
        return render_to_response('czm_blog_add.html', {'form': form, 'tag': tag},
                                  context_instance=RequestContext(request))


def czm_blog_update(request, blog_id):
    if request.method == 'GET':
        blog = Blog.objects.get(pk=blog_id)
        form = CzmBlogForm(initial={'title': blog.title, 'content': blog.content})
        tags = blog.tags.all()
        if tags:
            taginit = ''
            for i in tags:
                taginit += (str(i)+' ')
            tag = TagForm(initial={'tag_name': taginit})
        else:
            tag = TagForm()
        return render_to_response('czm_blog_add.html', {'form': form, 'tag': tag, 'czmblog.id': blog_id},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = CzmBlogForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            title = cd['title']
            content = cd['content']
            cdtag = tag.cleaned_data
            tag_name = cdtag['tag_name']
            unicode_tag_name_list = tag_name.split()  # todo split()后是一个unicode字符串的列表
            str_tag_name_list = []
            for i in unicode_tag_name_list:
                str_tag_name_list.append(i.encode('UTF-8'))  # 将unicode转换成UTF-8
            print str_tag_name_list
            # todo :不做个编码转化就无法正常删除,因为tag_name_list=[u'python', u'111', u'1']
            for tag_list in str_tag_name_list:
                Tag.objects.get_or_create(tag_name=tag_list.strip())
            blog = Blog.objects.get(pk=blog_id)
            if blog:
                blog.title = title
                blog.content = content
                blog.save()
                for tag_list in str_tag_name_list:
                    blog.tags.add(Tag.objects.get(tag_name=tag_list.strip()))
                    blog.save()
                tags = blog.tags.all()
                for tagname in tags:
                    if str(tagname) not in str_tag_name_list:  # 如果blog的当前标签不在表单提交的标签中，则删除当前标签
                        no_tag = blog.tags.get(tag_name=tagname)
                        blog.tags.remove(no_tag)
            else:
                blog = Blog(caption=blog.caption, content=blog.content)
                blog.save()
        else:
            return render_to_response('czm_blog_add.html', {'form': form, 'tag': tag},
                                      context_instance=RequestContext(request))
        return HttpResponseRedirect('/czmblog/czm_blog/%s' % blog_id)


def czm_blog_delete(request, blog_id):
    try:
       blog = Blog.objects.get(pk=blog_id)
    except Exception:
        raise Http404
    if blog:
        blog.delete()
        return HttpResponseRedirect('/czmblog/czm_blog_list')


def czm_blog_comment_add(request, blog_id):
    if request.method == 'POST':
        comment_name = request.POST.get('comment_name', None)
        comment_email = request.POST.get('comment_name', None)
        comment_website = request.POST.get('comment_website', None)
        comment = request.POST.get('comment', None)
        if request.META.get('HTTP_X_FORWARDED_FOR', None):  # 获取评论者的IP地址
            comment_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            comment_ip = request.META['REMOTE_ADDR']
        comment = Comments(author=comment_name, email=comment_email, website=comment_website, comment=comment,
                           ip_address=comment_ip, blog_id=blog_id)
        comment.save()
        blog = Blog.objects.get(pk=blog_id)
        blog.comments = comment
        blog.save()
        return HttpResponseRedirect('/czmblog/czm_blog/%s' % blog_id)


def czm_blog_contact(request):
    if request.method == 'POST':
        name = request.POST.get('feedback_name')
        email = request.POST.get('feedback_email')
        content = request.POST.get('feedback_content')
        if request.META.get('HTTP_X_FORWARDED_FOR', None):  # 获取评论者的IP地址
            feedback_ip_address = request.META['HTTP_X_FORWARDED_FOR']
        else:
            feedback_ip_address = request.META['REMOTE_ADDR']
        Feedback.objects.get_or_create(name=name, email=email, feedback_content=content, ip_address=feedback_ip_address)
        return HttpResponseRedirect('/czmblog/contact')
    return render_to_response('contact.html', context_instance=RequestContext(request))


def czm_blog_about(request):
    return render_to_response('about.html')