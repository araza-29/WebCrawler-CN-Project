import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class MyCrawlerSpider(scrapy.Spider):
    name = "my_crawler"
    start_urls = ['https://tribune.com.pk/article/98007/my-feminist-abcs-speaking-tanveer-anjums-rebellious-language']  # Replace with your seed URLs

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content
        text = soup.get_text(strip=True)

        # Extract image URLs
        images = [urljoin(response.url, img.get('src')) for img in soup.find_all('img') if img.get('src')]

        # Extract links to follow
        links = [urljoin(response.url, a.get('href')) for a in soup.find_all('a', href=True)]

        yield {
            'url': response.url,
            'text': text[:500],  # limit output
            'images': images,
            'links': links
        }

        # Follow links (limit depth with DEPTH_LIMIT in settings.py)
        for link in links:
            yield scrapy.Request(link, callback=self.parse)
