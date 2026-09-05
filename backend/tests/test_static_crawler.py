from app.ingestion.crawler.static_crawler import StaticCrawler

crawler = StaticCrawler(
    "https://www.cbsl.gov.lk"
)

links = crawler.get_links()

print(f"\nFound {len(links)} links\n")

for link in links[:20]:
    print(link)