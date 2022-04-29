import hashlib
import json

import scrapy
from scrapy.http import Request
from war2022_team9.items import War2022Team9Item


class SvobodaArticlesSpider(scrapy.Spider):
    name = 'svoboda_articles'
    allowed_domains = ['svoboda.org']

    def start_requests(self):

        with open('svoboda.json') as json_file:
            data = json.load(json_file)

        for link_url in data:
            print('URL: ' + link_url['article_url'])
            # Request to get the HTML content
            request = Request(link_url['article_url'], cookies={'store_language': 'ru'},
                              callback=self.parse)
            yield request

    def parse(self, response):
        print("\n")
        print("HTTP STATUS: " + str(response.status))
        print(response.xpath("//h2/a/text()").get())
        print("\n")

        item = War2022Team9Item()

        item['article_link'] = response.url
        item['article_uuid'] = hashlib.sha256(str(response.url).encode('utf-8')).hexdigest()
        item['article_id'] = response.url.split("/")[-1].split(".")[0]

        item['article_datetime'] = response.xpath('//*[@id="content"]/div[1]/div[1]/div/div[3]/div/div[1]/span/time').extract()

        item['article_title'] = response.xpath('//*[@id="content"]/div[1]/div[1]/div/div[2]/h1/text()').extract()


        content = response.xpath('//*[@id="article-content"]/div[1]')
        text = []

        for article_text in content.xpath('.//p'):
            text.append(article_text.xpath('.//text()').extract())

        item['article_text'] = "\n" + " ".join([sent for sent_list in text for sent in sent_list])


        return (item)
