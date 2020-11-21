import csv
import scrapy
from collections import namedtuple
from unidecode import unidecode


class CityCheckerSpider(scrapy.Spider):
    name = "city_checker"
    MATCH_CRITERIA = "Novembro/2020"
    ISSUE_DATE_SELECTOR = "div.data-caderno ::text"

    def start_requests(self):
        with open("result.csv", "w") as result_file:
            result_file.write("id,state,city,url\n")

        for territory in self.load_territories():
            url = f"http://{territory.state}.portaldatransparencia.com.br/prefeitura/{territory.city_uri}"
            yield scrapy.Request(
                url=url, callback=self.parse, meta={"territory": territory}
            )

    def parse(self, response):
        if response.status != 200:
            return

        issue_date = response.css(self.ISSUE_DATE_SELECTOR).get()

        if issue_date != None and self.MATCH_CRITERIA in issue_date:
            self.logger.info(f"Success for {response.url}")
            territory = response.meta["territory"]
            with open("result.csv", "a") as result_file:
                result_file.write(
                    f"{territory.id},{territory.state.upper()},{territory.city_name},{response.url}\n"
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
