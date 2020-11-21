import scrapy
import csv
from unidecode import unidecode
from collections import namedtuple
from scrapy import signals


class CityCheckerSpider(scrapy.Spider):
    name = "city_checker"
    matches = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CityCheckerSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def start_requests(self):
        for territory in self.load_territories():
            url = f"http://{territory.state}.portaldatransparencia.com.br/prefeitura/{territory.city_uri}"
            yield scrapy.Request(
                url=url, callback=self.parse, meta={"territory": territory}
            )

    def parse(self, response):
        if response.status == 200 and "Novembro/2020" in response.text:
            self.matches.append((response.url, response.meta["territory"]))

    def spider_closed(self, spider):
        spider.logger.info("============== Done! ===============")
        with open("result.csv", "w") as result_file:
            result_file.write("id,state,city,url\n")
            result_file.writelines(
                [
                    f"{territory.id},{territory.state.upper()},{territory.city_name},{url}\n"
                    for url, territory in self.matches
                ]
            )

    def normalize(self, city):
        return unidecode(city).lower().replace(" ", "")

    def load_territories(self):
        Territory = namedtuple("Territory", "id state city_uri city_name")
        with open("territories.csv") as csvfile:
            rows = csv.reader(csvfile, delimiter=",")
            return [
                Territory(id, self.normalize(state), self.normalize(city), city)
                for [id, city, state, _] in rows
            ]
