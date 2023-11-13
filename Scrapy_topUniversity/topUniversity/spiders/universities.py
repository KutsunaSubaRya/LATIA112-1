import scrapy


class TopuniversitySpider(scrapy.Spider):
    name = "topUniversity"
    allowed_domains = ["www.topuniversities.com"]
    start_urls = ["https://www.topuniversities.com/university-rankings/world-university-rankings/2024"]

    def start_requests(self):
        # I had write the reason why I use this url in the README.md
        url = "https://www.topuniversities.com/rankings/endpoint?nid=3897789&page=0&items_per_page=1500&tab=indicators&region=&countries=&cities=&search=&star=&sort_by=rank&order_by=asc&program_type="
        # Send a request to the url
        yield scrapy.Request(url=url)
    def parse(self, response):
        score_nodes = response.json()["score_nodes"]
        # Loop through the score_nodes
        for university in score_nodes:
            # Yield a dictionary and store the information that we want via I/O redirection. (See README.md)
            yield {
                "name": university["title"].strip(),
                "overall rank": university["rank"],
                "overall score": university["overall_score"],
                "academic reputation rank": university["scores"][0]["rank"],
                "academic reputation score": university["scores"][0]["score"],
                "employer reputation rank": university["scores"][1]["rank"],
                "employer reputation score": university["scores"][1]["score"],
                "faculty student rank": university["scores"][2]["rank"],
                "faculty student score": university["scores"][2]["score"],
                "citations per faculty rank": university["scores"][3]["rank"],
                "citations per faculty score": university["scores"][3]["score"],
                "international faculty rank": university["scores"][4]["rank"],
                "international faculty score": university["scores"][4]["score"],
                "international students rank": university["scores"][5]["rank"],
                "international students score": university["scores"][5]["score"],
                "international Research Network rank": university["scores"][6]["rank"],
                "international Research Network score": university["scores"][6]["score"],
                "employment outcomes rank": university["scores"][7]["rank"],
                "employment outcomes score": university["scores"][7]["score"],
                "sustainability rank": university["scores"][8]["rank"],
                "sustainability score": university["scores"][8]["score"],
            }
