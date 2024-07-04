import scrapy
import re


class CentauroSpider(scrapy.Spider):
    name = "centauro"
    allowed_domains = ["www.centauro.com.br"]
    start_urls = ["https://www.centauro.com.br/nav/categorias/calcados/produto/tenis/genero/masculino"]
    next_page = 2
    max_page = 10
    
    def __init__(self, *args, **kwargs):
        super(CentauroSpider, self).__init__(*args, **kwargs)
        self.feed_uri = kwargs.get('feed_uri')

    def get_brand(self, brand_list: list, item_name: str):
        """
        Função utilizada para extrair do nome do produto a marca.

        Parâmetros:
        brand_list - Lista de marcas extraidas do filtro de marcas do site
        item_name  - nome do item extraído so site

        Retorno:
        Retorna uma string contendo qual foi a marca extraída
        """
        item_name_lower = item_name.lower()
        print(f'Essa é a lista de marcas extraídas do site {brand_list}')
        print(f'Essa é o nome do item em minúsculo: {item_name_lower}')
        for brand in brand_list:
            brand_lower = brand.lower()
            pattern = r'\b' + re.escape(brand_lower) + r'\b' # \b significa a quebra de palavra
            result = re.search(pattern=pattern, string=item_name_lower)
            if result:
                return brand
        return None

            


    def parse(self, response):
        products = response.css('a.ProductCard-styled__Card-sc-97c94e5e-0.gpfLHL')
        next_page = (f'https://www.centauro.com.br/nav/categorias/calcados/produto/tenis/genero/masculino?page={self.next_page}')
        brand_list_raw = response.css('dd.Accordionstyled__SectionContent-sc-b3g7jv-4[id^="Marca"]')
        brand_list = brand_list_raw.css('span.Checkboxstyled__TextContainer-sc-l3e9sx-3.bpSEPF::text').getall()


        for product in products:
            name = product.css('p.Typographystyled__Paragraph-sc-bdxvrr-1.knvuZc.ProductCard-styled__Title-sc-97c94e5e-3.hzAjfq::text').get()
            yield{
                'nome': name,
                'brand': self.get_brand(brand_list=brand_list, item_name=name),
                'new_price': product.css('p.Typographystyled__Paragraph-sc-bdxvrr-1.eFDcLB.Price-styled__CurrentPrice-sc-e083f0ed-4.etKnUk::text').get(),
                'old_price': product.css('del.Typographystyled__Offer-sc-bdxvrr-4.cAyLkZ.Price-styled__OldPriceOffer-sc-e083f0ed-2.gaskFI::text').get()
            }

        if self.next_page < self.max_page:
            if next_page:
                self.next_page += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
        


