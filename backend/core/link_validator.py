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
    "36kr.com",
    "www.36kr.com",
    "huxiu.com",
    "www.huxiu.com",
}


def _host_matches_allowed(host: str, allowed: str) -> bool:
    host = host.lower()
    allowed = allowed.lower()
    return host == allowed or host.endswith(f".{allowed}")


def is_allowed_url(url: str) -> bool:
    try:
        host = urlparse(url).hostname
    except Exception:
        return False
    if not host:
        return False
    host = host.lower()
    return any(_host_matches_allowed(host, allowed) for allowed in ALLOWED_HOSTS)
