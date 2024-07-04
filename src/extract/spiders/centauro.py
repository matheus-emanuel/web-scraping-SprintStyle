import scrapy


class CentauroSpider(scrapy.Spider):
    name = "centauro"
    allowed_domains = ["www.centauro.com.br"]
    start_urls = ["https://www.centauro.com.br/nav/categorias/calcados/produto/tenis/genero/masculino"]
    next_page = 2
    max_page = 3
    
    def __init__(self, *args, **kwargs):
        super(CentauroSpider, self).__init__(*args, **kwargs)
        self.feed_uri = kwargs.get('feed_uri')

    def parse(self, response):
        products = response.css('a.ProductCard-styled__Card-sc-97c94e5e-0.gpfLHL')
        next_page = (f'https://www.centauro.com.br/nav/categorias/calcados/produto/tenis/genero/masculino?page={self.next_page}')
        # brand_list = brand = response.css('dd.Accordionstyled__SectionContent-sc-b3g7jv-4[id^="Marca"]')

        for product in products:
            yield{
                'nome': product.css('p.Typographystyled__Paragraph-sc-bdxvrr-1.knvuZc.ProductCard-styled__Title-sc-97c94e5e-3.hzAjfq::text').get(),
                # 'brand': get_brand(nome, brand_list)
                'new_price': product.css('p.Typographystyled__Paragraph-sc-bdxvrr-1.eFDcLB.Price-styled__CurrentPrice-sc-e083f0ed-4.etKnUk::text').get(),
                'old_price': product.css('del.Typographystyled__Offer-sc-bdxvrr-4.cAyLkZ.Price-styled__OldPriceOffer-sc-e083f0ed-2.gaskFI::text').get()
            }

        if self.next_page < self.max_page:
            if next_page:
                self.next_page += 1
                yield scrapy.Request(url=next_page, callback=self.parse)


