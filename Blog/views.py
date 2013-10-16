#coding=utf-8
from django.shortcuts import render_to_response
from Blog.models import Article,Category,OpenProject,FriendUrl
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
import urllib


class Sider():#侧栏
    def __init__(self):
        Category = None
        OpenProject = None
        HotArticle = None
        FriendUrl = None


def GetCategory():#分类
    category = Category.objects.all()
    return category

def GetOpenProject():#开源项目
    openproject = OpenProject.objects.all()
    return openproject

def GetHotArticle():#热门文章
    hotarticle = Article.objects.all().order_by('-num')
    num = 0
    h = hotarticle[:]
    hotarticle = []
    for i in h:
        hotarticle.append(i)
        num+=1
        if num==10:
            break
    return hotarticle

def GetFriendUrl():#友情链接
    friendurl = FriendUrl.objects.all()
    return friendurl

def GetSider():#获取侧栏
    sider = Sider()
    sider.Category = GetCategory()
    sider.OpenProject = GetOpenProject()
    sider.HotAtrile = GetHotArticle()
    sider.FriendUrl = GetFriendUrl()
    return sider


def Categorylist(request,category):#分类文章列表
    category = urllib.unquote(str(category))
    num = request.GET.get('page')
    if num:
        num = int(num)
    else:
        num=1
    article=Article.objects.filter(category__name=category).order_by('-id')
    p = Paginator(article, 5)
    page = p.page(num)
    if num == p.num_pages:
        pnum = None
    else:
        pnum = num+1
    sider = GetSider()
    return render_to_response('index.html',{'Page':page,'Pnum':pnum,'Sider':sider})



def Index(request):#主页
    num = request.GET.get('page')
    if num:
        num = int(num)
    else:
        num=1
    article=Article.objects.all().order_by("-id")#安时间从近到远输出
    p = Paginator(article, 5)
    page = p.page(num)
    if num == p.num_pages:
        pnum = None
    else:
        pnum = num+1
    sider = GetSider()
    return render_to_response('index.html',{'Page':page,'Pnum':pnum,'Sider':sider})


def Page(request,url):#文章页面
    url = urllib.unquote(str(url))#url中
    if url:
        try:
            article = Article.objects.get(url = url)
            Article.objects.filter(url=url).update(num=article.num+1)
            sider = GetSider()
            return render_to_response('article.html',{'page':article,'Sider':sider})
        except:
            return HttpResponseRedirect('/')
    else:
       return HttpResponseRedirect('/')


def Search(request):#文章搜索
    key = request.GET.get('keywords')
    a = Article.objects.all().order_by('-id')
    page = []
    for p in a:
        if key in p.content:
            page.append(p)
    sider = GetSider()
    return render_to_response('index.html',{'Page':page,'Sider':sider})

def article_out(request):#定时将文章保存到百度云存储中
    from bae.api import bcs
    AK = '' #AK
    SK = ''     #SK
    bname = 'blog-article'
    bcs2 = bcs.BaeBCS('http://bcs.duapp.com/', AK, SK)
    a = Article.objects.all()
    for i in a:
        ob = str(i.url+'.md')
        o = '/'+ob
        e, d = bcs2.put_object(bname, o,str(i.content))
        bcs2.make_public(bname,o)
    return HttpResponse("Success!")
