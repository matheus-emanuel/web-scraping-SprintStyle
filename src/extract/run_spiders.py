from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spider(spider_name, output_file):
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', output_file)
    process = CrawlerProcess(settings)
    process.crawl(spider_name)
    process.start()

if __name__ == "__main__":
    spiders = {
        "mercado_livre": "../data/data_mercado_livre.json",
        # "americanas": "../data/data_americanas.json",
        # "amazon": "../data/data_amazon.json",
    }

    for spider, output in spiders.items():
        run_spider(spider, output)
