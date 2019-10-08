from scrapy import Field, Item


class FoussierItem(Item):
    images = Field()
    image_urls = Field()

    sku = Field()
    title = Field()
    url = Field()
    description = Field()
    brand = Field()
    version = Field()
    length_in_mm = Field()
    load_in_kg = Field()

    pass
