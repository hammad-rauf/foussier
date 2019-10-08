from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest

from ..items import FoussierItem


class FoussierSpider(CrawlSpider):

    name = 'foussier'
    start_urls = [
        'https://www.foussier.fr/'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css = ['#itemMegaMenu','.arboViewAll','.arboViewAll','.seeMore.listLink'])),
         Rule(LinkExtractor(restrict_css = '.loaderContainer'),callback='parsee')
    )
    

    def parsee(self, response):

        item = FoussierItem()

        item['image_urls'] = response.css('#positionneVisuelsSecondaires .spanImageResponsive img::attr(src)').extract()

        image = []

        for img in item['image_urls']:
            img = img.replace("78-78","443-443")
            image.append(img)
        
        item['image_urls'] = image

        item["sku"] = response.css('.productCode::text').extract()[1]

        item['title'] = response.css('#page h1::text').extract_first()  
        item['title'] = item['title'].replace("'","")
        
        item['url'] = response.url

        description = response.css('#descriptifProduit li span::text').extract()
        a = " "
        item['description'] = a.join(description)
        item['description'] = item['description'].replace("'","")

        brand = response.css('.specificiteProduit a::text').extract()
        b = " "
        item['brand'] = b.join(brand)
        item['brand'] = item['brand'].replace("'","")

        return item

        