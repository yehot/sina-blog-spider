#!/urs/bin/env python
# -*_ coding: utf-8 -*-

import sys
import urllib.request
import codecs
import os
from time import strftime


def get_between(str0, str1, str2):
    start = str0.find(str1)+len(str1)
    end = str0.find(str2)
    return str0[start:end]

k_usage_tip = '''need input your url!
Usage:
    $ SBB.py <Sina blog URL> [asc]
Example:
    $ SBB.py http://blog.sina.com.cn/gongmin desc
    $ SBB.py http://blog.sina.com.cn/u/1239657051'''

# # 第一个参数
try:
    urlInput = sys.argv[1]
except Exception as e:
    print(k_usage_tip)
    print(e)
    sys.exit(0)

k_sina_domain = "http://blog.sina.com.cn/"
k_sina_article_url = k_sina_domain + "s/articlelist_"
k_sina_blog_url = k_sina_domain + "s/blog_"

if urlInput.find(k_sina_domain) == -1 or len(urlInput) <= 24:
    print(k_usage_tip)
    sys.exit(0)

# 第二个参数
# try except 用法 [https://segmentfault.com/a/1190000007736783]
try:
    orderInput = sys.argv[2]
except:
    orderInput = ""
    print("默认升序排列")


# 在python3.3里面，用urllib.request代替urllib2
# python2.7 中，使用 urllib2.urlopen(strUserInput) 获得的是 string
# 在 3.5 中使用，得到的是 bit,需要 decode
def get_html_body(url):
    response = urllib.request.urlopen(url)
    text = response.read()
    text = text.decode(encoding='utf-8', errors='ignore')
    response.close()
    return text


htmlText = get_html_body(urlInput)

# Get UID for the blog, UID is critical.
htmlBody = get_between(htmlText, "format=html5;", "format=wml;")
strUID = get_between(htmlBody, "/blog/u/", '">')

if len(strUID) > 10:
    print(k_usage_tip)
    sys.exit(0)

# Step 1: get list for first page and article count
htmlText = get_html_body(k_sina_article_url + strUID + "_0_1.html")

# 文章编号列表
strSortDOM = "$blogArticleSortArticleids"
srtCategoryDom = "$blogArticleCategoryids"
strList = get_between(htmlText, strSortDOM, srtCategoryDom)
srtBlogPostList = get_between(strList, " : [", "],")


def get_blog_count(text):
    strContent = get_between(text, "全部博文", "<!--第一列end-->")
    # 获取页数
    count = get_between(strContent, "<em>(", ")</em>")
    return int(count)

# 文章总数
blog_amount = get_blog_count(htmlText)
# 总页数 （默认每页 50 篇）
blog_page_amount = int(blog_amount / 50) + 1

strTitle = get_between(htmlText, "<title>", "</title>")
strBlogName = get_between(strTitle, "博文_", "_新浪博客")

# Step 2: get list for the rest of pages
for intPage in range(blog_page_amount - 1):
    strURL = k_sina_article_url + strUID + "_0_" + str(intPage + 2) + ".html"
    htmlText = get_html_body(strURL)
    strPost = get_between(htmlText, strSortDOM, srtCategoryDom)
    strPostList = get_between(strPost, " : [", "],")
    srtBlogPostList = srtBlogPostList + "," + strPostList

# strPostID <- this string has all article IDs for current blog
strPostID = srtBlogPostList.replace('"', '')

# Step 3: get all articles one by one
arrBlogPost = strPostID.split(',')
if orderInput != "desc":
    arrBlogPost.reverse()

kBlogDir = "sinaBlogs"
# python 3.2创建目录新增了可选参数existok
# 把 exist_ok 设置True，创建目录如果已经存在则不会往外抛出异常
os.makedirs(kBlogDir, exist_ok=True)


def ge_artile_title(page_code, name):
    title = get_between(page_code, "<title>", "</title>")
    title = title.replace("_新浪博客", "")
    title = title.replace("_" + name, "")
    return title


def get_artile_body(text):
    body = get_between(text, "<!-- 正文开始 -->", "<!-- 正文结束 -->")
    body = body.replace("http://simg.sinajs.cn/blog7style/images/common/sg_trans.gif", "")
    body = body.replace('src=""', "")
    body = body.replace("real_src =", "src =")
    return body


def get_artile_time(text):
    dom1 = '<span class="time SG_txtc">('
    dom2 = ')</span><div class="turnBoxzz">'
    return get_between(text, dom1, dom2)


# 3.x 中直接使用 open 会得到 <_io.TextIOWrapper name='' mode='' encoding='US-ASCII'> 对象
# 导致 write str 时，报错UnicodeEncodeError: 'ascii' codec can't encode characters in position
# 改用  codecs.open
def write_file(file_path, content):
    objFileIndex = codecs.open(file_path, "w", 'utf-8')
    objFileIndex.write(content)
    objFileIndex.close


intCounter = 0
# index.html 中的内容
strHTML4Index = ""

for strPostID in arrBlogPost:
    intCounter += 1

    htmlText = get_html_body(k_sina_blog_url + strPostID + '.html')
    # Parse blog title
    strTitle = ge_artile_title(htmlText, strBlogName)
    # Parse blog post
    strBody = get_artile_body(htmlText)
    # Parse blog timestamp
    strTime = get_artile_time(htmlText)

    # Write into local file
    strFileName = "Post_" + str(intCounter) + "_" + strPostID + ".html"
    # %s 的 format 字符串是 是 2.x 写法, 3.x 使用 str.format()
    # 参考[http://blog.xiayf.cn/2013/01/26/python-string-format/]
    strHTML4Post = '''
        <html>
            <head>
                <meta http-equiv=""Content-Type"" content=""text/html; charset=utf-8"" />
                <title>{strTitle}</title>
                <link href=""http://simg.sinajs.cn/blog7style/css/conf/blog/article.css""
                      type=""text/css"" rel=""stylesheet"" />
            </head>
            <body>
                <h2>{strTitle}</h2>
                <p>By: <em>{strBlogName}</em> 原文发布于：<em>{strTime}</em></p>
                    {strBody}
                <p><a href="index.html">返回目录</a></p>
            </body>
        </html>'''
    strHTML4Post = strHTML4Post.format(strTitle=strTitle, strBlogName=strBlogName, strTime=strTime, strBody=strBody)

    write_file(kBlogDir + '/' + strFileName, strHTML4Post)

    strHTML4Index = strHTML4Index + '<li><a href="' + strFileName + '">' + strTitle + '</a></li>\n'
    print(intCounter, "/", blog_amount)

strTimestamp = str(strftime("%Y-%m-%d %H:%M:%S"))
strHTMLBody = '''
    <html>
        <head>
            <meta http-equiv=""Content-Type"" content=""text/html; charset=utf-8"" />
            <title>{name} 博客文章汇总</title>
        </head>
        <body>
            <h2>新浪博客：{name}</h2>
            <p>共 {page} 篇文章，最后更新：<em>{time}</em></p>
            <ol>{index}</ol>
            </body>
        </html>'''
strHTML4Index = strHTMLBody.format(name=strBlogName, page=str(blog_amount), index=strHTML4Index, time=strTimestamp)
write_file(kBlogDir + "/index.html", strHTML4Index)
