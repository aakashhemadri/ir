# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ArsTechnicaItem(Item):
    article_id = Field()
    date = Field()
    tags = Field()
    title = Field()
    author = Field()
    author_url = Field()
    post_url = Field()
    image = Field()
    excerpt = Field()
    content = Field()
