import csv
import scrapy
from collections import namedtuple
from unidecode import unidecode
from datetime import datetime
from os import path, makedirs


class CityCheckerSpider(scrapy.Spider):
    name = "city_checker"
    MATCH_CRITERIA = "Novembro/2020"  # MUDE PARA O MES ATUAL QUE FIZER SENTIDO
    ISSUE_DATE_SELECTOR = "div.data-caderno ::text"
    RESULT_DIR = path.join("data", datetime.now().strftime("%Y%m%d_%H%M%S"))
    RESULT_PATH = path.join(RESULT_DIR, "result.csv")

    def start_requests(self):
        makedirs(self.RESULT_DIR)
        with open(self.RESULT_PATH, "w") as result_file:
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
            with open(self.RESULT_PATH, "a") as result_file:
                result_file.write(
                    f"{territory.id},{territory.state.upper()},{territory.city_name},{response.url}\n"
                )
            with open(
                path.join(
                    self.RESULT_DIR,
                    f"result_{territory.state}_{territory.city_uri}.html",
                ),
                "w",
            ) as html_file:
                html_file.write(response.text)

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
