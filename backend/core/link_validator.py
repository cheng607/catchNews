from urllib.parse import urlparse

ALLOWED_HOSTS = {
    "weibo.com",
    "s.weibo.com",
    "top.baidu.com",
    "www.baidu.com",
    "zhihu.com",
    "www.zhihu.com",
    "github.com",
    "www.github.com",
    "news.ycombinator.com",
    "producthunt.com",
    "bilibili.com",
    "www.bilibili.com",
}


def is_allowed_url(url: str) -> bool:
    try:
        host = urlparse(url).hostname
    except Exception:
        return False
    if not host:
        return False
    host = host.lower()
    return host in ALLOWED_HOSTS or any(host.endswith(f".{h}") for h in ALLOWED_HOSTS if "." not in h)
