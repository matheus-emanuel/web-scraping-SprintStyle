from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

def run_spider(spider_name, output_file):
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', output_file)
    process = CrawlerProcess(settings)
    process.crawl(spider_name)
    process.start()
    

if __name__ == "__main__":
    spiders = {
        "mercado_livre": "../../data/data_mercado_livre.json",
        "centauro": "../../data/data_centauro.json",
        "netshoes": "../../data/data_netshoes.json",
    }
  
    processes = []

    for spider, output in spiders.items():
        p = Process(target=run_spider, args=(spider, output))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
