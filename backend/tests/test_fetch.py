from app.core.sources import CBSL
from app.ingestion.crawler.static_crawler import StaticCrawler

crawler = StaticCrawler(CBSL)

html = crawler.fetch()

links = crawler.get_links(html)

print(html[:500])
print(links)