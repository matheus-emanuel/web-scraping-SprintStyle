import scrapy


class NetshoesSpider(scrapy.Spider):
    name = "netshoes"
    allowed_domains = ["www.netshoes.com.br"]
    start_urls = ["https://www.netshoes.com.br/tenis-performance/masculino"]

    def __init__(self, *args, **kwargs):
        super(NetshoesSpider, self).__init__(*args, **kwargs)
        self.feed_uri = kwargs.get('feed_uri')

    def get_attributes(self, response, brand, name):
        """
        Essa função foi criada pois existem informações que não são carregadas diretamente na página do produto
        então é necessário acessar produto por produto para extrair as informações de preço e avaliação
        """

        yield dict (
            old_price = response.css('span.listInCents-value::text').get(),
            new_price = response.css('span.saleInCents-value::text').get(),
            rating_number = response.css('div.link__average::text').get(),
            reviews_amount = response.css('p.link__infos--number-of-reviews::text').get(),
            brand = brand,
            name = name
        )

    def parse(self, response):
        products = response.css('div.card.double-columns.full-image')

        for product in products:
            url = f'https://www.netshoes.com.br{product.css('a.card__link::attr(href)').get()}'
            if url:
                self.log(f"URL: {url}")

                request = scrapy.Request(url=url, callback=self.get_attributes)
                request.cb_kwargs['brand'] = product.css('a.card__link::attr(data-brand)').get()
                request.cb_kwargs['name'] =  product.css('a.card__link::attr(data-name)').get()

                yield request

            else:
                self.log(f"Missing data: url={url}")

        
