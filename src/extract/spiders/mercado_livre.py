import scrapy


class MercadoLivreSpider(scrapy.Spider):
    name = "mercado_livre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    current_page = 1
    max_page = 10
    
    def __init__(self, *args, **kwargs):
        super(MercadoLivreSpider, self).__init__(*args, **kwargs)
        self.feed_uri = kwargs.get('feed_uri')

    def parse(self, response):
        products = response.css('div.ui-search-result__content')
        next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
        prices = products.css('span.andes-money-amount__fraction::text').getall()
        cents = products.css('span.andes-money-amount__cents::text').getall()
        
        for product in products:
            yield{
                'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                'name': product.css('h2.ui-search-item__title::text').get(),
                'old_price': prices[0] if len(prices) > 0 else None,
                'old_price_cents': cents[0] if len(cents) > 0 else None,
                'new_price': prices[1] if len(prices) > 0 else None,
                'new_price_cents': cents[1] if len(cents) > 0 else None,
                'rating_number': products.css('span.ui-search-reviews__rating-number::text').get(),
                'reviews_amount': products.css('span.ui-search-reviews__amount::text').get()

            }
        if self.current_page < self.max_page:
            if next_page:
                self.current_page += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
