from unidecode import unidecode
from collections import namedtuple
from os import path, makedirs

City = namedtuple("City", "id state name url")

spider_template = """
from gazette.spiders.base.portal_da_transparencia import PortalDaTransparenciaBaseSpider


class {spider_class_name}(PortalDaTransparenciaBaseSpider):
    TERRITORY_ID = "{id}"
    name = "{spider_name}"
    start_urls = [
        "{url}"
    ]
"""


def get_spider(city):
    spider_class_name = (
        f'{city.state.capitalize()}{unidecode(city.name).replace(" ","")}Spider'
    )
    print(spider_class_name)
    spider_name = (
        f'{city.state.lower()}_{unidecode(city.name.lower()).replace(" ","_")}'
    )
    code = (
        spider_template.replace("{spider_class_name}", spider_class_name)
        .replace("{spider_name}", spider_name)
        .replace("{id}", city.id)
        .replace("{url}", city.url.replace("\n", ""))
    )
    return spider_name, code


def save_spider(name, code):
    subdir = "generated_spiders"
    if not path.exists(subdir):
        makedirs(subdir)

    with open(path.join(subdir, f"{name}.py"), "w") as spider_file:
        spider_file.write(code)


with open("result.csv", "r") as result_file:
    cities = [City(*line.split(",")) for line in result_file.readlines()[1:]]
    spiders = [get_spider(city) for city in cities]
    [save_spider(spider_name, code) for spider_name, code in spiders]
