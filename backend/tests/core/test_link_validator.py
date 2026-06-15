from core.link_validator import is_allowed_url


def test_allowed_github_url() -> None:
    assert is_allowed_url("https://github.com/anthropics/claude-code") is True


def test_allowed_weibo_url() -> None:
    assert is_allowed_url("https://s.weibo.com/weibo?q=test") is True


def test_allowed_subdomain_github() -> None:
    assert is_allowed_url("https://api.github.com/repos/octocat/Hello-World") is True


def test_allowed_news_hosts() -> None:
    assert is_allowed_url("https://36kr.com/p/123") is True
    assert is_allowed_url("https://www.huxiu.com/article/123") is True


def test_rejected_unknown_host() -> None:
    assert is_allowed_url("https://evil.com/phishing") is False


def test_rejected_empty_url() -> None:
    assert is_allowed_url("") is False
