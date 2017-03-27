# sina-blog-spider

## python 新浪博客归档工具

- 用于下载并归档指定新浪博客作者全部文章的 Python 脚本；
- 抓取后整理生成本地 html 文件，以及一个 indxe 入口；
- 支持到 Python3.x

## Usage:

```python
# 排序开关是可选的，默认为按发表时间顺序排列（即 asc）
$ sina_blog_crawler.py http://blog.sina.com.cn/gongmin desc
$ sina_blog_crawler.py http://blog.sina.com.cn/u/1239657051
```

## 参考：
[bfishadow/SBB](https://github.com/bfishadow/SBB)

- 对 SBB 代码适配 Python3.x
- 进行了封装、重构，添加了踩坑注释
- SBB 作者原来不是程序员啊我摔，被坑了（代码实在太烂了，差点摧毁我对 Python 的认知）
- 吐槽归吐槽，原 po 思路还是非常赞的；
- 鸣谢 @bfishadow

## TODO:
* [ ] 添加可选参数：指定抓取页数支持
* [ ] 网络库从 urllib 替换为 requests
* [ ] 字符串匹配改用正则


