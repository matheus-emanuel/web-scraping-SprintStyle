import scrapy


class NetshoesSpider(scrapy.Spider):
    name = "netshoes"
    allowed_domains = ["www.netshoes.com.br"]
    start_urls = ["https://www.netshoes.com.br/tenis-performance/masculino"]

    def get_attributes(self, response):
        # old_price = response.css('span.listInCents-value::text').get()
        # new_price = response.css('span.saleInCents-value::text').get()
        # rating_number = response.css('div.link__average::text').get()
        # reviews_amount = response.css('p.link__infos--number-of-reviews::text').get()
        pass

    def parse(self, response):
        products = response.css('div.product-list__items.double-columns')

        for product in products:
            partial_link = product.css('a.card__link::attr(href)').get()
            yield{
                'brand': product.css('a.card__link::attr(data-brand)').get(),
                'name': product.css('a.card__link::attr(data-name)').get()
            }
        
