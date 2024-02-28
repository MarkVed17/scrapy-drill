from pathlib import Path
import json
import scrapy

class HackerNewsSpider(scrapy.Spider):
    # Name of the spider
    name = 'hacker-news-spider'

    def start_requests(self):
        # Page URLs to scrape
        urls = ['https://news.ycombinator.com/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        # Store scrapped and structured result
        result = {}

        # Scrape the desired values
        postTitles = response.css('span.titleline > a::text').getall()
        postUrls = response.css('span.titleline > a::attr(href)').getall()
        postScores = response.css('span.score::text').getall()
        postUserNames = response.css('a.hnuser::text').getall()


        # Loop over all the titles to build the result structure
        for i in range(len(postTitles)):            
            entry = {
                'url': postUrls[i],
                'score': postScores[i],
                'username': postUserNames[i],
            }

            result[postTitles[i]] = entry

        # Dump the result to the file in JSON format
        filename = f"hackerNews-latest.json"
        with open(filename, 'w') as fp:
            json.dump(result, fp)
        

        self.log(f"Saved file!")