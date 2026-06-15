from core.collectors.github_trending import GitHubTrendingCollector

SAMPLE_HTML = """
<html><body>
<article class="Box-row">
  <h2 class="h3 lh-condensed">
    <a href="/anthropics/claude-code">anthropics / claude-code</a>
  </h2>
  <span itemprop="programmingLanguage">TypeScript</span>
  <a class="Link Link--muted Link--secondary d-inline-block" href="/anthropics/claude-code/stargazers">
    <svg class="octicon-star"></svg>
    12,345
  </a>
</article>
</body></html>
"""


def test_parse_trending_html() -> None:
    collector = GitHubTrendingCollector(since="daily")
    tree_items = []
    from selectolax.parser import HTMLParser

    tree = HTMLParser(SAMPLE_HTML)
    for rank, article in enumerate(tree.css("article.Box-row"), start=1):
        item = collector._parse_repo(article, rank)
        if item:
            tree_items.append(item)

    assert len(tree_items) == 1
    assert tree_items[0].title == "anthropics / claude-code"
    assert tree_items[0].url == "https://github.com/anthropics/claude-code"
    assert tree_items[0].metrics.get("stars") == 12345
    assert tree_items[0].metrics.get("language") == "TypeScript"
